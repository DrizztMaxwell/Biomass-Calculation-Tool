# from helper_functions import do_mandatory_columns_exist
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
import flet as ft
import json

class Select_Data_Controller:
    def __init__(self, page: ft.Page, data_imported_callback: callable):
        self.page = page
        self.view = Select_Data_View(self)
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)
        self.selected_file_path = None
        self.error_messages = []
        self.data_imported_callback = data_imported_callback  # Fixed parameter name
        self.is_data_imported = False  # Track internal state

    async def on_file_selected(self, e: ft.FilePickerResultEvent):
        """Callback when a file is selected"""
        try:
            if e.files:
                self.selected_file_path = e.files[0].path
                print(f"Selected file: {self.selected_file_path}")
                
                # Process the file
                dataframe = convert_text_file_into_dataframe(selected_file_path=self.selected_file_path)
                if dataframe is None:
                    raise Exception("Error reading file. Text Input File may be empty.")
                
                print("DataFrame loaded:")
                print(dataframe)
                
                # Check mandatory columns
                do_mandatory_columns_exist(data_frame=dataframe)
                print("Mandatory columns check passed")
                
                original_dataframe = dataframe.copy()
                
                # Process dataframe
                dataframe = convert_columns_to_specific_types(data_frame=dataframe)
                print("Column type conversion completed")
                
                dataframe = convert_columns_to_lowercase(data_frame=dataframe)
                print("Column lowercase conversion completed")
                
                print("Processed DataFrame:")
                print(dataframe)
                
                # Validate data
                nan_detected, error_count, error_messages = check_dataframe_for_nan_values(data_frame=dataframe)
                print("NaN validation completed")
                
                error_message_for_out_of_bounds_dbh_or_height_value = validate_tree_dbh_and_height_values(dataframe)
                print("DBH and height validation completed")

                self.error_messages = error_messages
              
                # Show warnings if any
                if error_messages or error_message_for_out_of_bounds_dbh_or_height_value:
                    show_warning_dialog = Display_Warning_Dialog(
                        self.page, 
                        self.error_messages, 
                        error_message_for_out_of_bounds_dbh_or_height_value
                    ).build()
                    self.page.open(show_warning_dialog)
                    
                # Save data to local storage
                print("File processed successfully. Saving to local storage...")
                json_data = original_dataframe.to_json(orient='records')
                with open('storage/localstorage.json', 'w') as json_file:
                    json_file.write(json_data)
                
                # Update import status and call callback
                self.is_data_imported = True
                if self.data_imported_callback:
                    self.data_imported_callback(True)  # Call the callback to enable sidebar buttons
                
                self.page.update()
                return
                
            else:
                print("File selection cancelled")
                self.selected_file_path = None
                self.is_data_imported = False
                if self.data_imported_callback:
                    self.data_imported_callback(False)
                self.page.update()
                return

        except ValueError as ve:
            print("Value Error:", ve)
            self.page.open(Error_Alert_Import_Data_Dialog(page=self.page, error_message=str(ve)).show())
            self.is_data_imported = False
            if self.data_imported_callback:
                self.data_imported_callback(False)
            self.page.update()
            return
            
        except Exception as e:
            print("Error in select data controller:", e)
            self.page.open(Display_Error_Dialog(page=self.page, description=str(e)).show())
            self.is_data_imported = False
            if self.data_imported_callback:
                self.data_imported_callback(False)
            self.page.update()
            return
       
    def open_file_dialog(self):
        """Open file picker dialog"""
        return self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["txt"],
            dialog_title="Select Dataset File",
            file_type=ft.FilePickerFileType.ANY,
        )
        
    def on_import_text_file_click(self, e):
        """Handle import text file button click"""
        print("Import text file clicked")
        self.open_file_dialog()
     
    def on_import_from_database_click(self, e):
        """Handle import from database button click"""
        print("Import from database clicked - feature coming next semester")
        # Show a message that this feature is not yet available
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Database import feature coming in the next release!"),
                action="OK"
            )
        )
    
    def build(self):
        """Build the controller view"""
        return self.view.create_main_layout()