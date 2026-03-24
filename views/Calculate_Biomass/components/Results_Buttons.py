import os
import json
import flet as ft
from widgets.LogFileTxt import logger
from widgets.Loading_Spinner_Widget import Loading_Spinner_Widget
from widgets.Bar_Chart_Widget import Bar_Chart_Widget
from .File_Exporter_Handler import File_Exporter_Handler
from constants.Json_File_Path_Constants import json_paths
_DB_JSON_PATH = "data/selected_database.json"


class Results_Buttons:
    """Results action buttons component."""

    def __init__(self, controller, page: ft.Page,
                 file_exporter_handler: File_Exporter_Handler):
        self.controller            = controller
        self.page                  = page
        self.file_exporter_handler = file_exporter_handler

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _btn(self, label, icon, on_click, bgcolor, tooltip=None):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=13, color="#FFFFFF"),
                ft.Text(label, size=12, weight=ft.FontWeight.W_600, color="#FFFFFF"),
            ], spacing=6, tight=True),
            on_click=on_click,
            bgcolor=bgcolor,
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
            ink=True,
            tooltip=tooltip,
        )

    def create(self) -> ft.Row:
        buttons = [
            self._btn("View Chart", ft.Icons.BAR_CHART_ROUNDED,
                      lambda e: self.page.run_task(self._on_view_chart_click, e),
                      "#2563EB", "View biomass chart"),
            self._btn("Export TXT", ft.Icons.DOWNLOAD_ROUNDED,
                      lambda e: self.file_exporter_handler.open_export_dialog(),
                      "#16A34A", "Export results to TXT"),
        ]
        if self.controller.get_database_selected_flag():
            buttons.append(
                self._btn("Write to DB", ft.Icons.STORAGE_ROUNDED,
                          lambda e: self.page.run_task(
                              self.controller._on_write_database_click, e),
                          "#D97706", "Write results to database")
            )
        return ft.Row(buttons, spacing=8)

    def _resolve_source_label(self) -> str:
        """Return output table name (DB mode) or filename (file mode)."""
        if self.controller.get_database_selected_flag():
            equation_type = self.controller.get_equation_type()
            table_map = {
                "DBH-based":          "tCalcBiomassOutputD",
                "DBH + Height-based": "tCalcBiomassOutputDH",
            }
            table = table_map.get(equation_type, "tCalcBiomassOutput")
            return f"Table: {table}"
        else:
            file_path = self.file_exporter_handler.selected_file_path or ""
            if file_path:
                return os.path.basename(file_path)
            else:
                try:
                    with open(json_paths.INPUT_TEXT_FILE_NAME, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    return data.get("input_text_file_name", "input file")
                except Exception:
                    return "input file"
    async def _on_view_chart_click(self, event):
        logger.write("View Chart button clicked")
        spinner = Loading_Spinner_Widget(self.page)
        spinner.show_dialog()
        await spinner.simulate_progressive_loading(0.0, 0.2, 0.1, "Preparing Chart...")
        species_data = self.controller._click_on_show_chart_button()
        spinner.hide()
        source_label = self._resolve_source_label()
        chart = Bar_Chart_Widget(
            self.page,
            species_data=species_data,
            source_label=source_label,
        ).build()
        self.page.overlay.append(chart)
        self.page.update()
        logger.write("Biomass chart displayed")