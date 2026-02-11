import flet as ft
from .Equation_Section import Equation_Section
from .Components_Section import Components_Section

from widgets.Calculate_Biomass_Button import Calculate_Biomass_Button

class Layout:
    """Layout manager for Calculate Biomass view."""
    
    def __init__(self, controller, page: ft.Page):
        self.controller = controller
        self.page = page
        self.results_table_container = ft.Container(visible=False, key="results_table_container")
        
        # Initialize sections
        self.equation_section = Equation_Section(controller)
        self.components_section = Components_Section(page, controller)
        
    def build(self) -> ft.Column:
        """Build the complete layout."""
        return ft.Column(
            controls=[
                self.equation_section.create(),
                self.components_section.create(),
                self._create_calculate_button(),
                self.results_table_container
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    
    def _create_calculate_button(self) -> Calculate_Biomass_Button:
        """Create calculate biomass button."""
        return Calculate_Biomass_Button(
            on_click_callback=self.controller.on_calculate_biomass_click,
            is_disabled=False
        ).create()
    
    def get_results_container(self):
        """Get results container for updating."""
        return self.results_table_container
    
    def show_results_table(self, content):
        """Display results table."""
        self.results_table_container.content = content
        self.results_table_container.visible = True
        
    def scroll_to_results(self):
        """Scroll to results section."""
        self.page.scroll_to(
            key="results_table_container",
            duration=259,
            curve=ft.AnimationCurve.EASE_OUT
        )