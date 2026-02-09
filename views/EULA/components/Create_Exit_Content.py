import flet as ft
from constants.EULA_Constants import EULA_Constants as constants
from widgets.DescriptionText import DescriptionText
from widgets.TitleTextWidget import TitleTextWidget

def Create_Exit_Content(self) -> ft.Container:
        """Create exit view content."""
        return ft.Container(


            content=
        ft.Column(
            controls=[
                ft.Icon(
                    name=self.constants.EXIT_ICON,
                    size=64,
                    color=self.constants.ERROR_COLOR
                ),
                TitleTextWidget(
                    self.constants.EXIT_TITLE,
                    size=self.constants.TITLE_SIZE,
                    color=self.constants.ERROR_COLOR
                ),
                ft.Container(
                    DescriptionText(self.constants.EXIT_MESSAGE, size=self.constants.EXIT_MESSAGE_SIZE),
                    padding=ft.padding.all(20),
                    margin=ft.margin.symmetric(horizontal=20, vertical=10),
                    bgcolor=self.constants.PRIMARY_COLOR,
                    border_radius=self.constants.CONTENT_BORDER_RADIUS,
                    border=ft.border.all(1, self.constants.BORDER_COLOR)
                ),
                ft.ElevatedButton(
                    text="Exit Application",
                    bgcolor=self.constants.ERROR_COLOR,
                    color="white",
                    on_click=lambda e: self.page.window.close()
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
        )