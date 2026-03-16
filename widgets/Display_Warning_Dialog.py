import flet as ft
import numpy as np


class Display_Warning_Dialog:
    """Warning dialog showing validation, measurement, and duplication errors."""

    def __init__(self, page: ft.Page, error_messages,
                 error_message_for_out_of_bounds_dbh_or_height_value,
                 raw_data=None):
        """
        Parameters
        ----------
        raw_data : list[dict] | None
            The full parsed dataset rows (dicts with lowercase keys).
            If supplied, duplicate rows are detected automatically.
            If None the Duplication tab shows an empty state.
        """
        self.page = page
        self.error_messages = error_messages
        self.error_message_for_out_of_bounds_dbh_or_height_value = \
            error_message_for_out_of_bounds_dbh_or_height_value
        self.raw_data = raw_data or []
        self.dialog = None
        self.current_page_validation  = 0
        self.current_page_measurement = 0
        self.current_page_duplication = 0
        self.rows_per_page  = 20
        self.tabs_control   = None

        # Pre-detect duplicates once on init
        self._duplicate_groups = self._detect_duplicates()

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):           return "#1A1A1A" if self._is_dark else "#FFFFFF"
    def _surface(self):      return "#222222" if self._is_dark else "#F8FAFC"
    def _surface_card(self): return "#2A2A2A" if self._is_dark else "#FFFFFF"
    def _border(self):       return "#2E2E2E" if self._is_dark else "#E2E8F0"
    def _divider(self):      return "#333333" if self._is_dark else "#F1F5F9"
    def _text_primary(self): return "#F5F5F5" if self._is_dark else "#0F172A"
    def _text_secondary(self): return "#888888" if self._is_dark else "#64748B"
    def _heading_bg(self):   return "#3D2A00" if self._is_dark else "#D97706"
    def _dup_heading_bg(self): return "#312E81" if self._is_dark else "#4F46E5"

    # ── Dialog close ──────────────────────────────────────────────────────────

    def close_dialog(self, e=None):
        if self.dialog and self.dialog in self.page.overlay:
            self.page.overlay.remove(self.dialog)
            self.page.update()

    # ── Duplicate detection ───────────────────────────────────────────────────

    _DUP_KEY_COLS = ["plot", "year", "species", "tree number", "dbh", "height"]

    def _detect_duplicates(self) -> list:
        """
        Return a list of duplicate groups.
        Each group = list of (1-based row_index, row_dict) tuples that are identical
        on the key columns.
        """
        if not self.raw_data:
            return []

        from collections import defaultdict
        buckets: dict = defaultdict(list)

        for i, row in enumerate(self.raw_data):
            # normalise keys
            row_lower = {str(k).lower(): v for k, v in row.items()}
            key = tuple(str(row_lower.get(c, "")).strip().lower()
                        for c in self._DUP_KEY_COLS)
            buckets[key].append((i + 1, row_lower))   # 1-based index

        # Only keep buckets with more than one entry
        return [entries for entries in buckets.values() if len(entries) > 1]

    @property
    def _dup_count(self) -> int:
        """Total number of duplicate rows (all instances, not just extras)."""
        return sum(len(g) for g in self._duplicate_groups)

    # ── Data helpers ──────────────────────────────────────────────────────────

    def _convert_row_data_to_lowercase(self, row_data):
        return {str(k).lower(): v for k, v in row_data.items()}

    def _get_paginated_data(self, error_list, current_page):
        total_rows  = len(error_list)
        total_pages = max(1, (total_rows + self.rows_per_page - 1) // self.rows_per_page)
        start_idx   = current_page * self.rows_per_page
        end_idx     = min(start_idx + self.rows_per_page, total_rows)
        return error_list[start_idx:end_idx], total_rows, total_pages, current_page + 1

    # ── Cell builder ──────────────────────────────────────────────────────────

    def _create_cell(self, value, is_error=False, column_name=None,
                     row_data_lower=None, nan_columns_lower=None):
        should_error = is_error
        if value is None or (isinstance(value, float) and np.isnan(value)):
            display_value = "ERROR"
            should_error  = True
        else:
            display_value = str(value)
            if column_name and row_data_lower is not None:
                try:
                    if column_name == 'year':
                        y = int(float(value))
                        if y < 1900 or y > 2100: should_error = True
                    elif column_name == 'tree number':
                        if int(float(value)) <= 0: should_error = True
                    elif column_name == 'speccode':
                        v = float(value)
                        if v != int(v): should_error = True
                    elif column_name == 'dbh':
                        if not (2.5 <= float(value) <= 100.0): should_error = True
                    elif column_name == 'height':
                        if not (1.3 <= float(value) <= 50.0): should_error = True
                except (ValueError, TypeError):
                    should_error = True

        return ft.DataCell(
            ft.Container(
                content=ft.Text(
                    display_value, size=12,
                    color="#DC2626" if should_error else self._text_primary(),
                    weight=ft.FontWeight.W_600 if should_error else ft.FontWeight.W_400,
                ),
                padding=ft.padding.symmetric(horizontal=10, vertical=8),
                bgcolor=ft.Colors.with_opacity(0.08, "#DC2626") if should_error
                        else ft.Colors.TRANSPARENT,
                border_radius=ft.border_radius.all(4) if should_error
                              else ft.border_radius.all(0),
            )
        )

    def _dup_cell(self, value, highlight=False):
        color = "#4F46E5" if highlight else self._text_primary()
        return ft.DataCell(
            ft.Container(
                content=ft.Text(str(value) if value is not None else "—",
                                size=12, color=color,
                                weight=ft.FontWeight.W_600 if highlight
                                       else ft.FontWeight.W_400),
                padding=ft.padding.symmetric(horizontal=10, vertical=8),
            )
        )

    # ── Row builder ───────────────────────────────────────────────────────────

    def _create_table_row(self, error_data, is_tree_measurement_tab: bool):
        rdl      = self._convert_row_data_to_lowercase(error_data['row_data'])
        nan_cols = [c.lower() for c in error_data.get('nan_columns', [])]

        cells = [
            self._create_cell(error_data['index'] + 1),
            self._create_cell(rdl.get('plot'),        'plot'        in nan_cols, 'plot',        rdl, nan_cols),
            self._create_cell(rdl.get('year'),        'year'        in nan_cols, 'year',        rdl, nan_cols),
            self._create_cell(rdl.get('species'),     'species'     in nan_cols, 'species',     rdl, nan_cols),
            self._create_cell(rdl.get('tree number'), 'tree number' in nan_cols, 'tree number', rdl, nan_cols),
            self._create_cell(rdl.get('dbh'),         'dbh'         in nan_cols, 'dbh',         rdl, nan_cols),
            self._create_cell(rdl.get('height'),      'height'      in nan_cols, 'height',      rdl, nan_cols),
        ]

        if is_tree_measurement_tab:
            issues = []
            for col, lo, hi, label in [
                ('dbh',    2.5,  100.0, 'DBH'),
                ('height', 1.3,  50.0,  'Height'),
            ]:
                val = rdl.get(col)
                if val is None or (isinstance(val, float) and np.isnan(val)):
                    issues.append(f"Missing {label}")
                else:
                    try:
                        if not (lo <= float(val) <= hi):
                            issues.append(f"{label} out of bounds")
                    except:
                        issues.append(f"Invalid {label}")
            issue_text = ", ".join(issues) if issues else "Measurement error"
            cells.append(ft.DataCell(
                ft.Container(
                    content=ft.Text(issue_text, size=12, color="#DC2626",
                                    weight=ft.FontWeight.W_500),
                    padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    bgcolor=ft.Colors.with_opacity(0.08, "#DC2626"),
                    border_radius=ft.border_radius.all(4),
                )
            ))

        return ft.DataRow(cells=cells)

    # ── Pagination ────────────────────────────────────────────────────────────

    def _create_pagination_controls(self, total_pages, current_page, on_previous, on_next):
        def _nav_btn(label, icon, on_click, disabled):
            return ft.Container(
                content=ft.Row([
                    ft.Icon(icon, size=14,
                            color=self._text_secondary() if disabled else self._text_primary()),
                    ft.Text(label, size=12, weight=ft.FontWeight.W_500,
                            color=self._text_secondary() if disabled else self._text_primary()),
                ], spacing=6, tight=True),
                on_click=None if disabled else on_click,
                bgcolor=ft.Colors.with_opacity(
                    0.04 if disabled else 0.06,
                    ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK),
                border=ft.border.all(1, self._border()),
                border_radius=ft.border_radius.all(7),
                padding=ft.padding.symmetric(horizontal=14, vertical=8),
                ink=not disabled,
                opacity=0.4 if disabled else 1.0,
            )

        return ft.Container(
            content=ft.Row([
                ft.Text(f"Page {current_page} of {total_pages}",
                        size=12, color=self._text_secondary()),
                ft.Container(expand=True),
                _nav_btn("Previous", ft.Icons.ARROW_BACK_IOS_ROUNDED,
                         on_previous, current_page <= 1),
                ft.Container(width=8),
                _nav_btn("Next", ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                         on_next, current_page >= total_pages),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=self._surface(),
            border=ft.border.only(top=ft.BorderSide(1, self._border())),
            border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
        )

    # ── Generic table builder ─────────────────────────────────────────────────

    def _wrap_table(self, count_label, count_color, table,
                    total_pages, current_page_display,
                    on_previous, on_next) -> ft.Column:
        count_row = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(count_label, size=11,
                                    weight=ft.FontWeight.W_600, color=count_color),
                    bgcolor=ft.Colors.with_opacity(0.08, count_color),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, count_color)),
                    border_radius=ft.border_radius.all(20),
                    padding=ft.padding.symmetric(horizontal=12, vertical=5),
                ),
            ]),
            padding=ft.padding.symmetric(horizontal=16, vertical=10),
        )
        table_card = ft.Container(
            content=ft.Column([
                ft.Row([ft.Container(content=table, expand=True)],
                       scroll=ft.ScrollMode.ADAPTIVE),
            ], scroll=ft.ScrollMode.ADAPTIVE, spacing=0),
            border=ft.border.all(1, self._border()),
            border_radius=ft.border_radius.only(top_left=8, top_right=8),
            bgcolor=self._surface_card(),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            expand=True,
        )
        return ft.Column([
            count_row,
            table_card,
            self._create_pagination_controls(total_pages, current_page_display,
                                             on_previous, on_next),
            ft.Container(height=8),
        ], spacing=0, expand=True)

    # ── Error table ───────────────────────────────────────────────────────────

    def _create_error_table(self, error_list, is_tree_measurement_tab: bool, page_type: str):
        if not error_list:
            return self._empty_state(
                ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED, "#16A34A",
                "No errors found", "All data passed validation checks.",
            )

        current_page = (self.current_page_validation if page_type == "validation"
                        else self.current_page_measurement)
        paginated_data, total_rows, total_pages, current_page_display = \
            self._get_paginated_data(error_list, current_page)

        def go_previous(e):
            if page_type == "validation":
                if self.current_page_validation > 0: self.current_page_validation -= 1
            else:
                if self.current_page_measurement > 0: self.current_page_measurement -= 1
            self._refresh_current_tab()

        def go_next(e):
            if page_type == "validation":
                if self.current_page_validation < total_pages - 1:
                    self.current_page_validation += 1
            else:
                if self.current_page_measurement < total_pages - 1:
                    self.current_page_measurement += 1
            self._refresh_current_tab()

        cols = [ft.DataColumn(ft.Text(h, size=12, weight=ft.FontWeight.W_700, color="#FFFFFF"))
                for h in ["Row", "Plot", "Year", "Species", "Tree Number", "DBH", "Height"]]
        if is_tree_measurement_tab:
            cols.append(ft.DataColumn(
                ft.Text("Issue", size=12, weight=ft.FontWeight.W_700, color="#FFFFFF")))

        table = ft.DataTable(
            columns=cols,
            rows=[self._create_table_row(e, is_tree_measurement_tab) for e in paginated_data],
            vertical_lines=ft.BorderSide(1, self._divider()),
            horizontal_lines=ft.BorderSide(1, self._divider()),
            heading_row_height=42,
            data_row_min_height=40,
            data_row_max_height=40,
            column_spacing=10,
            heading_row_color=self._heading_bg(),
            show_checkbox_column=False,
        )

        return self._wrap_table(
            f"{len(paginated_data)} of {total_rows} errors", "#DC2626",
            table, total_pages, current_page_display, go_previous, go_next,
        )

    # ── Duplication table ─────────────────────────────────────────────────────

    def _build_duplication_tab_content(self):
        groups = self._duplicate_groups
        if not groups:
            return self._empty_state(
                ft.Icons.CONTENT_COPY_OUTLINED, "#4F46E5",
                "No duplicates found",
                "All rows are unique across the key fields.",
            )

        # Flatten groups into a pageable list of (row_num, group_id, row_dict)
        flat: list = []
        for g_idx, group in enumerate(groups):
            for row_num, row_dict in group:
                flat.append((row_num, g_idx + 1, row_dict))
        flat.sort(key=lambda x: x[0])

        current_page = self.current_page_duplication
        paginated_data, total_rows, total_pages, current_page_display = \
            self._get_paginated_data(flat, current_page)

        def go_previous(e):
            if self.current_page_duplication > 0:
                self.current_page_duplication -= 1
            self._refresh_current_tab()

        def go_next(e):
            if self.current_page_duplication < total_pages - 1:
                self.current_page_duplication += 1
            self._refresh_current_tab()

        cols = [
            ft.DataColumn(ft.Text(h, size=12, weight=ft.FontWeight.W_700, color="#FFFFFF"))
            for h in ["Row #", "Group", "Plot", "Year", "Species",
                      "Tree Number", "DBH", "Height"]
        ]

        rows = []
        for row_num, group_id, rdl in paginated_data:
            rows.append(ft.DataRow(cells=[
                self._dup_cell(row_num,            highlight=True),
                self._dup_cell(f"#{group_id}",     highlight=True),
                self._dup_cell(rdl.get('plot')),
                self._dup_cell(rdl.get('year')),
                self._dup_cell(rdl.get('species')),
                self._dup_cell(rdl.get('tree number')),
                self._dup_cell(rdl.get('dbh')),
                self._dup_cell(rdl.get('height')),
            ]))

        table = ft.DataTable(
            columns=cols,
            rows=rows,
            vertical_lines=ft.BorderSide(1, self._divider()),
            horizontal_lines=ft.BorderSide(1, self._divider()),
            heading_row_height=42,
            data_row_min_height=40,
            data_row_max_height=40,
            column_spacing=10,
            heading_row_color=self._dup_heading_bg(),
            show_checkbox_column=False,
        )

        # Summary pill — number of groups
        n_groups = len(groups)
        summary_pill = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=13, color="#4F46E5"),
                ft.Text(
                    f"{n_groups} duplicate group{'s' if n_groups != 1 else ''} "
                    f"· {self._dup_count} affected rows  ·  "
                    "Rows sharing identical Plot / Year / Species / Tree Number / DBH / Height",
                    size=11, weight=ft.FontWeight.W_500, color=self._text_secondary(),
                ),
            ], spacing=8),
            bgcolor=ft.Colors.with_opacity(0.07, "#4F46E5"),
            border=ft.border.all(1, ft.Colors.with_opacity(0.15, "#4F46E5")),
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            margin=ft.margin.only(bottom=10),
        )

        return ft.Column([
            summary_pill,
            self._wrap_table(
                f"{len(paginated_data)} of {total_rows} duplicate rows", "#4F46E5",
                table, total_pages, current_page_display, go_previous, go_next,
            ),
        ], spacing=0, expand=True)

    # ── Empty state ───────────────────────────────────────────────────────────

    def _empty_state(self, icon, color, title, subtitle) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(icon, size=36, color=color),
                    bgcolor=ft.Colors.with_opacity(0.08, color),
                    border_radius=ft.border_radius.all(24),
                    width=60, height=60,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=12),
                ft.Text(title, size=15, weight=ft.FontWeight.W_700,
                        color=self._text_primary(), text_align=ft.TextAlign.CENTER),
                ft.Text(subtitle, size=13,
                        color=self._text_secondary(), text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
               spacing=0, tight=True),
            padding=ft.padding.symmetric(vertical=40),
            alignment=ft.alignment.center,
        )

    # ── Refresh ───────────────────────────────────────────────────────────────

    def _refresh_current_tab(self):
        if not self.tabs_control or not self.tabs_control.tabs:
            return
        idx = self.tabs_control.selected_index
        if idx == 0:
            self.tabs_control.tabs[0].content.content = \
                self._create_error_table(self.error_messages, False, "validation")
        elif idx == 1:
            self.tabs_control.tabs[1].content = \
                self._build_measurement_tab_content()
        else:
            self.tabs_control.tabs[2].content.content = \
                self._build_duplication_tab_content()
        self.tabs_control.update()
        self.page.update()

    # ── Info banner ───────────────────────────────────────────────────────────

    def _build_info_banner(self):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=15, color="#2563EB"),
                    bgcolor=ft.Colors.with_opacity(0.10, "#2563EB"),
                    border_radius=ft.border_radius.all(6),
                    width=28, height=28,
                    alignment=ft.alignment.center,
                ),
                ft.Text("DBH range: 2.5 – 100.0 cm   ·   Height range: 1.3 – 50.0 m",
                        size=12, weight=ft.FontWeight.W_500,
                        color=self._text_secondary()),
            ], spacing=10),
            bgcolor=ft.Colors.with_opacity(0.07, "#2563EB"),
            border=ft.border.all(1, ft.Colors.with_opacity(0.15, "#2563EB")),
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            margin=ft.margin.only(bottom=10),
        )

    def _build_measurement_tab_content(self):
        return ft.Column([
            self._build_info_banner(),
            self._create_error_table(
                self.error_message_for_out_of_bounds_dbh_or_height_value,
                True, "measurement"
            ),
        ], spacing=0, expand=True)

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self):
        v_count = len(self.error_messages)
        m_count = len(self.error_message_for_out_of_bounds_dbh_or_height_value)
        d_count = self._dup_count
        total   = v_count + m_count + d_count

        def _badge(count, label, color):
            return ft.Container(
                content=ft.Row([
                    ft.Text(str(count), size=12, weight=ft.FontWeight.W_700, color=color),
                    ft.Text(label, size=11,
                            color=ft.Colors.with_opacity(0.75, "#FFFFFF")),
                ], spacing=5, tight=True),
                bgcolor=ft.Colors.with_opacity(0.18, "#FFFFFF"),
                border_radius=ft.border_radius.all(20),
                padding=ft.padding.symmetric(horizontal=10, vertical=4),
            )

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=22, color="#FFFFFF"),
                    bgcolor=ft.Colors.with_opacity(0.18, "#FFFFFF"),
                    border_radius=ft.border_radius.all(10),
                    width=44, height=44,
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text("Validation Warnings", size=18,
                            weight=ft.FontWeight.W_700, color="#FFFFFF"),
                    ft.Row([
                        _badge(total,   "total",         "#FFFFFF"),
                        _badge(v_count, "validation",    "#FCA5A5"),
                        _badge(m_count, "measurement",   "#FCD34D"),
                        _badge(d_count, "duplicates",    "#C4B5FD"),
                    ], spacing=6),
                ], spacing=4, expand=True),
                ft.Container(
                    content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=16, color="#FFFFFF"),
                    on_click=self.close_dialog,
                    bgcolor=ft.Colors.with_opacity(0.15, "#FFFFFF"),
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.all(6),
                    ink=True,
                    tooltip="Close",
                ),
            ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#D97706",
            padding=ft.padding.symmetric(horizontal=24, vertical=18),
            border_radius=ft.border_radius.only(top_left=14, top_right=14),
        )

    # ── Actions bar ───────────────────────────────────────────────────────────

    def _build_actions(self):
        return ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CLOSE_ROUNDED, size=14, color="#FFFFFF"),
                        ft.Text("Close", size=13, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                    ], spacing=6, tight=True),
                    on_click=self.close_dialog,
                    bgcolor="#D97706",
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    ink=True,
                ),
            ]),
            padding=ft.padding.only(left=24, right=24, top=12, bottom=16),
            bgcolor=self._bg(),
            border=ft.border.only(top=ft.BorderSide(1, self._border())),
            border_radius=ft.border_radius.only(bottom_left=14, bottom_right=14),
        )

    # ── Show ──────────────────────────────────────────────────────────────────

    def show_dialog(self):
        self.current_page_validation  = 0
        self.current_page_measurement = 0
        self.current_page_duplication = 0

        initial_tab = 0
        if (len(self.error_message_for_out_of_bounds_dbh_or_height_value) > 0 and
                (len(self.error_messages) == 0 or
                 len(self.error_message_for_out_of_bounds_dbh_or_height_value) >
                 len(self.error_messages))):
            initial_tab = 1

        def _tab_container(content):
            return ft.Container(
                content=content,
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                expand=True,
                bgcolor=self._bg(),
            )

        self.tabs_control = ft.Tabs(
            selected_index=initial_tab,
            animation_duration=200,
            indicator_color="#D97706",
            indicator_tab_size=True,
            label_color="#D97706",
            unselected_label_color=self._text_secondary(),
            divider_color=self._border(),
            tabs=[
                ft.Tab(
                    text="Validation Errors",
                    icon=ft.Icons.WARNING_AMBER_ROUNDED,
                    content=_tab_container(
                        self._create_error_table(self.error_messages, False, "validation")
                    ),
                ),
                ft.Tab(
                    text="Measurement Errors",
                    icon=ft.Icons.STRAIGHTEN_ROUNDED,
                    content=_tab_container(self._build_measurement_tab_content()),
                ),
                ft.Tab(
                    text="Duplicates",
                    icon=ft.Icons.CONTENT_COPY_OUTLINED,
                    content=_tab_container(self._build_duplication_tab_content()),
                ),
            ],
            expand=True,
        )

        max_h = min((self.page.height or 700) * 0.88, 700)

        main_panel = ft.Container(
            content=ft.Column([
                self._build_header(),
                ft.Container(
                    content=self.tabs_control,
                    expand=True,
                    bgcolor=self._bg(),
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
                self._build_actions(),
            ], spacing=0, expand=True),
            height=max_h,
            bgcolor=self._bg(),
            border_radius=ft.border_radius.all(14),
            shadow=ft.BoxShadow(
                blur_radius=40, spread_radius=0,
                color=ft.Colors.with_opacity(0.35, ft.Colors.BLACK),
                offset=ft.Offset(0, 10),
            ),
        )

        self.dialog = ft.Container(
            content=ft.Container(
                content=main_panel,
                margin=ft.margin.symmetric(horizontal=40, vertical=30),
            ),
            bgcolor=ft.Colors.with_opacity(0.75, ft.Colors.BLACK),
            alignment=ft.alignment.center,
            expand=True,
        )

        return self.dialog

    # ── Public helpers ────────────────────────────────────────────────────────

    def display_error_card_for_validation_information(self):
        return self._create_error_table(self.error_messages, False, "validation")

    def display_error_card_for_tree_measurements_information(self):
        return self._create_error_table(
            self.error_message_for_out_of_bounds_dbh_or_height_value, True, "measurement"
        )

    def __del__(self):
        pass