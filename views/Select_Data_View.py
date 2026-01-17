import datetime
import os
import flet as ft
import json

from widgets.DescriptionText import DescriptionText
from widgets.TitleTextWidget import TitleTextWidget
from widgets.Connect_To_Database_Dialog_Widget import Connect_To_Database_Dialog_Widget

class Select_Data_View:
    def __init__(self, page: ft.Page, controller):
        self.controller = controller
        self.page = page
        self.db_dialog = None

        self.file_status_text = ft.Text(
            "File selected: No file selected",
            size=13,
            color=ft.Colors.GREY_700,
            weight=ft.FontWeight.W_500,
        )

        self.sql_data_path = None

    # -------------------------------------------------
    # MAIN LAYOUT
    # -------------------------------------------------
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

    # -------------------------------------------------
    # HEADER / WARNING
    # -------------------------------------------------
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
                    ft.Icon(
                        ft.Icons.WARNING_AMBER_ROUNDED,
                        color=ft.Colors.AMBER_700,
                        size=20,
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.Text(
                            spans=[
                                ft.TextSpan(
                                    "Note: ",
                                    style=ft.TextStyle(
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLACK,
                                    ),
                                ),
                                ft.TextSpan(
                                    "Your dataset columns must include the following core fields: ",
                                    style=ft.TextStyle(color=ft.Colors.BLACK),
                                ),
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

    # -------------------------------------------------
    # IMPORT BUTTONS
    # -------------------------------------------------
    def _create_import_buttons(self):
        return ft.Column(
            [
                # TEXT FILE IMPORT
                ft.Container(
                    content=ft.Row(
                        [
                            self._icon_circle(
                                ft.Icons.UPLOAD_FILE_ROUNDED,
                                ft.Colors.GREEN_700,
                            ),
                            self._import_text_block(
                                "Import Local Text File",
                                "Select a text file from your computer",
                            ),
                            ft.IconButton(
                                icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                                on_click=self.controller.on_import_text_file_click,
                            ),
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

                # DATABASE IMPORT (NEW)
                ft.Container(
                    content=ft.Row(
                        [
                            self._icon_circle(
                                ft.Icons.TABLE_CHART_SHARP,
                                ft.Colors.BLUE_700,
                            ),
                            self._import_text_block(
                                "Import From Database",
                                "Select an existing SQL Server database",
                            ),
                            ft.IconButton(
                                icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                                on_click=lambda e: self.x(e),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=ft.border_radius.all(12),
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    ink=True,
                    on_click=lambda e: self.x(e),
                ),
            ],
            spacing=16,
        )

    def x(self, e):
        print("Opening database connection dialog...")
        
        
        
        # Create dialog and set callback
        self.db_dialog = Connect_To_Database_Dialog_Widget(self.page)
        self.db_dialog.on_connect_callback = self.controller.on_connection_result
        self.db_dialog.open_dialog()
        # import the data
        
    
    def save_connection_info(self, server, database):
        """Save connection information"""
        try:
            if server and database:
                with open('data/selected_database.json', 'w') as f:
                    json.dump({
                        "server": server,
                        "database": database,
                        "connection_type": "sql_server",
                        "timestamp": datetime.now().isoformat()
                    }, f, indent=2)
            else:
                with open('data/selected_database.json', 'w') as f:
                    json.dump({}, f)
        except Exception as e:
            print(f"Error saving connection info: {e}")
    
    def _icon_circle(self, icon, color):
        return ft.Container(
            content=ft.Icon(icon, color=ft.Colors.WHITE, size=24),
            width=50,
            height=50,
            bgcolor=color,
            border_radius=ft.border_radius.all(25),
            alignment=ft.alignment.center,
        )

    def _import_text_block(self, title, subtitle):
        return ft.Column(
            [
                ft.Text(title, size=14, weight=ft.FontWeight.W_600),
                ft.Text(subtitle, size=12, color=ft.Colors.GREY_600),
            ],
            spacing=4,
            expand=True,
        )

    # -------------------------------------------------
    # STATUS
    # -------------------------------------------------
    def _create_file_status(self):
        return ft.Container(
            content=self.file_status_text,
            padding=ft.padding.all(16),
            bgcolor=ft.Colors.CYAN_50,
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(1, ft.Colors.CYAN_200),
        )

    def update_file_status(self, status_text):
        """Update the file status display"""
        self.file_status_text.value = status_text
        self.page.update()