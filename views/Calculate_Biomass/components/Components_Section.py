import flet as ft
from widgets.Select_Components_Widget import Select_Components_Widget
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
from data.components_data import COMPONENTS_DATA

class Components_Section:
    """Tree components selection section."""
    
    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller
        print("Components_Section initialized with controller:", controller)
        self.component_cards_row = ft.Row(wrap=True)
        self.selected_components_text = ft.Text(
            value="",
            color=ft.Colors.BLACK,
            weight=ft.FontWeight.W_500
        )
    
    def create(self) -> Select_Components_Widget:
        """Create components selection widget."""
        return Select_Components_Widget(
            page=self.page,
            title=TitleTextWidget("Select Tree Component"),
            description_text=DescriptionText("Select tree components for biomass calculation"),
            components_card_row=self.component_cards_row,
            selected_card_component=self.selected_components_text,
            components_data=COMPONENTS_DATA,
            is_database_selected=self.controller.get_database_selected_flag(),
        ).get_widget()
    
    def get_selected_components(self):
        """Get selected components."""
        return [
            comp['title']
            for comp in COMPONENTS_DATA
            if comp['is_selected']
        ]