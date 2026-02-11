import flet as ft
from .Results_Buttons import Results_Buttons
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
from helper_functions.Results_Data_Loader import Results_Data_Loader
from .File_Exporter_Handler import File_Exporter_Handler
class Results_Table:
    """Results table component."""
    
    _MAX_DISPLAY_ROWS = 10
    _BIOMASS_COLUMNS = {
        "Wood (KG)", "Bark (KG)", "Branch (KG)", "Foliage (KG)",
        "Stem (KG)", "Crown (KG)", "Total (KG)"
    }
    
    def __init__(self, controller, page: ft.Page, results_loader: Results_Data_Loader, file_exporter_handler: File_Exporter_Handler):
        self.controller = controller
        self.page = page
        self.results_loader = results_loader
        self.file_exporter_handler = file_exporter_handler
        self.results_buttons = Results_Buttons(controller, page, file_exporter_handler)
        
    
    def create(self) -> ft.Container:
        """Create results table."""
        data = self.results_loader.load()
        if not data:
            return self._create_empty_results_message("No biomass results available")
        
        display_data = data[:self._MAX_DISPLAY_ROWS]
        data_table = self._create_data_table(display_data)
        
        return self._wrap_results_table(
            self._create_scrollable_table(data_table, len(data)),
            self.results_buttons.create(),
            len(data)
        )
    
    def _create_data_table(self, display_data: list) -> ft.DataTable:
        """Create data table."""
        if not display_data:
            return ft.DataTable()
        
        headers = list(display_data[0].keys())
        data_rows = []
        
        for item in display_data:
            cells = [
                ft.DataCell(self._format_table_cell(header, item.get(header)))
                for header in headers
            ]
            data_rows.append(ft.DataRow(cells=cells))
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text(header, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                )
                for header in headers
            ],
            rows=data_rows,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            horizontal_margin=10,
            heading_row_color=ft.Colors.GREEN_700,
            heading_row_height=40,
            data_row_color={ft.ControlState.HOVERED: ft.Colors.GREY_100},
            data_text_style=ft.TextStyle(color=ft.Colors.PRIMARY),
            show_checkbox_column=False,
        )
    
    def _format_table_cell(self, header: str, value) -> ft.Text:
        """Format table cell value."""
        if value is None:
            return ft.Text("N/A", color=ft.Colors.PRIMARY)
        
        if isinstance(value, (int, float)):
            if header in self._BIOMASS_COLUMNS:
                formatted_value = f"{value:.4f}"
            else:
                formatted_value = str(value)
        else:
            formatted_value = str(value)
        
        return ft.Text(formatted_value, color=ft.Colors.PRIMARY)
    
    def _create_scrollable_table(self, data_table: ft.DataTable, total_records: int) -> ft.Container:
        """Create scrollable table container."""
        return ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[data_table],
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            shadow=self._create_shadow(),
        )
    
    def _wrap_results_table(self, scrollable_table: ft.Container, buttons_row: ft.Row, total_records: int) -> ft.Container:
        """Wrap results table in final container."""
        return ft.Container(
            border_radius=10,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            content=ft.Column([
                ft.Row([
                    TitleTextWidget("Calculated Biomass Results Table"),
                    buttons_row
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(
                    content=ft.Column([
                        self._create_results_info_row(total_records),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        scrollable_table
                    ])
                )
            ]),
            margin=ft.margin.all(20),
            padding=ft.padding.all(30),
            shadow=self._create_shadow(),
        )
    
    def _create_results_info_row(self, total_records: int) -> ft.Row:
        """Create info row for results."""
        return ft.Row([
            DescriptionText(f"Showing first {self._MAX_DISPLAY_ROWS} of {total_records} records"),
            ft.Text(
                "← Scroll horizontally →",
                color=ft.Colors.GREEN_700,
                size=12,
                weight=ft.FontWeight.W_500
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def _create_empty_results_message(self, message: str) -> ft.Container:
        """Create empty results message."""
        return ft.Container(
            content=ft.Text(message, color=ft.Colors.GREY_600),
            padding=20
        )
    
    def _create_shadow(self) -> ft.BoxShadow:
        """Create consistent shadow."""
        return ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
            offset=ft.Offset(0, 3),
        )