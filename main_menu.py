import flet as ft
from main_menu_view import get_main_menu_view
import view_species_menu
import import_dataset_menu
import calculate_biomass_menu

def main(page: ft.Page):

    def on_import_dataset_click(e):
        # Could also make this a popup later
        import_dataset_menu.show_import_dataset_page(page, main)

    def on_view_species_click(e):
        view_species_menu.show_view_species_page(page, main)

    def on_calculate_biomass_click(e):
        calculate_biomass_menu.show_calculate_biomass_page(page, main)

    layout = get_main_menu_view(
        on_import_dataset_click,
        on_view_species_click,
        on_calculate_biomass_click
    )
    page.add(layout)

ft.app(target=main)

