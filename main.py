import flet as ft
from data.data_manager import DataManager
from controller.EULA_Controller import EULA_Controller
from views.EULA_View import EULA_View
from views.SideNavbar_View import SideNavbar_View
from controller.SideNavbar_Controller import SideNavbar_Controller
from config.App_Config import AppConfig
from widgets.LogFileTxt import logger
def main(page: ft.Page):
    """Main entry point for the Biomass Calculation Tool application."""
    
    DataManager().clear()
    AppConfig(page).configure_page()

    def handle_eula_result(agreed):
        """Handle the EULA agreement result"""
        if agreed:
            logger.write("User agreed to EULA - proceeding with application")
            page.clean()
            SideNavbar_Controller(SideNavbar_View(page)).build()
            page.update()
        else:
            logger.write("User rejected EULA - application cannot proceed")
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
    
