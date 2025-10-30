#import_dataset_view
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget
import widgets.input_widget as input_widget

def get_import_dataset_view(on_choose_file_click, on_back_click):
    """
    Returns the layout for the Import Dataset menu with a back button.
    """

    # Title and instructions using text_widget
    title = text_widget.TextWidget.create_title_text("Import Dataset Menu", size=22)
    instructions = text_widget.TextWidget.create_description_text(
        "Select a CSV or TSV file to import and convert to JSON."
    )

    # Button to choose CSV/TSV file using button_widget
    choose_file_button = button_widget.ButtonWidget.create_button(
        "Choose CSV File",
        on_click=on_choose_file_click,
        width=220
    )

    # Back button using button_widget
    back_button = button_widget.ButtonWidget.create_button(
        "Back",
        on_click=on_back_click,
        color="#888888",
        width=220
    )

    # Layout using container_widget for consistent structure
    layout = container_widget.ContainerWidget.create_column(
        widgets=[
            title,
            instructions,
            choose_file_button,
            back_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    return layout
