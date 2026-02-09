import flet as ft
def DescriptionText(message: str, size: int = 14, letter_spacing: int = 1,  color: str = ft.Colors.PRIMARY, font_weight=ft.FontWeight.W_100) -> ft.Text:
    return ft.Text(message, color=color, font_family="Poppins-Regular", weight=font_weight, size=size, style=ft.TextStyle(letter_spacing=letter_spacing))
