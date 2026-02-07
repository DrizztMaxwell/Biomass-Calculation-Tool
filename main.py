import flet as ft
import asyncio
from data.data_manager import DataManager
from views.EULA_View import EULA_View
from views.SideNavbar_View import SideNavbar_View
from controller.SideNavbar_Controller import SideNavbar_Controller
from config.App_Config import AppConfig
from widgets.LogFileTxt import logger

def main(page: ft.Page):
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
                            ft.Icons.NATURE,  # Using a nature icon for biomass app
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
        await asyncio.sleep(0.3)  # Wait for fade animation
        
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