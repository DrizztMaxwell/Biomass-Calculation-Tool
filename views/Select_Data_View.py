# select_data_view.py

import os
import flet as ft
import json
from datetime import datetime
from data.database_config import get_mssql_data_path
from widgets.DescriptionText import DescriptionText
from widgets.TitleTextWidget import TitleTextWidget
from widgets.Display_Error_Dialog import Display_Error_Dialog
from widgets.Loading_Spinner_Widget import Loading_Spinner_Widget as Loading


class Select_Data_View:
    def __init__(self, page: ft.Page, controller):
        self.controller = controller
        self.page = page
        self.db_dialog = None
        self.connection_history_file = "connection_history.json"
        self.connection_history: list[dict] = []

        self.file_status_text = ft.Text(
            "File selected: No file selected",
            size=13,
            color=ft.Colors.GREY_700,
            weight=ft.FontWeight.W_500,
        )

        self.sql_data_path = None
        self._load_connection_history()

    # -------------------------
    # MAIN LAYOUT
    # -------------------------
    def create_main_layout(self):
        main_content = self._create_main_content()
        return ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Container(
                content=main_content,
                padding=ft.padding.all(40),
                margin=ft.margin.all(30),
                border_radius=ft.border_radius.all(20),
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                expand=True,
                height=600,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=40,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 20),
                ),
                border=ft.border.all(1, ft.Colors.GREY_200),
                alignment=ft.alignment.center,
            )
        )

    def _create_main_content(self):
        return ft.Column(
            [
                self._create_header(),
                self._create_warning_banner(),
                self._create_import_buttons(),
                self._create_file_status(),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=20,
        )

    # -------------------------
    # HEADER / WARNING
    # -------------------------
    def _create_header(self):
        return ft.Container(
            content=ft.Column(
                [
                    TitleTextWidget("Select Import Data"),
                    DescriptionText("Select how you wish to import the dataset"),
                ],
                spacing=8,
            ),
            padding=ft.padding.only(bottom=10),
        )

    def _create_warning_banner(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER_700, size=20),
                    ft.Container(
                        expand=True,
                        content=ft.Text(
                            spans=[
                                ft.TextSpan("Note: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan("Your dataset columns must include the following core fields: ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                                ft.TextSpan("Plot", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                ft.TextSpan(", "),
                                ft.TextSpan("Year", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                ft.TextSpan(", "),
                                ft.TextSpan("Species", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                ft.TextSpan(", "),
                                ft.TextSpan("Tree Number", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                ft.TextSpan(", "),
                                ft.TextSpan("DBH", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                ft.TextSpan(", "),
                                ft.TextSpan("Height", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                ft.TextSpan("."),
                            ],
                            size=12,
                        ),
                    ),
                ],
                spacing=12,
            ),
            padding=ft.padding.all(16),
            bgcolor=ft.Colors.AMBER_50,
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(1, ft.Colors.AMBER_200),
        )

    # -------------------------
    # IMPORT BUTTONS
    # -------------------------
    def _create_import_buttons(self):
        return ft.Column(
            [
                # TEXT FILE IMPORT
                ft.Container(
                    content=ft.Row(
                        [
                            self._icon_circle(ft.Icons.UPLOAD_FILE_ROUNDED, ft.Colors.GREEN_700),
                            self._import_text_block("Import Local Text File", "Select a text file from your computer"),
                            ft.IconButton(icon=ft.Icons.ARROW_FORWARD_ROUNDED, on_click=self.controller.on_import_text_file_click),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=ft.border_radius.all(12),
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    ink=True,
                    on_click=self.controller.on_import_text_file_click,
                ),
                # DATABASE IMPORT
                ft.Container(
                    content=ft.Row(
                        [
                            self._icon_circle(ft.Icons.TABLE_CHART_SHARP, ft.Colors.BLUE_700),
                            self._import_text_block("Import From Database", "Select an existing SQL Server database"),
                            ft.IconButton(icon=ft.Icons.ARROW_FORWARD_ROUNDED, on_click=self._open_database_dialog),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=ft.border_radius.all(12),
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    ink=True,
                    on_click=self._open_database_dialog,
                ),
            ],
            spacing=16,
        )

    # -------------------------
    # DATABASE DIALOG (UI-ONLY)
    # -------------------------
    def _open_database_dialog(self, e):
        detected_path = get_mssql_data_path()
        detected_servers = []
        if detected_path:
            folder_name = os.path.basename(os.path.dirname(os.path.dirname(detected_path)))
            if "SQLEXPRESS" in folder_name.upper():
                detected_servers.append(f"{os.environ.get('COMPUTERNAME')}\\SQLEXPRESS")

        server_input = ft.TextField(
            label="Server Name",
            value=detected_servers[0] if len(detected_servers) == 1 else "",
            hint_text="e.g., COMPUTER\\SQLEXPRESS",
            prefix_icon=ft.Icons.COMPUTER,
            filled=True,
            capitalization=ft.TextCapitalization.CHARACTERS,
        )
        db_input = ft.TextField(
            label="Database Name",
            value=os.path.basename(detected_path) if detected_path else "",
            prefix_icon=ft.Icons.TABLE_CHART,
            filled=True,
        )

        history_dropdown = ft.Dropdown(
            label="Recent Connections",
            prefix_icon=ft.Icons.HISTORY,
            options=[ft.dropdown.Option(key=str(i), text=f"{c['server']} | {c['database']} ({c['last_used']})")
                     for i, c in enumerate(self.connection_history)] or
                    [ft.dropdown.Option("empty", "No history", disabled=True)],
            on_change=lambda ev: self._on_history_selected(ev, server_input, db_input),
            filled=True,
        )

        def _close_dialog(dlg):
            dlg.open = False
            self.page.update()

        def _clear_history(dlg_dropdown):
            self.connection_history.clear()
            os.makedirs("data", exist_ok=True)
            with open("data/connection_history.json", "w") as f:
                json.dump(self.connection_history, f, indent=2)
            dlg_dropdown.options = [ft.dropdown.Option("empty", "No history", disabled=True)]
            dlg_dropdown.update()

        def _submit_dialog(srv_input, db_input_field, dlg):
            """UI-only: validate + save history, notify controller, do not connect"""
            server = srv_input.value.strip()
            database = db_input_field.value.strip()

            if not server or not database:
                Display_Error_Dialog(self.page, "Missing Information", "Server and database are required.").show()
                return

            self._add_to_history(server, database)
            dlg.open = False
            self.page.update()

            # Notify controller
            if hasattr(self.controller, "on_database_selected"):
                self.controller.on_database_selected(server, database)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Database Connection", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                [history_dropdown, ft.Text("OR", size=12), server_input, db_input],
                spacing=12,
                width=450,
            ),
            actions=[
                ft.TextButton("Clear History", on_click=lambda ev: _clear_history(history_dropdown)),
                ft.TextButton("Cancel", on_click=lambda ev: _close_dialog(dialog)),
                ft.ElevatedButton("Submit", on_click=lambda ev: _submit_dialog(server_input, db_input, dialog)),
            ],
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    # -------------------------
    # HISTORY LOGIC
    # -------------------------
    def _load_connection_history(self):
        if os.path.exists(self.connection_history_file):
            try:
                with open(self.connection_history_file, "r") as f:
                    self.connection_history = json.load(f)
            except Exception:
                self.connection_history = []

    def _save_connection_history(self):
        with open(self.connection_history_file, "w") as f:
            json.dump(self.connection_history, f, indent=2)

    def _add_to_history(self, server, database):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.connection_history = [
            c for c in self.connection_history if not (c["server"] == server and c["database"] == database)
        ]
        self.connection_history.insert(0, {"server": server, "database": database, "last_used": now})
        self.connection_history = self.connection_history[:10]
        self._save_connection_history()

    def _on_history_selected(self, e, server_input, db_input):
        if e.control.value != "empty":
            conn = self.connection_history[int(e.control.value)]
            server_input.value = conn["server"]
            db_input.value = conn["database"]
            server_input.update()
            db_input.update()

    # -------------------------
    # FILE STATUS
    # -------------------------
    def _create_file_status(self):
        return ft.Container(
            content=self.file_status_text,
            padding=ft.padding.all(16),
            bgcolor=ft.Colors.CYAN_50,
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(1, ft.Colors.CYAN_200),
        )

    def update_file_status(self, status_text):
        self.file_status_text.value = status_text
        self.page.update()

    # -------------------------
    # HELPERS
    # -------------------------
    def _icon_circle(self, icon, color):
        return ft.Container(
            content=ft.Icon(icon, color=ft.Colors.WHITE, size=24),
            width=50, height=50,
            bgcolor=color,
            border_radius=ft.border_radius.all(25),
            alignment=ft.alignment.center,
        )

    def _import_text_block(self, title, subtitle):
        return ft.Column(
            [ft.Text(title, size=14, weight=ft.FontWeight.W_600),
             ft.Text(subtitle, size=12, color=ft.Colors.GREY_600)],
            spacing=4,
            expand=True,
        )