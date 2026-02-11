import flet as ft
from widgets.LogFileTxt import logger

class Header:
    def __init__(self, close_callback):
        self.close_callback = close_callback
        
    def create(self):
        return ft.Container(
            content=ft.Row([
                # Info icon and title with elegant styling
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.INFO_ROUNDED, color="#34D399", size=32),
                        padding=ft.padding.all(8),
                        bgcolor=ft.Colors.with_opacity(0.15, "#34D399"),
                        border_radius=ft.border_radius.all(16),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=8,
                            color=ft.Colors.with_opacity(0.3, "#34D399"),
                            offset=ft.Offset(0, 2),
                        )
                    ),
                    ft.Column([
                        ft.Text(
                            "About the Tool", 
                            size=24,
                            weight=ft.FontWeight.BOLD, 
                            color=ft.Colors.WHITE,
                        ),
                        ft.Text(
                            "Biomass Calculator", 
                            size=14,
                            color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE),
                        ),
                    ], spacing=2)
                ], spacing=14),
                    
                # Close button
                ft.Container(
                    content=ft.Icon(ft.Icons.CLOSE_ROUNDED, color=ft.Colors.WHITE70, size=24),
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    ink=True,
                    on_click=lambda e: self.close_callback(),
                    tooltip="Close",
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=25, vertical=20),
            border_radius=ft.border_radius.only(top_left=20, top_right=20),
            bgcolor="#1B2433",
        )