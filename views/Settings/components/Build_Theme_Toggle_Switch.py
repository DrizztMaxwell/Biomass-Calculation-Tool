import flet as ft
from constants.Settings_Constants import SettingsConstants

def Build_Theme_Toggle_Switch(toggle_theme, page) -> ft.Switch:
    """Build the theme toggle switch."""
    return ft.Switch(
        label=SettingsConstants.THEME_SWITCH_LABEL,
        label_style=ft.TextStyle(
            color=SettingsConstants.PRIMARY,
            size=SettingsConstants.TITLE_FONT_SIZE,
        ),
        value=page.theme_mode == ft.ThemeMode.DARK,
        on_change=toggle_theme,
        active_color=SettingsConstants.TERTIARY,
        inactive_thumb_color=SettingsConstants.GREY_700,
        inactive_track_color=SettingsConstants.GREY_300,
    )