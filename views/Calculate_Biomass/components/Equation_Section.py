import flet as ft
from widgets.Equation_Card_Description_Text import Equation_Card_Description_Text
from widgets.Equation_Card_Formula_Text import Equation_Card_Formula_Text
from widgets.Equation_Card_Title_Text import Equation_Card_Title_Text
from widgets.Equation_Type_Card import Equation_Type_Card
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText

class Equation_Section:
    """Equation type selection section."""
    
    def __init__(self, controller):
        self.controller = controller
    
    def create(self) -> ft.Container:
        """Create equation section."""
        equation_cards = [
            self._create_equation_card(
                title="DBH-based",
                formula="B = b₁ × DBHᵇ²",
                description="Uses only Diameter at Breast Height for calculation",
                radio_value="DBH-based"
            ),
            self._create_equation_card(
                title="DBH + Height-based",
                formula="B = b₁ × DBHᵇ² × Heightᵇ³",
                description="Uses both DBH and tree height for more accurate estimation",
                radio_value="DBH + Height-based"
            )
        ]
        
        radio_group = ft.RadioGroup(
            content=ft.Column(equation_cards),
            on_change=self._on_equation_type_change,
            value="DBH-based"
        )
        
        return ft.Container(
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            padding=20,
            margin=30,
            border_radius=10,
            shadow=self._create_shadow(),
            content=ft.Column([
                self._create_section_header(
                    title="Equation Type",
                    description="Choose the calculation method for biomass estimation"
                ),
                radio_group
            ])
        )
    
    def _create_equation_card(self, title: str, formula: str, description: str, radio_value: str) -> Equation_Type_Card:
        """Create an equation type card."""
        title_formula = ft.Column(
            controls=[
                Equation_Card_Title_Text(title),
                Equation_Card_Formula_Text(formula)
            ],
            spacing=2,
        )
        desc = Equation_Card_Description_Text(description)
        
        return Equation_Type_Card(title_formula, desc, radio_value)
    
    def _on_equation_type_change(self, event):
        """Handle equation type selection change."""
        self.controller.set_equation_type(event.control.value)
    
    def _create_section_header(self, title: str, description: str) -> ft.Container:
        """Create section header."""
        return ft.Container(
            margin=ft.margin.only(top=15, left=5, right=5, bottom=5),
            content=ft.Column([
                TitleTextWidget(title),
                DescriptionText(description),
            ]),
        )
    
    def _create_shadow(self) -> ft.BoxShadow:
        """Create consistent shadow."""
        return ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
            offset=ft.Offset(0, 3),
        )