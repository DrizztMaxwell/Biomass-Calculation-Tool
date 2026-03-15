import flet as ft


class No_Data_Display(ft.Container):
    def __init__(self, primary_color, text_primary, text_secondary):
        super().__init__(
            expand=True,
            visible=False,
            border_radius=12,
            alignment=ft.alignment.center,
            padding=40,
            
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    # Icon circle
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.ADD,
                            size=48,
                            color=ft.Colors.with_opacity(0.5, primary_color),
                        ),
                        width=90,
                        height=90,
                        bgcolor=ft.Colors.with_opacity(0.08, primary_color),
                        border_radius=ft.border_radius.all(45),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=20),
                    ),

                    # Title
                    ft.Text(
                        "No species data yet",
                        size=17,
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Container(height=6),

                    # Subtitle
                    ft.Text(
                        "Create a new species to see it listed here.",
                        size=13,
                        color=ft.Colors.with_opacity(0.6, ft.Colors.PRIMARY),
                        text_align=ft.TextAlign.CENTER,
                    ),

                
                ],
            ),
        )