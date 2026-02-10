import flet as ft

class Pagination_Controls(ft.Container):
    def __init__(self, primary_color, text_primary, text_secondary):
        self.primary_color = primary_color
        self.text_primary = text_primary
        self.text_secondary = text_secondary
        
        self.pagination_info = ft.Text(
            "", size=14, color=text_secondary, weight=ft.FontWeight.W_500
        )

        self.prev_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            icon_color=ft.Colors.GREY_400,
            icon_size=24,
            tooltip="Previous Page",
            disabled=True,
        )

        self.next_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            icon_color=ft.Colors.GREY_400,
            icon_size=24,
            tooltip="Next Page",
            disabled=True,
        )

        self.page_number_display = ft.Container(
            content=ft.Text(
                "1", size=14, weight=ft.FontWeight.W_600, color=text_primary
            ),
            padding=ft.padding.symmetric(horizontal=15, vertical=8),
            bgcolor=ft.Colors.with_opacity(0.1, primary_color),
            border_radius=8,
        )

        pagination_row = ft.Row(
            [
                self.pagination_info,
                ft.Container(expand=True),
                ft.Row(
                    [
                        self.prev_button,
                        self.page_number_display,
                        self.next_button,
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        super().__init__(
            content=pagination_row,
            padding=ft.padding.symmetric(vertical=15, horizontal=20),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_200)),
            visible=True,
        )

    def update_pagination(self, info_text, current_page, prev_disabled, next_disabled,
                          prev_color, next_color):
        self.pagination_info.value = info_text
        self.page_number_display.content.value = str(current_page)
        self.prev_button.disabled = prev_disabled
        self.next_button.disabled = next_disabled
        self.prev_button.icon_color = prev_color
        self.next_button.icon_color = next_color