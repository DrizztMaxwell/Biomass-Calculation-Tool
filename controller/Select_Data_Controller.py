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
    def __init__(self, page: ft.Page,):
        self.page = page
        
        self.view = Select_Data_View(self)
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)
        self.selected_file_path = None
        self.error_messages = []

    async def on_file_selected(self, e: ft.FilePickerResultEvent):
        """Callback when a file is selected"""
        try:
            
            if e.files:
                self.selected_file_path = e.files[0].path
                print(f"Selected file: {self.selected_file_path}")
                # print_file_content(self.selected_file_path)
                dataframe = convert_text_file_into_dataframe(selected_file_path=self.selected_file_path)
                print(dataframe)
                if dataframe is None:
                    raise Exception("Error reading file. Text Input File may be empty.")
                # print(dataframe)
                do_mandatory_columns_exist(data_frame=dataframe)
                print(f"DONE MANDATORY CHECK")
                original_dataframe = dataframe.copy()
                # dataframe = set_first_row_as_header(data_frame=dataframe)
                dataframe = convert_columns_to_specific_types(data_frame=dataframe)
                print(f"DONE CONVERTINT")
                dataframe = convert_columns_to_lowercase(data_frame=dataframe)
                print(f"DONE CONVERTINT TO LOWERCASE")
                print(dataframe)
                nan_detected, error_count, error_messages = check_dataframe_for_nan_values(data_frame=dataframe) 
                print("Its for validation1 ")
                
                error_message_for_out_of_bounds_dbh_or_height_value = validate_tree_dbh_and_height_values(dataframe)
                print("Its for validation2 ")

                self.error_messages = error_messages
              
                if error_messages:
                    show_warning_dialog = Display_Warning_Dialog(self.page, self.error_messages, error_message_for_out_of_bounds_dbh_or_height_value).build()
                    self.page.open(show_warning_dialog)
                    
               
                print("File processed successfully.")
                json_data = original_dataframe.to_json(orient='records')
                with open('storage/localstorage.json', 'w') as json_file:
                    json_file.write(json_data)
       
            else:
                print("File selection cancelled")
                self.selected_file_path = None

        except ValueError as ve:
            print("Value Error:")
            print(ve)
            self.page.open(Error_Alert_Import_Data_Dialog(page=self.page, error_message=str(ve)).show())
            return
        except Exception as e:
            print("Error in select data controller:")
            self.page.open(Display_Error_Dialog(page=self.page, description=str(e)).show())
            print(e)
           
            return
       
    def open_file_dialog(self):
        return self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["txt"],
            dialog_title="Select Dataset File",
            file_type=ft.FilePickerFileType.ANY,
        )
        
        
        # Standalone function to handle the button click and page updates
    def on_import_text_file_click(self,e):
        print("Clicked")
        # print(self.open_file_dialog())
        self.open_file_dialog()
     
    
    def on_import_from_database_click(self,e):
        pass # --> Next Semester :)
    
    def build(self):
        return self.view.create_main_layout()