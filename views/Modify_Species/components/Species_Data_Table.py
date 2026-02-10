import flet as ft

class Species_Data_Table(ft.DataTable):
    def __init__(self):
        super().__init__(
            columns=[
                ft.DataColumn(
                    ft.Text(
                        "ROW",
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                        size=12,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "SPECIES",
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                        size=12,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "ORIGIN",
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                        size=12,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "EQUATION TYPE",
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                        size=12,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "ACTIONS",
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                        size=12,
                    )
                ),
            ],
            rows=[],
            border=ft.border.all(0.5, ft.Colors.GREY_200),
            border_radius=10,
            vertical_lines=ft.BorderSide(0.5, ft.Colors.GREY_100),
            horizontal_lines=ft.BorderSide(0.5, ft.Colors.GREY_100),
            heading_row_color=ft.Colors.with_opacity(0.08, ft.Colors.GREEN_700),
            heading_row_height=55,
            data_row_min_height=60,
            data_row_max_height=70,
            column_spacing=30,
            width=9999,
            heading_text_style=ft.TextStyle(
                size=12, weight=ft.FontWeight.W_700, color=ft.Colors.GREY_900
            ),
        )