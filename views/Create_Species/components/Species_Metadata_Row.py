import flet as ft
from widgets.Create_Label_With_Icon import Create_Label_With_Icon

class Species_Metadata_Row:
    """Creates the Code, Origin, and Equation Type row."""
    
    FORM_ELEMENT_WIDTH = 300
    
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.species_textfield = None
        self.origin_dropdown = None
        self.equation_type_dropdown = None
        
    def build(self):
        """Build the metadata row."""
        
        # Species Code Control
        self.species_textfield = ft.TextField(
            hint_text="Alpine fir or 123",
            width=self.FORM_ELEMENT_WIDTH,
            border_color=ft.Colors.PRIMARY,
            on_change=lambda e: self.controller.set_species_code_or_name(e.control.value)
        )
        
        species_container = ft.Container(
            content=ft.Column([
                Create_Label_With_Icon(
                    self.page, 
                    label_text="Species (Code or Name)", 
                    icon_src="./assets/images/key.png"
                ),
                self.species_textfield
            ], width=self.FORM_ELEMENT_WIDTH),
            padding=ft.padding.only(top=10),
            alignment=ft.alignment.center,
        )

        # Origin Dropdown Control
        self.origin_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("Natural Stand"),
                ft.dropdown.Option("Plantation"),
            ],
            value="Natural Stand",
            content_padding=ft.padding.only(left=8, right=8),
            border_radius=5,
            border_color=ft.Colors.PRIMARY,
            on_change=lambda e: self.controller.set_origin_type(e.control.value),
            width=self.FORM_ELEMENT_WIDTH,
        )
        
        origin_container = ft.Container(
            content=ft.Column([
                Create_Label_With_Icon(
                    self.page, 
                    label_text="Select Origin", 
                    icon_src="./assets/images/origin.png"
                ),
                self.origin_dropdown
            ], width=self.FORM_ELEMENT_WIDTH),
            padding=ft.padding.only(top=10),
        )

        # Equation Type Dropdown Control
        self.equation_type_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("DBH-based"),
                ft.dropdown.Option("DBH + Height-based"),
            ],
            value="DBH-based",
            content_padding=ft.padding.only(left=8, right=8),
            border_radius=5,
            on_change=self._on_equation_type_change,
            width=self.FORM_ELEMENT_WIDTH,
            border_color=ft.Colors.PRIMARY,
        )
        
        equation_container = ft.Container(
            content=ft.Column([
                Create_Label_With_Icon(
                    self.page, 
                    label_text="Equation Type", 
                    icon_src="./assets/images/calculating.png"
                ),
                self.equation_type_dropdown
            ], width=self.FORM_ELEMENT_WIDTH),
            padding=ft.padding.only(top=10),
        )

        return ft.Row(
            controls=[
                species_container,
                origin_container,
                equation_container,
            ],
            spacing=20,
        )
    
    def _on_equation_type_change(self, e):
        """Handle equation type change."""
        self.controller.set_current_equation_type(e.control.value)
        
    # Getters
    def get_species_textfield(self):
        return self.species_textfield
    
    def get_origin_dropdown(self):
        return self.origin_dropdown
    
    def get_equation_type_dropdown(self):
        return self.equation_type_dropdown