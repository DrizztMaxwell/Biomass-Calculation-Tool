# select_data_view.py
import flet as ft
from .components.Warning_Banner import Warning_Banner
from .components.Import_Buttons import Import_Buttons
from .components.Database_Dialog import Database_Dialog
from .components.Connection_History_Manager import Connection_History_Manager
from .components.Page_Header import Page_Header
from constants.Json_File_Path_Constants import json_paths


class Select_Data_View:
    """Main view for selecting data import method."""

    def __init__(self, page: ft.Page, controller):
        self.page       = page
        self.controller = controller

        self.file_status_text = ft.Text(
            "No file selected",
            size=13,
            color=ft.Colors.ON_SURFACE_VARIANT,
            weight=ft.FontWeight.W_500,
        )

        self.history_manager  = Connection_History_Manager(json_paths.CONNECTION_HISTORY_PATH)
        self.database_dialog  = Database_Dialog(
            page=self.page,
            history_manager=self.history_manager,
            on_connect_callback=self._handle_database_connection,
        )

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):      return "#1A1A1A" if self._is_dark else "#FFFFFF"
    def _surface(self): return "#222222" if self._is_dark else "#F8FAFC"
    def _border(self):  return "#2E2E2E" if self._is_dark else "#E2E8F0"
    def _text_primary(self):   return "#F5F5F5" if self._is_dark else "#0F172A"
    def _text_secondary(self): return "#888888" if self._is_dark else "#64748B"

    # ── History ───────────────────────────────────────────────────────────────

    def add_to_history(self, server, database):
        self.history_manager.add_connection(server, database)

    # ── Page header ───────────────────────────────────────────────────────────

    def _build_page_header(self) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.UPLOAD_FILE_OUTLINED,
                                        size=22, color="#FFFFFF"),
                        bgcolor="#16A34A",
                        border_radius=ft.border_radius.all(10),
                        width=44, height=44,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column([
                        ft.Text("Select Import Data", size=18,
                                weight=ft.FontWeight.W_700,
                                color=self._text_primary()),
                        ft.Text("Select how you wish to import the dataset",
                                size=12, color=self._text_secondary()),
                    ], spacing=2, expand=True),
                ], spacing=14,
                   vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=1, bgcolor=self._border(),
                             margin=ft.margin.only(top=14)),
            ], spacing=0),
            margin=ft.margin.only(bottom=4),
        )

    # ── File status strip ─────────────────────────────────────────────────────

    def _create_file_status(self) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=15,
                        color="#2563EB"),
                self.file_status_text,
            ], spacing=8),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=ft.Colors.with_opacity(0.07, "#2563EB"),
            border=ft.border.all(1, ft.Colors.with_opacity(0.18, "#2563EB")),
            border_radius=ft.border_radius.all(8),
        )

    # ── Main content ──────────────────────────────────────────────────────────

    def _create_main_content(self) -> ft.Column:
        return ft.Column(
            [
                self._build_page_header(),
                Warning_Banner.create(),
                Import_Buttons.create(
                    text_file_click_handler=self._handle_import_text_file_click,
                    database_click_handler=self._open_database_dialog,
                ),
                self._create_file_status(),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=20,
        )

    def create_main_layout(self) -> ft.Container:
        return ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Container(
                content=self._create_main_content(),
                padding=ft.padding.all(28),
                margin=ft.margin.all(20),
                border_radius=ft.border_radius.all(12),
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                border=ft.border.all(1, self._border()),
                expand=True,
                shadow=ft.BoxShadow(
                    spread_radius=0, blur_radius=20,
                    color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4),
                ),
            ),
        )

    # ── Status update ─────────────────────────────────────────────────────────

    def update_file_status(self, status_text: str):
        self.file_status_text.value = status_text
        self.page.update()

    # ── Event handlers ────────────────────────────────────────────────────────

    def _handle_import_text_file_click(self, e):
        self.controller.on_import_text_file_click(e)
        self.page.update()

    def _open_database_dialog(self, e=None):
        self.database_dialog.open()

    def _handle_database_connection(self, server, database):
        if hasattr(self.controller, "on_database_selected"):
            self.controller.on_database_selected(server, database)