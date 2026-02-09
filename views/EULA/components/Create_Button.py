import flet as ft
from constants.EULA_Constants import EULA_Constants as constants

def Create_Button(text, color, bgcolor, onclick) -> ft.ElevatedButton:
        """Create the 'Agree' button."""
        return ft.ElevatedButton(
            text=text,
            bgcolor=bgcolor,
            color=color,
            on_click=onclick,
            width=120,
            height=40,
        )