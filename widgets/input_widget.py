import flet as ft

class InputWidget:
    """Reusable input field factory"""

    @staticmethod
    def create_text_field(label: str, value: str = "", keyboard_type=ft.KeyboardType.TEXT, width=None):
        return ft.TextField(
            label=label,
            value=value,
            keyboard_type=keyboard_type,
            width=width
        )
