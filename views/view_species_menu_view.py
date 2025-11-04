# view_species_menu_view.py
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import time

def get_loading_view(title_text="Loading Species Data"):
    """
    Returns a layout showing a progress bar and text.
    Can be displayed while data is being loaded.
    """
    title = text_widget.TextWidget.create_title_text(title_text, size=20)

    progress_text = ft.Text("Loading: 0%", size=16)
    progress_bar = ft.ProgressBar(width=300, height=20, value=0)

    progress_container = ft.Column(
        controls=[progress_text, progress_bar],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    layout = container_widget.ContainerWidget.create_column(
        widgets=[title, progress_container],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    return layout, progress_text, progress_bar


def get_species_view(data, page: ft.Page, progress_text=None, progress_bar=None):
    headers = [
        "SpecCode", "PlotName", "PlotKey", "FieldSeasonYear", "StandOriginCode",
        "TreeStatusCode", "TreeNum", "DBH", "HtTot", "SpecAbbrev",
        "SpecCommon"
    ]

    title = text_widget.TextWidget.create_title_text("Species Data", size=20)

    table_header = ft.Row(
        [ft.Container(ft.Text(h, weight="bold"), expand=True) for h in headers],
        spacing=10
    )

    list_view = ft.ListView(
        controls=[],
        spacing=5,
        padding=5,
        expand=True,
        auto_scroll=False
    )

    scroll_container = ft.Container(
        content=list_view,
        height=500,
        border=ft.border.all(1, "#CCCCCC"),
        border_radius=5
    )

    # ---- Prepare layout first ----
    layout = container_widget.ContainerWidget.create_column(
        widgets=[title, progress_text, progress_bar, table_header, scroll_container],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
    )

    page.update()

    # ---- Load in visible batches ----
    batch_size = 50
    total_entries = len(data)
    loaded_count = 0

    while loaded_count < total_entries:
        batch = data[loaded_count:loaded_count + batch_size]
        for entry in batch:
            row = ft.Row(
                [ft.Container(ft.Text(str(entry.get(h, ""))), expand=True) for h in headers],
                spacing=10
            )
            list_view.controls.append(row)

        loaded_count += len(batch)

        # Update progress bar if provided
        if progress_bar and progress_text:
            progress = loaded_count / total_entries
            progress_bar.value = progress
            progress_text.value = f"Loading: {int(progress*100)}%"
            page.update()

        time.sleep(0.01)  # allow UI to render

    # Once fully loaded, remove the progress bar cleanly
    layout.controls.remove(progress_text)
    layout.controls.remove(progress_bar)
    page.update()

    return layout

