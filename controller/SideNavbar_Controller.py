# controller/SideNavbar_Controller.py
import flet as ft
from model.SideNavbar_Model import SideNavbar_Model
# from view.SideNavbar_View import Sid

class SideNavbar_Controller:
    """Controller class for the Sidebar Navigation component."""
    
    def __init__(self, main_controller=None):
        self.model = SideNavbar_Model()
        self.view = SideNavbar_View(self)
        self.main_controller = main_controller  # Reference to main controller for navigation
        self.page = None
        
    def build(self, page):
        """Build the sidebar component."""
        self.page = page
        return self.view.build()
    
    def toggle_sidebar(self, e):
        """Handle sidebar toggle."""
        is_expanded = self.model.toggle_sidebar()
        updated_sidebar = self.view.update_sidebar()
        
        # If we have a main controller, notify it about the sidebar state change
        if self.main_controller:
            self.main_controller.on_sidebar_toggle(is_expanded)
        
        # Update the page if we have direct access
        if self.page:
            self.page.update()
        
        return updated_sidebar
    
    def navigate_to_page(self, page_name):
        """Navigate to the specified page."""
        self.model.set_active_nav_item(page_name)
        
        # Update sidebar to reflect active state
        self.view.update_sidebar()
        
        # Delegate actual page navigation to main controller
        if self.main_controller:
            self.main_controller.navigate_to_page(page_name)
        
        # Update the page if we have direct access
        if self.page:
            self.page.update()
    
    def show_about_dialog(self, e):
        """Show the About dialog."""
        if self.main_controller:
            self.main_controller.show_about_dialog(e)
        else:
            # Fallback: create basic about dialog if no main controller
            self._create_basic_about_dialog(e)
    
    def _create_basic_about_dialog(self, e):
        """Create a basic about dialog as fallback."""
        about_dialog = ft.AlertDialog(
            title=ft.Text("About Biomass Calculator"),
            content=ft.Text("Biomass Calculator v1.0\n\nThis tool provides biomass estimation for Canadian tree species."),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self._close_dialog(e))
            ]
        )
        
        if self.page:
            self.page.dialog = about_dialog
            about_dialog.open = True
            self.page.update()
    
    def _close_dialog(self, e):
        """Close the dialog."""
        if self.page and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
    
    def set_active_page(self, page_name):
        """Set the active page from external source."""
        self.model.set_active_nav_item(page_name)
        if self.page:
            self.view.update_sidebar()
            self.page.update()
    
    def get_sidebar_component(self):
        """Get the sidebar component."""
        return self.view.sidebar_container
    
    def get_sidebar_state(self):
        """Get current sidebar state."""
        return self.model.get_sidebar_state()