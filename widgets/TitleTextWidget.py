import flet as ft

def TitleTextWidget( message: str, size=22, color=ft.Colors.PRIMARY):
    return ft.Text(message, color=color, font_family="Poppins-Medium", weight=ft.FontWeight.W_700, size=size)
