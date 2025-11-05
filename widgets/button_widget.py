#button_widget
import flet as ft

class ButtonWidget:
    """Reusable button factory"""

    @staticmethod
    def create_button(label: str, on_click=None, color="#049A5E", text_color="white", width=None, size=20):
        return ft.ElevatedButton(
            
            text=label,
            bgcolor=color,
            color=text_color,
            on_click=on_click,
            width=width,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=size) 
                ,
                padding=ft.padding.symmetric(
                    horizontal=30, 
                    vertical=15
                )
            )
        )
