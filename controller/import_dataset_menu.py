# import_dataset_menu.py
import flet as ft
from views.import_dataset_view import get_import_dataset_view
from data.import_dataset_helper import csv_to_json

def show_import_dataset_page(container: ft.Column, page: ft.Page, on_dataset_imported=None):
    file_picker = ft.FilePicker()

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            csv_to_json(file_path)
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ Imported from {file_path}"))
            page.snack_bar.open = True
            page.update()
            # Call callback if provided
            if on_dataset_imported:
                on_dataset_imported()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("❌ No file selected"))
            page.snack_bar.open = True
            page.update()

    file_picker.on_result = on_file_picked
    page.overlay.append(file_picker)  # attach to page, not container

    layout = get_import_dataset_view(
        on_choose_file_click=lambda e: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["csv", "tsv"]
        ),
    )

    # container.controls.clear()
    # container.controls.append(layout)
    # page.update()
