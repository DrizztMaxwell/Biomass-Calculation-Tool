import flet as ft
from import_dataset_view import get_import_dataset_view
from import_dataset_helper import csv_to_json


def show_import_dataset_page(page: ft.Page, main_menu_callback):
    """
    Shows the Import Dataset menu as a full page.
    `main_menu_callback` is used to return to the main menu.
    """

    # FilePicker setup
    file_picker = ft.FilePicker()

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            csv_to_json(file_path)
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ Imported from {file_path}"))
        else:
            page.snack_bar = ft.SnackBar(ft.Text("❌ No file selected"))

        page.snack_bar.open = True
        page.update()

    file_picker.on_result = on_file_picked
    page.overlay.append(file_picker)

    # Back button handler
    def on_back_click(e):
        page.clean()
        main_menu_callback(page)

    # Get the view layout
    layout = get_import_dataset_view(
        on_choose_file_click=lambda e: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["csv", "tsv"]
        ),
        on_back_click=on_back_click
    )

    # Clear page and display layout
    page.clean()
    page.add(layout)
    page.update()
