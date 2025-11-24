# from helper_functions import do_mandatory_columns_exist
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
import flet as ft
from widgets.Loading_Spinner_Widget import Loading_Spinner_Widget
import json
import concurrent.futures
class Select_Data_Controller:
    def __init__(self, page: ft.Page, data_imported_callback: callable, view: Select_Data_View):
        self.page = page
        self.view = view
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
                self.view.update_file_status(self.selected_file_path)
                print(f"Selected file: {self.selected_file_path}")
                loading_spinner = Loading_Spinner_Widget(self.page)
                loading_spinner.show_dialog()
                await loading_spinner.simulate_progressive_loading(0.0, 0.2, 0.1, "Processing the file...")
               
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:

                    # Process the file
                    # dataframe = convert_text_file_into_dataframe(selected_file_path=self.selected_file_path)
                    dataframe = pool.submit(convert_text_file_into_dataframe, self.selected_file_path)
                    
                    try:
                        dataframe = dataframe.result()
                    except Exception as e:
                        # Handle exceptions from the worker thread
                        raise Exception(f"Error reading file: {e}")

                    if dataframe is None:
                        raise Exception("Error reading file. Text Input File may be empty.")
                    # await asyncio.sleep(1)
                    # print("DataFrame loaded:")
                    # print(dataframe)
                    await loading_spinner.simulate_progressive_loading(0.2, 0.4, 0.1, "Beginning mandatory column checking...")
                    # # Check mandatory columns
                    work_2 = pool.submit(do_mandatory_columns_exist, dataframe)
                    if (work_2.result()):
                        print("OK")
                    
                    # # Process dataframe
                    original_dataframe = dataframe.copy()
                    work_3 = pool.submit(convert_columns_to_specific_types, dataframe)
                    dataframe = work_3.result()
                    print("JAIAIOPEJIPWEJIPDJPDJIPDJIPWDJIP")
                    print(dataframe)
                    # print("Column type conversion completed")
                    print("DAAAMN")
                    
                    work_4 = pool.submit(convert_columns_to_lowercase, dataframe)
                    dataframe = work_4.result()
                    # print("Column lowercase conversion completed")
                    
                    # print("Processed DataFrame:")
                    # print(dataframe)
                    
                    work_5 = pool.submit(check_dataframe_for_nan_values, dataframe)
                    errors_detected, error_count, error_messages = work_5.result()
                    print(error_messages)
                    # # Validate data
                    # nan_detected, error_count, error_messages = check_dataframe_for_nan_values(data_frame=dataframe)
                    # print("NaN validation completed")
                 
                    work_6 = pool.submit(validate_tree_dbh_and_height_values, dataframe)
                    error_message_for_out_of_bounds_dbh_or_height_value = work_6.result()
                    # error_message_for_out_of_bounds_dbh_or_height_value = validate_tree_dbh_and_height_values(dataframe)
                    
                    # print("DBH and height validation completed")
                    await loading_spinner.simulate_progressive_loading(0.4, 0.8, 0.1, "DBH and Height validation completed...")

                    self.error_messages = error_messages
                
                    # Show warnings if any
                    if error_messages or error_message_for_out_of_bounds_dbh_or_height_value:
                        
                       self.page.overlay.append( Display_Warning_Dialog(
                        self.page, 
                        self.error_messages, 
                        error_message_for_out_of_bounds_dbh_or_height_value
                    ).show_dialog()
                       )
                        # self.page.open(self.show_warning_dialog.build())
                        
                        
                    # Save data to local storage
                    print("File processed successfully. Saving to local storage...")
                    json_data = original_dataframe.to_json(orient='records')
                    with open('storage/localstorage.json', 'w') as json_file:
                        json_file.write(json_data)
                    await loading_spinner.simulate_progressive_loading(0.8, 1.0, 0.1, "Completed successfully...")
                    loading_spinner.hide()  
                    # Update import status and call callback
                    self.is_data_imported = True
                    if self.data_imported_callback:
                        pool.shutdown()
                        
                        self.data_imported_callback(True) # Call the callback to enable sidebar buttons
                    self.page.update()

                    return
                    
                    
            else:
                print("File selection cancelled")
                self.selected_file_path = None
                self.view.update_file_status(self.selected_file_path)
                self.is_data_imported = False
                # if self.data_imported_callback:
                #     self.data_imported_callback(False)
                self.page.update()
                # self.__del__()
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