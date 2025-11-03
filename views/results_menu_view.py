#results_menu_view
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget

def get_results_view(data, headers, on_generate_plot_click, on_generate_outputfile_click):
    """
    Returns a layout for displaying biomass calculation results.
    Only shows the columns passed in `headers`.
    """

    # Title using TextWidget
    title = text_widget.TextWidget.create_title_text("Biomass Calculation Results", size=20)

    # --- Table Header ---
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

    # --- Table Rows (limit preview to 10 rows for performance) ---
    table_rows = []
    for entry in data[:7]:
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

    # --- Action Buttons ---
    generate_plot_btn = button_widget.ButtonWidget.create_button(
        "Generate Plot",
        on_click=on_generate_plot_click
    )
    generate_output_btn = button_widget.ButtonWidget.create_button(
        "Generate Output File",
        on_click=on_generate_outputfile_click
    )

    # --- Scrollable Layout ---
    scrollable_table = ft.Column(
        controls=[table_header, *table_rows],
        spacing=5,
        scroll=ft.ScrollMode.AUTO
    )

    layout = ft.Column(
        controls=[
            title,
            scrollable_table,
            ft.Row([generate_plot_btn, generate_output_btn], spacing=10)
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )

    return layout
