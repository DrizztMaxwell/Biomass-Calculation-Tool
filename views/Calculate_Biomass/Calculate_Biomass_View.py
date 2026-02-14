import flet as ft
from typing import Optional
from widgets.Hardwood_or_Softwood_Dialog import HardwoodOrSoftwoodDialog
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
from widgets.LogFileTxt import logger
from .components.Layout import Layout
from .components.Results_Table import Results_Table
from .components.File_Exporter_Handler import File_Exporter_Handler
from helper_functions.Results_Data_Loader import Results_Data_Loader
from constants.Biomass_Config import Biomass_Config
from constants.Json_File_Path_Constants import json_paths
class Calculate_Biomass_View:
    """Main view for calculating and displaying biomass results."""
    
    def __init__(self, controller, page: ft.Page, selected_file_path: Optional[str] = None):
        self.controller = controller
        self.page = page
        self.selected_file_path = selected_file_path
        self.is_button_disabled = False
        self.is_database_selected = False
        self.hardwood_softwood_dialog = None
        # Constants
        self._RESULTS_JSON_PATH = json_paths.BIOMASS_RESULTS_PATH
        self._STORAGE_DIR = 'storage'
        self._MAX_DISPLAY_ROWS = 10
        self._BIOMASS_COLUMNS = set(Biomass_Config.BIOMASS_COLUMNS)
        
        # Initialize components
        self.results_loader = Results_Data_Loader()
        self.layout = Layout(controller, page)
        self.export_handler = File_Exporter_Handler(page, selected_file_path, controller)
        self.results_table = Results_Table(controller, page, self.results_loader, self.export_handler)
        
        print("Calculate_Biomass_View initialized")
    
    def build(self) -> ft.Column:
        """Build main view."""
        return self.layout.build()
    
    # -------------------------
    # PUBLIC METHODS
    # -------------------------
    def display_success_message(self, message: str):
        """Display success message."""
        Custom_Alert_Dialog(
            self.page,
            title_icon=ft.Icons.CHECK_CIRCLE,
            title_icon_color=ft.Colors.GREEN,
            title_color=ft.Colors.GREEN,
            title="Success",
            message=message,
            button_text="OK",
        ).show()
        self.page.update()
    def show_results(self):
        """Display results table."""
        results_content = self.results_table.create()
        self.layout.show_results_table(results_content)
        self.layout.scroll_to_results()
        
        if self.page:
            self.page.update()
            print("Results table updated")
    
    async def show_species_code_dialog(self, missing_species_codes: list):
        """Show species code selection dialog."""
        self.hardwood_softwood_dialog = HardwoodOrSoftwoodDialog(
            self.page,
            missing_species_codes
        )
        
        return await self.hardwood_softwood_dialog.show_species_code_dialog()
    
    def show_error_message(self, message: str):
        """Display error message."""
        Custom_Alert_Dialog(
            self.page,
            title_icon=ft.Icons.ERROR,
            title_icon_color=ft.Colors.RED,
            title_color=ft.Colors.RED,
            title="Error",
            message=message,
            button_text="OK",
        ).show()
        self.page.update()
    
    def show_success_dialog(self, title: str, message: str):
        """Show success dialog."""
        Custom_Alert_Dialog(
            self.page,
            title_icon=ft.Icons.CHECK_CIRCLE,
            title_icon_color=ft.Colors.GREEN,
            title_color=ft.Colors.GREEN,
            title=title,
            message=message,
            button_text="OK",
        ).show()
        self.page.update()
    
    def show_error_dialog(self, title: str, message: str):
        """Show error dialog."""
        Custom_Alert_Dialog(
            self.page,
            title_icon=ft.Icons.ERROR,
            title_icon_color=ft.Colors.RED,
            title_color=ft.Colors.RED,
            title=title,
            message=message,
            button_text="OK",
        ).show()
        self.page.update()
    
    def get_selected_components(self) -> list:
        """Get selected components from components section."""
        return self.layout.components_section.get_selected_components()
    
    # -------------------------
    # BUTTON STATE MANAGEMENT
    # -------------------------
    
    def disable_calculation_button(self, button):
        """Disable calculation button."""
        self.is_button_disabled = True
        button.bgcolor = "#CCCCCC"
        button.color = "#888888"
        button.disabled = True
        button.update()
    
    def enable_calculation_button(self, button):
        """Enable calculation button."""
        self.is_button_disabled = False
        button.bgcolor = ft.Colors.GREEN_700
        button.color = ft.Colors.WHITE
        button.disabled = False
        button.update()