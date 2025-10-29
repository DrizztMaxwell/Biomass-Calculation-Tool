# species_menu.py
import flet as ft
from data_manager import DataManager
from view_species_menu_view import get_species_view

def show_view_species_page(page: ft.Page, main_menu_callback):
    """
    Load species data from DataManager and display in a scrollable table.
    """
    manager = DataManager()
    data = manager.get_all()
    print(f"📦 Loaded {len(data)} species records")

    # Handler for Back button
    def on_back_click(e):
        page.clean()
        main_menu_callback(page)

    # Create the scrollable species view
    layout = get_species_view(data, on_back_click)

    page.clean()
    page.add(layout)
    page.update()
    print("✅ Species page displayed successfully")
