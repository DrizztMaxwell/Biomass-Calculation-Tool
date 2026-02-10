# components/WarningBanner.py

import flet as ft

class Warning_Banner:
    @staticmethod
    def create():
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER_700, size=20),
                    ft.Container(
                        expand=True,
                        content=ft.Text(
                            spans=[
                                ft.TextSpan("Note: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan("Your dataset columns must include the following core fields: ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                                ft.TextSpan("Plot", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                                ft.TextSpan("Year", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                                ft.TextSpan("Species", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                                ft.TextSpan("Tree Number", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                                ft.TextSpan("DBH", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan(", ", style=ft.TextStyle(color=ft.Colors.BLACK)),
                                ft.TextSpan("Height", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)),
                                ft.TextSpan(".", style=ft.TextStyle(color=ft.Colors.BLACK)),
                            ],
                            size=12,
                        ),
                    ),
                ],
                spacing=12,
            ),
            padding=ft.padding.all(16),
            bgcolor=ft.Colors.AMBER_50,
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(1, ft.Colors.AMBER_200),
        )