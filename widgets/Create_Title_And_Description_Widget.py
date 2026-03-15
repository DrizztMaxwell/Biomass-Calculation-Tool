from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
import flet as ft


def Create_Title_And_Description_Widget(
    title: str = "",
    description: str = "",
) -> ft.Column:
    """Page header — bold title + muted description, consistent spacing."""
    return ft.Column(
        controls=[
            TitleTextWidget(title),
            DescriptionText(description),
        ],
        spacing=4,
    )