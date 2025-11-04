import flet as ft
from data.data_manager import DataManager
from views.view_species_menu_view import get_species_view, get_loading_view
import threading

def show_view_species_page(container: ft.Column, page: ft.Page):
    manager = DataManager()
    data = manager.get_all()
    print(f"📦 Loaded {len(data)} species records")

    # Show loading view first
    loading_layout, progress_text, progress_bar = get_loading_view()
    container.controls.clear()
    container.controls.append(loading_layout)
    page.update()

    # Build table in a background thread to keep UI responsive
    def build_table():
        layout = get_species_view(data, page, progress_text, progress_bar)
        container.controls.clear()
        container.controls.append(layout)
        page.update()
        print("✅ Species page displayed successfully")

    threading.Thread(target=build_table, daemon=True).start()
