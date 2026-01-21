# from helper_functions import do_mandatory_columns_exist
#select_data_controller.py
import asyncio
from helper_functions.convert_columns_to_specific_types import convert_columns_to_specific_types
from helper_functions.convert_text_file_into_dataframe import convert_text_file_into_dataframe
from views.Select_Data_View import Select_Data_View
from widgets.Display_Error_Dialog import Display_Error_Dialog
from widgets.Display_Warning_Dialog import Display_Warning_Dialog
from controller.import_dataset_menu import show_import_dataset_page
from helper_functions import do_mandatory_columns_exist
from helper_functions.convert_columns_to_lowercase import convert_columns_to_lowercase
from widgets.Display_Warning_Dialog import Display_Warning_Dialog
from widgets.Error_Alert_Import_Data_Dialog import Error_Alert_Import_Data_Dialog
from widgets.Import_Option_card import Import_Option_Card
from helper_functions.print_file_content import print_file_content
from helper_functions.convert_text_file_into_dataframe import convert_text_file_into_dataframe
from helper_functions.set_first_row_as_header import set_first_row_as_header
from helper_functions.validate_tree_dbh_and_height_values import validate_tree_dbh_and_height_values
from helper_functions.check_dataframe_for_nan_values import check_dataframe_for_nan_values
from helper_functions.do_mandatory_columns_exist import do_mandatory_columns_exist
from data.data_manager import DataManager
from data.database_config import get_sql_server_odbc_driver, get_mssql_data_path
import flet as ft
from widgets.Loading_Spinner_Widget import Loading_Spinner_Widget
import json
import pyodbc
import os
import uuid
import time
import decimal
import concurrent.futures


