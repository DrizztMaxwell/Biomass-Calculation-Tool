import flet as ft


class Parameter_Section:
    def __init__(self):
        self.COMPONENTS = ["Wood", "Bark", "Branch", "Foliage", "Crown", "Stem", "Total"]
        self.PARAM_NAMES = ["b1", "b2", "b3"]
        self.EQUATION_TYPES = ["DBH-based", "DBH + Height-based"]
        
        self.param_controls = {eq_type: {} for eq_type in self.EQUATION_TYPES}
        self.param_labels = {}
        self.component_sections = []
        
    def create_parameter_input(self, param_name):
        """Create a standardized parameter input field."""
        return ft.TextField(
            label=param_name,
            hint_text=f"Enter {param_name} value",
            width=120,
            border_color=ft.Colors.PRIMARY,
            on_change=self._on_parameter_change
        )
    
    def create_component_section(self, component_name):
        """Create a section for a single component with all its parameters."""
        # Create label
        label = ft.Text(
            component_name,
            size=14,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.ON_PRIMARY_CONTAINER,
            visible=False
        )
        self.param_labels[component_name] = label
        
        # Create parameter inputs
        params = {name: self.create_parameter_input(name) for name in self.PARAM_NAMES}
        
        # Set visibility to False initially
        for param in params.values():
            param.visible = False
        
        # Store in controls dictionary
        self.param_controls["DBH-based"][component_name] = [params["b1"], params["b2"]]
        self.param_controls["DBH + Height-based"][component_name] = [params["b1"], params["b2"], params["b3"]]
        
        # Create the section layout
        return ft.Column([
            label,
            ft.Row([
                ft.Container(content=params[param], expand=True)
                for param in self.PARAM_NAMES
            ], spacing=20)
        ], spacing=10)
    
    def build(self):
        """Build the complete parameters section."""
        # Create header
        header = ft.Row([
            ft.Text("Parameters", size=16, weight=ft.FontWeight.BOLD),
            ft.Icon(ft.Icons.SETTINGS)
        ], spacing=5)
        
        # Create component sections
        self.component_sections = [
            self.create_component_section(component)
            for component in self.COMPONENTS
        ]
        
        # Create empty state message
        self.empty_message = ft.Text(
            "No components selected. Select components to see parameters.",
            italic=True,
            color=ft.Colors.GREY_600
        )
        
        # Return the complete section
        return ft.Column([
            header,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            self.empty_message,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            *self.component_sections
        ], spacing=15)
    
    def update_visibility(self, selected_components, equation_type):
        """Update which parameters are visible based on selection."""
        # Hide all first
        for label in self.param_labels.values():
            label.visible = False
        
        for eq_type in self.param_controls.values():
            for component_params in eq_type.values():
                for param in component_params:
                    param.visible = False
        
        # Show selected components
        if selected_components:
            self.empty_message.visible = False
            for component in selected_components:
                if component in self.param_labels:
                    # Show component label
                    self.param_labels[component].visible = True
                    
                    # Show appropriate parameters based on equation type
                    if component in self.param_controls.get(equation_type, {}):
                        params = self.param_controls[equation_type][component]
                        for param in params:
                            param.visible = True
        else:
            self.empty_message.visible = True
    
    def get_parameter_values(self, component, equation_type):
        """Get parameter values for a specific component."""
        if component in self.param_controls.get(equation_type, {}):
            params = self.param_controls[equation_type][component]
            return {
                f"b{i+1}": param.value
                for i, param in enumerate(params)
                if param.visible
            }
        return {}
    
    def _on_parameter_change(self, e):
        """Handle parameter value changes."""
        # You could add validation or update calculations here
        pass