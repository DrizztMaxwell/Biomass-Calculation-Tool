from widgets.TitleTextWidget import TitleTextWidget
import flet as ft

def Title_With_Icon(title: str, icon: ft.Icons) -> ft.Container:
    return ft.Container(
                        content=ft.Row([
                             TitleTextWidget(title),
                            ft.Icon(icon, size=22, color=ft.Colors.PRIMARY),
                           
                        ], spacing=15),
                       
                    )