import flet as ft

class Calculate_Biomass_Button:
    def __init__(self, on_click_callback=None, button_text="Calculate Biomass", 
                 bgcolor="#28A745", color="#FFFFFF", is_disabled=False):
        self.is_disabled = is_disabled
        self.on_click_callback = on_click_callback
        self.button_text = button_text
        self.bgcolor = bgcolor
        self.color = color
    
    def create(self):
        # Use grey color when disabled, otherwise use the provided bgcolor
        button_bgcolor = "#CCCCCC" if self.is_disabled else self.bgcolor
        button_color = "#888888" if self.is_disabled else self.color
        
        return ft.ElevatedButton(
            disabled=self.is_disabled,
            text=self.button_text,
            icon=ft.Icons.CALCULATE,
            bgcolor=button_bgcolor,
            color=button_color,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(10)),
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            ),
            on_click=self._handle_click
        )
    
    def _handle_click(self, e):
        if self.on_click_callback and not self.is_disabled:
            self.on_click_callback(e)