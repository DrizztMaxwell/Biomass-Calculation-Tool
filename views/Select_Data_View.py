from tkinter import filedialog
import flet as ft
import pandas as pd

from controller.import_dataset_menu import show_import_dataset_page
from helper_functions import do_mandatory_columns_exist
from helper_functions.convert_columns_to_lowercase import convert_columns_to_lowercase
from widgets.Display_Warning_Dialog import Display_Warning_Dialog
from widgets.Error_Alert_Import_Data_Dialog import Error_Alert_Import_Data_Dialog
from widgets.Import_Option_card import Import_Option_Card
from helper_functions.print_file_content import print_file_content
from helper_functions.convert_text_file_into_dataframe import convert_text_file_into_dataframe
from helper_functions.set_first_row_as_header import set_first_row_as_header
from helper_functions.convert_columns_to_specific_types import convert_columns_to_specific_types
from helper_functions.validate_tree_dbh_and_height_values import validate_tree_dbh_and_height_values
from helper_functions.check_dataframe_for_nan_values import check_dataframe_for_nan_values
from helper_functions.do_mandatory_columns_exist import do_mandatory_columns_exist


class Select_Data_View:

    def __init__(self, page: ft.Page):
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self.on_file_selected)
        self.page.overlay.append(self.file_picker)
        self.selected_file_path = None
        self.error_messages = None
        
        self.selected_file = None
        
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
                    raise Exception("Error reading file.")
                # print(dataframe)
                do_mandatory_columns_exist(data_frame=dataframe)
                print(f"DONE MANDATORY CHECK")
                
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
                print(error_message_for_out_of_bounds_dbh_or_height_value)
                self.error_messages = error_messages
                # print(f"ERROR MESSAGES: {error_messages}")
                if error_messages:
                    print("Befin SHOW DIALOG ALERT DIALOG")
                    show_warning_dialog = Display_Warning_Dialog(self.page, self.error_messages, error_message_for_out_of_bounds_dbh_or_height_value).build()
                    self.page.open(show_warning_dialog)
                print("YOLO")
                # error_message = validate_tree_dbh_and_height_values(data_frame=dataframe)
                
                
                
                
            else:
                print("File selection cancelled")
                self.selected_file_path = None

        except Exception as e:
            print("Error:S")
            print(e)
            self.page.open(Error_Alert_Import_Data_Dialog(page=self.page).show())
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
   
        file = self.open_file_dialog()
     
        return None
    
            
    
    
    def read_text_file_dataset(self, file_path):
        """
        Read a text file dataset into a pandas DataFrame.

        Args:
            file_path: Path to the text file

        Returns:
            pandas DataFrame or None if error occurs
        """
        try:
            df = pd.read_csv(file_path, delim_whitespace=True, header=None)
            print("Dataset loaded successfully:")
            print(df)
            return df
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def process_dataframe(self, df):

        column_names = [df.iloc[0][i] for i in range(len(df.columns))]

        print("Dataset Information:")
        print(f"Number of columns: {len(df.columns)}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Data types: {df.dtypes}")
        print(f"Extracted column names: {column_names}")
        print("===================================")

        # Set column names and remove the first row
        df.columns = column_names
        df = df.iloc[1:].reset_index(drop=True)

        # Set data types
        set_column_data_types(data_frame=df)

        print("\nAfter conversion:")
        print(df.info())
        print(df.head())

        return df


    
    
    
    def begin_execution(self):
        global ERROR_COUNT, app

        # Read the dataset
        df = self.read_text_file_dataset(file_path)
        if df is None:
            print("ERROR, NO DATA PRESENT")
            messagebox.showerror("Error", "Failed to read the dataset. Please check if the file is valid.")
            return

        # Process the DataFrame
        df = self.process_dataframe(df)

        # Check for NaN values
        nan_detected, nan_error_count, nan_error_messages = check_nan_values(df)

        # Check for DBH/Height range violations
        range_error_messages = validate_dbh_height_values(df)
        range_error_count = len(range_error_messages)

        # Combine all errors
        all_error_messages = nan_error_messages + range_error_messages
        total_error_count = nan_error_count + range_error_count
        ERROR_COUNT += total_error_count

        # Print range error messages
        for error_msg in range_error_messages:
            print(error_msg)

        # Report results
        if not nan_detected and range_error_count == 0:
            print("✅ No data quality issues detected in the dataset")
        else:
            if nan_detected:
                print(f"\n🚨 TOTAL RECORDS WITH NaN VALUES: {df.isna().any(axis=1).sum()}")
                print_nan_summary(df)

            if range_error_count > 0:
                print_range_violation_summary(df)

            print(f"\n🚨 TOTAL ERRORS FOUND: {total_error_count}")

        # Show error dialog if errors found
        if total_error_count >= 1:
            CustomErrorBox(
                app,
                title="Data Quality Issues",
                message=f"Found {total_error_count} data quality issues in the dataset. Please fix them.",
                details=all_error_messages
            )
    
    
    
    
    
    
    
    
    
    
    
    
    
    def on_import_from_database_click():
        pass # --> Next Semester

    """
    A class containing static methods to build the Flet UI components.
    It does NOT inherit from ft.UserControl.
    """
    

    def create_main_layout(self):
        header = ft.Column(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Data Import Hub",
                            size=36,
                            weight=ft.FontWeight.W_900,
                            color=ft.Colors.BLUE_GREY_900,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=10),
                        ft.Text(
                            "Select your preferred method to import datasets into the platform",
                            size=16,
                            color=ft.Colors.BLUE_GREY_600,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ]),
                    padding=ft.padding.only(bottom=40)
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        # Row holding the two import cards
        options_row = ft.Row(
            [
               Import_Option_Card(
                    icon_name=ft.Icons.FOLDER_OPEN,
                    title="Local File Import",
                    subtitle="Upload CSV, TXT, or Excel files from your local storage with advanced parsing options.",
                    color=ft.Colors.BLUE_600,
                    handle_on_click=self.on_import_text_file_click
                ),
                Import_Option_Card(
                    icon_name=ft.Icons.STORAGE,
                    title="Database Connection",
                    subtitle="Connect securely to SQL databases using JDBC/ODBC drivers with real-time data streaming.",
                    color=ft.Colors.INDIGO_600
                    , handle_on_click=self.on_import_text_file_click
                ),
            ],
            spacing=40,
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True
        )

     
        # Main content container
        main_content = ft.Column(
            [
                header,
                options_row,
              
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )

        # Enhanced outer container with gradient background - NOW CENTERED
        main_layout = ft.Container(
            content=main_content,
            padding=ft.padding.symmetric(vertical=50, horizontal=40),
            margin=ft.margin.all(30),
            border_radius=ft.border_radius.all(30),
            bgcolor=ft.Colors.WHITE,
            width=900,
            # Enhanced shadow and border
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=40,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 20),
            ),
            border=ft.border.all(1, ft.Colors.GREY_200),
            # Center the container both horizontally and vertically
            alignment=ft.alignment.center,
        )
    
        # Wrap in a container that centers both horizontally and vertically
        centered_layout = ft.Container(
            content=main_layout,
            expand=True,  # Take up all available space
            alignment=ft.alignment.center,  # Center the content
        )
    
        return centered_layout