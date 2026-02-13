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

def get_base_path():
    """Get the base path for the application (works for both dev and PyInstaller)"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return sys._MEIPASS
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def setup_paths():
    """Setup paths for both development and compiled environments"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        project_root = Path(sys._MEIPASS)
        logger.write(f"Running as compiled executable. Base path: {sys._MEIPASS}")
    else:
        # Running as script
        project_root = Path(__file__).parent
        logger.write(f"Running as script. Base path: {project_root}")
    
    # Add to sys.path if not already there
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    return project_root

def main(page: ft.Page):
    """Main entry point for the Biomass Calculation Tool application."""
    
    try:
        # Setup paths first
        project_root = setup_paths()
        logger.write("Application starting...")
        
        # Configure the page with AppConfig
        AppConfig(page).configure_page()
        logger.write("Page configured")
        
        async def show_splash_and_proceed():
            """Show splash screen and then proceed to EULA"""
            try:
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
                page.update()  # IMPORTANT: Update after clearing
                
                logger.write("Splash screen cleared")
                
                # Now proceed with the rest of the application
                DataManager().clear()
                logger.write("DataManager cleared, proceeding to EULA")
                
                # Create and show EULA view
                eula_view = EULA_View(page=page, controller=None)
                eula_view.get_eula_view()
                
                # IMPORTANT: Update page after adding EULA
                page.update()
                logger.write("EULA view displayed")
                
            except Exception as e:
                logger.write(f"Error in splash_and_proceed: {str(e)}")
                # Show error on page
                page.add(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.ERROR_OUTLINE, size=60, color=ft.Colors.RED_400),
                                ft.Text("Application Error", size=24, color=ft.Colors.RED_700),
                                ft.Text(str(e), size=14, color=ft.Colors.GREY_700),
                                ft.Text("Check logs for details", size=12, color=ft.Colors.GREY_500),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        expand=True,
                        alignment=ft.alignment.center,
                        padding=20
                    )
                )
                page.update()
        
        # Start the splash screen sequence
        page.run_task(show_splash_and_proceed)
        
    except Exception as e:
        logger.write(f"Error in main: {str(e)}")
        # Show error message
        page.add(
            ft.Text(f"Fatal Error: {str(e)}", color=ft.Colors.RED_700)
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)