import json
import pandas as pd
from data.components_data_2 import COMPONENTS_DATA_2
from widgets.LogFileTxt import logger
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog

import flet as ft

class Create_Species_Controller:
    """Controller for Create Species functionality."""
    
    def __init__(self, page, view):
        self.page = page
        self.view = view
        self.selected_components = []
        self.current_equation_type = "DBH-based"
        self.error_messages = []
        
        # Initialize component data
        self.component_data = COMPONENTS_DATA_2.copy()
        
    def handle_equation_type_change(self, e):
        """Handle equation type change and update parameters visibility."""
        self.current_equation_type = e.control.value
        self.view.update_parameters_visibility(self.selected_components, self.current_equation_type)
    
    def get_component_data(self):
        """Get component data."""
        return self.component_data
    
    def update_component_selection(self, component_title, is_selected):
        """Update component selection state."""
        for component in self.component_data:
            if component["title"] == component_title:
                component["is_selected"] = is_selected
                break
        
        # Update selected components list
        if is_selected:
            if component_title not in self.selected_components:
                self.selected_components.append(component_title)
        else:
            if component_title in self.selected_components:
                self.selected_components.remove(component_title)
    
    def on_component_selection_change(self, selected_components):
        """Callback function when component selection changes."""
        self.selected_components = selected_components
        self.view.update_parameters_visibility(selected_components, self.current_equation_type)
    
    def show_confirmation_dialog(self, e, page: ft.Page):
        """Show confirmation dialog with preview of selected items."""
        print("Create Species button clicked!")
        
        # Get selected components
        selected_components = self.selected_components
        
        # Get equation type
        equation_type = self.current_equation_type
        
        # Get parameter values
        param_values = {}
        
        param_controls = self.view.get_parameter_controls()
        if equation_type in param_controls:
            components = param_controls[equation_type]
            for component_name, controls_list in components.items():
                for control in controls_list:
                    if control.visible:
                        param_key = f"{equation_type}_{component_name}_{control.label}"
                        param_values[param_key] = control.value
                        print(f"Parameter {param_key}: {control.value}")
        
        if not self._is_form_valid():
            print("Form is not valid, cannot show preview modal.")
            return
            
        # Update preview modal with species data
        preview_modal = self.view.get_preview_modal()
        preview_modal.species_data = {
            "species_code": self.view.get_species_textfield().value,
            "origin": self.view.get_origin_dropdown().value,
            "equation_type": equation_type,
            "selected_components": selected_components,
            "parameters": param_values
        }
        preview_modal.show()
    
    def handle_create_species_button_click(self, e):
        """Handle Create Species button click."""
        species_textfield = self.view.get_species_textfield()
        
        # Validate form
        if not self._is_form_valid():
            print("Form is not valid, cannot create species.")
            return
        
        
        does_species_code_exist_in_tree_parameters = self._does_species_code_exist_within_dataset(
            species_textfield.value, "data/treeparameters.json"
        )
        if does_species_code_exist_in_tree_parameters:
            logger.write(f"Species code {species_textfield.value} already exists in treeparameters.json")
            Custom_Alert_Dialog(
                self.page, 
                title_icon=ft.Icons.ERROR_OUTLINE, 
                title_color=ft.Colors.RED_700, 
                title_icon_color=ft.Colors.RED, 
                title="Error", 
                message="Species Code already exists in the Lamberts et al. (2005) dataset.", 
                solution="Please use a different code."
            ).show()
            return
        
        does_species_code_exist_in_created_species = self._does_species_code_exist_within_dataset(
            species_textfield.value, "data/create_species.json"
        )
        if does_species_code_exist_in_created_species:
            logger.write(f"Species code {species_textfield.value} already exists in create_species.json")
            Custom_Alert_Dialog(
                self.page, 
                title_icon=ft.Icons.ERROR_OUTLINE, 
                title_color=ft.Colors.RED_700, 
                title_icon_color=ft.Colors.RED, 
                title="Error", 
                message="User has already created a species with this code.", 
                solution="Please use a different code."
            ).show()
            return
        
        # If everything checks out then proceed
        self._proceed_with_creation(e)
    
    def _does_species_code_exist_within_dataset(self, species_name_or_code, json_file_path: str) -> bool:
        """Check if the species code already exists in the given JSON dataset."""
        try:
            data_set = pd.read_json(json_file_path)
            # try to convert species_code to int
            if species_name_or_code.isdigit():
                species_name_or_code = int(species_name_or_code)
                if 'SpeciesCode' in data_set.columns:
                    logger.write(f"Checking if species code {species_name_or_code} exists in {json_file_path}")
                    return species_name_or_code in data_set['SpeciesCode'].values
            else:
                species_name_or_code = str(species_name_or_code)
                if 'SpecCommon' in data_set.columns:
                    logger.write(f"Checking if species name {species_name_or_code} exists in {json_file_path}")
                    # lowercase comparison
                    return species_name_or_code.lower() in data_set['SpecCommon'].str.lower().values
            return False
          
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            logger.write(f"Error reading JSON file {json_file_path}: {e}")  
            return False
    
    def _proceed_with_creation(self, e):
        """Proceed with species creation."""
        species_textfield = self.view.get_species_textfield()
        origin_dropdown = self.view.get_origin_dropdown()
        
        logger.write(f"Selected components for creation: {self.selected_components}")
        
        if self.current_equation_type == "DBH-based":
            logger.write("Current equation type is DBH-based")
            data_to_be_inserted_into_json = self._collect_parameter_data(self.selected_components)
        else:
            data_to_be_inserted_into_json = self._collect_parameter_data(self.selected_components)
            print("Data to be inserted into JSON:")
            print(data_to_be_inserted_into_json)
            
        # Insert the data into the JSON file
        created_species_json = json.loads(open("data/create_species.json").read())
        
        if species_textfield.value.isdigit():
            created_species_json.append({
                "SpeciesCode": int(species_textfield.value),
                **data_to_be_inserted_into_json
            })
        else:
            created_species_json.append({
                "SpecCommon": species_textfield.value,
                **data_to_be_inserted_into_json
            })
            
        with open("data/create_species.json", "w") as f:
            json.dump(created_species_json, f, indent=4)
            print("Species data inserted into JSON file successfully.")
            
            Custom_Alert_Dialog(
                self.page, 
                title_icon=ft.Icons.CHECK_CIRCLE_OUTLINED, 
                title_color=ft.Colors.GREEN_700, 
                title_icon_color=ft.Colors.GREEN, 
                title="Success",  
                message="Species created successfully!"
            ).show()
            logger.write(f"Species {species_textfield.value} created successfully and added to create_species.json")
    
    def _get_equation_prefix(self, equation_type):
        """Get equation prefix based on equation type."""
        return "bh" if equation_type == "DBH + Height-based" else "b"
    
    def _collect_parameter_data(self, components):
        """Collect parameter data for selected components and equation type."""
        prefix = self._get_equation_prefix(self.current_equation_type)
        is_bh_equation = (prefix == "bh")
        param_count = 3 if is_bh_equation else 2
        
        print(components)
        print("Collecting parameter data...")
        
        # Build the data dictionary
        data = {
            "Origin": self.view.get_origin_dropdown().value,
            "EquationType": self.current_equation_type,
            **self._collect_component_params(components, prefix, param_count)
        }
        
        return data
    
    def _collect_component_params(self, components, prefix, param_count):
        """Helper method to collect component parameters."""
        component_params = {}
        param_labels = [f"b{i+1}" for i in range(param_count)]
        
        param_controls = self.view.get_parameter_controls()
        for component in components:
            params = param_controls.get(self.current_equation_type, {}).get(component, [])
            
            for idx, param in enumerate(params[:param_count]):
                label = param_labels[idx]
                component_key = "branches" if component.lower() == "branch" else component.lower()
                json_key = f"{prefix}{component_key}{label}"
                component_params[json_key] = float(param.value)
        
        return component_params
    
    def _is_form_valid(self):
        """Validate the form."""
        species_textfield = self.view.get_species_textfield()
        
        # Clear previous errors
        self.error_messages = []
        
        # Validate species code
        if not species_textfield.value.strip():
            self.error_messages.append("Species code/name is required")
            species_textfield.error_text = "Required"
        else:
            species_textfield.error_text = None
        
        # Validate at least one component selected
        if not self.selected_components:
            Custom_Alert_Dialog(
                self.page, 
                title_icon=ft.Icons.ERROR_OUTLINE, 
                title_color=ft.Colors.RED_700, 
                title_icon_color=ft.Colors.RED, 
                title="Error", 
                message="At least one component must be selected.", 
                solution="Please select at least one component."
            ).show()
            return False
        
        # Validate parameter values
        param_controls = self.view.get_parameter_controls()
        for component in self.selected_components:
            params = param_controls.get(self.current_equation_type, {}).get(component, [])
            for param in params:
                if param.visible:
                    try:
                        value = float(param.value)
                        print(f"Validating parameter {param.label} with value {value}")
                        if value < -5.0 or value > 5.0:
                            
                            Custom_Alert_Dialog(
                                self.page, 
                                title_icon=ft.Icons.ERROR_OUTLINE, 
                                title_color=ft.Colors.RED_700, 
                                title_icon_color=ft.Colors.RED, 
                                title="Error", 
                                message=f"{component} parameter {param.label} must be between -5.0 and 5.0.", 
                                solution="Please enter a valid number within the range -5.0 to 5.0."
                            ).show()
                            return False
                       
                    except ValueError:
                        param.error_text = "Must be a number"
                        Custom_Alert_Dialog(
                            self.page, 
                            title_icon=ft.Icons.ERROR_OUTLINE, 
                            title_color=ft.Colors.RED_700, 
                            title_icon_color=ft.Colors.RED, 
                            title="Error", 
                            message=f"{component} parameter {param.label} must be a valid number.", 
                            solution="Please enter a valid number."
                        ).show()
                        return False
        
        
        return True