# select_data_view.py

import flet as ft
from .components.Warning_Banner import Warning_Banner
from .components.Import_Buttons import Import_Buttons
from .components.Database_Dialog import Database_Dialog
from .components.Connection_History_Manager import Connection_History_Manager
from .components.Page_Header import Page_Header

class Select_Data_View:
    """Main view for selecting data import method"""
    
    def __init__(self, page: ft.Page, controller):
        self.file_status_text = ft.Text(
            "File selected: No file selected",
            size=13,
            color=ft.Colors.GREY_700,
            weight=ft.FontWeight.W_500,
        )

        self.controller = controller
        self.page = page
        
        # Initialize components
        self.history_manager = Connection_History_Manager()
        self.database_dialog = Database_Dialog(
            page=self.page,
            history_manager=self.history_manager,
            on_connect_callback=self._handle_database_connection
        )
        
    def add_to_history(self, server, database):
        """Add a new connection to history"""
        self.history_manager.add_connection(server, database)
    # -------------------------
    # MAIN LAYOUT
    # -------------------------
    def create_main_layout(self):
        """Create the main layout container"""
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

    
    def _handle_import_text_file_click(self, e):
        """Handle click event for importing text file"""
        print("Import Text File button clicked")
        print(self.controller.on_import_text_file_click(e))
        self.page.update()
        
    def _create_main_content(self):
        """Create the main content column"""
        return ft.Column(
            [
                Page_Header.create(),
                Warning_Banner.create(),
                Import_Buttons.create(
                    text_file_click_handler=self._handle_import_text_file_click,
                    database_click_handler=self._open_database_dialog
                ),
                self._create_file_status()
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=20,
        )
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
    # EVENT HANDLERS
    # -------------------------
    def _open_database_dialog(self, e=None):
        """Open the database connection dialog"""
        self.database_dialog.open()
    
    def _handle_database_connection(self, server, database):
        """
        Handle database connection callback
        
        Args:
            server: Server name
            database: Database name
        """
        if hasattr(self.controller, "on_database_selected"):
            self.controller.on_database_selected(server, database)