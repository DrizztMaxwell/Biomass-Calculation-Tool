# calculate_biomass_menu_view.py
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget

def get_calculate_biomass_menu_view(on_run_click):
    """
    Returns the layout for the Calculate Biomass menu with global equation selection,
    component selection checkboxes, and the Run Calculations button.
    """

    # --- Title and instructions ---
    title = text_widget.TextWidget.create_title_text("Calculate Biomass Menu", size=22)
    instructions = text_widget.TextWidget.create_description_text(
        "Select the equation type and biomass components to calculate:"
    )

    # --- Equation selection ---
    radio_label = text_widget.TextWidget.create_description_text("Equation Type:")
    equation_radio = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="dbh", label="DBH only"),
            ft.Radio(value="dbh_height", label="DBH + Height"),
        ])
    )
    equation_radio.value = "dbh"

    # --- Component checkboxes ---
    component_label = text_widget.TextWidget.create_description_text("Select Biomass Components:")
    wood_checkbox = ft.Checkbox(label="Wood", value=True)
    bark_checkbox = ft.Checkbox(label="Bark", value=True)
    foliage_checkbox = ft.Checkbox(label="Foliage", value=True)
    branches_checkbox = ft.Checkbox(label="Branches", value=True)

    # --- Run button ---
    run_btn = button_widget.ButtonWidget.create_button(
        "Run Calculations",
        on_click=on_run_click,
        width=220
    )

    # --- Layout ---
    layout = container_widget.ContainerWidget.create_column(
        widgets=[
            title,
            instructions,
            radio_label,
            equation_radio,
            component_label,
            wood_checkbox,
            bark_checkbox,
            foliage_checkbox,
            branches_checkbox,
            run_btn,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    return layout, equation_radio, wood_checkbox, bark_checkbox, foliage_checkbox, branches_checkbox
