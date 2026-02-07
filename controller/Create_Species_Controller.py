import json
import pandas as pd
from data.components_data_2 import COMPONENTS_DATA_2
from widgets.LogFileTxt import logger
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog

import flet as ft

class Create_Species_Controller:
    """Controller for Create Species functionality."""
    
    def __init__(self, ):
     
        # self.view = view
        self.__selected_components = []
        self.current_equation_type = "DBH-based"
        self.error_messages = []
        self.__origin_type = "Natural Stand"
        self.__species_code_or_name = ""
        self.__params_controls = {}
        # Initialize component data
        self.component_data = COMPONENTS_DATA_2.copy()
    
    def set_species_code_or_name(self, species_code_or_name):
        """Set species code or name."""
        self.__species_code_or_name = species_code_or_name
    
    def set_param_controls(self, param_controls, ):
        """Set parameter controls."""
        self.__params_controls = param_controls
    
    def get_param_controls(self):
        """Get parameter controls."""
        return self.__params_controls
    
    def get_species_code_or_name(self):
        """Get species code or name."""
        return self.__species_code_or_name
    
    def set_origin_type(self, origin_type):
        """Set origin type."""
        self.__origin_type = origin_type
    def get_origin_type(self):
        """Get origin type."""
        return self.__origin_type
    
    def get_selected_components(self):
        """Get currently selected components."""
        return self.__selected_components
    
    def set_selected_components(self, selected_components):
        """Set selected components."""
        self.__selected_components = selected_components
    
    def get_current_equation_type(self):
        """Get current equation type."""
        return self.current_equation_type
    def set_current_equation_type(self, equation_type):
        """Set current equation type."""
        self.current_equation_type = equation_type
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
            if component_title not in self.__selected_components:
                self.__selected_components.append(component_title)
        else:
            if component_title in self.__selected_components:
                self.__selected_components.remove(component_title)
    
    def on_component_selection_change(self, __selected_components):
        """Callback function when component selection changes."""
        self.__selected_components = __selected_components
        self.view.update_parameters_visibility(__selected_components, self.current_equation_type)
    
    # def show_confirmation_dialog(self, e, page: ft.Page):
    #     """Show confirmation dialog with preview of selected items."""
    #     print("Create Species button clicked!")
        
    #     # Get selected components
    #     __selected_components = self.__selected_components
        
    #     # Get equation type
    #     equation_type = self.current_equation_type
        
    #     # Get parameter values
    #     param_values = {}
        
    #     param_controls = self.view.get_parameter_controls()
    #     if equation_type in param_controls:
    #         components = param_controls[equation_type]
    #         for component_name, controls_list in components.items():
    #             for control in controls_list:
    #                 if control.visible:
    #                     param_key = f"{equation_type}_{component_name}_{control.label}"
    #                     param_values[param_key] = control.value
    #                     print(f"Parameter {param_key}: {control.value}")
        
    #     if not self._is_form_valid():
    #         print("Form is not valid, cannot show preview modal.")
    #         return
            
    #     # Update preview modal with species data
    #     preview_modal = self.view.get_preview_modal()
    #     preview_modal.species_data = {
    #         "species_code": self.view.get_species_textfield().value,
    #         "origin": self.view.get_origin_dropdown().value,
    #         "equation_type": equation_type,
    #         "__selected_components": __selected_components,
    #         "parameters": param_values
    #     }
    #     preview_modal.show()
    
    def handle_create_species_button_click(self) -> bool:
        """Handle Create Species button click."""
     
        print("Create Species button clicked!")
        # Validate form
        if not self._is_form_valid():
            
            print("Form is not valid, cannot create species.")
            logger.write("Form is not valid, cannot create species.")
            raise ValueError("Form is not valid, cannot create species.")
        print("Form is valid, proceeding with species creation.")
        # Check if species code already exists in datasets
        if self._does_species_code_exist_within_dataset(self.get_species_code_or_name(), "data/treeparameters.json"):
            logger.write(f"Species code or name '{self.get_species_code_or_name()}' already exists in treeparameters.json")
            raise ValueError(f"Species code or name '{self.get_species_code_or_name()}' already exists in the Lamberts et al. (2005) dataset. Please use a different code or name.")
        print("Species code or name does not exist in treeparameters.json, checking create_species.json...")
        if self._does_species_code_exist_within_dataset(self.get_species_code_or_name(), "data/create_species.json"):
            logger.write(f"Species code or name '{self.get_species_code_or_name()}' already exists in create_species.json")
            raise ValueError(f"Species code or name '{self.get_species_code_or_name()}' already exists in create_species.json. Please use a different code or name.")
        print("Species code or name does not exist in create_species.json, proceeding with creation...")
        
        return True
        
        # if not self._proceed_with_creation():
        #     raise ValueError("Failed to create species due to an unknown error.")
        print("Species created successfully.")
        # success
    
        
        # does_species_code_exist_in_tree_parameters = self._does_species_code_exist_within_dataset(
        #     self.get_species_code_or_name(), "data/treeparameters.json"
        # )
        # if does_species_code_exist_in_tree_parameters:
        #     logger.write(f"Species code {self.get_species_code_or_name()} already exists in treeparameters.json")
        #     # Custom_Alert_Dialog(
        #     #     self.page, 
        #     #     title_icon=ft.Icons.ERROR_OUTLINE, 
        #     #     title_color=ft.Colors.RED_700, 
        #     #     title_icon_color=ft.Colors.RED, 
        #     #     title="Error", 
        #     #     message="Species Code already exists in the Lamberts et al. (2005) dataset.", 
        #     #     solution="Please use a different code."
        #     # ).show()
        #     return
        
        # does_species_code_exist_in_created_species = self._does_species_code_exist_within_dataset(
        #      self.get_species_code_or_name(), "data/create_species.json"
        # )
        # if does_species_code_exist_in_created_species:
        #     # logger.write(f"Species code {species_textfield.value} already exists in create_species.json")
        #     # Custom_Alert_Dialog(
        #     #     self.page, 
        #     #     title_icon=ft.Icons.ERROR_OUTLINE, 
        #     #     title_color=ft.Colors.RED_700, 
        #     #     title_icon_color=ft.Colors.RED, 
        #     #     title="Error", 
        #     #     message="User has already created a species with this code.", 
        #     #     solution="Please use a different code."
        #     # ).show()
        #     return
        
        # # If everything checks out then proceed
        # self._proceed_with_creation(e)
    
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
    
    def _proceed_with_creation(self):
        """Proceed with species creation."""
        
        logger.write(f"Selected components for creation: {self.get_selected_components()}")
        
        if self.get_current_equation_type() == "DBH-based":
            logger.write("Current equation type is DBH-based")
            data_to_be_inserted_into_json = self._collect_parameter_data(self.get_selected_components())
        else:
            data_to_be_inserted_into_json = self._collect_parameter_data(self.get_selected_components())
            print("Data to be inserted into JSON:")
            
            print(data_to_be_inserted_into_json)
            
        # Insert the data into the JSON file
        created_species_json = json.loads(open("data/create_species.json").read())
        
        if self.get_species_code_or_name().isdigit():
            created_species_json.append({
                "SpeciesCode": int(self.get_species_code_or_name()),
                **data_to_be_inserted_into_json
            })
        else:
            created_species_json.append({
                "SpecCommon": self.get_species_code_or_name(),
                **data_to_be_inserted_into_json
            })
            
        with open("data/create_species.json", "w") as f:
            json.dump(created_species_json, f, indent=4)
            print("Species data inserted into JSON file successfully.")
            
            logger.write(f"Species {self.get_species_code_or_name()} created successfully and added to create_species.json")
            return True
        return False
    def _get_equation_prefix(self, equation_type):
        """Get equation prefix based on equation type."""
        return "bh" if equation_type == "DBH + Height-based" else "b"
    
    def _collect_parameter_data(self, components):
        """Collect parameter data for selected components and equation type."""
        prefix = self._get_equation_prefix(self.get_current_equation_type())
        is_bh_equation = (prefix == "bh")
        param_count = 3 if is_bh_equation else 2
        
        print(components)
        print("Collecting parameter data...")
        
        # Build the data dictionary
        data = {
            "Origin": self.view.get_origin_dropdown().value,
            "EquationType": self.get_current_equation_type(),
            **self._collect_component_params(components, prefix, param_count)
        }
        
        return data
    
    def _collect_component_params(self, components, prefix, param_count):
        """Helper method to collect component parameters."""
        component_params = {}
        param_labels = [f"b{i+1}" for i in range(param_count)]
        
        param_controls = self.get_param_controls()
        for component in components:
            params = param_controls.get(self.get_current_equation_type(), {}).get(component, [])
            
            for idx, param in enumerate(params[:param_count]):
                label = param_labels[idx]
                component_key = "branches" if component.lower() == "branch" else component.lower()
                json_key = f"{prefix}{component_key}{label}"
                component_params[json_key] = float(param.value)
        
        return component_params
    
    def _check_if_species_code_is_an_integer(self, value):
        try:
            
            int_value = int(value)
           
            print(f"Successfully parsed as integer: {int_value}")

            # Validate integer range for species code
            if int_value < 0:
                raise ValueError(f"Species Code must be non-negative. Got: {int_value}")
            if int_value > 99999999:  # 99,999,999 maximum
                raise ValueError(f"Species Code exceeds maximum allowed value of 99,999,999. Got: {int_value}")

            # Valid numeric species code
            print(f"Valid numeric species code: {int_value}")
            return int_value
        except ValueError as e:
            raise e
    
    def _validate_species_code_or_name_value(self, value):
        """Validate the species code or name value.
        
        Species Code can be:
        1. Numeric: Positive integer (0 to 99,999,999)
        2. Alphanumeric: Mixed letters and numbers (2-50 chars)
        
        Species Name: Letters only or with basic punctuation (2-50 chars)
        """
        if value is None:
            raise ValueError("Species Code/Name cannot be None.")
        
        print(f"Validating species code/name value: '{value}'")
        
        str_value = str(value).strip()
        
        if not str_value:
            raise ValueError("Species Code/Name cannot be empty or contain only whitespace.")
        
        # Check length first (applies to all types)
        if len(str_value) < 1:
            raise ValueError("Species Code/Name must be at least 1 character long.")
        
        if len(str_value) > 50:
            raise ValueError("Species Code/Name exceeds maximum length of 50 characters.")
        if str_value.isdigit() or (str_value.startswith("-") and str_value[1:].isdigit()):
            print(f"Numeric species code detected: '{str_value}'")
            # Purely numeric, try to parse as integer
            return self._check_if_species_code_is_an_integer(str_value)
        if str_value.isalpha():
            # Purely alphabetic, treat as species name
            print(f"Species name detected: '{str_value}'")
            
            # Check for invalid characters in species names
            # Allow letters, spaces, hyphens, apostrophes, periods, parentheses
            allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMONPQRSTUVWXYZ0123456789 -'._(),")
            invalid_chars = [c for c in str_value if c not in allowed_chars]
            
            if invalid_chars:
                raise ValueError(
                    f"Species Name contains invalid characters: {', '.join(repr(c) for c in invalid_chars)}. "
                    f"Only letters, numbers, spaces, hyphens, apostrophes, periods, parentheses and commas are allowed."
                )
            
            # Check for excessive whitespace
            if "  " in str_value:  # Multiple consecutive spaces
                raise ValueError("Species Name contains multiple consecutive spaces.")
            
            # Valid species name
            return str_value
        
        
       
    def _is_form_valid(self):
        """Validate the form."""
 
        # Clear previous errors
        self.error_messages = []
        try:
            self._validate_species_code_or_name_value(self.get_species_code_or_name())
            if self.get_selected_components() == []:
                raise ValueError("At least one component must be selected.")
            if self.get_origin_type() == "":
                raise ValueError("Origin must be selected.")
            if self.get_current_equation_type() == "":
                raise ValueError("Equation type must be selected.")
            # validate parameter values
            self.validate_parameter_values()
            
        except ValueError as e:
            raise e
            
        # # Validate species code
        # if not self.get_species_code_or_name().strip():
        #     raise ValueError("Species Code/Name cannot be empty.")
        #     return False
        # # Validate at least one component selected
        # if not self.__selected_components:
        #     return False
            # Custom_Alert_Dialog(
            #     self.page, 
            #     title_icon=ft.Icons.ERROR_OUTLINE, 
            #     title_color=ft.Colors.RED_700, 
            #     title_icon_color=ft.Colors.RED, 
            # #     title="Error", 
            #     message="At least one component must be selected.", 
            #     solution="Please select at least one component."
           # ).show()
            # return False
        
        # Validate parameter values
        # param_controls = self.view.get_parameter_controls()
        # for component in self.__selected_components:
        #     params = param_controls.get(self.current_equation_type, {}).get(component, [])
        #     for param in params:
        #         if param.visible:
        #             try:
        #                 value = float(param.value)
        #                 print(f"Validating parameter {param.label} with value {value}")
        #                 if value < -5.0 or value > 5.0:
                            
        #                     # Custom_Alert_Dialog(
        #                     #     self.page, 
        #                     #     title_icon=ft.Icons.ERROR_OUTLINE, 
        #                     #     title_color=ft.Colors.RED_700, 
        #                     #     title_icon_color=ft.Colors.RED, 
        #                     #     title="Error", 
        #                     #     message=f"{component} parameter {param.label} must be between -5.0 and 5.0.", 
        #                     #     solution="Please enter a valid number within the range -5.0 to 5.0."
        #                     # ).show()
        #                     return False
                       
        #             except ValueError:
        #                 param.error_text = "Must be a number"
        #                 # Custom_Alert_Dialog(
        #                 #     self.page, 
        #                 #     title_icon=ft.Icons.ERROR_OUTLINE, 
        #                 #     title_color=ft.Colors.RED_700, 
        #                 #     title_icon_color=ft.Colors.RED, 
        #                 #     title="Error", 
        #                 #     message=f"{component} parameter {param.label} must be a valid number.", 
        #                 #     solution="Please enter a valid number."
        #                 # ).show()
        #                 return False
        
        
        return True

    def validate_parameter_values(self):
        param_controls = self.get_param_controls()
        print("Parameter controls for validation:")
        # print(param_controls)

        for component in self.get_selected_components():
            params = param_controls.get(self.current_equation_type, {}).get(component, [])
            for param in params:
                if param.visible:
                        # Get the raw value
                    raw_value = param.value
                        
                        # Check if empty
                    if raw_value is None or str(raw_value).strip() == "":
                        raise ValueError(f"{component} parameter {param.label} cannot be empty.")
                        
                        # Check if it contains letters (which would make float conversion fail)
                    value_str = str(raw_value).strip()
                        
                        # Check if it's purely alphabetic (letters only, no numbers)
                    if value_str.isalpha():
                        raise ValueError(f"{component} parameter {param.label} must be a number, not text.")
                        
                        # Check if it's alphanumeric (contains both letters and numbers)
                        # This is tricky because "123" is also alphanumeric!
                        # Better to check if it contains any letters when we want only numbers
                    has_letters = any(c.isalpha() for c in value_str)
                    has_digits = any(c.isdigit() for c in value_str)
                        
                    if has_letters and has_digits:
                        raise ValueError(f"{component} parameter {param.label} must be a number only, not a mix of letters and numbers.")
                        
                    try:
                            # Try to convert to float
                        value = float(value_str)
                        print(f"Validating parameter {param.label} with value {value}")
                            
                            # Check range
                        if value < -5.0 or value > 5.0:
                            raise ValueError(f"{component} parameter {param.label} must be between -5.0 and 5.0.")
                                
                    except ValueError:
                            # float() conversion failed
                            # Provide a helpful error message
                        if has_letters:
                            raise ValueError(f"{component} parameter {param.label} must be a number, not text.")
                        else:
                                # Might be something like "1.2.3" or "1,2" or other invalid number format
                            raise ValueError(f"{component} parameter {param.label} must be a valid number between -5.0 and 5.0. Got: '{value_str}'")