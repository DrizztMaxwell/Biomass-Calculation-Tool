import flet as ft

from widgets.Equation_Card_Description_Text import Equation_Card_Description_Text
from widgets.Equation_Card_Formula_Text import Equation_Card_Formula_Text
from widgets.Equation_Card_Title_Text import Equation_Card_Title_Text
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
from widgets.Select_Components_Widget import Select_Components_Widget
from widgets.Equation_Type_Card import Equation_Type_Card
from data.components_data import COMPONENTS_DATA

# Import the Model and Controller
from model.Main_Model import Main_Model 

class Main_View:
    def __init__(self):
        self.selected_components_text = ft.Text(
            value="",
            color=ft.Colors.BLACK,
            weight=ft.FontWeight.W_500
        )
        self.component_cards_row = ft.Row(wrap=True)

    def _create_equation_card(self, title: str, formula: str, description: str, radio_value: str) -> Equation_Type_Card:
        """Helper method to create equation type cards."""
        title_formula = ft.Column(
            controls=[
                Equation_Card_Title_Text(title),
                Equation_Card_Formula_Text(formula)
            ],
            spacing=2,
        )
        desc = Equation_Card_Description_Text(description)
        return Equation_Type_Card(title_formula, desc, radio_value)

    def _create_equation_section(self) -> ft.Container:
        """Create the equation type selection section."""
        equation_cards = [
            self._create_equation_card(
                title="DBH-based",
                formula="B = b₁ × DBHᵇ²",
                description="Uses only Diameter at Breast Height for calculation",
                radio_value="DBH-based"
            ),
            self._create_equation_card(
                title="DBH + Height-based Equation",
                formula="B = b₁ × DBHᵇ² × Heightᵇ³",
                description="Uses both DBH and tree height for more accurate estimation",
                radio_value="DBH-Height-based"
            )
        ]

        radio_group = ft.RadioGroup(
            content=ft.Column(equation_cards),
            value="DBH-based"
        )

        return ft.Container(
            bgcolor="white",
            padding=20,
            margin=30,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
                offset=ft.Offset(0, 3),
            ),
            content=ft.Column([
                ft.Container(
                    margin=ft.margin.only(top=15, left=5, right=5, bottom=5),
                    content=ft.Column([
                        TitleTextWidget("Equation Type"),
                        DescriptionText("Choose the calculation method for biomass estimation"),
                    ]),
                ),
                radio_group
            ])
        )

    def _create_components_section(self) -> Select_Components_Widget:
        """Create the components selection section."""
        
        return Select_Components_Widget(
            title=TitleTextWidget("Select Tree Component"),
            description_text=DescriptionText("Select tree components for biomass calculation"),
            components_card_row=self.component_cards_row,
            selected_card_component=self.selected_components_text,
            components_data=COMPONENTS_DATA  # Pass the data
            
        )
    def build(self) -> ft.Column:
        """Build the main view layout."""
        return ft.Column(
            controls=[
                self._create_equation_section(),
                self._create_components_section()
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )