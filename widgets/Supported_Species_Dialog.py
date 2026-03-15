import flet as ft
import json
from widgets.LogFileTxt import logger
from constants.Json_File_Path_Constants import json_paths


class Supported_Species_Dialog:
    def __init__(self, page: ft.Page):
        self.page = page
        try:
            with open(json_paths.TREE_PARAMS_PATH, "r") as f:
                self.species_data = json.load(f)
                logger.write(f"Loaded species data from {json_paths.TREE_PARAMS_PATH} successfully.")
        except Exception:
            self.species_data = [
                {"SpeciesCode": "1", "SpecCommon": "alpine fir"},
                {"SpeciesCode": "2", "SpecCommon": "lodgepole pine"},
            ]
            logger.write(f"[Error] - Failed to load species data from {json_paths.TREE_PARAMS_PATH}")

        self._current_dialog = None

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self) -> bool:
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):
        return "#1A1A1A" if self._is_dark else "#FFFFFF"

    def _surface(self):
        return "#222222" if self._is_dark else "#F8FAFC"

    def _surface_card(self):
        return "#2A2A2A" if self._is_dark else "#FFFFFF"

    def _border(self):
        return "#2E2E2E" if self._is_dark else "#E2E8F0"

    def _divider(self):
        return "#333333" if self._is_dark else "#F1F5F9"

    def _text_primary(self):
        return "#F5F5F5" if self._is_dark else "#0F172A"

    def _text_secondary(self):
        return "#888888" if self._is_dark else "#64748B"

    def _input_bg(self):
        return "#2A2A2A" if self._is_dark else "#FFFFFF"

    def _search_hint(self):
        return "#555555" if self._is_dark else "#94A3B8"

    # ── Species tile ──────────────────────────────────────────────────────────

    def _create_species_tile(self, code, name, is_last=False):
        formatted_name = str(name).title()
        code_str = str(code) if code else "N/A"

        return ft.Container(
            content=ft.Row([
                # Green icon badge
                ft.Container(
                    content=ft.Icon(ft.Icons.FOREST_OUTLINED, size=16,
                                    color="#16A34A"),
                    width=34, height=34,
                    bgcolor=ft.Colors.with_opacity(0.10, "#16A34A"),
                    border_radius=ft.border_radius.all(8),
                    alignment=ft.alignment.center,
                ),
                ft.Container(width=12),
                # Name + code
                ft.Column([
                    ft.Text(formatted_name, size=13, weight=ft.FontWeight.W_600,
                            color=self._text_primary(),
                            overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(f"Code: {code_str}", size=11,
                            color=self._text_secondary()),
                ], spacing=2, expand=True),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=16, vertical=10),
            border=ft.border.only(
                bottom=ft.BorderSide(1, self._divider()) if not is_last else ft.BorderSide(0)
            ),
        )

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self) -> ft.Container:
        total = len(self.species_data)
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.FOREST_OUTLINED, size=22, color="#FFFFFF"),
                    width=44, height=44,
                    bgcolor=ft.Colors.with_opacity(0.18, "#FFFFFF"),
                    border_radius=ft.border_radius.all(10),
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text("Supported Species", size=18, weight=ft.FontWeight.W_700,
                            color="#FFFFFF"),
                    ft.Text(f"{total} species available", size=12,
                            color=ft.Colors.with_opacity(0.75, "#FFFFFF")),
                ], spacing=2, expand=True),

                # Close button
                ft.Container(
                    content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=16, color="#FFFFFF"),
                    on_click=lambda e: self.page.close(self._current_dialog),
                    bgcolor=ft.Colors.with_opacity(0.15, "#FFFFFF"),
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.all(6),
                    ink=True,
                    tooltip="Close",
                ),
            ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#16A34A",
            padding=ft.padding.symmetric(horizontal=24, vertical=18),
            border_radius=ft.border_radius.only(top_left=14, top_right=14),
        )

    # ── Search bar ────────────────────────────────────────────────────────────

    def _build_search(self, list_column) -> ft.Container:
        def on_clear(e):
            search_input.value = ""
            clear_btn.visible = False
            search_input.update()
            clear_btn.update()
            _rebuild_list("")

        def on_change(e):
            term = (e.control.value or "").strip()
            clear_btn.visible = bool(term)
            clear_btn.update()
            _rebuild_list(term.lower())

        def _rebuild_list(term: str):
            items = []
            matched = [
                s for s in self.species_data
                if not term
                or term in str(s.get("SpecCommon", "")).lower()
                or term in str(s.get("SpeciesCode", "")).lower()
            ]
            for i, s in enumerate(matched):
                items.append(self._create_species_tile(
                    s.get("SpeciesCode"), s.get("SpecCommon"),
                    is_last=(i == len(matched) - 1)
                ))

            # Empty state
            if not items:
                items.append(ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SEARCH_OFF_ROUNDED, size=32,
                                color=ft.Colors.with_opacity(0.3, "#16A34A")),
                        ft.Container(height=8),
                        ft.Text("No species found", size=13,
                                weight=ft.FontWeight.W_600,
                                color=self._text_primary(),
                                text_align=ft.TextAlign.CENTER),
                        ft.Text("Try different keywords", size=12,
                                color=self._text_secondary(),
                                text_align=ft.TextAlign.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                       spacing=0, tight=True),
                    padding=ft.padding.symmetric(vertical=40),
                    alignment=ft.alignment.center,
                ))

            list_column.controls = items
            list_column.update()

        search_input = ft.TextField(
            hint_text="Search by name or code...",
            on_change=on_change,
            border=ft.InputBorder.NONE,
            filled=False,
            color=self._text_primary(),
            hint_style=ft.TextStyle(color=self._search_hint(), size=13),
            text_style=ft.TextStyle(size=13),
            cursor_color=self._text_primary(),
            expand=True,
            content_padding=ft.padding.symmetric(vertical=10),
        )

        clear_btn = ft.Container(
            content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=15,
                            color=self._search_hint()),
            on_click=on_clear,
            visible=False,
            padding=ft.padding.all(4),
            border_radius=ft.border_radius.all(20),
            ink=True,
            tooltip="Clear",
        )

        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SEARCH_ROUNDED, size=17,
                        color=self._search_hint()),
                ft.Container(width=8),
                search_input,
                clear_btn,
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            bgcolor=self._input_bg(),
            border=ft.border.all(1, self._border()),
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.symmetric(horizontal=14, vertical=2),
            margin=ft.margin.symmetric(horizontal=20, vertical=10),
        )

    # ── Actions bar ───────────────────────────────────────────────────────────

    def _build_actions(self) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CLOSE_ROUNDED, size=14, color="#FFFFFF"),
                        ft.Text("Dismiss", size=13, weight=ft.FontWeight.W_600,
                                color="#FFFFFF"),
                    ], spacing=6),
                    on_click=lambda e: self.page.close(self._current_dialog),
                    bgcolor="#16A34A",
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    ink=True,
                ),
            ]),
            padding=ft.padding.only(left=24, right=24, top=12, bottom=16),
            bgcolor=self._bg(),
            border=ft.border.only(top=ft.BorderSide(1, self._border())),
        )

    # ── Main show ─────────────────────────────────────────────────────────────

    def show(self):
        # Build initial list
        tiles = [
            self._create_species_tile(
                s.get("SpeciesCode"), s.get("SpecCommon"),
                is_last=(i == len(self.species_data) - 1)
            )
            for i, s in enumerate(self.species_data)
        ]
        list_column = ft.Column(controls=tiles, spacing=0, tight=True)

        # Results count label
        count_label = ft.Container(
            content=ft.Text(
                f"{len(self.species_data)} species",
                size=11,
                weight=ft.FontWeight.W_500,
                color=self._text_secondary(),
            ),
            padding=ft.padding.only(left=20, bottom=6),
        )

        main = ft.Container(
            content=ft.Column([
                self._build_header(),
                self._build_search(list_column),
                count_label,
                # Scrollable list
                ft.Container(
                    content=ft.ListView(
                        controls=[
                            ft.Container(
                                content=list_column,
                                bgcolor=self._surface_card(),
                                border=ft.border.all(1, self._border()),
                                border_radius=ft.border_radius.all(10),
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                margin=ft.margin.symmetric(horizontal=20),
                            ),
                            ft.Container(height=12),
                        ],
                        spacing=0,
                        padding=0,
                    ),
                    expand=True,
                    bgcolor=self._bg(),
                ),
                self._build_actions(),
            ], spacing=0, tight=True),
            width=460,
            height=580,
            bgcolor=self._bg(),
            border_radius=ft.border_radius.all(14),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            shadow=ft.BoxShadow(
                blur_radius=30,
                spread_radius=0,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            ),
        )

        dialog = ft.AlertDialog(
            modal=True,
            content=main,
            content_padding=ft.padding.all(0),
            shape=ft.RoundedRectangleBorder(radius=14),
            bgcolor=ft.Colors.TRANSPARENT,
            inset_padding=ft.padding.symmetric(horizontal=20, vertical=20),
            alignment=ft.alignment.center,
        )

        self._current_dialog = dialog
        self.page.open(dialog)
        return dialog