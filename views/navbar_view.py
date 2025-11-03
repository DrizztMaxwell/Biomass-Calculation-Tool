# navbar_view.py
import flet as ft
from widgets.button_widget import ButtonWidget
from widgets.container_widget import ContainerWidget
from widgets.text_widget import TextWidget
from data.data_manager import DataManager

def get_navbar(
    on_home_click,
    on_import_dataset_click,
    on_view_species_click,
    on_calculate_biomass_click,
    dataset_status_text  # <- pass a Text widget reference
):
    """
    Returns a vertical navigation bar with buttons for each section.
    Uses reusable widgets for consistent styling.
    """

    # Logo / title
    logo = TextWidget.create_title_text("🌿 Biomass Tool", size=20)

    # Buttons stacked vertically
    home_btn = ButtonWidget.create_button("Home", on_click=on_home_click, width=180, color="#026440")
    import_btn = ButtonWidget.create_button("Import Dataset", on_click=on_import_dataset_click, width=180)
    species_btn = ButtonWidget.create_button("View Species", on_click=on_view_species_click, width=180)
    biomass_btn = ButtonWidget.create_button("Calculate Biomass", on_click=on_calculate_biomass_click, width=180)

    # Vertical column layout
    navbar_column = ContainerWidget.create_column(
        widgets=[
            logo,
            ft.Divider(),
            home_btn,
            import_btn,
            species_btn,
            biomass_btn,
            ft.Column(expand=True),  # <- acts as a spacer
            dataset_status_text
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    # Outer container for styling and fixed width
    navbar_container = ContainerWidget.create_generic_card(
        content_widgets=[navbar_column],
        padding=ft.padding.symmetric(horizontal=10, vertical=20),
        border_radius=10,
        expand=True
    )

    return navbar_container
