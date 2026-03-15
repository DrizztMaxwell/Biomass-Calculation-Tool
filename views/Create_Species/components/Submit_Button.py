import flet as ft


class Submit_Button:
    """Creates the submit button."""

    def __init__(self, page: ft.Page, on_click_handler):
        self.page = page
        self.on_click_handler = on_click_handler

    def build(self):
        return ft.Row([
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE_ROUNDED, size=18, color="#FFFFFF"),
                    ft.Text("Create Species", size=15, weight=ft.FontWeight.W_600,
                            color="#FFFFFF"),
                ], spacing=8, tight=True),
                on_click=self.on_click_handler,
                bgcolor="#16A34A",
                border_radius=ft.border_radius.all(10),
                padding=ft.padding.symmetric(horizontal=28, vertical=14),
                ink=True,
                shadow=ft.BoxShadow(
                    blur_radius=8, spread_radius=0,
                    color=ft.Colors.with_opacity(0.25, "#16A34A"),
                    offset=ft.Offset(0, 3),
                ),
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)