import flet as ft

class No_Search_Results_Display(ft.Container):
    def __init__(self, clear_search_callback):
        # 1. Simplified the layout: Removed the Stack. 
        # A single Container with alignment=ft.alignment.center is more efficient.
        super().__init__(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.SEARCH_OFF,
                            size=70,
                            color=ft.Colors.with_opacity(0.4, ft.Colors.RED_500),
                        ),
                        padding=25,
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED_500),
                        border_radius=55,
                        margin=ft.margin.only(bottom=25),
                    ),
                    ft.Text(
                        "No Results Found",
                        size=22,
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                    ),
                    ft.Text(
                        "No species match your search criteria.\nTry different keywords or clear the search.",
                        size=16,
                        color=ft.Colors.PRIMARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        "Clear Search",
                        icon=ft.Icons.CLEAR,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.RED_500,
                            color=ft.Colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=12),
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        on_click=clear_search_callback,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER, # Centering inside the Column
                tight=True, # Important: wraps content closely
            ),
            # 2. Appearance & Positioning
            # bgcolor=ft.Colors.GREY_50,
            expand=True,           # Tells the container to take all available space
            alignment=ft.alignment.center, # Centers the Column vertically and horizontally
            visible=False,
        )