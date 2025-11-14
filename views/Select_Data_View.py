import json
from tkinter import filedialog
import flet as ft
import pandas as pd
from widgets.Import_Option_card import Import_Option_Card


class Select_Data_View:

    def __init__(self, controller):
        self.controller = controller
        
    def create_main_layout(self):
        main_content = self._create_main_content()

        main_layout = ft.Container(expand=True, alignment=ft.alignment.center,
                                   
                                 content=  ft.Container(
            content=main_content,
            padding=ft.padding.symmetric(vertical=50, horizontal=40),
            margin=ft.margin.all(30),
            border_radius=ft.border_radius.all(30),
            bgcolor=ft.Colors.WHITE,
            width=900,
            # Enhanced shadow and border
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=40,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 20),
            ),
            border=ft.border.all(1, ft.Colors.GREY_200),
            # Center the container both horizontally and vertically
            alignment=ft.alignment.center,
        )
        )
    
        return main_layout
    
    def _create_main_content(self):
        return ft.Column(
            [
                self._create_header(),
                self._create_options_row_cards(),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )

    def _create_options_row_cards(self):
        options_row = ft.Row(
            [
               Import_Option_Card(
                    icon_name=ft.Icons.FOLDER_OPEN,
                    title="Local File Import",
                    subtitle="Upload CSV, TXT, or Excel files from your local storage with advanced parsing options.",
                    color=ft.Colors.BLUE_600,
                    handle_on_click=self.controller.on_import_text_file_click
                ),
                Import_Option_Card(
                    icon_name=ft.Icons.STORAGE,
                    title="Database Connection",
                    subtitle="Connect securely to SQL databases using JDBC/ODBC drivers with real-time data streaming.",
                    color=ft.Colors.INDIGO_600
                    , handle_on_click=self.controller.on_import_from_database_click
                ),
            ],
            spacing=40,
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True
        )
        
        return options_row

    def _create_header(self):
        return ft.Column(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Data Import Hub",
                            size=36,
                            weight=ft.FontWeight.W_900,
                            color=ft.Colors.BLUE_GREY_900,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=10),
                        ft.Text(
                            "Select your preferred method to import datasets into the platform",
                            size=16,
                            color=ft.Colors.BLUE_GREY_600,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ]),
                    padding=ft.padding.only(bottom=40)
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )