import flet as ft

class Calculate_Biomass_Button:
    def __init__(self, on_click_callback=None, button_text="Calculate Biomass", 
                 bgcolor="#28A745", color="#FFFFFF"):
        self.on_click_callback = on_click_callback
        self.button_text = button_text
        self.bgcolor = bgcolor
        self.color = color
    
    def create(self):
        return ft.ElevatedButton(
            text=self.button_text,
            icon=ft.Icons.CALCULATE,
            bgcolor=self.bgcolor,
            color=self.color,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(10)),
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            ),
            on_click=self._handle_click
        )
    
    def _handle_click(self, e):
        if self.on_click_callback:
            self.on_click_callback()