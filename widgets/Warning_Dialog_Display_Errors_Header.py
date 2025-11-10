import flet as ft

def Warning_Dialog_Display_Errors_Header():
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Warning Details", 
                            size=18, 
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800,
                        ),
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Review each issue below",
                            size=12,
                            color=ft.Colors.GREY_500,
                            italic=True,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.padding.only(left=20, right=20, top=10, bottom=10),
        )
