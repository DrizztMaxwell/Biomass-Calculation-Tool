# select_data_controller.py
from helper_functions.convert_columns_to_specific_types import convert_columns_to_specific_types
from helper_functions.convert_text_file_into_dataframe import convert_text_file_into_dataframe
from widgets.Display_Error_Dialog import Display_Error_Dialog
from widgets.Display_Warning_Dialog import Display_Warning_Dialog
from helper_functions import do_mandatory_columns_exist
from helper_functions.convert_columns_to_lowercase import convert_columns_to_lowercase
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
from widgets.Loading_Spinner_Widget import Loading_Spinner_Widget
from constants.Json_File_Path_Constants import json_paths
import json
from widgets.LogFileTxt import logger
import os
import decimal
import flet as ft


class Select_Data_Controller:
    def __init__(self, page: ft.Page, data_imported_callback: callable, view):
        self.page = page
        self.view = view
        self.database_name = None
        self.selected_file_path = None
        self.error_messages = []
        self.data_imported_callback = data_imported_callback
        self.is_data_imported = False

        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)
        self.view.controller = self

    # ── Text file import ──────────────────────────────────────────────────────

    async def on_file_selected(self, e: ft.FilePickerResultEvent):
        """Handle text file selection and processing asynchronously."""
        try:
            if not e.files:
                self.selected_file_path = None
                logger.write("File selection cancelled by user")
                self.view.update_file_status("No file selected")
                self.data_imported_callback(False)
                self.is_data_imported = False
                self.page.update()
                return

            self.selected_file_path = e.files[0].path
            self.view.update_file_status(f"Processing: {self.selected_file_path}")
            logger.write(f"Selected file for import: {self.selected_file_path}")

            spinner = Loading_Spinner_Widget(self.page)
            spinner.show_dialog()
            await spinner.simulate_progressive_loading(0.0, 0.2, 0.1, "Processing the file...")

            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                dataframe = pool.submit(convert_text_file_into_dataframe,
                                        self.selected_file_path).result()
                if dataframe is None:
                    raise ValueError("Text file may be empty or invalid.")

                await spinner.simulate_progressive_loading(0.2, 0.4, 0.1,
                                                           "Checking mandatory columns...")
                if not pool.submit(do_mandatory_columns_exist, dataframe).result():
                    raise ValueError("Mandatory columns missing from dataset.")

                original_dataframe = dataframe.copy()
                dataframe = pool.submit(convert_columns_to_specific_types, dataframe).result()
                dataframe = pool.submit(convert_columns_to_lowercase, dataframe).result()

                errors_detected, error_count, error_messages = \
                    pool.submit(check_dataframe_for_nan_values, dataframe).result()
                error_message_out_of_bounds = \
                    pool.submit(validate_tree_dbh_and_height_values, dataframe).result()

                await spinner.simulate_progressive_loading(0.4, 0.8, 0.1,
                                                           "DBH and Height validation completed...")
                self.error_messages = error_messages

                # ── Detect duplicates before deciding whether to show dialog ──
                raw_data = dataframe.to_dict('records')

                # Build duplicate groups using same logic as Display_Warning_Dialog
                from collections import defaultdict
                _DUP_COLS = ["plot", "year", "species", "tree number", "dbh", "height"]
                _buckets: dict = defaultdict(list)
                for _i, _row in enumerate(raw_data):
                    _rlow = {str(k).lower(): v for k, v in _row.items()}
                    _key  = tuple(str(_rlow.get(c, "")).strip().lower() for c in _DUP_COLS)
                    _buckets[_key].append(_i)
                has_duplicates = any(len(v) > 1 for v in _buckets.values())

                if error_messages or error_message_out_of_bounds or has_duplicates:
                    self.page.overlay.append(
                        Display_Warning_Dialog(
                            self.page,
                            self.error_messages,
                            error_message_out_of_bounds,
                            raw_data=raw_data,
                        ).show_dialog()
                    )

                records = json.loads(original_dataframe.to_json(orient='records'))
                dm = DataManager()
                dm.set_all(records)

            await spinner.simulate_progressive_loading(0.8, 1.0, 0.1, "Completed successfully...")
            spinner.hide()

            self.is_data_imported = True
            self.view.update_file_status(
                f"File processed: {os.path.basename(self.selected_file_path)}"
            )
            if self.data_imported_callback:
                with open(json_paths.SELECTED_DATABASE_PATH, "w") as f:
                    f.write("{}")
                self.data_imported_callback(True)

            Custom_Alert_Dialog(
                self.page,
                title_icon=ft.Icons.CHECK_CIRCLE,
                title_icon_color=ft.Colors.GREEN,
                title_color=ft.Colors.GREEN,
                title="Success",
                message=f"Data successfully imported from file: "
                        f"{os.path.basename(self.selected_file_path)}",
                button_text="OK",
            ).show()
            logger.write(f"Text file imported successfully with {len(records)} records "
                         f"and {error_count} errors.")
            self.page.update()

        except Exception as exc:
            self.view.update_file_status(
                f"Error processing file: "
                f"{os.path.basename(self.selected_file_path) if self.selected_file_path else 'No file'}"
            )
            logger.write(f"Error importing text file: {str(exc)}")
            self.page.open(Display_Error_Dialog(self.page, description=str(exc)).show())
            self.is_data_imported = False
            if self.data_imported_callback:
                self.data_imported_callback(False)
            self.page.update()
        finally:
            # Delete the .parquet file created alongside the .txt file (if it exists)
            if self.selected_file_path:
                parquet_path = (
                    self.selected_file_path
                    .replace('.txt', '.parquet')
                    .replace('.csv', '.parquet')
                )
                if os.path.exists(parquet_path):
                    try:
                        os.remove(parquet_path)
                        logger.write(f"Deleted temporary parquet file: {parquet_path}")
                        print(f"Deleted temporary parquet file: {parquet_path}")
                    except Exception as clean_exc:
                        logger.write(f"Error deleting parquet file: {str(clean_exc)}")

    def on_import_text_file_click(self, e):
        logger.write("Import text file dialog opened")
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["txt"],
            dialog_title="Select Dataset File",
            file_type=ft.FilePickerFileType.ANY,
        )

    # ── Database import ───────────────────────────────────────────────────────

    def on_database_selected(self, server: str, database: str):
        if not server or not database:
            self.page.open(
                Display_Error_Dialog(self.page,
                                     description="Server and database are required").show()
            )
            return
        try:
            import asyncio
            asyncio.get_running_loop()
            asyncio.create_task(self._connect_and_import_database(server, database))
        except RuntimeError:
            import asyncio
            asyncio.run(self._connect_and_import_database(server, database))

    async def _connect_and_import_database(self, server: str, database: str):
        spinner = Loading_Spinner_Widget(self.page)
        spinner.show_dialog()
        await spinner.simulate_progressive_loading(0.0, 0.3, 0.05, "Initializing connection...")
        import asyncio
        loop = asyncio.get_running_loop()
        try:
            success = await loop.run_in_executor(
                None, self._connect_and_save_db_info, server, database
            )
            if success:
                self.view.update_file_status(f"Connected to database: {database}")
                await loop.run_in_executor(
                    None, self.import_from_database, database, None, server
                )
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
        try:
            driver   = get_sql_server_odbc_driver()
            conn_str = (
                f"Driver={{{driver}}};"
                f"Server={server};"
                f"Database={database};"
                "Trusted_Connection=yes;"
                "Encrypt=no;"
                "TrustServerCertificate=yes;"
                "Connection Timeout=5;"
            )
            import pyodbc
            with pyodbc.connect(conn_str) as conn:
                conn.cursor().execute("SELECT 1")
            logger.write(f"Successfully connected to {database} on {server}")
            db_config = {
                "server": server, "database": database,
                "driver": driver,
                "data_folder_path": get_mssql_data_path(),
            }
            with open(json_paths.SELECTED_DATABASE_PATH, "w") as f:
                json.dump(db_config, f, indent=4)
            self.view.add_to_history(server, database)
            logger.write(f"Database connection info saved: {db_config}")
            return True
        except Exception as exc:
            logger.write(f"Error connecting to database: {str(exc)}")
            args0 = exc.args[0] if exc.args else ""
            if args0 == '08001':
                msg = (f"Could not connect to server '{server}'. "
                       "Check server name and network connection.")
            elif args0 == '28000':
                msg = (f"Authentication failed for database '{database}'. "
                       "Check credentials.")
            else:
                msg = str(exc)
            self.page.open(Display_Error_Dialog(self.page, description=msg).show())
            return False

    def import_from_database(self, db_name=None, driver=None, server=None):
        try:
            if not all([db_name, driver, server]):
                with open(json_paths.SELECTED_DATABASE_PATH, "r") as f:
                    db_info = json.load(f)
                server  = db_info["server"]
                db_name = db_info["database"]
                driver  = db_info["driver"]

            import pyodbc
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
            cursor.execute("SELECT * FROM dbo.tCalcBiomassInput;")
            conn.commit()
            cursor.execute(
                "SELECT Plot, Year, Species, Tree_number, DBH, Height "
                "FROM dbo.tCalcBiomassInput;"
            )
            columns = [c[0] for c in cursor.description]
            rows    = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.close()

            if not rows:
                raise ValueError(f"{db_name} tCalcBiomassInput is empty")

            rows_safe = [
                {k: float(v) if isinstance(v, decimal.Decimal) else v
                 for k, v in row.items()}
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

        except Exception as exc:
            logger.write(f"Error importing from database: {str(exc)}")
            args0 = exc.args[0] if exc.args else ""
            if args0 == '08001':
                msg, title = (f"Could not connect to server '{server}'.", "Connection Error")
            elif args0 == '42S02':
                msg, title = (f"Table 'tCalcBiomassInput' not found in '{db_name}'.",
                              "Table Not Found")
            elif args0 == '28000':
                msg, title = (f"Authentication failed for '{db_name}'.", "Authentication Error")
            elif "Cannot open database" in str(args0):
                msg, title = (f"Cannot open database '{db_name}'.", "Database Access Error")
            else:
                msg, title = str(exc), "Import Error"
            self.page.open(
                Display_Error_Dialog(self.page, title=title, description=msg).show()
            )
            self.view.update_file_status("Failed to import data from database.")
            self.is_data_imported = False
            if self.data_imported_callback:
                self.data_imported_callback(False)
            self.page.update()
            return False

    # ── Database button ───────────────────────────────────────────────────────

    def on_import_from_database_click(self, e):
        self.view._open_database_dialog(e)
        logger.write("Database dialog opened")

    def set_database_name(self, db_name: str):
        self.database_name = db_name

    def get_database_name(self) -> str:
        return self.database_name

    def build(self):
        return self.view.create_main_layout()