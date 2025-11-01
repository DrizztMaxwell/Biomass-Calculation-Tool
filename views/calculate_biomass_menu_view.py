#calculate_biomass_menu_view.py
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget
import widgets.input_widget as input_widget

def get_calculate_biomass_menu_view(on_run_click):
    """
    Returns the layout for the Calculate Biomass menu with checkboxes and action buttons.
    """

    # Title and instructions using text_widget
    title = text_widget.TextWidget.create_title_text("Calculate Biomass Menu", size=22)
    instructions = text_widget.TextWidget.create_description_text("Select components to calculate biomass:")

    # Checkbox controls
    wood_cb = ft.Checkbox(label="Wood")
    bark_cb = ft.Checkbox(label="Bark")
    foilage_cb = ft.Checkbox(label="Foilage")
    branches_cb = ft.Checkbox(label="Branches")

    checkboxes = [wood_cb, bark_cb, foilage_cb, branches_cb]

    # Buttons using button_widget
    run_btn = button_widget.ButtonWidget.create_button("Run Calculations", on_click=on_run_click, width=220)

    # Use container_widget for layout consistency
    layout = container_widget.ContainerWidget.create_column(
        widgets=[
            title,
            instructions,
            *checkboxes,
            run_btn
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    # Return layout + checkbox map for caller access
    return layout, {
        "wood": wood_cb,
        "bark": bark_cb,
        "foilage": foilage_cb,
        "branches": branches_cb
    }
