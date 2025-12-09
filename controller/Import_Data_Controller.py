"""
Controller for the Data Import Platform
Handles user interactions and coordinates between Model and View.
"""
import flet as ft
from views.import_dataset_view import get_import_dataset_view
from views.Select_Data_View import ImportDataView
# from model import AppState

class ImportDataController:
    """
    Controller class that handles user interactions and business logic.
    """
    
    def __init__(self):
        self.view = ImportDataView(self)
        # self.state = AppState()

    def handle_import_click(self, e, title):
        """
        Handles the click event for the Import buttons, showing a SnackBar message.
        """
        print(f"Importing {title}...")
        
        # Import the dataset view (this would typically be coordinated by the controller)
        get_import_dataset_view()
        e.page.update()

    def handle_begin_click(self, e):
        """
        Handles the Begin button click event.
        """
        e.page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.ROCKET_LAUNCH, color=ft.Colors.BLACK),
                ft.Text("Starting your data journey...", weight=ft.FontWeight.BOLD),
            ]),
            bgcolor=ft.Colors.BLUE_600,
            duration=2000
        )
        e.page.snack_bar.open = True
        e.page.update()

    def setup_application(self, page):
        """Sets up the complete application"""
        self.view.create_main_layout()
