import flet as ft
from constants.Settings_Constants import SettingsConstants
from widgets.DescriptionText import DescriptionText
from widgets.TitleTextWidget import TitleTextWidget
from widgets.Title_With_Icon import Title_With_Icon
from constants.Settings_Constants import SettingsConstants
def Build_Header() -> ft.Container:
        """Build the header section with title and description."""
        return ft.Container(
            content=ft.Column([
                Title_With_Icon(SettingsConstants.TITLE, SettingsConstants.SETTINGS_ICON),
                DescriptionText(SettingsConstants.DESCRIPTION),
                ft.Divider(color=SettingsConstants.GREY_300, height=SettingsConstants.DIVIDER_HEIGHT),
            ]),
            margin=ft.margin.only(bottom=SettingsConstants.HEADER_BOTTOM_MARGIN)
        )