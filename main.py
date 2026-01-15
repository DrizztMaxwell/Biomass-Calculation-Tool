# main.py
import flet as ft
from data.data_manager import DataManager
from controller.EULA_Controller import EULA_Controller
from views.EULA_View import EULA_View
from views.SideNavbar_View import SideNavbar_View
from controller.SideNavbar_Controller import SideNavbar_Controller
import pyautogui
def _screen_configuration(page:ft.Page):
    page.title = "Biomass Calculator"
    width, height = pyautogui.size()

    page.window.resizable = True  # window is not resizable
    page.window.width = width        # window's width is 200 px
    page.window.height = height       # window's height is 200 px
    # page.theme_mode = ft.ThemeMode.DARK
    page.window_full_screen = True
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLACK,      # For text colors in light theme
           secondary=ft.Colors.WHITE ,       # background colors in light theme
           secondary_container=ft.Colors.WHITE, # container backgrounds
           tertiary=ft.Colors.BLUE_700  
           
           

        )
    )
    page.dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.WHITE,      # For text colors in dark theme
            secondary=ft.Colors.BLACK87  ,     # background colors in dark theme
            secondary_container=ft.Colors.GREY_900, # container backgrounds
            tertiary=ft.Colors.PURPLE_600,
            background=ft.Colors.BLACK
        )
    )
    page.bgcolor = ft.Colors.SECONDARY

    page.padding = 0
     # Set fonts
    page.fonts = {
        
            "Poppins-Medium": "./assets/fonts/poppins/Poppins-Medium.ttf",
            "Poppins-Regular": "./assets/fonts/poppins/Poppins-Regular.ttf" 
        }
    page.update()
    


# from views.SideNavBar_View import main
def main(page: ft.Page):
    _screen_configuration(page)
   
  
    """
    Entry point for the app.
    """
    manager = DataManager()

    # Clear any existing localstorage.json to trigger the import restriction
    manager.clear()

    # Optional: attach cleanup on close if you want to clear again
    def cleanup(e=None):
        manager.clear()

    page.on_close = cleanup
    
    
    def handle_eula_result(agreed):
        """Handle the EULA agreement result"""
        if agreed:
            print("✅ User agreed to EULA - proceeding with application")
            page.clean()
            SideNavbar_Controller(SideNavbar_View(page)).build()
            page.update()
        else:
            print("❌ User rejected EULA - application cannot proceed")
            page.clean()
            
            eula_controller.get_exit_view()
            page.update()
    
    eula_view = EULA_View(page=page, controller=None)
    eula_controller = EULA_Controller(page=page, view=eula_view)
    eula_view.controller = eula_controller
    
    # Set the callback to handle the EULA result
    eula_controller.set_callback(handle_eula_result)
    
    # Build and show EULA page
    eula_controller.build()
    


if __name__ == "__main__":
    ft.app(target=main)
    
