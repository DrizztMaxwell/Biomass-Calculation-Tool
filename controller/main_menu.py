#main_menu.py
import flet as ft
from views.navbar_view import get_navbar
from views.main_menu_view import get_main_menu_view
from controller import import_dataset_menu, view_species_menu, calculate_biomass_menu

def show_main_menu_page(page: ft.Page):
    """
    Displays the main menu with a persistent navbar.
    Only the content area changes when navigating.
    """

    # --- Container for dynamic content ---
    content_container = ft.Column(expand=True)

    # --- Navigation functions ---
    def go_home(e=None):
        content_container.controls.clear()
        content_container.controls.append(get_main_menu_view())
        page.update()

    def go_import_dataset(e=None):
        content_container.controls.clear()
        import_dataset_menu.show_import_dataset_page(content_container, page)
        # show_import_dataset_page should now accept a container to update instead of page.clean()

    def go_view_species(e=None):
        content_container.controls.clear()
        view_species_menu.show_view_species_page(content_container, page)

    def go_calculate_biomass(e=None):
        content_container.controls.clear()
        calculate_biomass_menu.show_calculate_biomass_page(content_container, page)

    # --- Navbar ---
    navbar = get_navbar(
        on_home_click=go_home,
        on_import_dataset_click=go_import_dataset,
        on_view_species_click=go_view_species,
        on_calculate_biomass_click=go_calculate_biomass
    )

    # --- Page layout ---
    page.controls.clear()
    page.add(
        ft.Row(
            controls=[
                ft.Container(
                    content=navbar,
                    width=200,
                    expand=False,
                    padding=ft.padding.all(10)
                ),
                content_container  # dynamic content container
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH
        )
    )

    # Load home content by default
    go_home()
