import flet as ft
from widgets.LogFileTxt import logger
from widgets.Loading_Spinner_Widget import Loading_Spinner_Widget
from widgets.Bar_Chart_Widget import Bar_Chart_Widget
from .File_Exporter_Handler import File_Exporter_Handler

class Results_Buttons:
    """Results action buttons component."""
    
    def __init__(self, controller, page: ft.Page, file_exporter_handler: File_Exporter_Handler):
        self.controller = controller
        self.page = page
        self.file_exporter_handler = file_exporter_handler
    
    def create(self) -> ft.Row:
        """Create results buttons row."""
        buttons = [
            self._create_view_chart_button(),
            self._create_export_button(),
        ]
        
        if self.controller.get_database_selected_flag():
            buttons.append(self._create_write_database_button())
        
        return ft.Row(buttons)
    
    def _create_view_chart_button(self) -> ft.ElevatedButton:
        """Create View Chart button."""
        return ft.ElevatedButton(
            text="View Chart",
            icon=ft.Icons.BAR_CHART,
            bgcolor=ft.Colors.TERTIARY,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.page.run_task(self._on_view_chart_click, e),
            style=self._create_button_style()
        )
    
    def _create_export_button(self) -> ft.ElevatedButton:
        """Create Export button."""
        return ft.ElevatedButton(
            text="Export to TXT",
            icon=ft.Icons.DOWNLOAD,
            bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.file_exporter_handler.open_export_dialog(),
            style=self._create_button_style()
        )
    
    def _create_write_database_button(self) -> ft.ElevatedButton:
        """Create Write to Database button."""
        return ft.ElevatedButton(
            text="Write to Database",
            icon=ft.Icons.STORAGE,
            bgcolor=ft.Colors.ORANGE_700,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.page.run_task(
                self.controller._on_write_database_click, e
            ),
            style=self._create_button_style()
        )
    
    async def _on_view_chart_click(self, event):
        """Handle View Chart button click."""
        logger.write("View Chart button clicked")
        
        loading_spinner = Loading_Spinner_Widget(self.page)
        loading_spinner.show_dialog()
        
        await loading_spinner.simulate_progressive_loading(
            0.0, 0.2, 0.1, "Preparing Chart..."
        )
        
        species_data = self.controller._click_on_show_chart_button()
        self._show_biomass_chart(species_data)
        
        logger.write("Biomass chart displayed")
        await loading_spinner.simulate_progressive_loading(
            1.0, 1.0, 0.1, "Completed..."
        )
        loading_spinner.hide()
    
    def _show_biomass_chart(self, species_data):
        """Show biomass chart."""
        chart = Bar_Chart_Widget(self.page, species_data=species_data).build()
        logger.write("Biomass chart displayed")
        self.page.overlay.append(chart)
        self.page.update()
    
    def _create_button_style(self) -> ft.ButtonStyle:
        """Create button style."""
        return ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(10)),
            padding=ft.padding.symmetric(horizontal=20, vertical=10)
        )