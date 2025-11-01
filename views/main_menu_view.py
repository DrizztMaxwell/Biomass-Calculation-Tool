# main_menu_view.py
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget


def get_main_menu_view():
    """
    Returns the layout for the Main Menu screen with centered welcome text.
    """

    title = text_widget.TextWidget.create_title_text(
        "Biomass Calculation Tool",
        size=28
    )

    subtitle = text_widget.TextWidget.create_description_text(
        "Use the navigation bar above to import datasets, view species data, or calculate biomass."
    )

    layout = container_widget.ContainerWidget.create_column(
        widgets=[title, subtitle],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    return layout
