# select_data_view.py
import os
import flet as ft

from widgets.DescriptionText import DescriptionText
from widgets.TitleTextWidget import TitleTextWidget



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

        self.directory_picker = ft.FilePicker(
        on_result=self._on_sql_directory_selected
        )
        self.page.overlay.append(self.directory_picker)

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
                                on_click=lambda e: self._ensure_sql_path_and_open_db_picker(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=ft.border_radius.all(12),
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    ink=True,
                    on_click=lambda e: self._ensure_sql_path_and_open_db_picker(),
                ),
            ],
            spacing=16,
        )

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
    # DATABASE PICKER
    # -------------------------------------------------

    def _ensure_sql_path_and_open_db_picker(self):
        if not self.sql_data_path:
            self.directory_picker.get_directory_path(
                dialog_title="Select SQL Server DATA folder"
            )
        else:
            self.open_database_picker()



    def open_database_picker(self):
        databases = self._get_databases_from_disk()

        radio_group = ft.RadioGroup(
            content=ft.Column(
                [ft.Radio(value=db, label=db) for db in databases],
                height=300,
                scroll=ft.ScrollMode.AUTO,
            )
        )

        self.db_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Select Database"),
            content=radio_group,
            actions=[
                ft.TextButton(
                    "Cancel",
                    on_click=lambda e: self.page.close(self.db_dialog),
                ),
                ft.ElevatedButton(
                    "Import",
                    on_click=lambda e: self._confirm_database(radio_group.value),
                ),
            ],
        )

        self.page.open(self.db_dialog)

    def _on_sql_directory_selected(self, e: ft.FilePickerResultEvent):
        if not e.path:
            return

        self.sql_data_path = e.path
        self.open_database_picker()

    def _confirm_database(self, db_name):
        if not db_name:
            return
        self.page.close(self.db_dialog)
        self.controller.import_from_database(db_name)

    def _get_databases_from_disk(self):
        if not self.sql_data_path or not os.path.exists(self.sql_data_path):
            return []

        return sorted(
            {
                os.path.splitext(f)[0]
                for f in os.listdir(self.sql_data_path)
                if f.lower().endswith(".mdf")
            }
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

    def update_file_status(self, file_path):
        self.file_status_text.value = (
            f"File selected: {file_path}"
            if file_path
            else "File selected: No file selected"
        )
        self.page.update()
