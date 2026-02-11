import flet as ft
class Header:
    def __init__(self, close_callback):
        self.close_callback = close_callback
        
    def create(self):
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.SETTINGS_SUGGEST_ROUNDED, color=ft.Colors.BLUE_400, size=28),
                    ft.Column([
                        ft.Text("System Information", size=18, weight=ft.FontWeight.W_800, color=ft.Colors.WHITE),
                        ft.Text("Biomass Calculator | MNRF & Trent University", size=11, color=ft.Colors.BLUE_200),
                    ], spacing=0)
                ], spacing=15),
                ft.IconButton(
                    icon=ft.Icons.CLOSE_ROUNDED,
                    icon_color=ft.Colors.WHITE70,
                    on_click=lambda _: self.close_callback(),
                    style=ft.ButtonStyle(overlay_color=ft.Colors.WHITE10)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=25, vertical=15),
            bgcolor="#1A202C", # Deep professional Slate
            border_radius=ft.border_radius.only(top_left=15, top_right=15)
        )