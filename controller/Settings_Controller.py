import flet as ft
from widgets.LogFileTxt import logger


class Settings_Controller:
    """Controller for managing application settings and preferences."""
    
    def __init__(self, page: ft.Page):
        self.page = page
    
    def toggle_theme(self, event: ft.ControlEvent) -> None:
        """Toggle between dark and light theme modes."""
        self._update_theme_mode(event.control.value)
        self._log_theme_change()
        self._refresh_page()
    
    def _update_theme_mode(self, is_dark_mode: bool) -> None:
        """Set theme mode based on switch value."""
        self.page.theme_mode = (
            ft.ThemeMode.DARK if is_dark_mode else ft.ThemeMode.LIGHT
        )
    
    def _log_theme_change(self) -> None:
        """Log the current theme mode for debugging."""
        logger.write(f"Theme toggled to: {self.page.theme_mode}")
    
    def _refresh_page(self) -> None:
        """Update the page to apply theme changes."""
        self.page.update()