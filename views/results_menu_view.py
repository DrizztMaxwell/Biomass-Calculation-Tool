# results_menu_view.py
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget

def get_results_view(data, on_generate_plot_click, on_generate_outputfile_click):
    """
    Returns a layout for displaying biomass calculation results.
    `data` should be a list of dicts with the biomass and other relevant fields.
    """

    # Title using TextWidget
    title = text_widget.TextWidget.create_title_text("Biomass Calculation Results", size=20)

    # Define headers
    headers = [
        "SpecCode", "SpecCommon",
        "DBH", "bio_wood", "bio_bark", "bio_foilage", "bio_branches"
    ]

    # Table header row using container_widget
    table_header = ft.Row(
        [
            container_widget.ContainerWidget.create_generic_card(
                [text_widget.TextWidget.create_label_text(h, size=16)],
                padding=3,
                margin=ft.margin.all(2),
                expand=True
            )
            for h in headers
        ],
        spacing=5
    )

    # Table rows
    table_rows = []
    for entry in data[:5]:  # Limit to first 10 rows
        row = ft.Row(
            [
                container_widget.ContainerWidget.create_generic_card(
                    [text_widget.TextWidget.create_label_text(str(entry.get(h, "")))],
                    padding=3,
                    margin=ft.margin.all(2),
                    expand=True
                )
                for h in headers
            ],
            spacing=5
        )
        table_rows.append(row)

    # Buttons using button_widget
    generate_plot_btn = button_widget.ButtonWidget.create_button("Generate Plot", on_click=on_generate_plot_click)
    generate_output_btn = button_widget.ButtonWidget.create_button("Generate Output File", on_click=on_generate_outputfile_click)

    # Full layout
    layout = ft.Column(
        controls=[title, table_header, *table_rows, generate_plot_btn, generate_output_btn],
        spacing=10,
        alignment=ft.MainAxisAlignment.START
    )

    return layout
