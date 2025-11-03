# main.py
import flet as ft
from controller.eula_menu import show_eula_page
from controller.main_menu import show_main_menu_page
from data.data_manager import DataManager

def main(page: ft.Page):
    """
    Entry point for the app.
    """
    manager = DataManager()

    # Clear any existing localstorage.json to trigger the import restriction
    manager.clear()

    # Optional: attach cleanup on close if you want to clear again
    def cleanup(e=None):
        manager.clear()

    page.on_close = cleanup

    # Show EULA first, then main menu
    show_eula_page(page, show_main_menu_page)


if __name__ == "__main__":
    ft.app(target=main)
