# results_menu_view.py
import flet as ft
from gui_elements import WidgetFactory

def get_results_view(data, on_back_click, on_generate_plot_click, on_generate_outputfile_click):
    """
    Returns a layout for displaying biomass calculation results.
    `data` should be a list of dicts with the biomass and other relevant fields.
    `on_back_click` and `on_generate_plot_click` are handlers for the respective buttons.
    """

    title = ft.Text("Biomass Calculation Results", size=20, weight="bold")

    # Define the headers we want to display
    headers = ["SpecCommon", "PlotName", "DBH", "bio_wood", "bio_bark", "bio_foilage", "bio_branches"]

    # Table header row
    table_header = ft.Row(
        [ft.Container(ft.Text(h, weight="bold"), expand=True) for h in headers],
        spacing=10
    )

    # Limit display to first 10 rows
    table_rows = []
    for entry in data[:10]:
        row = ft.Row(
            [ft.Container(ft.Text(str(entry.get(h, ""))), expand=True) for h in headers],
            spacing=10
        )
        table_rows.append(row)

    # Buttons
    back_btn = WidgetFactory.create_button("Back to Main Menu", on_click=on_back_click)
    generate_plot_btn = WidgetFactory.create_button("Generate Plot", on_click=on_generate_plot_click)
    generate_output_btn = WidgetFactory.create_button("Generate Output File", on_click=on_generate_outputfile_click)


    # Full layout
    layout = ft.Column(
        controls=[title, table_header, *table_rows, generate_plot_btn, generate_output_btn, back_btn],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START
    )

    return layout
