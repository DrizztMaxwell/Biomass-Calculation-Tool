# view_species_menu_view.py
import flet as ft
import time
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget

def get_species_view(data, on_back_click, page: ft.Page):
    title = text_widget.TextWidget.create_title_text("Species Data", size=20)

    headers = [
        "SpecCode", "PlotName", "PlotKey", "FieldSeasonYear", "StandOriginCode",
        "TreeStatusCode", "TreeNum", "DBH", "HtTot", "SpecAbbrev",
        "SpecCommon"
    ]

    table_header = ft.Row(
        [ft.Container(ft.Text(h, weight="bold"), expand=True) for h in headers],
        spacing=10
    )

    # Scrollable ListView
    list_view = ft.ListView(
        controls=[],
        spacing=5,
        padding=5,
        expand=True,
        auto_scroll=False
    )

    # Wrap ListView in a fixed-height container to always show scrollbar
    scroll_container = ft.Container(
        content=list_view,
        height=500,  # adjust height as needed
        border=ft.border.all(1, "#CCCCCC"),
        border_radius=5
    )

    back_btn = button_widget.ButtonWidget.create_button(
        "Back to Main Menu", on_click=on_back_click
    )

    layout = container_widget.ContainerWidget.create_column(
        widgets=[title, table_header, scroll_container, back_btn],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
    )

    # Load entries in batches synchronously (with small delay)
    batch_size = 20
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        for entry in batch:
            row = ft.Row(
                [ft.Container(ft.Text(str(entry.get(h, ""))), expand=True) for h in headers],
                spacing=10
            )
            list_view.controls.append(row)
        page.update()
        time.sleep(0.05)  # small delay for gradual loading effect

    return layout
