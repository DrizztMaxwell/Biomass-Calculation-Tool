import flet as ft

from widgets.DescriptionText import DescriptionText
from widgets.TitleTextWidget import TitleTextWidget

class Select_Data_View:

    def __init__(self, page:ft.Page, controller):
        self.controller = controller
        self.page = page
        self.file_status_text = ft.Text(
            "File selected: No file selected",
            size=13,
            color=ft.Colors.GREY_700,
            weight=ft.FontWeight.W_500,
        )
        
    def create_main_layout(self):
        main_content = self._create_main_content()

        main_layout = ft.Container(
            expand=True, 
            alignment=ft.alignment.center,
            content=ft.Container(
                content=main_content,
                padding=ft.padding.all(40),
                margin=ft.margin.all(30),
                border_radius=ft.border_radius.all(20),
                bgcolor=ft.Colors.WHITE,
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
    
        return main_layout
    
    def _create_main_content(self):
        return ft.Column(
            [
                self._create_header(),
                self._create_warning_banner(),
                self._create_import_buttons(),
                self._create_file_status(),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=20
        )

    def _create_header(self):
        return ft.Container(
            content=ft.Column([
               TitleTextWidget("Select Import Data"),
            DescriptionText("Select how you wish to import the dataset")
            ], spacing=8),
            padding=ft.padding.only(bottom=10)
        )

    def _create_warning_banner(self):
        return ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.WARNING_AMBER_ROUNDED,
                    color=ft.Colors.AMBER_700,
                    size=20
                ),
                ft.Container(
                    content=ft.Text(
                        spans=[
                            ft.TextSpan(
                                "Note: ",
                                style=ft.TextStyle(
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK,
                                )
                            ),
                            ft.TextSpan(
                                "Your dataset columns must ensure that all attributes to include the following core entities or column names: ",
                                style=ft.TextStyle(color=ft.Colors.BLACK)
                            ),
                            ft.TextSpan(
                                "Plot",
                                style=ft.TextStyle(
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK,
                                )
                            ),
                            ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                            ft.TextSpan(
                                "Year",
                                style=ft.TextStyle(
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK,
                                )
                            ),
                            ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                            ft.TextSpan(
                                "SpecCode",
                                style=ft.TextStyle(
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK,
                                )
                            ),
                            ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                            ft.TextSpan(
                                "Tree Number",
                                style=ft.TextStyle(
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK,
                                )
                            ),
                            ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                            ft.TextSpan(
                                "DBH",
                                style=ft.TextStyle(
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK,
                                )
                            ),
                            ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                            ft.TextSpan(
                                "Height",
                                style=ft.TextStyle(
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK,
                                )
                            ),
                            ft.TextSpan(".", style=ft.TextStyle(color=ft.Colors.BLACK)),
                        ],
                        size=12,
                    ),
                    expand=True,
                )
            ], spacing=12),
            padding=ft.padding.all(16),
            bgcolor=ft.Colors.AMBER_50,
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(1, ft.Colors.AMBER_200),
        )

    def _create_import_buttons(self):
        return ft.Column([
            # First import button
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.UPLOAD_FILE_ROUNDED,
                            color=ft.Colors.WHITE,
                            size=24
                        ),
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.GREEN_700,
                        border_radius=ft.border_radius.all(25),
                        alignment=ft.alignment.center,
                    ),
                    ft.Column([
                        ft.Text(
                            "Import Local Text File",
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.GREY_900,
                        ),
                        ft.Text(
                            "Select a text file from your computer to import its contents directly into the application",
                            size=12,
                            color=ft.Colors.GREY_600,
                        ),
                    ], spacing=4, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                        icon_color=ft.Colors.GREY_700,
                        icon_size=20,
                        on_click=self.controller.on_import_text_file_click,
                    )
                ], spacing=16, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(20),
                bgcolor=ft.Colors.GREY_50,
                border_radius=ft.border_radius.all(12),
                border=ft.border.all(1, ft.Colors.GREY_200),
                ink=True,
                on_click=self.controller.on_import_text_file_click,
            ),
            
            # Second import button
           ft.Container(
    content=ft.Row([
        ft.Container(
            content=ft.Icon(
                ft.Icons.TABLE_CHART_SHARP,
                color=ft.Colors.WHITE,
                size=24
            ),
            width=50,
            height=50,
            bgcolor=ft.Colors.GREY_400,  # Changed to lighter grey
            border_radius=ft.border_radius.all(25),
            alignment=ft.alignment.center,
        ),
        ft.Column([
            ft.Text(
                "Import From Database",
                size=14,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.GREY_500,  # Changed to lighter grey
            ),
             ft.Text(
                            "Connect to database and import the dataset.",
                            size=12,
                            color=ft.Colors.GREY_600,
                        ),
            ft.Text(
                "Coming Soon...",  # Changed text to "Coming Soon..."
                size=12,
                color=ft.Colors.GREY_400,  # Changed to lighter grey
            ),
        ], spacing=4, expand=True),
        ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD_ROUNDED,
            icon_color=ft.Colors.GREY_400,  # Changed to lighter grey
            icon_size=20,
            on_click=None,  # Disabled click handler
        )
    ], spacing=16, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    padding=ft.padding.all(20),
    bgcolor=ft.Colors.GREY_100,  # Changed to lighter grey
    border_radius=ft.border_radius.all(12),
    border=ft.border.all(1, ft.Colors.GREY_300),  # Changed to lighter grey
    ink=False,  # Disabled ink effect
    on_click=None,  # Disabled click handler
),
        ], spacing=16)

    def _create_file_status(self):
        return ft.Container(
            content=self.file_status_text,
            padding=ft.padding.all(16),
            bgcolor=ft.Colors.CYAN_50,
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(1, ft.Colors.CYAN_200),
        )
    
    def update_file_status(self, file_path):
        """Update the file status display with the selected file path"""
        if file_path:
            self.file_status_text.value = f"File selected: {file_path}"
        else:
            self.file_status_text.value = "File selected: No file selected"
        
        self.page.update()