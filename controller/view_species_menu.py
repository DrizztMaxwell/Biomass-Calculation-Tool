import flet as ft
from data.data_manager import DataManager
from views.view_species_menu_view import get_species_view

def show_view_species_page(container: ft.Column, page: ft.Page):
    manager = DataManager()
    data = manager.get_all()
    print(f"📦 Loaded {len(data)} species records")

    layout = get_species_view(data, page)

    container.controls.clear()
    container.controls.append(layout)
    page.update()

    print("✅ Species page displayed successfully")
