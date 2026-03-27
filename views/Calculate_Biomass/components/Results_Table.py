import flet as ft
from .Results_Buttons import Results_Buttons
from helper_functions.Results_Data_Loader import Results_Data_Loader
from .File_Exporter_Handler import File_Exporter_Handler


class Results_Table:
    """Results table component with pagination."""

    _PAGE_SIZE = 10
    _BIOMASS_COLUMNS = {
        "Wood (KG)", "Bark (KG)", "Branch (KG)", "Foliage (KG)",
        "Stem (KG)", "Crown (KG)", "Total (KG)"
    }

    _COLUMN_ORDER = [
    "Wood (KG)",
    "Bark (KG)",
    "Foliage (KG)",
    "Branch (KG)",
    "Crown (KG)",
    "Stem (KG)",
    "Total (KG)",
    ]

    def __init__(self, controller, page: ft.Page,
                 results_loader: Results_Data_Loader,
                 file_exporter_handler: File_Exporter_Handler):
        self.controller            = controller
        self.page                  = page
        self.results_loader        = results_loader
        self.file_exporter_handler = file_exporter_handler
        self.results_buttons       = Results_Buttons(controller, page, file_exporter_handler)

        self._current_page = 0
        self._all_data: list = []

        # Persistent controls updated in-place on page change
        self._table_col      = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, spacing=0)
        self._info_text      = ft.Text("", size=12)
        self._page_label     = ft.Text("", size=12)
        self._pills_row      = ft.Row(spacing=4)
        self._prev_btn       = self._make_nav_btn("Previous", ft.Icons.ARROW_BACK_IOS_ROUNDED,  self._go_prev)
        self._next_btn       = self._make_nav_btn("Next",     ft.Icons.ARROW_FORWARD_IOS_ROUNDED, self._go_next)

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):           return "#1A1A1A" if self._is_dark else "#FFFFFF"
    def _surface(self):      return "#222222" if self._is_dark else "#F8FAFC"
    def _surface_card(self): return "#2A2A2A" if self._is_dark else "#FFFFFF"
    def _border(self):       return "#2E2E2E" if self._is_dark else "#E2E8F0"
    def _text_primary(self): return "#F5F5F5" if self._is_dark else "#0F172A"
    def _text_secondary(self): return "#888888" if self._is_dark else "#64748B"
    def _heading_bg(self):   return "#1E3A2F" if self._is_dark else "#16A34A"

    # ── Pagination helpers ────────────────────────────────────────────────────

    @property
    def _total_pages(self):
        return max(1, (len(self._all_data) + self._PAGE_SIZE - 1) // self._PAGE_SIZE)

    @property
    def _page_data(self):
        start = self._current_page * self._PAGE_SIZE
        return self._all_data[start: start + self._PAGE_SIZE]

    def _go_prev(self, e):
        if self._current_page > 0:
            self._current_page -= 1
            self._update_table()

    def _go_next(self, e):
        if self._current_page < self._total_pages - 1:
            self._current_page += 1
            self._update_table()

    def _jump_to(self, p: int):
        if p != self._current_page:
            self._current_page = p
            self._update_table()

    # ── Nav button (persistent container) ────────────────────────────────────

    def _make_nav_btn(self, label, icon, on_click) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=13),
                ft.Text(label, size=12, weight=ft.FontWeight.W_500),
            ], spacing=5, tight=True),
            on_click=on_click,
            border_radius=ft.border_radius.all(7),
            padding=ft.padding.symmetric(horizontal=12, vertical=7),
            animate=ft.Animation(150, ft.AnimationCurve.LINEAR),
        )

    def _style_nav_btn(self, btn: ft.Container, disabled: bool, icon_name):
        color = self._text_secondary() if disabled else self._text_primary()
        row   = btn.content
        row.controls[0].color = color
        row.controls[1].color = color
        btn.bgcolor  = ft.Colors.with_opacity(
            0.04 if disabled else 0.06,
            ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK,
        )
        btn.border   = ft.border.all(1, self._border())
        btn.opacity  = 0.4 if disabled else 1.0
        btn.on_click = None if disabled else btn.on_click if btn.on_click else None
        # restore correct callback
        if not disabled:
            if "Previous" in row.controls[1].value:
                btn.on_click = self._go_prev
            else:
                btn.on_click = self._go_next
        else:
            btn.on_click = None

    # ── Update in-place ───────────────────────────────────────────────────────

    def _update_table(self):
        display_data  = self._page_data
        total_records = len(self._all_data)

        headers = []

        if display_data:
            first_row = display_data[0]

            # Keep columns in desired order
            headers = [h for h in self._COLUMN_ORDER if h in first_row]

            # Add any extra columns not in _COLUMN_ORDER
            headers += [h for h in first_row.keys() if h not in headers]

        # Rebuild table rows
        columns = [
            ft.DataColumn(ft.Text(h, size=11, weight=ft.FontWeight.W_700, color="#FFFFFF"))
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
                cells=[ft.DataCell(self._format_cell(h, item.get(h))) for h in headers],
            ))

        table = ft.DataTable(
            columns=columns, rows=rows,
            heading_row_color=self._heading_bg(),
            heading_row_height=40,
            data_row_min_height=38, data_row_max_height=38,
            column_spacing=14, horizontal_margin=12,
            divider_thickness=0, show_checkbox_column=False,
        )
        self._table_col.controls = [ft.Row([table], scroll=ft.ScrollMode.ADAPTIVE)]

        # Update info text
        start_rec = self._current_page * self._PAGE_SIZE + 1
        end_rec   = min(start_rec + self._PAGE_SIZE - 1, total_records)
        self._info_text.value = f"Showing {start_rec}–{end_rec} of {total_records} records"
        self._info_text.color = self._text_secondary()

        # Update page label
        self._page_label.value = f"Page {self._current_page + 1} of {self._total_pages}"
        self._page_label.color = self._text_secondary()

        # Rebuild pills
        self._rebuild_pills(update=False)  # ← don't call .update() on pills directly

        # Style nav buttons
        prev_disabled = self._current_page <= 0
        next_disabled = self._current_page >= self._total_pages - 1
        self._style_nav_btn(self._prev_btn, prev_disabled, ft.Icons.ARROW_BACK_IOS_ROUNDED)
        self._style_nav_btn(self._next_btn, next_disabled, ft.Icons.ARROW_FORWARD_IOS_ROUNDED)

        # ✅ One single page update — no individual control .update() calls needed
        self.page.update()
    def _rebuild_pills(self, update=True):
        cp    = self._current_page
        total = self._total_pages
        pills = []

        # Which page numbers to show
        if total <= 7:
            indices = list(range(total))
        else:
            keep = sorted({0, total - 1, cp,
                           max(0, cp - 1), min(total - 1, cp + 1)})
            indices = keep

        prev_idx = -1
        for p in indices:
            if prev_idx >= 0 and p > prev_idx + 1:
                pills.append(ft.Text("…", size=12, color=self._text_secondary()))
            is_active = (p == cp)
            pills.append(ft.Container(
                content=ft.Text(
                    str(p + 1), size=12,
                    weight=ft.FontWeight.W_700 if is_active else ft.FontWeight.W_400,
                    color="#FFFFFF" if is_active else self._text_secondary(),
                ),
                on_click=(lambda e, pg=p: self._jump_to(pg)) if not is_active else None,
                bgcolor="#16A34A" if is_active else ft.Colors.with_opacity(
                    0.06, ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK,
                ),
                border=ft.border.all(1, "#16A34A" if is_active else self._border()),
                border_radius=ft.border_radius.all(6),
                width=32, height=30,
                alignment=ft.alignment.center,
                ink=not is_active,
            ))
            prev_idx = p

        self._pills_row.controls = pills
        if update:
            self._pills_row.update()

    # ── Public ────────────────────────────────────────────────────────────────

    def create(self) -> ft.Container:
        self._all_data     = self.results_loader.load() or []
        self._current_page = 0
        if not self._all_data:
            return self._empty_state()
        return self._build_card()

    # ── Card (built once, updated in-place) ───────────────────────────────────

    def _build_card(self) -> ft.Container:
        display_data  = self._page_data
        total_records = len(self._all_data)
        print("Display data for page 1:", display_data[0].keys())  # Debug log
        headers       = list(display_data[0].keys()) if display_data else []

        # Initial table
        columns = [
            ft.DataColumn(ft.Text(h, size=11, weight=ft.FontWeight.W_700, color="#FFFFFF"))
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
                cells=[ft.DataCell(self._format_cell(h, item.get(h))) for h in headers],
            ))

        table = ft.DataTable(
            columns=columns, rows=rows,
            heading_row_color=self._heading_bg(),
            heading_row_height=40,
            data_row_min_height=38, data_row_max_height=38,
            column_spacing=14, horizontal_margin=12,
            divider_thickness=0, show_checkbox_column=False,
        )
        self._table_col.controls = [ft.Row([table], scroll=ft.ScrollMode.ADAPTIVE)]

        # Info text
        start_rec = 1
        end_rec   = min(self._PAGE_SIZE, total_records)
        self._info_text.value = f"Showing {start_rec}–{end_rec} of {total_records} records"
        self._info_text.color = self._text_secondary()

        # Page label
        self._page_label.value = f"Page 1 of {self._total_pages}"
        self._page_label.color = self._text_secondary()

        # Pills — no update() during initial build, controls not on page yet
        self._rebuild_pills(update=False)

        # Style nav buttons (no .update — not on page yet)
        self._style_nav_btn(self._prev_btn, True,  ft.Icons.ARROW_BACK_IOS_ROUNDED)
        self._style_nav_btn(self._next_btn, self._total_pages <= 1,
                            ft.Icons.ARROW_FORWARD_IOS_ROUNDED)

        table_container = ft.Container(
            content=self._table_col,
            border=ft.border.all(1, self._border()),
            border_radius=ft.border_radius.only(top_left=8, top_right=8),
            bgcolor=self._surface_card(),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        pagination_bar = ft.Container(
            content=ft.Row([
                self._page_label,
                ft.Container(expand=True),
                self._prev_btn,
                ft.Container(width=6),
                self._pills_row,
                ft.Container(width=6),
                self._next_btn,
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=16, vertical=10),
            bgcolor=self._surface(),
            border=ft.border.only(top=ft.BorderSide(1, self._border())),
            border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
        )

        info_strip = ft.Row([
            ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=13,
                        color=self._text_secondary()),
                self._info_text,
            ], spacing=6),
            ft.Row([
                ft.Icon(ft.Icons.SWAP_HORIZ_ROUNDED, size=13,
                        color=self._text_secondary()),
                ft.Text("Scroll horizontally to see all columns",
                        size=12, color=self._text_secondary()),
            ], spacing=6),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

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
                        pagination_bar,
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