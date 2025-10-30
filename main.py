# main.py
import flet as ft
from controller.main_menu import show_main_menu_page


def main(page: ft.Page):
    """
    Entry point for the app.
    """
    show_main_menu_page(page)


if __name__ == "__main__":
    ft.app(target=main)
