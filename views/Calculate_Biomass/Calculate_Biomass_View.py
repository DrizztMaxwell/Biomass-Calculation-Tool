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

    def __init__(self, controller, page: ft.Page, selected_file_path=None):
        self.controller           = controller
        self.page                 = page
        self.selected_file_path   = selected_file_path
        self.is_button_disabled   = False
        self.is_database_selected = False
        self.hardwood_softwood_dialog = None

        self._RESULTS_JSON_PATH = json_paths.BIOMASS_RESULTS_PATH
        self._STORAGE_DIR       = 'storage'
        self._MAX_DISPLAY_ROWS  = 10
        self._BIOMASS_COLUMNS   = set(Biomass_Config.BIOMASS_COLUMNS)

        self.results_loader  = Results_Data_Loader()
        self.layout          = Layout(controller, page)
        self.export_handler  = File_Exporter_Handler(page, selected_file_path, controller)
        self.results_table   = Results_Table(controller, page,
                                             self.results_loader, self.export_handler)

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _text_primary(self):   return "#F5F5F5" if self._is_dark else "#0F172A"
    def _text_secondary(self): return "#888888" if self._is_dark else "#64748B"
    def _border(self):         return "#2E2E2E" if self._is_dark else "#E2E8F0"

    # ── Build ─────────────────────────────────────────────────────────────────

    def build(self) -> ft.Column:
        return self.layout.build()

    # ── Public methods ────────────────────────────────────────────────────────

    def display_success_message(self, message: str):
        self._alert(ft.Icons.CHECK_CIRCLE_ROUNDED, ft.Colors.GREEN, "Success", message)

    def show_results(self):
        results_content = self.results_table.create()
        self.layout.show_results_table(results_content)
        self.layout.scroll_to_results()
        if self.page:
            self.page.update()

    async def show_species_code_dialog(self, missing_species_codes: list):
        self.hardwood_softwood_dialog = HardwoodOrSoftwoodDialog(
            self.page, missing_species_codes
        )
        return await self.hardwood_softwood_dialog.show_species_code_dialog()

    def show_error_message(self, message: str):
        self._alert(ft.Icons.ERROR_ROUNDED, ft.Colors.RED, "Error", message)

    def show_success_dialog(self, title: str, message: str):
        self._alert(ft.Icons.CHECK_CIRCLE_ROUNDED, ft.Colors.GREEN, title, message)

    def show_error_dialog(self, title: str, message: str):
        self._alert(ft.Icons.ERROR_ROUNDED, ft.Colors.RED, title, message)

    def get_selected_components(self) -> list:
        return self.layout.components_section.get_selected_components()

    # ── Button state ──────────────────────────────────────────────────────────

    def disable_calculation_button(self, button):
        self.is_button_disabled = True
        if hasattr(button, 'bgcolor'):  button.bgcolor  = "#4A4A4A"
        if hasattr(button, 'color'):    button.color    = "#888888"
        if hasattr(button, 'opacity'):  button.opacity  = 0.5
        if hasattr(button, 'disabled'): button.disabled = True
        button.update()

    def enable_calculation_button(self, button):
        self.is_button_disabled = False
        if hasattr(button, 'bgcolor'):  button.bgcolor  = "#16A34A"
        if hasattr(button, 'color'):    button.color    = "#FFFFFF"
        if hasattr(button, 'opacity'):  button.opacity  = 1.0
        if hasattr(button, 'disabled'): button.disabled = False
        button.update()

    # ── Helper ────────────────────────────────────────────────────────────────

    def _alert(self, icon, icon_color, title, message, button_text="OK"):
        Custom_Alert_Dialog(
            self.page,
            title_icon=icon,
            title_icon_color=icon_color,
            title_color=icon_color,
            title=title,
            message=message,
            button_text=button_text,
        ).show()
        self.page.update()