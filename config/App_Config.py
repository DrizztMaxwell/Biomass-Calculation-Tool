import flet as ft
import pyautogui

class AppConfig:
    """Handles application-wide configuration and theming"""
    
     # Theme constants
    LIGHT_THEME = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLACK,
            secondary=ft.Colors.WHITE,
            secondary_container=ft.Colors.WHITE,
            tertiary=ft.Colors.BLUE_700
        )
    )
    
    DARK_THEME = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.WHITE,
            secondary=ft.Colors.BLACK87,
            secondary_container=ft.Colors.GREY_900,
            tertiary=ft.Colors.PURPLE_600,
            background=ft.Colors.BLACK
        )
    )
    
    FONTS = {
        "Poppins-Medium": "./assets/fonts/poppins/Poppins-Medium.ttf",
        "Poppins-Regular": "./assets/fonts/poppins/Poppins-Regular.ttf"
    }
    
    def __init__(self, page: ft.Page):
        self.page = page
    
    def get_screen_dimensions(self) -> tuple[int, int]:
        """Get the screen dimensions"""
        return pyautogui.size()
    
    
    def configure_page(self) -> None:
        """Configure the main page with all settings"""
        self.page.title = "Biomass Calculator"
        
        # Set window size to full screen
        screen_width, screen_height = self.get_screen_dimensions()
        self.page.window.resizable = True
        self.page.window.width = screen_width
        self.page.window.height = screen_height
        self.page.window_full_screen = True
        
        # Apply themes
        self.page.theme = self.LIGHT_THEME
        self.page.dark_theme = self.DARK_THEME
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # Apply styling
        self.page.bgcolor = ft.Colors.SECONDARY
        self.page.padding = 0
        
        # Register fonts
        self.page.fonts = self.FONTS
        
        self.page.update()