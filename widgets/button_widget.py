import flet as ft

class ButtonWidget:
    """Reusable button factory"""

    @staticmethod
    def create_button(label: str, on_click=None, color="#049A5E", text_color="white", width=None):
        return ft.ElevatedButton(
            text=label,
            bgcolor=color,
            color=text_color,
            on_click=on_click,
            width=width
        )
