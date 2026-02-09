import flet as ft
from constants.Settings_Constants import SettingsConstants

def Build_Appearance_Header() -> ft.ListTile:
        """Build the appearance card header."""
        return ft.ListTile(
            leading=ft.Icon(
                SettingsConstants.PALETTE_ICON,
                color=SettingsConstants.BLUE_700,
                size=SettingsConstants.PALETTE_ICON_SIZE
            ),
            title=ft.Text(
                SettingsConstants.APPEARANCE_TITLE,
                color=SettingsConstants.ON_PRIMARY_CONTAINER,
                size=SettingsConstants.APPEARANCE_TITLE_SIZE,
                weight=SettingsConstants.APPEARANCE_TITLE_WEIGHT,
            ),
            subtitle=ft.Text(
                SettingsConstants.APPEARANCE_SUBTITLE,
                color=SettingsConstants.ON_PRIMARY_CONTAINER,
                size=SettingsConstants.APPEARANCE_SUBTITLE_SIZE,
            ),
            content_padding=SettingsConstants.HEADER_PADDING,
        )
