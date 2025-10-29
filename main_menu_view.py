import flet as ft
from gui_elements import WidgetFactory

def get_main_menu_view(on_import_dataset_click, on_view_species_click, on_calculate_biomass_click):
    """
    Returns a Column layout with three main menu buttons
    Event handlers are passed from the Controller
    """

    import_dataset_btn = WidgetFactory.create_button(
        "Import Dataset",
        on_click=on_import_dataset_click,
        width=200
    )

    view_species_btn = WidgetFactory.create_button(
        "View Species",
        on_click=on_view_species_click,
        width=200
    )

    calculate_biomass_btn = WidgetFactory.create_button(
        "Calculate Biomass",
        on_click=on_calculate_biomass_click,
        width=200
    )

    layout = ft.Column(
        controls=[
            import_dataset_btn,
            view_species_btn,
            calculate_biomass_btn
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    return layout
