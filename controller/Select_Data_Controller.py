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
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
from data.database_config import get_sql_server_odbc_driver, get_mssql_data_path
import flet as ft
from widgets.Loading_Spinner_Widget import Loading_Spinner_Widget
import json
from widgets.LogFileTxt import logger
import pyodbc
import os
import uuid
import time
import decimal
import concurrent.futures
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog

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
                logger.write("File selection cancelled by user")
                self.view.update_file_status("No file selected")
                self.data_imported_callback(False)
                
                self.is_data_imported = False
                self.page.update()
                return

            self.selected_file_path = e.files[0].path
            self.view.update_file_status(f"Processing: {self.selected_file_path}")
            print(f"Selected file: {self.selected_file_path}")
            logger.write(f"Selected file for import: {self.selected_file_path}")

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
            Custom_Alert_Dialog(
                self.page,
                title_icon=ft.Icons.CHECK_CIRCLE,
                title_icon_color=ft.Colors.GREEN,
                title_color=ft.Colors.GREEN,
                title="Success",
                message=f"Data successfully imported from file: {os.path.basename(self.selected_file_path)}",
                button_text="OK",
            ).show()
            logger.write(f"Text file imported successfully with {len(records)} records and {error_count} errors.")
            self.page.update()

        except Exception as e:
            print("Error in text file import:", e)
            logger.write(f"Error importing text file: {str(e)}")
            self.page.open(Display_Error_Dialog(self.page, description=str(e)).show())
            self.is_data_imported = False
            if self.data_imported_callback:
                self.data_imported_callback(False)
            self.page.update()

    def on_import_text_file_click(self, e):
        """Trigger file picker"""
        print("Import text file clicked")
        logger.write("Import text file dialog opened")
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
                logger.write(f"Database import process completed for {database}")
            else:
                logger.write(f"Database connection failed for {database}")
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
            logger.write(f"Successfully connected to database {database} on server {server}")
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
            logger.write(f"Database connection info saved: {db_config}")
            print(f"Database connection info saved: {db_config}")
            return True
        except Exception as e:
            print("Error connecting to database:", e)
            logger.write(f"Error connecting to database: {str(e)}")
            if e.args:
                if e.args[0] == '08001':
                    error_dialog = Display_Error_Dialog(
                        self.page,
                        title="Connection Error",
                        description=f"Could not connect to the database server '{server}'. Please check the server name and your network connection.",
                     
                    )
                    self.page.open(error_dialog.show())
                elif e.args[0] == '28000' and "Cannot open database" not in e.args:
                    error_dialog = Display_Error_Dialog(
                        self.page,
                        title="No Database Found",
                        description=f"Please check if the database '{database}' exists and your authentication details are correct.",
                     
                    )
                    self.page.open(error_dialog.show())
                else:
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
            
            logger.write(f"Connecting to database {db_name} on server {server} using driver {driver}")
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

            # STEP 1 — Drop & recreate input/output tables, then insert
            cursor.execute("""
            DROP TABLE IF EXISTS dbo.tCalcBiomassInput;

            CREATE TABLE dbo.tCalcBiomassInput
            (
                Plot         VARCHAR(MAX) NOT NULL,
                Year         INT          NOT NULL,
                Species      INT          NOT NULL,
                Tree_number  SMALLINT     NOT NULL,
                DBH          DECIMAL(4,1)  NOT NULL,
                Height       DECIMAL(3,1)  NOT NULL
            );

            DROP TABLE IF EXISTS dbo.tCalcBiomassOutput;

            CREATE TABLE dbo.tCalcBiomassOutput
            (
                Plot               VARCHAR(MAX) NOT NULL,
                Year               INT          NOT NULL,
                Species            INT          NOT NULL,
                Tree_number        INT          NOT NULL,
                DBH                DECIMAL(4,1)  NOT NULL,
                Height             DECIMAL(4,2)  NULL,
                Wood_kg            NUMERIC(10,3),
                Bark_kg            NUMERIC(10,3),
                Foliage_kg         NUMERIC(10,3),
                Branch_kg          NUMERIC(10,3),
                Crown_kg           NUMERIC(10,3),
                Stem_kg            NUMERIC(10,3),
                Total_kg           NUMERIC(10,3),
                CoefficientSource  VARCHAR(100)  NULL,
                processed_at       DATETIMEOFFSET(0) NOT NULL DEFAULT SYSUTCDATETIME()
            );

            INSERT INTO dbo.tCalcBiomassInput
            SELECT TOP 10000
                tblPlot.PlotName                AS Plot,
                tblVisit.FieldSeasonYear       AS Year,
                tblTree.SpecCode               AS Species,
                tblTree.TreeNum                AS Tree_number,
                tblTreeMsr.DBH                 AS DBH,
                tCalcTreeHtSharma.CalculatedHeight AS Height
            FROM tblTreeGrowthPlot
            INNER JOIN tblTreeHeader
                ON tblTreeGrowthPlot.TreeHeaderKey = tblTreeHeader.TreeHeaderKey
            INNER JOIN tblTreeMsr
                ON tblTreeGrowthPlot.TreeGrowthPlotKey = tblTreeMsr.TreeGrowthPlotKey
            INNER JOIN tblTree
                ON tblTreeMsr.TreeKey = tblTree.TreeKey
            INNER JOIN tblVisit
                ON tblTreeHeader.VisitKey = tblVisit.VisitKey
            INNER JOIN tblPackage
                ON tblVisit.PackageKey = tblPackage.PackageKey
            INNER JOIN tblPlot
                ON tblPackage.PlotKey = tblPlot.PlotKey
            INNER JOIN tCalcTreeHtSharma
                ON tblTreeMsr.TreeMsrKey = tCalcTreeHtSharma.TreeMsrKey
            WHERE tblTreeMsr.TreeStatusCode = 'L';
            """)

            conn.commit()  # ensure data is written

            # STEP 2 — Query separately
            cursor.execute("""
            SELECT Plot, Year, Species, Tree_number, DBH, Height
            FROM dbo.tCalcBiomassInput;
            """)

            columns = [c[0] for c in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.close()

            if not rows:
                raise ValueError(f"{db_name} tCalcBiomassInput is empty")

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
            
            Custom_Alert_Dialog(
                self.page,
                title_icon=ft.Icons.CHECK_CIRCLE,
                title_icon_color=ft.Colors.GREEN,
                title_color=ft.Colors.GREEN,
                title="Success",
                message=f"Data successfully imported from database: {db_name}",
                button_text="OK",
            ).show()
            logger.write(f"Database import successful with {len(rows_safe)} records.")
            self.page.update()
            
            return True

        except Exception as e:
            print("Error importing from database:", e.args[0])
            logger.write(f"Error importing from database: {str(e)}")
            if e.args and e.args[0] == '08001':
                error_dialog = Display_Error_Dialog(
                    self.page,
                    title="Connection Error",
                    description=f"Could not connect to the database server '{server}'. Please check the server name and your network connection.",
                 
                )
                self.page.open(error_dialog.show())
            elif e.args and e.args[0] == '42S02':
                error_dialog = Display_Error_Dialog(
                    self.page,
                    title="Table Not Found",
                    description=f"The required table 'tCalcBCTInput' was not found in database '{db_name}'. Please ensure the database is set up correctly.",
                 
                )
                self.page.open(error_dialog.show())
            elif e.args and  e.args[0] == '28000':
                error_dialog = Display_Error_Dialog(
                    self.page,
                    title="Authentication Error",
                    description=f"Authentication failed when connecting to database '{db_name}'. Please check your credentials and try again.",
                 
                )
                self.page.open(error_dialog.show())
            elif e.args and "Cannot open database" in e.args[0]:
                error_dialog = Display_Error_Dialog(
                    self.page,
                    title="Database Access Error",
                    description=f"Cannot open database '{db_name}'. Please ensure the database exists and you have access rights.",
                 
                )
                self.page.open(error_dialog.show())
            else:    
                self.page.open(Display_Error_Dialog(self.page, description=str(e)).show())
            
            self.view.update_file_status("Failed to import data from database.")
            logger.write(f"Failed to import data from database: {str(e)}")
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
        logger.write("Database dialog opened")

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