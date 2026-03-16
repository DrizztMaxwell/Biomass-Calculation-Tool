import flet as ft


class Species_Data_Table:
    """
    DataTable that matches the current page width and scrolls horizontally
    on small screens. Pass page so width can be set correctly.
    """

    def __init__(self, page: ft.Page = None):
        self._page = page

        self._table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ROW",          weight=ft.FontWeight.W_700, color=ft.Colors.PRIMARY, size=12)),
                ft.DataColumn(ft.Text("SPECIES",       weight=ft.FontWeight.W_700, color=ft.Colors.PRIMARY, size=12)),
                ft.DataColumn(ft.Text("ORIGIN",        weight=ft.FontWeight.W_700, color=ft.Colors.PRIMARY, size=12)),
                ft.DataColumn(ft.Text("EQUATION TYPE", weight=ft.FontWeight.W_700, color=ft.Colors.PRIMARY, size=12)),
                ft.DataColumn(ft.Text("ACTIONS",       weight=ft.FontWeight.W_700, color=ft.Colors.PRIMARY, size=12)),
            ],
            rows=[],
            border=ft.border.all(0.5, ft.Colors.GREY_200),
            border_radius=10,
            vertical_lines=ft.BorderSide(0.5, ft.Colors.GREY_100),
            horizontal_lines=ft.BorderSide(0.5, ft.Colors.GREY_100),
            heading_row_color=ft.Colors.with_opacity(0.08, ft.Colors.GREEN_700),
            heading_row_height=55,
            data_row_min_height=60,
            data_row_max_height=70,
            column_spacing=30,
            heading_text_style=ft.TextStyle(
                size=12, weight=ft.FontWeight.W_700, color=ft.Colors.GREY_900
            ),
            width=self._table_width(),
        )

        self.scroll_container = ft.Row(
            controls=[self._table],
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
            on_scroll_interval=0,
        )

        # Update table width whenever window resizes
        if page:
            page.on_resized = self._on_resize

    def _table_width(self) -> float:
        if self._page and self._page.width:
            # Subtract sidebar (~180px) + outer margins (~100px)
            return max(400, self._page.width - 320)
        return 900   # sensible default before page.width is known

    def _on_resize(self, e):
        self._table.width = self._table_width()
        self._table.update()

    # ── Proxy ─────────────────────────────────────────────────────────────────

    @property
    def rows(self):
        return self._table.rows

    @rows.setter
    def rows(self, value):
        self._table.rows = value

    @property
    def visible(self):
        return self.scroll_container.visible

    @visible.setter
    def visible(self, value):
        self.scroll_container.visible = value