# model/SideNavbar_Model.py
class SideNavbar_Model:
    """Model class for the Sidebar Navigation component."""
    
    def __init__(self):
        self.sidebar_expanded = True
        self.active_nav_item = "calculate_biomass"
        self.sidebar_width_expanded = 250
        self.sidebar_width_collapsed = 80
    
    def toggle_sidebar(self):
        """Toggle sidebar state."""
        self.sidebar_expanded = not self.sidebar_expanded
        return self.sidebar_expanded
    
    def set_active_nav_item(self, item_name):
        """Set the active navigation item."""
        self.active_nav_item = item_name
    
    def get_sidebar_state(self):
        """Get current sidebar state."""
        return self.sidebar_expanded
    
    def get_active_nav_item(self):
        """Get current active navigation item."""
        return self.active_nav_item
    
    def get_sidebar_width(self):
        """Get current sidebar width based on state."""
        return self.sidebar_width_expanded if self.sidebar_expanded else self.sidebar_width_collapsed