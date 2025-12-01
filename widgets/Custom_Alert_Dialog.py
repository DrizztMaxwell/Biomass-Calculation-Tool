import flet as ft

class Custom_Alert_Dialog:
    def __init__(self, page: ft.Page, title_icon: ft.Icons, title_color: ft.Color, title_icon_color: ft.Color, title: str = "Error", message: str = "", solution: str = "", button_text: str = "I Understand"):
        self.page = page
        self.display_alert = ft.AlertDialog(
            modal=True,
            title=ft.Container(
                content=ft.Row([
                    ft.Icon(title_icon, color=title_icon_color, size=24),
                    ft.Text(f" {title}", size=20, weight=ft.FontWeight.BOLD, color=title_color),
                ]),
                padding=ft.padding.only(bottom=10),
            ),
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text(
                        f"{message}",
                        size=16,
                        color=ft.Colors.GREY_800,
                    ),
                    ft.Text(
                        f"{solution}",
                        size=16,
                        color=ft.Colors.GREY_800,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
            ),
            actions=[
                ft.Container(
                    content=ft.TextButton(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINED, size=18, color=ft.Colors.WHITE),
                                ft.Text(f"{button_text}", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            ], tight=True, spacing=8),
                            padding=ft.padding.symmetric(horizontal=20, vertical=10),
                        ),
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLACK87,
                            elevation=2,
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=0,
                        ),
                        on_click=self.close_alert
                    ),
                    margin=ft.margin.only(top=10),
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=15),
            bgcolor=ft.Colors.WHITE,
            elevation=20,
            content_padding=ft.padding.all(20),
            inset_padding=ft.padding.symmetric(horizontal=40, vertical=20),
        )

    def show(self):
        self.page.dialog = self.display_alert
        self.display_alert.open = True
        self.page.open(self.display_alert)
        self.page.update()

    def close_alert(self, e):
        self.display_alert.open = False
        self.page.close(self.display_alert)
        self.page.update()