import flet as ft

def Warning_Dialog_Header( error_messages, error_message_for_out_of_bounds_dbh_or_height_value) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.WARNING_ROUNDED, 
                                    color=ft.Colors.WHITE, 
                                    size=36
                                ),
                                bgcolor=ft.Colors.GREEN_700,
                                border_radius=50,
                                padding=10,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=20,
                                    color=ft.Colors.with_opacity(0.4, ft.Colors.ORANGE_ACCENT),
                                    offset=ft.Offset(0, 4),
                                ),
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Data Validation Warnings", 
                                        size=24, 
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            f"{len(error_messages) + len(error_message_for_out_of_bounds_dbh_or_height_value)} critical issue(s) detected",
                                            size=13,
                                            color=ft.Colors.WHITE70,
                                            weight=ft.FontWeight.W_500,
                                        ),
                                        padding=ft.padding.only(top=2),
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=20,
                    ),
                 
                ],
            ),
            padding=25,
            bgcolor=ft.Colors.BLACK,
            border_radius=ft.border_radius.only(top_left=15, top_right=15),
        )