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

    def __init__(self, controller, page: ft.Page,
                 results_loader: Results_Data_Loader,
                 file_exporter_handler: File_Exporter_Handler):
        self.controller       = controller
        self.page             = page
        self.results_loader   = results_loader
        self.file_exporter_handler = file_exporter_handler
        self.results_buttons  = Results_Buttons(controller, page, file_exporter_handler)

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):          return "#1A1A1A" if self._is_dark else "#FFFFFF"
    def _surface(self):     return "#222222" if self._is_dark else "#F8FAFC"
    def _surface_card(self):return "#2A2A2A" if self._is_dark else "#FFFFFF"
    def _border(self):      return "#2E2E2E" if self._is_dark else "#E2E8F0"
    def _divider(self):     return "#333333" if self._is_dark else "#F1F5F9"
    def _text_primary(self):return "#F5F5F5" if self._is_dark else "#0F172A"
    def _text_secondary(self): return "#888888" if self._is_dark else "#64748B"
    def _heading_bg(self):  return "#1E3A2F" if self._is_dark else "#16A34A"

    # ── Public ────────────────────────────────────────────────────────────────

    def create(self) -> ft.Container:
        data = self.results_loader.load()
        if not data:
            return self._empty_state()

        display_data = data[:self._MAX_DISPLAY_ROWS]
        return self._build_card(display_data, len(data))

    # ── Card wrapper ──────────────────────────────────────────────────────────

    def _build_card(self, display_data: list, total_records: int) -> ft.Container:
        headers = list(display_data[0].keys()) if display_data else []

        # Table
        columns = [
            ft.DataColumn(
                ft.Text(h, size=11, weight=ft.FontWeight.W_700, color="#FFFFFF")
            )
            for h in headers
        ]
        rows = []
        for i, item in enumerate(display_data):
            row_bg = ft.Colors.with_opacity(
                0.04 if i % 2 != 0 else 0.0,
                ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK,
            )
            rows.append(ft.DataRow(
                color=row_bg,
                cells=[
                    ft.DataCell(self._format_cell(h, item.get(h)))
                    for h in headers
                ],
            ))

        table = ft.DataTable(
            columns=columns,
            rows=rows,
            heading_row_color=self._heading_bg(),
            heading_row_height=40,
            data_row_min_height=38,
            data_row_max_height=38,
            column_spacing=14,
            horizontal_margin=12,
            divider_thickness=0,
            show_checkbox_column=False,
        )

        table_container = ft.Container(
            content=ft.Column([
                ft.Row([table], scroll=ft.ScrollMode.ADAPTIVE),
            ], scroll=ft.ScrollMode.ADAPTIVE, spacing=0),
            border=ft.border.all(1, self._border()),
            border_radius=ft.border_radius.all(8),
            bgcolor=self._surface_card(),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        # Info strip
        info_strip = ft.Row([
            ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=13,
                        color=self._text_secondary()),
                ft.Text(
                    f"Showing {len(display_data)} of {total_records} records",
                    size=12, color=self._text_secondary(),
                ),
            ], spacing=6),
            ft.Row([
                ft.Icon(ft.Icons.SWAP_HORIZ_ROUNDED, size=13,
                        color=self._text_secondary()),
                ft.Text("Scroll horizontally to see all columns",
                        size=12, color=self._text_secondary()),
            ], spacing=6),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Card header
        card_header = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.TABLE_CHART_ROUNDED,
                                        size=15, color="#16A34A"),
                        bgcolor=ft.Colors.with_opacity(0.10, "#16A34A"),
                        border_radius=ft.border_radius.all(7),
                        width=30, height=30,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text("Calculated Biomass Results", size=15,
                            weight=ft.FontWeight.W_700,
                            color=self._text_primary()),
                ], spacing=10),
                self.results_buttons.create(),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
               vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(left=16, right=16, top=14, bottom=12),
            bgcolor=self._surface(),
        )

        return ft.Container(
            content=ft.Column([
                card_header,
                ft.Container(height=1, bgcolor=self._border()),
                ft.Container(
                    content=ft.Column([
                        info_strip,
                        ft.Container(height=10),
                        table_container,
                    ], spacing=0),
                    padding=ft.padding.all(16),
                    bgcolor=self._bg(),
                ),
            ], spacing=0),
            bgcolor=self._bg(),
            border=ft.border.all(1, self._border()),
            border_radius=ft.border_radius.all(10),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=8,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            margin=ft.margin.all(20),
        )

    # ── Cell formatter ────────────────────────────────────────────────────────

    def _format_cell(self, header: str, value) -> ft.Text:
        if value is None:
            return ft.Text("N/A", size=12, color=self._text_secondary())
        if isinstance(value, (int, float)):
            display = f"{value:.1f}" if header in self._BIOMASS_COLUMNS else str(value)
        else:
            display = str(value)
        return ft.Text(display, size=12, color=self._text_primary())

    # ── Empty state ───────────────────────────────────────────────────────────

    def _empty_state(self) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(ft.Icons.TABLE_CHART_OUTLINED, size=30,
                                    color=ft.Colors.with_opacity(0.4, ft.Colors.PRIMARY)),
                    bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.PRIMARY),
                    border_radius=ft.border_radius.all(24),
                    width=56, height=56,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=10),
                ft.Text("No results available", size=14,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.ON_SURFACE,
                        text_align=ft.TextAlign.CENTER),
                ft.Text("Run a biomass calculation to see results here.",
                        size=12, color=ft.Colors.ON_SURFACE_VARIANT,
                        text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
               spacing=0, tight=True),
            padding=ft.padding.symmetric(vertical=32),
            alignment=ft.alignment.center,
            margin=ft.margin.all(20),
        )