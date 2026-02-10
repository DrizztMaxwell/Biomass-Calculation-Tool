import flet as ft

class Search_Field(ft.TextField):
    def __init__(self, placeholder: str, on_change_callback):
        super().__init__(
            hint_text=placeholder,
            hint_style=ft.TextStyle(size=14, color=ft.Colors.PRIMARY, italic=True),
            text_size=14,
            border_color=ft.Colors.PRIMARY,
            bgcolor=ft.Colors.SECONDARY,
            height=48,
            content_padding=ft.padding.only(left=20, right=20, top=15, bottom=15),
            border_radius=15,
            expand=True,
            filled=True,
            fill_color=ft.Colors.SECONDARY,
            focused_border_color=ft.Colors.PRIMARY,
            focused_bgcolor=ft.Colors.PRIMARY,
            on_change=on_change_callback,
            suffix_icon=ft.Icon(ft.Icons.SEARCH, color=ft.Colors.BLUE_700, size=20),
        )