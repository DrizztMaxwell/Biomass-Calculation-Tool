import flet as ft

class No_Data_Display(ft.Container):
    def __init__(self, primary_color, text_primary, text_secondary):
        super().__init__(
            # Ensures the container fills available space to allow centering
            expand=True, 
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.AUTO_GRAPH_OUTLINED,
                            size=60,
                            color=ft.Colors.with_opacity(0.3, primary_color),
                        ),
                        padding=20,
                        bgcolor=ft.Colors.with_opacity(0.1, primary_color),
                        border_radius=50,
                        margin=ft.margin.only(bottom=20),
                    ),
                    ft.Text(
                        "No species data available.",
                        size=18,
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                    ),
                    ft.Text(
                        "Add a new species to get started.",
                        size=14,
                        color=ft.Colors.PRIMARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                ],
                # Centers content horizontally within the Column
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                # Centers content vertically within the Column
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            # Centers the Column within the Container
            alignment=ft.alignment.center,
            padding=40,
            visible=False,
            
            border_radius=15,
            # Shadow removed
            shadow=None, 
        )