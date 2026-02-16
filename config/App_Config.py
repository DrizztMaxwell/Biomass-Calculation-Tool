import flet as ft
import pyautogui
import os
import sys

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
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.debug = False  # Set to True for debugging
    
    def _get_resource_path(self, relative_path):
        """Get absolute path to resource for both development and production"""
        try:
            if getattr(sys, 'frozen', False):
                # Running in production (PyInstaller bundle)
                base_path = sys._MEIPASS
                if self.debug:
                    print(f"Production mode - using MEIPASS: {base_path}")
            else:
                # Running in development
                # Get the project root (assuming this file is in config folder)
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                if self.debug:
                    print(f"Development mode - using base_path: {base_path}")
            
            # Clean the relative path (remove ./ if present)
            clean_path = relative_path.replace('./', '').replace('\\', '/')
            
            # Construct full path
            full_path = os.path.join(base_path, clean_path)
            
            if self.debug:
                print(f"Resource path: {full_path}")
                print(f"Exists: {os.path.exists(full_path)}")
            
            return full_path
        except Exception as e:
            if self.debug:
                print(f"Error getting resource path: {e}")
            return relative_path
    
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
        
        # Register fonts with proper paths (fonts are inside assets folder)
        self.page.fonts = {
            "Poppins-Medium": self._get_resource_path("assets/fonts/poppins/Poppins-Medium.ttf"),
            "Poppins-Regular": self._get_resource_path("assets/fonts/poppins/Poppins-Regular.ttf")
        }
        
        if self.debug:
            print(f"Production mode: {getattr(sys, 'frozen', False)}")
            if hasattr(sys, '_MEIPASS'):
                print(f"MEIPASS path: {sys._MEIPASS}")
            print("Fonts registered:")
            for font_name, font_path in self.page.fonts.items():
                print(f"  {font_name}: {font_path}")
                print(f"    Exists: {os.path.exists(font_path)}")
        
        self.page.update()
    
    def enable_debug(self, enabled=True):
        """Enable or disable debug mode"""
        self.debug = enabled
    
    def check_assets_exist(self):
        """Check if all asset files exist (useful for debugging)"""
        assets_to_check = {
            "Poppins-Medium": "assets/fonts/poppins/Poppins-Medium.ttf",
            "Poppins-Regular": "assets/fonts/poppins/Poppins-Regular.ttf",
            # Add image assets if needed
            "Wood": "assets/images/wood (2).png",
            "Bark": "assets/images/bark.png",
            "Branch": "assets/images/branch.png",
            "Foliage": "assets/images/foliage.png",
            "Crown": "assets/images/crown.png",
            "Stem": "assets/images/stem.png",
            "Total": "assets/images/total.png"
        }
        
        missing_assets = []
        
        for asset_name, relative_path in assets_to_check.items():
            full_path = self._get_resource_path(relative_path)
            if not os.path.exists(full_path):
                missing_assets.append(f"{asset_name}: {full_path}")
            elif self.debug:
                print(f"✓ Found {asset_name}: {full_path}")
        
        if missing_assets:
            print("\n❌ Missing assets:")
            for missing in missing_assets:
                print(f"  - {missing}")
            return False
        else:
            print("\n✅ All assets found!")
            return True