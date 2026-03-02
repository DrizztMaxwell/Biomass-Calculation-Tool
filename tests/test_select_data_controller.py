import unittest
from unittest.mock import MagicMock, patch, AsyncMock, mock_open
import pandas as pd
import flet as ft
import decimal

from controller.Select_Data_Controller import Select_Data_Controller

class TestSelectDataController(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Mock dependencies needed for initialization
        self.mock_page = MagicMock(spec=ft.Page)
        self.mock_page.overlay = []
        self.mock_view = MagicMock()
        self.mock_callback = MagicMock()
        
        # Instantiate the controller with mock components
        self.controller = Select_Data_Controller(
            page=self.mock_page,
            data_imported_callback=self.mock_callback,
            view=self.mock_view
        )
    
    @patch('controller.Select_Data_Controller.convert_text_file_into_dataframe')
    @patch('controller.Select_Data_Controller.do_mandatory_columns_exist')
    @patch('controller.Select_Data_Controller.convert_columns_to_specific_types')
    @patch('controller.Select_Data_Controller.convert_columns_to_lowercase')
    @patch('controller.Select_Data_Controller.check_dataframe_for_nan_values')
    @patch('controller.Select_Data_Controller.validate_tree_dbh_and_height_values')
    @patch('controller.Select_Data_Controller.DataManager')
    @patch('controller.Select_Data_Controller.Loading_Spinner_Widget')
    @patch('controller.Select_Data_Controller.logger')
    @patch('builtins.open', new_callable=mock_open)
    async def test_on_file_selected_success(self, mock_file, mock_logger, mock_spinner_cls, 
                                          mock_dm_cls, mock_validate, mock_nan, 
                                          mock_lower, mock_types, mock_mandatory, mock_convert):
        
        # Arrange a Mock FilePicker event
        mock_event = MagicMock(spec=ft.FilePickerResultEvent)
        mock_file_obj = MagicMock()
        mock_file_obj.path = "/path/to/test_data.txt"
        mock_event.files = [mock_file_obj]

        # Mock Dataframe processing results
        mock_df = pd.DataFrame({'Plot': [1], 'DBH': [20.5]})
        mock_convert.return_value = mock_df
        mock_mandatory.return_value = True
        mock_types.return_value = mock_df
        mock_lower.return_value = mock_df
        mock_nan.return_value = (False, 0, []) # Errors detected, count, messages
        mock_validate.return_value = [] # Ensure no out-of-bounds errors

        # Mock Spinner instance 
        mock_spinner = MagicMock()
        mock_spinner.simulate_progressive_loading = AsyncMock()
        mock_spinner_cls.return_value = mock_spinner

        # Mock DataManager component
        mock_dm = MagicMock()
        mock_dm_cls.return_value = mock_dm

        await self.controller.on_file_selected(mock_event)

        # Verify file path was stored (dummy filepath)
        self.assertEqual(self.controller.selected_file_path, "/path/to/test_data.txt")
        
        # Verify DataManager was updated with records
        mock_dm.set_all.assert_called_once()
        
        # Verify UI/Callback updates
        self.assertTrue(self.controller.is_data_imported)
        self.mock_callback.assert_called_with(True)
        self.mock_view.update_file_status.assert_any_call("File processed: test_data.txt")
        
        # Verify the success dialog/spinner were handled
        mock_spinner.hide.assert_called_once()
        self.mock_page.update.assert_called()

    async def test_on_file_selected_cancelled(self):
        mock_event = MagicMock(spec=ft.FilePickerResultEvent)
        mock_event.files = None  # Simulate user clicking 'Cancel'

        await self.controller.on_file_selected(mock_event)

        # Assertion for testing
        self.assertIsNone(self.controller.selected_file_path)
        self.assertFalse(self.controller.is_data_imported)
        self.mock_callback.assert_called_with(False)
        self.mock_view.update_file_status.assert_called_with("No file selected")


    @patch('controller.Select_Data_Controller.logger')
    def test_on_import_text_file_click(self, mock_logger):
        # Mock the FilePicker object 
        mock_file_picker = MagicMock(spec=ft.FilePicker)
        self.controller.file_picker = mock_file_picker
        
        # Create a dummy event object
        mock_event = MagicMock()

        self.controller.on_import_text_file_click(mock_event)

        # Verify the logger was called with the correct message
        mock_logger.write.assert_called_with("Import text file dialog opened")

        # Verify the file picker was triggered with the correct parameters
        mock_file_picker.pick_files.assert_called_once_with(
            allow_multiple=False,
            allowed_extensions=["txt"],
            dialog_title="Select Dataset File",
            file_type=ft.FilePickerFileType.ANY,
        )

    @patch('asyncio.get_running_loop')
    @patch('asyncio.create_task')
    def test_on_database_selected_schedules_task(self, mock_create_task, mock_get_loop):
        """Verify that valid input schedules an async task"""
        # Set up mock values for behavior checking
        server = "LocalHost"
        database = "MariaDB"
        mock_loop = MagicMock()
        mock_get_loop.return_value = mock_loop

        # Simulate action (method call)
        self.controller.on_database_selected(server, database)

        # Ensure it tried to get the loop and schedule the private connection method
        mock_get_loop.assert_called_once()
        mock_create_task.assert_called_once()
        
        # Verify the task being created is our internal connection method
        # Note: use ANY because the coroutine object itself is complicated to compare
        mock_create_task.assert_called_with(unittest.mock.ANY)

    @patch('controller.Select_Data_Controller.Display_Error_Dialog')
    def test_on_database_selected_missing_input(self, mock_error_dialog):
        """Verify that empty inputs trigger an error dialog"""
        # Mock the dialog instance and its .show() method
        mock_dialog_instance = MagicMock()
        mock_error_dialog.return_value = mock_dialog_instance
        
        # Call with empty database
        self.controller.on_database_selected("ServerName", "")

        # Verify the error dialog was initialized with the correct description
        mock_error_dialog.assert_called_once_with(
            self.controller.page, 
            description="Server and database are required"
        )

        # Verify the page actually opened the dialog
        self.mock_page.open.assert_called_once()

    @patch('pyodbc.connect')
    @patch('controller.Select_Data_Controller.get_sql_server_odbc_driver')
    @patch('controller.Select_Data_Controller.get_mssql_data_path')
    @patch('controller.Select_Data_Controller.os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_connect_and_save_db_info_success(self, mock_file, mock_makedirs, mock_path, mock_driver, mock_pyodbc):
        # Set up mock results for behavior checking
        mock_driver.return_value = "ODBC Driver 17 for SQL Server"
        mock_path.return_value = "C:/SQLData"
        
        # Mock successful pyodbc connection context manager
        mock_conn = MagicMock()
        mock_pyodbc.return_value.__enter__.return_value = mock_conn

        # Simulate action
        result = self.controller._connect_and_save_db_info("localhost", "MariaDB")

        self.assertTrue(result)
        # Verify connection string had the right server/db
        args, _ = mock_pyodbc.call_args
        self.assertIn("Server=localhost;", args[0])
        self.assertIn("Database=MariaDB;", args[0])
        
        # Verify JSON config was saved
        mock_file.assert_called_with(unittest.mock.ANY, "a")
        self.mock_view.add_to_history.assert_called_with("localhost", "MariaDB")

    @patch("pyodbc.connect")
    @patch("data.data_manager.DataManager.set_all")
    @patch("data.data_manager.DataManager.set_database_path")
    @patch("widgets.Custom_Alert_Dialog")
    def test_import_from_database_success(self, mock_alert_show, mock_set_db_path, mock_set_all, mock_connect):
        """Test successful data import from a database"""
        # Setup mock database response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock the column names and row data
        mock_cursor.description = [
            ('Plot',), ('Year',), ('Species',), ('Tree_number',), ('DBH',), ('Height',)
        ]
        mock_cursor.fetchall.return_value = [
            (1, 2023, "Oak", 101, decimal.Decimal("25.5"), decimal.Decimal("15.0"))
        ]

        # Execute the method
        result = self.controller.import_from_database(
            db_name="TestDB", 
            driver="SQL Server", 
            server="localhost"
        )

        # Assertions
        self.assertTrue(result)
        self.assertTrue(self.controller.is_data_imported)
        
        # Verify DataManager received the data (converted from decimal to float)
        expected_data = [{
            'Plot': 1, 'Year': 2023, 'Species': 'Oak', 
            'Tree_number': 101, 'DBH': 25.5, 'Height': 15.0
        }]
        mock_set_all.assert_called_once_with(expected_data)
        
        # Verify View and Callbacks
        self.mock_view.update_file_status.assert_called_with("Data imported from database: TestDB")
        self.mock_callback.assert_called_with(True)
        self.mock_page.update.assert_called()

    @patch("pyodbc.connect")
    def test_import_from_database_empty_table(self, mock_connect):
        """Test behavior when the database table is empty"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Return empty list for fetchall
        mock_cursor.fetchall.return_value = []

        result = self.controller.import_from_database("TestDB", "Driver", "Server")

        self.assertFalse(result)
        self.mock_callback.assert_called_with(False)
        self.mock_view.update_file_status.assert_called_with("Failed to import data from database.")

    @patch("pyodbc.connect")
    @patch("builtins.open", new_callable=mock_open, read_data='{"server": "S", "database": "D", "driver": "Dr"}')
    def test_import_from_database_no_args_uses_json(self, mock_file, mock_connect):
        """Test that missing arguments trigger a load from the JSON config file"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.description = [('Plot',)]
        mock_cursor.fetchall.return_value = [(1,)]

        # Call without arguments
        self.controller.import_from_database()

        # Verify pyodbc.connect was called with data from the mock_open JSON
        args, kwargs = mock_connect.call_args
        self.assertIn("Server=S", args[0])
        self.assertIn("Database=D", args[0])

    @patch("pyodbc.connect")
    def test_import_from_database_connection_error(self, mock_connect):
        """Test specific error handling for pyodbc connection issues"""
        # Simulate a pyodbc error (using the '08001' code in controller)
        import pyodbc
        mock_connect.side_effect = pyodbc.Error('08001', 'Server not found')

        result = self.controller.import_from_database("BadDB", "Driver", "BadServer")

        self.assertFalse(result)
        # Check if the error dialog was opened on the page
        self.mock_page.open.assert_called()

    @patch("widgets.LogFileTxt.logger.write")
    def test_on_import_from_database_click(self, mock_logger_write):
        """Test that clicking the database button triggers the view dialog and logs it"""
        # Setup mock event
        mock_event = MagicMock() # This represents the flet event 'e'

        # Execute (simulate method call)
        self.controller.on_import_from_database_click(mock_event)

        # Assertions to verify the controller told the view to open the dialog
        self.mock_view._open_database_dialog.assert_called_once_with(mock_event)

        # Verify the action was logged
        mock_logger_write.assert_called_with("Database dialog opened")

    def test_set_database_name(self):
        """Test that set_database_name correctly updates the internal attribute"""
        # Setup mock database name
        test_db_name = "Biomass_Plot_DB"

        # Execute (simulate method call)
        self.controller.set_database_name(test_db_name)

        # Assertions to check that the internal attribute was updated
        self.assertEqual(self.controller.database_name, test_db_name)

    def test_get_database_name(self):
        """Test that get_database_name correctly retrieves the internal attribute"""
        # Setup mock data and attribute
        test_db_name = "Tree_Measurements_Algonquin_2026"
        self.controller.database_name = test_db_name

        # Execute (Simulate method call)
        retrieved_name = self.controller.get_database_name()

        # Assertions to Check that the returned value matches what was set
        self.assertEqual(retrieved_name, test_db_name)