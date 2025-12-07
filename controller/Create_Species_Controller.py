from typing import TYPE_CHECKING
import flet as ft
from data.components_data import COMPONENTS_DATA
if TYPE_CHECKING:
    from views.Create_Species_View import Create_Species_View


class Create_Species_Controller:
    """Controller for the Create Species View."""
    
    def __init__(self, view:Create_Species_View=None):
        self.view = view
        self.SPECIES_CODE_LOWER_CHARACTER_LIMIT = 1
        self.SPECIES_CODE_UPPER_CHARACTER_LIMIT = 30
        self.PARAMETER_VALUE_LOWER_LIMIT = -5.0
        self.PARAMETER_VALUE_UPPER_LIMIT = 5.0
        self.species_textfield_value = ""
   
    def build(self):
        """Initializes the model."""
        return self.view.build()
       
    def is_species_code_valid(self) -> bool:
        """Validates the species code input."""
        self.species_textfield_value = self.view.species_textfield.value.strip()
        if self.species_textfield_value == "":
            return False
        try:
            species_code_value = self.species_textfield_value
            species_code_value = int(species_code_value)
            self.species_textfield_value = species_code_value
            return len(str(species_code_value)) >= self.SPECIES_CODE_LOWER_CHARACTER_LIMIT and len(str(species_code_value)) <= self.SPECIES_CODE_UPPER_CHARACTER_LIMIT
        except:
            # Not a valid integer, mening its probably speccommon a.k.a species name
            print("Validating as species name its A STRING")
            species_name_value = str(self.species_textfield_value.strip())
            self.species_textfield_value = species_name_value
            return len(species_name_value) >= self.SPECIES_CODE_LOWER_CHARACTER_LIMIT and len(species_name_value) <= self.SPECIES_CODE_UPPER_CHARACTER_LIMIT
   
    
    def _is_at_least_one_component_selected(self) -> bool:
        """Checks if at least one component is selected."""
        selected_components = self.view._get_current_selected_components()
        return len(selected_components) > 0
    
    def _is_form_valid(self) -> bool:
        """Checks if all required fields are valid."""
    
        # Validate species code
        if not self.is_species_code_valid():
            self._update_species_code_error_text_message()
            return False
        self._update_species_code_error_text_message()
        
        # Checking to see if species code already exists in both created_species.json and tree_params.json
        
        
        # Validate at least one component is selected
        if not self._is_at_least_one_component_selected():
            self._show_component_selection_error()
            return False
        
        # Validate parameter fields
        if not self._is_parameter_fields_valid():
            return False
        
        is_valid = self.is_species_code_valid() and self._is_at_least_one_component_selected() and self._is_parameter_fields_valid()
        return is_valid
    
    def _show_component_selection_error(self):
        """Display error message for component selection."""
        from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
        Custom_Alert_Dialog(
            self.view.page,
            title_icon=ft.Icons.ERROR_OUTLINE,
            title_color=ft.Colors.RED_700,
            title_icon_color=ft.Colors.RED,
            title="Selection Required",
            message="Please select at least one tree component.",
            solution="Choose one or more components (Wood, Bark, Branch, etc.) to continue."
        ).show()
        
    def _is_parameter_fields_valid(self) -> bool:
        """Checks if all parameter fields are valid."""
        all_valid = True
        
        for equation_type, components in self.view.param_controls.items():
            for component_name, controls_list in components.items():
                for control in controls_list:
                    # Check if control is visible and validate value range
                    if hasattr(control, 'visible') and control.visible:
                        try:
                            value = float(control.value)
                            print(f"Validating parameter '{control.label}' with value: {value}")
                            if value < self.PARAMETER_VALUE_LOWER_LIMIT or value > self.PARAMETER_VALUE_UPPER_LIMIT:
                                print(f"Value {value} is out of range.")
                                control.error_text = f"Value must be between {self.PARAMETER_VALUE_LOWER_LIMIT} and {self.PARAMETER_VALUE_UPPER_LIMIT}"
                                control.update()
                                all_valid = False
                            else:
                                # Clear error text if value is valid
                                print("Clearing error text")
                                control.error_text = None
                                control.update()
                        except (ValueError, TypeError):
                            control.error_text = "Invalid number"
                            control.update()
                            all_valid = False
        
        return all_valid
    
    def _update_species_code_error_text_message(self):
        if not self.is_species_code_valid():
            self.view.species_textfield.error_text = f"It must be a number or a name ({self.SPECIES_CODE_LOWER_CHARACTER_LIMIT}-{self.SPECIES_CODE_UPPER_CHARACTER_LIMIT} characters)."
            
            self.view.species_textfield.update()
        else:
            self.view.species_textfield.error_text = None
            self.view.species_textfield.update()