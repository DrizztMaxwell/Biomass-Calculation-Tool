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
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
from widgets.LogFileTxt import logger
from widgets.Title_With_Icon import Title_With_Icon

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
                    Title_With_Icon("Select Import Data", ft.Icons.FILE_PRESENT_OUTLINED),
                    DescriptionText("Select how you wish to import the dataset"),
                        ft.Divider(color=ft.Colors.GREY_300, height=30),  # More space
                    
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
                                ft.TextSpan("Plot", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                                ft.TextSpan("Year", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                                ft.TextSpan("Species", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)  ),
                                ft.TextSpan("Tree Number", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                                ft.TextSpan("DBH", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)  ),
                                ft.TextSpan("Height", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan("." , style=ft.TextStyle(color=ft.Colors.BLACK)  ),
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
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
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
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
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
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            filled=True,
            color=ft.Colors.PRIMARY,
            capitalization=ft.TextCapitalization.CHARACTERS,
        )
        db_input = ft.TextField(
            label="Database Name",
            value="",
            prefix_icon=ft.Icons.TABLE_CHART,
            filled=True,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            color=ft.Colors.PRIMARY,
        )

        history_dropdown = ft.Dropdown(
            label="Recent Connections",
            prefix_icon=ft.Icons.HISTORY,
            options=[ft.dropdown.Option(key=str(i), text=f"{c['server']} | {c['database']} ({c['last_used']})")
                     for i, c in enumerate(self.connection_history)] or
                    [ft.dropdown.Option("empty", "No history", disabled=True)],
            on_change=lambda ev: self._on_history_selected(ev, server_input, db_input),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            color=ft.Colors.PRIMARY,
            expand=True,
        )

        def _close_dialog(dlg):
            dlg.open = False
            self.page.update()

        def _clear_history(dlg_dropdown):
            dialog = ft.AlertDialog(
                title=ft.Text("Clear History"),
                content=ft.Text("Are you sure you want to clear the connection history?"),
                actions=[
                    ft.ElevatedButton(style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_600), text="Cancel", on_click=lambda e: self.page.close(dialog)),
                    ft.ElevatedButton( style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.RED), text="Clear", on_click=lambda e: _confirm_clear_history(dlg_dropdown)),
                ],
            )
            self.page.open(dialog)
            self.page.update()
        def _confirm_clear_history(dlg_dropdown):
            self.connection_history.clear()
            os.makedirs("data", exist_ok=True)
            with open("data/connection_history.json", "w") as f:
                json.dump(self.connection_history, f, indent=2)
            dlg_dropdown.options = [ft.dropdown.Option("empty", "No history", disabled=True)]
            dlg_dropdown.update()
            Custom_Alert_Dialog(self.page, title_icon=ft.Icons.HISTORY, title_icon_color=ft.Colors.PRIMARY, title_color=ft.Colors.PRIMARY, title="History Cleared", message="Connection history has been cleared successfully.").show()
            

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
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.SECONDARY,
            shadow_color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            elevation=10,
            title=ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.CLOUD_QUEUE_ROUNDED,
                                color=ft.Colors.WHITE,
                                size=24
                            ),
                            width=44,
                            height=44,
                            bgcolor=ft.Colors.BLUE_600,
                            border_radius=ft.border_radius.all(12),
                            alignment=ft.alignment.center,
                            shadow=ft.BoxShadow(
                                blur_radius=12,
                                color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_600),
                                offset=ft.Offset(0, 2),
                            ),
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Database Connection", 
                                    weight=ft.FontWeight.W_700, 
                                    size=20,
                                    color=ft.Colors.PRIMARY,
                                ),
                                ft.Text(
                                    "Establish secure connection to SQL Server", 
                                    size=13, 
                                    color=ft.Colors.PRIMARY,
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=16,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.only(bottom=4, top=8, left=24, right=24),
            ),
            content=ft.Container(
                
                content=ft.Column(
                    [
                        # Recent Connections Card
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.HISTORY, size=18, color=ft.Colors.PRIMARY),
                                            ft.Text("Recent Connections", color=ft.Colors.PRIMARY, size=14, weight=ft.FontWeight.W_600),
                                        ],
                                        spacing=10,
                                    ),
                                    ft.Container(height=12),
                                    history_dropdown,
                                ],
                                spacing=0,
                            ),
                            padding=ft.padding.all(20),
                            bgcolor=ft.Colors.SECONDARY_CONTAINER,
                            border_radius=ft.border_radius.all(12),
                            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                        ),
                        
                        ft.Container(height=20),
                        
                        # OR Divider
                        ft.Row(
                            [
                                ft.Container(expand=True, height=1, bgcolor=ft.Colors.PRIMARY),
                                ft.Container(
                                    content=ft.Text("OR", size=12, weight=ft.FontWeight.W_600, color=ft.Colors.PRIMARY),
                                    padding=ft.padding.symmetric(horizontal=16),
                                    bgcolor=ft.Colors.WHITE,
                                ),
                                ft.Container(expand=True, height=1, bgcolor=ft.Colors.PRIMARY),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        
                        ft.Container(height=20),
                        
                        # Manual Connection Card
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.EDIT_SHARP, size=18, color=ft.Colors.PRIMARY),
                                            ft.Text("Manual Connection", color=ft.Colors.PRIMARY, size=14, weight=ft.FontWeight.W_600),
                                        ],
                                        spacing=10,
                                    ),
                                    ft.Container(height=16),
                                    server_input,
                                    ft.Container(height=12),
                                    db_input,
                                    ft.Container(height=8),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.INFO_OUTLINED, size=14, color=ft.Colors.PRIMARY),
                                            ft.Text("Ensure SQL Server is running and accessible.", size=12, color=ft.Colors.PRIMARY),
                                        ],
                                        spacing=6,
                                    ),
                                ],
                                spacing=0,
                            ),
                            padding=ft.padding.all(20),
                            bgcolor=ft.Colors.SECONDARY_CONTAINER,
                            border_radius=ft.border_radius.all(12),
                            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                        ),
                    ],
                    spacing=0,
                    scroll=ft.ScrollMode.AUTO,
                ),
                width=480,
                height=420,
                padding=ft.padding.symmetric(horizontal=24),
            ),
            actions=[
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(expand=True),
                            # Clear History Button
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.DELETE_SWEEP_ROUNDED, size=18),
                                        ft.Text("Clear History"),
                                    ],
                                    spacing=8,
                                ),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.RED_600,
                                    padding=ft.padding.symmetric(horizontal=20, vertical=12),
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation=2,
                                    overlay_color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                                ),
                                on_click=lambda ev: _clear_history(history_dropdown),
                                tooltip="Remove all connection history",
                            ),
                            
                            ft.Container(width=12),
                            
                            # Cancel Button
                            ft.OutlinedButton(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.CLOSE, size=18, color=ft.Colors.WHITE),
                                        ft.Text("Cancel", color=ft.Colors.WHITE),
                                    ],
                                    spacing=8,
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLACK87,
                                    side=ft.border.BorderSide(1, ft.Colors.WHITE),
                                    padding=ft.padding.symmetric(horizontal=24, vertical=12),
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    overlay_color=ft.Colors.with_opacity(0.05, ft.Colors.BLUE_GREY_500),
                                ),
                                on_click=lambda ev: _close_dialog(dialog),
                            ),
                            
                            ft.Container(width=12),
                            
                            # Connect Button
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Icon(
                                                ft.Icons.CLOUD_DONE_ROUNDED,
                                                size=20,
                                                color=ft.Colors.WHITE,
                                            ),

                                        ),
                                        ft.Text("Connect", weight=ft.FontWeight.W_600, size=14),
                                    ],
                                    spacing=10,
                                ),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.TERTIARY,
                                    padding=ft.padding.symmetric(horizontal=28, vertical=14),
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    elevation=3,
                                    shadow_color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_600),
                                    overlay_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                                ),
                                on_click=lambda ev: _submit_dialog(server_input, db_input, dialog),
                               
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.padding.symmetric(vertical=20, horizontal=24),
                    border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_100)),
                )
            ],
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)
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
            [ft.Text(title, size=14, weight=ft.FontWeight.W_600, color=ft.Colors.PRIMARY),
             ft.Text(subtitle, size=12, color=ft.Colors.PRIMARY)],
            spacing=4,
            expand=True,
        )