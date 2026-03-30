import flet as ft
from views.SideNavbar_View import SideNavbar_View


class SideNavbar_Controller:
    """Controller class for the Sidebar Navigation component.
       (Model logic merged directly into controller)
    """

    def __init__(self, view: SideNavbar_View):
        # ---- Model state (previously in SideNavbar_Model) ----
        self.sidebar_expanded = True
        self.active_nav_item = "calculate_biomass"
        self.sidebar_width_expanded = 250
        self.sidebar_width_collapsed = 80
        # -------------------------------------------------------

        self.view = view
        self.page = None
        self.main_controller = None

    # ========================
    # Model Logic (Merged)
    # ========================

    def toggle_sidebar_state(self):
        """Toggle sidebar state."""
        self.sidebar_expanded = not self.sidebar_expanded
        return self.sidebar_expanded

    def set_active_nav_item(self, item_name):
        """Set active navigation item."""
        self.active_nav_item = item_name

    def get_sidebar_state(self):
        """Get current sidebar state."""
        return self.sidebar_expanded

    def get_active_nav_item(self):
        """Get current active navigation item."""
        return self.active_nav_item

    def get_sidebar_width(self):
        """Get sidebar width based on state."""
        return (
            self.sidebar_width_expanded
            if self.sidebar_expanded
            else self.sidebar_width_collapsed
        )

    # ========================
    # Controller Logic
    # ========================

    def build(self):
        """Build the sidebar component."""
        return self.view.build()

    def toggle_sidebar(self, e):
        """Handle sidebar toggle."""
        is_expanded = self.toggle_sidebar_state()
        updated_sidebar = self.view.update_sidebar()

        if self.main_controller:
            self.main_controller.on_sidebar_toggle(is_expanded)

        if self.page:
            self.page.update()

        return updated_sidebar

    def navigate_to_page(self, page_name):
        """Navigate to the specified page."""
        self.set_active_nav_item(page_name)
        self.view.update_sidebar()

        if self.main_controller:
            self.main_controller.navigate_to_page(page_name)

        if self.page:
            self.page.update()

    def show_about_dialog(self, e):
        """Show the About dialog."""
        if self.main_controller:
            self.main_controller.show_about_dialog(e)
        else:
            self._create_basic_about_dialog(e)

    def _create_basic_about_dialog(self, e):
        """Create a basic about dialog as fallback."""
        about_dialog = ft.AlertDialog(
            title=ft.Text("About Biomass Calculator"),
            content=ft.Text(
                "Biomass Calculator v1.0\n\n"
                "This tool provides biomass estimation for Canadian tree species."
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self._close_dialog(e))
            ],
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
        """Set active page externally."""
        self.set_active_nav_item(page_name)
        if self.page:
            self.view.update_sidebar()
            self.page.update()

    def get_sidebar_component(self):
        """Get the sidebar component."""
        return self.view.sidebar_container