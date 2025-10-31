#main_menu_view
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget
import widgets.input_widget as input_widget


def get_main_menu_view(on_import_dataset_click, on_view_species_click, on_calculate_biomass_click):
    """
    Returns the layout for the Main Menu screen with navigation buttons.
    """

    # Title text using text_widget
    title = text_widget.TextWidget.create_title_text("Biomass Calculation Tool", size=26)

    # Subtitle using text_widget
    subtitle = text_widget.TextWidget.create_description_text(
        "Select an option below to continue."
    )

    # Buttons using button_widget
    import_button = button_widget.ButtonWidget.create_button(
        "Import Dataset",
        on_click=on_import_dataset_click,
        width=250
    )

    view_species_button = button_widget.ButtonWidget.create_button(
        "View Species Data",
        on_click=on_view_species_click,
        width=250
    )

    calculate_biomass_button = button_widget.ButtonWidget.create_button(
        "Calculate Biomass",
        on_click=on_calculate_biomass_click,
        width=250
    )

    # Layout using container_widget for consistent visual hierarchy
    layout = container_widget.ContainerWidget.create_column(
        widgets=[
            title,
            subtitle,
            import_button,
            view_species_button,
            calculate_biomass_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=25
        
    )

    return layout
