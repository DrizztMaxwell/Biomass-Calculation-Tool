# view_species_menu.py
import flet as ft
from gui_elements import WidgetFactory

def get_species_view(data, on_back_click):
    """
    Returns a scrollable table view for species data.
    `data` should be a list of dicts from localstorage.json.
    """
    title = ft.Text("Species Data", size=20, weight="bold")

    # Define the headers
    headers = [
        "SpecCode", "PlotName", "PlotKey", "FieldSeasonYear", "StandOriginCode",
        "TreeStatusCode", "TreeNum", "DBH", "HtTot", "SpecAbbrev",
        "SpecCommon"
    ]

    # Table header row
    table_header = ft.Row(
        [ft.Container(ft.Text(h, weight="bold"), expand=True) for h in headers],
        spacing=10
    )

    # Table rows
    table_rows = []
    for entry in data:
        row = ft.Row(
            [ft.Container(ft.Text(str(entry.get(h, ""))), expand=True) for h in headers],
            spacing=10
        )
        table_rows.append(row)
        
    # Scrollable container for table rows
    scrollable_table = ft.ListView(
        controls=table_rows,
        spacing=5,
        padding=5,
        expand=True  # this makes it scrollable inside a Column
    )


    # Back button
    back_btn = WidgetFactory.create_button("Back to Main Menu", on_click=on_back_click)

    # Full layout
    layout = ft.Column(
        controls=[title, table_header, scrollable_table, back_btn],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )

    return layout
