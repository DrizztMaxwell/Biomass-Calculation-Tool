import flet as ft
from widgets.LogFileTxt import logger

class Settings_Controller:
    def __init__(self, page):
        self.page = page
    
    def toggle_theme(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        )
        logger.write(f"Theme toggled to: {self.page.theme_mode}")
        
        self.page.update()