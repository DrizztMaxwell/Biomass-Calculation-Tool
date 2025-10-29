#calculate_biomass_menu_view.py
import flet as ft
from gui_elements import WidgetFactory

def get_calculate_biomass_menu_view(on_run_click, on_back_click):
    """
    Returns the layout for the Calculate Biomass menu with checkboxes and action buttons.
    """

    title = ft.Text("Calculate Biomass Menu", size=20, weight="bold")
    instructions = ft.Text("Select components to calculate biomass:")

    # Checkbox controls
    wood_cb = ft.Checkbox(label="Wood")
    bark_cb = ft.Checkbox(label="Bark")
    foilage_cb = ft.Checkbox(label="Foilage")
    branches_cb = ft.Checkbox(label="Branches")

    checkboxes = [wood_cb, bark_cb, foilage_cb, branches_cb]

    # Buttons
    run_btn = WidgetFactory.create_button("Run Calculations", on_click=on_run_click)
    back_btn = WidgetFactory.create_button("Back", on_click=on_back_click)

    layout = ft.Column(
        controls=[
            title,
            instructions,
            *checkboxes,
            run_btn,
            back_btn
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )

    # Return both layout and the checkboxes so caller can read their values
    return layout, {
        "wood": wood_cb,
        "bark": bark_cb,
        "foilage": foilage_cb,
        "branches": branches_cb
    }