class Select_Data_Controller:
    def __init__(self, page: ft.Page, data_imported_callback: callable, view):
        self.page = page
        self.view = view
        self.database_name = None
        self.selected_file_path = None
        self.error_messages = []
        self.data_imported_callback = data_imported_callback
        self.is_data_imported = False

        # File picker setup
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)

        # Bind the view callback
        self.view.controller = self

    # -------------------------
    # TEXT FILE IMPORT
    # -------------------------
    async def on_file_selected(self, e: ft.FilePickerResultEvent):
        """Handle text file selection and processing asynchronously"""
        try:
            if not e.files:
                print("File selection cancelled")
                self.selected_file_path = None
                self.view.update_file_status("No file selected")
                self.data_imported_callback(False)
                
                self.is_data_imported = False
                self.page.update()
                return

            self.selected_file_path = e.files[0].path
            self.view.update_file_status(f"Processing: {self.selected_file_path}")
            print(f"Selected file: {self.selected_file_path}")

            spinner = Loading_Spinner_Widget(self.page)
            spinner.show_dialog()
            await spinner.simulate_progressive_loading(0.0, 0.2, 0.1, "Processing the file...")

            # Use ThreadPoolExecutor for CPU-bound processing
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                dataframe_future = pool.submit(convert_text_file_into_dataframe, self.selected_file_path)
                dataframe = dataframe_future.result()
                if dataframe is None:
                    raise ValueError("Text file may be empty or invalid.")

                await spinner.simulate_progressive_loading(0.2, 0.4, 0.1, "Checking mandatory columns...")
                if not pool.submit(do_mandatory_columns_exist, dataframe).result():
                    raise ValueError("Mandatory columns missing from dataset.")

                original_dataframe = dataframe.copy()
                dataframe = pool.submit(convert_columns_to_specific_types, dataframe).result()
                dataframe = pool.submit(convert_columns_to_lowercase, dataframe).result()

                errors_detected, error_count, error_messages = pool.submit(check_dataframe_for_nan_values, dataframe).result()
                error_message_out_of_bounds = pool.submit(validate_tree_dbh_and_height_values, dataframe).result()

                await spinner.simulate_progressive_loading(0.4, 0.8, 0.1, "DBH and Height validation completed...")
                self.error_messages = error_messages

                if error_messages or error_message_out_of_bounds:
                    self.page.overlay.append(Display_Warning_Dialog(
                        self.page,
                        self.error_messages,
                        error_message_out_of_bounds
                    ).show_dialog())

                # Save processed data to DataManager
                records = json.loads(original_dataframe.to_json(orient='records'))
                dm = DataManager()
                dm.set_all(records)

            await spinner.simulate_progressive_loading(0.8, 1.0, 0.1, "Completed successfully...")
            spinner.hide()

            self.is_data_imported = True
            self.view.update_file_status(f"File processed: {os.path.basename(self.selected_file_path)}")
            if self.data_imported_callback:
                with open("data/selected_database.json", "w") as f:
                    f.write("{}")  # Clear DB info
                self.data_imported_callback(True)

            self.page.update()

        except Exception as e:
            print("Error in text file import:", e)
            self.page.open(Display_Error_Dialog(self.page, description=str(e)).show())
            self.is_data_imported = False
            if self.data_imported_callback:
                self.data_imported_callback(False)
            self.page.update()

    def on_import_text_file_click(self, e):
        """Trigger file picker"""
        print("Import text file clicked")
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["txt"],
            dialog_title="Select Dataset File",
            file_type=ft.FilePickerFileType.ANY,
        )

    # -------------------------
    # DATABASE IMPORT
    # -------------------------
    def on_database_selected(self, server: str, database: str):
        """
        Called by view after user submits dialog.
        Safely schedules async database connection/import.
        """
        if not server or not database:
            self.page.open(Display_Error_Dialog(self.page, description="Server and database are required").show())
            return

        # Schedule async task without blocking Flet
        try:
            loop = asyncio.get_running_loop()
            asyncio.create_task(self._connect_and_import_database(server, database))
        except RuntimeError:
            # No loop running, start a temporary loop
            asyncio.run(self._connect_and_import_database(server, database))

    async def _connect_and_import_database(self, server: str, database: str):
        spinner = Loading_Spinner_Widget(self.page)
        spinner.show_dialog()
        await spinner.simulate_progressive_loading(0.0, 0.3, 0.05, "Initializing connection...")

        loop = asyncio.get_running_loop()
        try:
            success = await loop.run_in_executor(None, self._connect_and_save_db_info, server, database)
            if success:
                self.view.update_file_status(f"Connected to database: {database}")
                await loop.run_in_executor(None, self.import_from_database, database, None, server)
            else:
                self.view.update_file_status("Database connection failed.")
                if self.data_imported_callback:
                    self.data_imported_callback(False)
        finally:
            spinner.hide()
            self.page.update()

    def _connect_and_save_db_info(self, server: str, database: str) -> bool:
        """Connects to SQL Server and saves connection info to JSON"""
        try:
            driver = get_sql_server_odbc_driver()
            conn_str = (
                f"Driver={{{driver}}};"
                f"Server={server};"
                f"Database={database};"
                "Trusted_Connection=yes;"
                "Encrypt=no;"
                "TrustServerCertificate=yes;"
                "Connection Timeout=5;"
            )
            # Test connection
            with pyodbc.connect(conn_str) as conn:
                conn.cursor().execute("SELECT 1")

            data_folder_path = get_mssql_data_path()
            db_config = {
                "server": server,
                "database": database,
                "driver": driver,
                "data_folder_path": data_folder_path,
            }
            os.makedirs("data", exist_ok=True)
            with open("data/selected_database.json", "w") as f:
                json.dump(db_config, f, indent=4)

            # Save to history
            self.view._add_to_history(server, database)

            print(f"Database connection info saved: {db_config}")
            return True
        except Exception as e:
            print("Error connecting to database:", e)
            self.page.open(Display_Error_Dialog(self.page, description=str(e)).show())
            return False

    def import_from_database(self, db_name: str = None, driver: str = None, server: str = None):
        try:
            if not all([db_name, driver, server]):
                with open("data/selected_database.json", "r") as f:
                    db_info = json.load(f)
                server = db_info["server"]
                db_name = db_info["database"]
                driver = db_info["driver"]

            conn = pyodbc.connect(
                f"Driver={{{driver}}};"
                f"Server={server};"
                f"Database={db_name};"
                "Trusted_Connection=yes;"
                "Encrypt=no;"
                "TrustServerCertificate=yes;"
                "Connection Timeout=5;"
            )
            cursor = conn.cursor()

            # STEP 1 — Setup and insert (no SELECT here)
            cursor.execute("""
            IF NOT EXISTS (
                SELECT 1
                FROM sys.tables t
                JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE t.name = 'tCalcBCTInput'
                AND s.name = 'dbo'
            )
            BEGIN
                CREATE TABLE dbo.tCalcBCTInput
                (
                    plot        INT            NOT NULL,
                    species     SMALLINT       NOT NULL,
                    tree_number SMALLINT       NOT NULL,
                    section     TINYINT        NULL,
                    height      DECIMAL(5,2)   NULL,
                    dbh         DECIMAL(5,2)   NULL
                );
            END;

            TRUNCATE TABLE dbo.tCalcBCTInput;

            INSERT INTO dbo.tCalcBCTInput
                (plot, species, tree_number, section, height, dbh)
            SELECT
                t.PlotMapGrowthPlotKey,
                t.SpecCode,
                t.TreeNum,
                t.Section,
                m.HtToDBH,
                m.DBH
            FROM dbo.tblTree t
            JOIN dbo.tblTreeMsr m
                ON t.TreeKey = m.TreeKey;
            """)

            conn.commit()  # ensure data is written

            # STEP 2 — Query separately
            cursor.execute("""
            SELECT plot, species, tree_number, section, dbh, height
            FROM dbo.tCalcBCTInput;
            """)

            columns = [c[0] for c in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.close()

            if not rows:
                raise ValueError(f"{db_name} tCalcBCTInput is empty")

            rows_safe = [
                {k: float(v) if isinstance(v, decimal.Decimal) else v for k, v in row.items()}
                for row in rows
            ]

            dm = DataManager()
            dm.set_all(rows_safe)
            dm.set_database_path(db_name)

            self.is_data_imported = True
            self.view.update_file_status(f"Data imported from database: {db_name}")
            if self.data_imported_callback:
                self.data_imported_callback(True)
            self.page.update()
            return True

        except Exception as e:
            print("Error importing from database:", e)
            self.page.open(Display_Error_Dialog(self.page, description=str(e)).show())
            self.view.update_file_status("Failed to import data from database.")
            self.is_data_imported = False
            if self.data_imported_callback:
                self.data_imported_callback(False)
            self.page.update()
            return False


    # -------------------------
    # DATABASE BUTTON
    # -------------------------
    def on_import_from_database_click(self, e):
        """Trigger database dialog in view"""
        self.view._open_database_dialog(e)

    # -------------------------
    # DATABASE NAME
    # -------------------------
    def set_database_name(self, db_name: str):
        self.database_name = db_name

    def get_database_name(self) -> str:
        return self.database_name

    # -------------------------
    # BUILD VIEW
    # -------------------------
    def build(self):
        return self.view.create_main_layout()