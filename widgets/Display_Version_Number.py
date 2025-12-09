import flet as ft

def Display_Version_Number(is_expanded: bool) -> ft.Text:
     return ft.Text("Version 1.0", color=ft.Colors.GREY, size=12, visible=is_expanded)