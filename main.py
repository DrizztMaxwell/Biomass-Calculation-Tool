import flet as ft
import asyncio
from data.data_manager import DataManager
from views.EULA.EULA_View import EULA_View
from views.SideNavbar_View import SideNavbar_View
from controller.SideNavbar_Controller import SideNavbar_Controller
from config.App_Config import AppConfig
from widgets.LogFileTxt import logger
import sys
import os
from pathlib import Path

# Add this helper function
def get_base_path():
    """Get the base path for the application (works for both dev and PyInstaller)"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return sys._MEIPASS
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def get_project_root():
    """Get project root (works in both dev and compiled mode)"""
    if getattr(sys, 'frozen', False):
        # When frozen, the root is the _MEIPASS directory
        return Path(sys._MEIPASS)
    else:
        # When in development, go up 2 levels from this file
        return Path(__file__).parent.parent.parent

def main(page: ft.Page):
    # Set the project root correctly for frozen environment
    if getattr(sys, 'frozen', False):
        project_root = Path(sys._MEIPASS)
    else:
        project_root = Path(__file__).parent.parent.parent
    
    sys.path.insert(0, str(project_root))
    
    """Main entry point for the Biomass Calculation Tool application."""
    
    # First, configure the page with AppConfig
    AppConfig(page).configure_page()
    
    async def show_splash_and_proceed():
        """Show splash screen and then proceed to EULA"""
        # Create splash screen content
        splash_content = ft.Container(
            content=ft.Column(
                [
                    # App Logo/Icon
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.NATURE,
                            size=80,
                            color=ft.Colors.GREEN_700
                        ),
                        width=120,
                        height=120,
                        border_radius=60,
                        bgcolor=ft.Colors.GREEN_50,
                        alignment=ft.alignment.center,
                        border=ft.border.all(2, ft.Colors.GREEN_200),
                    ),
                    
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    
                    # App Name
                    ft.Text(
                        "Biomass Calculation Tool",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_800
                    ),
                    
                    ft.Text(
                        "Professional Edition",
                        size=16,
                        color=ft.Colors.GREY_600
                    ),
                    
                    ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                    
                    # Loading indicator
                    ft.Column(
                        [
                            ft.ProgressRing(
                                color=ft.Colors.GREEN_700,
                                stroke_width=4
                            ),
                            ft.Text(
                                "Loading application...",
                                size=14,
                                color=ft.Colors.GREY_600
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15
                    ),
                    
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    
                    # Version/Footer
                    ft.Text(
                        "Version 1.0",
                        size=12,
                        color=ft.Colors.GREY_400
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor=ft.Colors.WHITE,
            padding=20,
            animate_opacity=300,
        )
        
        # Add splash screen to page
        page.add(splash_content)
        page.update()
        
        logger.write("Splash screen displayed")
        
        # Simulate loading time (2 seconds)
        await asyncio.sleep(2)
        
        # Fade out animation
        splash_content.opacity = 0
        page.update()
        await asyncio.sleep(0.3)
        
        # Clear splash screen
        page.controls.clear()
        
        # Now proceed with the rest of the application
        DataManager().clear()
        logger.write("DataManager cleared, proceeding to EULA")

        eula_view = EULA_View(page=page, controller=None)
        eula_view.get_eula_view()
        page.update()
    
    # Start the splash screen sequence
    page.run_task(show_splash_and_proceed)

if __name__ == "__main__":
    ft.app(target=main)