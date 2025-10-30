# view_species_menu.py
import flet as ft
from data.data_manager import DataManager
from views.view_species_menu_view import get_species_view

def show_view_species_page(page: ft.Page, main_menu_callback):
    manager = DataManager()
    data = manager.get_all()
    print(f"📦 Loaded {len(data)} species records")

    def on_back_click(e):
        page.clean()
        main_menu_callback(page)

    # Get layout
    layout = get_species_view(data, on_back_click, page)

    page.clean()
    page.add(layout)
    page.update()

    print("✅ Species page displayed successfully")
