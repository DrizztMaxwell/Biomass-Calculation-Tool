# calculate_biomass_menu_view.py
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget

def get_calculate_biomass_menu_view(on_run_click):
    """
    Returns the layout for the Calculate Biomass menu with a global equation selection
    and the Run Calculations button.
    """

    # Title and instructions
    title = text_widget.TextWidget.create_title_text("Calculate Biomass Menu", size=22)
    instructions = text_widget.TextWidget.create_description_text(
        "Select the equation to use for all biomass components:"
    )

    # Label for radio buttons
    radio_label = text_widget.TextWidget.create_description_text("Equation Type:")

    # Global radio buttons for equation selection (pass content directly)
    equation_radio = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="dbh", label="DBH only"),
            ft.Radio(value="dbh_height", label="DBH + Height")
        ])
    )
    equation_radio.value = "dbh"
    # Run button
    run_btn = button_widget.ButtonWidget.create_button(
        "Run Calculations",
        on_click=on_run_click,
        width=220
    )

    # Layout using container_widget
    layout = container_widget.ContainerWidget.create_column(
        widgets=[
            title,
            instructions,
            radio_label,
            equation_radio,
            run_btn
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    return layout, equation_radio
