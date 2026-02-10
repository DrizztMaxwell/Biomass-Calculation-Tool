import flet as ft

class Import_Buttons:
    """Component for rendering import option buttons"""
    
    @staticmethod
    def create(text_file_click_handler, database_click_handler):
        """
        Create the import buttons section
        
        Args:
            text_file_click_handler: Callback for text file import
            database_click_handler: Callback for database import
            
        Returns:
            ft.Column with import button options
        """
        return ft.Column(
            [
                # TEXT FILE IMPORT
                ft.Container(
                    content=ft.Row(
                        [
                            Import_Buttons._icon_circle(
                                ft.Icons.UPLOAD_FILE_ROUNDED, 
                                ft.Colors.GREEN_700
                            ),
                            Import_Buttons._import_text_block(
                                "Import Local Text File", 
                                "Select a text file from your computer"
                            ),
                            ft.IconButton(
                                icon=ft.Icons.ARROW_FORWARD_ROUNDED, 
                                on_click=text_file_click_handler
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=ft.border_radius.all(12),
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    ink=True,
                    on_click=text_file_click_handler,
                ),
                # DATABASE IMPORT
                ft.Container(
                    content=ft.Row(
                        [
                            Import_Buttons._icon_circle(
                                ft.Icons.TABLE_CHART_SHARP, 
                                ft.Colors.BLUE_700
                            ),
                            Import_Buttons._import_text_block(
                                "Import From Database", 
                                "Select an existing SQL Server database"
                            ),
                            ft.IconButton(
                                icon=ft.Icons.ARROW_FORWARD_ROUNDED, 
                                on_click=database_click_handler
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=ft.border_radius.all(12),
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    ink=True,
                    on_click=database_click_handler,
                ),
            ],
            spacing=16,
        )
    
    @staticmethod
    def _icon_circle(icon, color):
        """Create a circular icon container"""
        return ft.Container(
            content=ft.Icon(icon, color=ft.Colors.WHITE, size=24),
            width=50, 
            height=50,
            bgcolor=color,
            border_radius=ft.border_radius.all(25),
            alignment=ft.alignment.center,
        )
    
    @staticmethod
    def _import_text_block(title, subtitle):
        """Create a text block with title and subtitle"""
        return ft.Column(
            [
                ft.Text(
                    title, 
                    size=14, 
                    weight=ft.FontWeight.W_600, 
                    color=ft.Colors.PRIMARY
                ),
                ft.Text(
                    subtitle, 
                    size=12, 
                    color=ft.Colors.PRIMARY
                )
            ],
            spacing=4,
            expand=True,
        )