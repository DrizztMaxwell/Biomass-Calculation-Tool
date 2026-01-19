from views.EULA_View import EULA_View
import flet as ft


class EULA_Controller:
    def __init__(self, page:ft.Page, view: EULA_View, callback=None):
        self.view = view
        self.page = page
        self.callback = callback  # Callback to notify main
    
    def set_callback(self, callback):
        """Set a callback function to notify main.py of the user's choice"""
        self.callback = callback
    
    def on_agree(self, e):
        if self.callback:
            self.callback(True)
  
    def on_disagree(self, e):
        if self.callback:
            self.callback(False)
    
    def build(self):
        self.view.get_eula_view()
        
    def get_exit_view(self):
        self.view.get_exit_view()
