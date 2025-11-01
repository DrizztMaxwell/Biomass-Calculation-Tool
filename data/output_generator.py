#output_generator.py
import csv
import flet as ft
from data.data_manager import DataManager

def generate_csv_output(page: ft.Page):
    """
    Opens a Save File dialog to export species results as CSV.
    """
    manager = DataManager()
    data = manager.get_all()
    if not data:
        page.snack_bar = ft.SnackBar(ft.Text("⚠️ No data to export"))
        page.snack_bar.open = True
        page.update()
        return

    # FilePicker setup
    file_picker = ft.FilePicker(on_result=lambda e: _on_saved(e, page, data))
    page.overlay.append(file_picker)
    page.update()

    # Open Save As dialog
    file_picker.save_file(
        dialog_title="Save CSV output as…",
        file_name="biomass_output.csv",
        allowed_extensions=["csv", "txt"]
    )


def _on_saved(e: ft.FilePickerResultEvent, page: ft.Page, data):
    path = e.path
    if path:
        headers = ["SpecCommon", "PlotName", "DBH", "HtTot", "bio_wood", "bio_bark", "bio_foilage", "bio_branches"]
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                for entry in data:
                    writer.writerow({k: entry.get(k, "") for k in headers})
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ CSV saved to {path}"))
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Failed to save CSV: {err}"))
    else:
        page.snack_bar = ft.SnackBar(ft.Text("❌ Save cancelled"))

    page.snack_bar.open = True
    page.update()
