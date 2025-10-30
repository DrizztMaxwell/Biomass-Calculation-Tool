# main_menu.py
import flet as ft
from views.main_menu_view import get_main_menu_view
from controller import view_species_menu
from controller import import_dataset_menu
from controller import calculate_biomass_menu


def show_main_menu_page(page: ft.Page):
    """
    Displays the main menu and handles navigation to other pages.
    """

    def on_import_dataset_click(e):
        import_dataset_menu.show_import_dataset_page(page, show_main_menu_page)

    def on_view_species_click(e):
        view_species_menu.show_view_species_page(page, show_main_menu_page)

    def on_calculate_biomass_click(e):
        calculate_biomass_menu.show_calculate_biomass_page(page, show_main_menu_page)

    layout = get_main_menu_view(
        on_import_dataset_click,
        on_view_species_click,
        on_calculate_biomass_click
    )
    page.add(layout)


