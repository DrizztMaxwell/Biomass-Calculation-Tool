import flet as ft

class Action_Buttons(ft.Row):
    def __init__(self, index, on_view_click, on_edit_click, on_delete_click,
                 primary_color, secondary_color):
        view_button = ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.REMOVE_RED_EYE_OUTLINED,
                icon_color=ft.Colors.WHITE,
                icon_size=18,
                tooltip="View Details",
                on_click=lambda e: on_view_click(index),
            ),
            bgcolor=primary_color,
            border_radius=8,
            padding=ft.padding.all(2),
        )

        edit_button = ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.EDIT_OUTLINED,
                icon_color=ft.Colors.WHITE,
                icon_size=18,
                tooltip="Edit",
                on_click=lambda e: on_edit_click(index),
            ),
            bgcolor=secondary_color,
            border_radius=8,
            padding=ft.padding.all(2),
        )

        delete_button = ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINED,
                icon_color=ft.Colors.WHITE,
                icon_size=18,
                tooltip="Delete",
                on_click=lambda e: on_delete_click(index),
            ),
            bgcolor=ft.Colors.RED_400,
            border_radius=8,
            padding=ft.padding.all(2),
        )

        super().__init__(
            [view_button, edit_button, delete_button],
            spacing=8,
        )