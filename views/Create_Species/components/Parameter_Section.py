import flet as ft
from widgets.TitleTextWidget import TitleTextWidget
from .Parameter_Input import Parameter_Input

class ParametersSection:
    """Creates the parameter input fields section with component labels."""
    
    def __init__(self, controller):
        self.controller = controller
        self.param_labels = {}
        self.no_parameters = None
        self.sections = {}  # Store the entire section columns
        
    def _create_component_section(self, component_name: str, 
                                  b1_control: ft.Control, 
                                  b2_control: ft.Control, 
                                  b3_control: ft.Control = None) -> ft.Column:
        """Create a section for a specific component."""
        
        label = ft.Text(
            component_name, 
            size=14, 
            weight=ft.FontWeight.BOLD, 
            color=ft.Colors.ON_PRIMARY_CONTAINER
        )
        self.param_labels[component_name] = label
        
        # Create parameter row
        param_row_items = [
            ft.Container(content=b1_control, expand=True),
            ft.Container(content=b2_control, expand=True),
        ]
        
        if b3_control:
            param_row_items.append(ft.Container(content=b3_control, expand=True))
        
        section = ft.Column([
            label,
            ft.Row(param_row_items, spacing=20)
        ], spacing=10)
        
        # Store the entire section for visibility control
        self.sections[component_name] = section
        return section
    
    def build(self):
        """Build the complete parameters section."""
        
        # Create parameter controls for DBH-based (b1, b2)
        wood_b1 = Parameter_Input.create("b1", self.controller)
        wood_b2 = Parameter_Input.create("b2", self.controller)
        bark_b1 = Parameter_Input.create("b1", self.controller)
        bark_b2 = Parameter_Input.create("b2", self.controller)
        branch_b1 = Parameter_Input.create("b1", self.controller)
        branch_b2 = Parameter_Input.create("b2", self.controller)
        foliage_b1 = Parameter_Input.create("b1", self.controller)
        foliage_b2 = Parameter_Input.create("b2", self.controller)
        crown_b1 = Parameter_Input.create("b1", self.controller)
        crown_b2 = Parameter_Input.create("b2", self.controller)
        stem_b1 = Parameter_Input.create("b1", self.controller)
        stem_b2 = Parameter_Input.create("b2", self.controller)
        total_b1 = Parameter_Input.create("b1", self.controller)
        total_b2 = Parameter_Input.create("b2", self.controller)

        # DBH+Height-based parameters (b1, b2, b3)
        wood_b3 = Parameter_Input.create("b3", self.controller)
        bark_b3 = Parameter_Input.create("b3", self.controller)
        branch_b3 = Parameter_Input.create("b3", self.controller)
        foliage_b3 = Parameter_Input.create("b3", self.controller)
        crown_b3 = Parameter_Input.create("b3", self.controller)
        stem_b3 = Parameter_Input.create("b3", self.controller)
        total_b3 = Parameter_Input.create("b3", self.controller)

        # Store references for dynamic visibility
        self.controller.set_param_controls({
            "DBH-based": {
                "Wood": [wood_b1, wood_b2],
                "Bark": [bark_b1, bark_b2],
                "Branch": [branch_b1, branch_b2],
                "Foliage": [foliage_b1, foliage_b2],
                "Crown": [crown_b1, crown_b2],
                "Stem": [stem_b1, stem_b2],
                "Total": [total_b1, total_b2]
            },
            "DBH + Height-based": {
                "Wood": [wood_b1, wood_b2, wood_b3],
                "Bark": [bark_b1, bark_b2, bark_b3],
                "Branch": [branch_b1, branch_b2, branch_b3],
                "Foliage": [foliage_b1, foliage_b2, foliage_b3],
                "Crown": [crown_b1, crown_b2, crown_b3],
                "Stem": [stem_b1, stem_b2, stem_b3],
                "Total": [total_b1, total_b2, total_b3]
            }
        })

        # Create header
        parameters_header = ft.Row([
            TitleTextWidget("Parameters"),
            ft.Icon(ft.Icons.SETTINGS)
        ], spacing=5)

        # Create "no parameters" message
        self.no_parameters = ft.Text("No Components selected.", visible=True)

        # Build sections list
        sections_list = [
            parameters_header,
            ft.Container(height=15),
            self.no_parameters,
            ft.Container(height=15),
        ]

        # Add component sections
        for component in ["Wood", "Bark", "Branch", "Foliage", 
                         "Crown", "Stem", "Total"]:
            section = self._create_component_section(
                component,
                locals()[f"{component.lower()}_b1"],
                locals()[f"{component.lower()}_b2"],
                locals().get(f"{component.lower()}_b3")
            )
            sections_list.append(section)
            sections_list.append(ft.Container(height=15))

        # Initially hide all component sections
        self._hide_all_sections()
        
        return ft.Column(controls=sections_list, spacing=5)
    
    def _hide_all_parameters(self):
        """Hide all parameter controls and labels."""
        param_controls = self.controller.get_param_controls()
        if param_controls:
            for equation_type in param_controls.values():
                for component_params in equation_type.values():
                    for param in component_params:
                        param.visible = False
        
        for label in self.param_labels.values():
            label.visible = False
    
    def _hide_all_sections(self):
        """Hide all component sections."""
        for section in self.sections.values():
            section.visible = False
    
    def update_visibility(self, selected_components, current_equation_type):
        """Update parameter visibility based on selected components and equation type."""
        
        equation_key = "DBH-based" if current_equation_type == "DBH-based" else "DBH + Height-based"
        
        # Hide all parameters and labels first
        self._hide_all_parameters()
        
        # Hide all sections first
        self._hide_all_sections()
        
        # Show selected components
        any_visible = False
        param_controls = self.controller.get_param_controls()
        
        for component in selected_components:
            if component in param_controls[equation_key]:
                # Show the entire component section
                if component in self.sections:
                    self.sections[component].visible = True
                
                # Show component label (redundant since section shows it, but keeping for backward compatibility)
                if component in self.param_labels:
                    self.param_labels[component].visible = True
                
                # Show parameters
                for param in param_controls[equation_key][component]:
                    param.visible = True
                    any_visible = True
        
        # Update "no parameters" text visibility
        if self.no_parameters:
            self.no_parameters.visible = not any_visible