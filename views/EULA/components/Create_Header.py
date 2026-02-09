import flet as ft
from constants.EULA_Constants import EULA_Constants as constants
from widgets.DescriptionText import DescriptionText
from widgets.TitleTextWidget import TitleTextWidget
def Create_Header() -> ft.Container:
        """Create the EULA header with icon and title."""
        return ft.Container(
            bgcolor=constants.PRIMARY_COLOR,
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=constants.HEADER_ICON,
                        size=constants.HEADER_SIZE,
                        color=constants.HEADER_COLOR
                    ),
                    ft.Column(
                        controls=[
                            TitleTextWidget(
                                constants.TITLE,
                                size=constants.TITLE_SIZE
                              
                            ),
                            DescriptionText(
                                constants.SUBTITLE,
                               
                            )
                        ],
                        spacing=2
                    )
                ],
                spacing=15
            ),
            padding=ft.padding.only(bottom=20)
        )