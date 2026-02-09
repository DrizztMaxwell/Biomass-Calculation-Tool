
import flet as ft
from constants.EULA_Constants import EULA_Constants as constants
from widgets.DescriptionText import DescriptionText
from widgets.TitleTextWidget import TitleTextWidget

def Create_Section( heading: str, content: str, icon: str) -> ft.Container:
        """Create a consistent section with heading and content."""
        return ft.Container(
            bgcolor=constants.PRIMARY_COLOR,
            content=ft.Column(
                controls=[
                    _create_section_heading(heading, icon),
                    _create_section_content(content)
                ],
                spacing=constants.SECTION_SPACING,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            padding=ft.padding.symmetric(vertical=10)
        )
    
def _create_section_heading(heading: str, icon: str) -> ft.Row:
    """Create section heading with icon."""
    return ft.Row(
        controls=[
            ft.Icon(
                name=icon,
                size=20,
                color=constants.HEADER_COLOR
            ),
            TitleTextWidget(
                heading,
                size=constants.SECTION_HEADING_SIZE,
                color=constants.HEADER_COLOR
            )
        ],
        spacing=10
    )
    
def _create_section_content(content: str) -> ft.Container:
    """Create styled section content container."""
    return ft.Container(
        content=DescriptionText(content, size=constants.SECTION_TEXT_SIZE),
        margin=ft.margin.only(left=30),
        padding=ft.padding.all(15),
        bgcolor=constants.PRIMARY_COLOR,
        border_radius=constants.CONTENT_BORDER_RADIUS,
        border=ft.border.all(1, constants.BORDER_COLOR),
        expand=False
    )