from flet import ft
from constants.Settings_Constants import SettingsConstants

def Build_Appearance_Content() -> ft.Container:
        """Build the appearance card content section."""
        return ft.Container(
            content=ft.Column([
                self._build_theme_switch_row(),
                ft.Container(height=self.cnst.EXTRA_SPACING),
            ], spacing=self.cnst.CONTENT_SPACING),
            padding=self.cnst.CONTENT_PADDING_OBJ,
        )