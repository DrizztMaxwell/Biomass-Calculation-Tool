import flet as ft
from gui_elements import WidgetFactory

def get_import_dataset_view(on_choose_file_click, on_back_click):
    """
    Returns the layout for the Import Dataset menu with a back button.
    """

    title = ft.Text("Import Dataset Menu", size=20, weight="bold")
    instructions = ft.Text("Select a CSV or TSV file to import and convert to JSON.")

    # Button to choose CSV/TSV file
    choose_file_button = WidgetFactory.create_button(
        "Choose CSV File",
        on_click=on_choose_file_click
    )

    # Back button to return to main menu
    back_button = WidgetFactory.create_button(
        "Back",
        on_click=on_back_click
    )

    layout = ft.Column(
        controls=[
            title,
            instructions,
            choose_file_button,
            back_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    return layout

