# main.py
import flet as ft
from controller.eula_menu import show_eula_page
from controller.main_menu import show_main_menu_page

def main(page: ft.Page):
    """
    Entry point for the app.
    """
    show_eula_page(page, show_main_menu_page)


if __name__ == "__main__":
    ft.app(target=main)
