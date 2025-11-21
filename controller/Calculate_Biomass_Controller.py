import pandas as pd
from model.Calculate_Biomass_Model import Calculate_Biomass_Model


class Calculate_Biomass_Controller:
    """Controller for calculating tree biomass based on selected components and equation types."""
    
    def __init__(self, model: Calculate_Biomass_Model, view):
        self.model = model
        self.view = view
        self.equation_type = "DBH-based"
        self.selected_components = []

    def set_equation_type(self, equation_type: str) -> None:
        """Set the equation type for biomass calculations."""
        self.equation_type = equation_type
        print(f"Selected Equation Type: {equation_type}")

    def get_equation_type(self) -> str:
        """Get the currently selected equation type."""
        return self.equation_type
    
    def build(self):
        """Build the main view."""
        return self.view.build()

    def calculate_biomass(self) -> None:
        """Calculate biomass based on selected parameters and equation type."""
        print("Calculate Biomass button clicked.")
        self.selected_components = self.view.get_selected_components()
        self.equation_type = self.get_equation_type()
        print(f"Selected Components: {self.selected_components}")
        print(f"Equation Type: {self.equation_type}")

        try:
            local_storage_data = pd.read_json("storage/localstorage.json")
            tree_params_data = pd.read_json("data/treeparameters.json")
            
            self._lower_column_names(local_storage_data, tree_params_data)
            self._process_biomass_calculations(local_storage_data, tree_params_data)
            self._save_results(local_storage_data)
            
        except Exception as e:
            print(f"Error calculating biomass: {e}")
            # self.view.show_error_dialog(str(e))  # Uncomment for user error display

    def _lower_column_names(self, *dataframes) -> None:
        """Convert all column names to lowercase for consistency."""
        for df in dataframes:
            df.columns = [col.lower() for col in df.columns]

    def _process_biomass_calculations(self, local_data: pd.DataFrame, tree_params: pd.DataFrame) -> None:
        """Calculate biomass for each row in the dataset."""
        for index, row in local_data.iterrows():
            raw_species_code = row.get('speccode')
            species_code = None

            try:
                # 1. Attempt to convert to integer
                # We first check if the value is NaN or None, and handle it if possible.
                if pd.isna(raw_species_code):
                    # Treat NaN/None as a signal to skip
                    species_code = None 
                else:
                    # Attempt conversion. This handles both strings ('123') and floats (123.0)
                    species_code = int(raw_species_code)

            except (ValueError, TypeError) as e:
                # If conversion fails (e.g., 'ABC', or complex types), set code to None
                print(f"Skipping row {index}: 'speccode' value '{raw_species_code}' could not be converted to integer. Error: {e}")
                species_code = None
                
            # 2. Check if the code is valid (None means skip)
            if species_code is None or species_code == 0:
                continue  # Skip rows without a valid species code (None or 0)
            
            # 3. Proceed with calculation if species_code is valid
            species_params = self._get_species_parameters(tree_params, float(species_code))
            print(species_params)
            if species_params:
                self._calculate_row_biomass(local_data, index, row, species_params)

    def _get_species_parameters(self, tree_params: pd.DataFrame, species_code: str) -> dict:
        """Retrieve parameters for a specific species code."""
        matching_row = tree_params[tree_params['speciescode'] == species_code]
        return matching_row.iloc[0].to_dict() if not matching_row.empty else None

    def _calculate_row_biomass(self, data: pd.DataFrame, index: int, row: pd.Series, species_params: dict) -> None:
        """Calculate biomass for a single row based on equation type."""
        if self.equation_type == "DBH-based":
            self._calculate_dbh_based_biomass(data, index, row, species_params)
        if self.equation_type == "DBH + Height-based":
            self._calculate_dbh_height_based_biomass(data, index, row, species_params)
        # Add other equation types here when implemented
    def _calculate_dbh_height_based_biomass(self, data: pd.DataFrame, index: int, row: pd.Series, species_params: dict) -> None:
        """
        Calculate DBH + Height-based biomass for all selected components. 
        Skips the row if DBH or Height are missing (0) or cannot be converted to a number.
        """
        
        # 1. Safely retrieve raw values, defaulting to 0 or None if key is missing
        raw_dbh = row.get('dbh')
        raw_height = row.get('height')

        # 2. Attempt safe conversion to float (and handle missing/zero values)
        try:
            # Check if the values are truthy (not None, not empty string) and convert
            dbh = float(raw_dbh) if raw_dbh is not None and str(raw_dbh).strip() != '' else 0.0
            height = float(raw_height) if raw_height is not None and str(raw_height).strip() != '' else 0.0
            
        except (ValueError, TypeError):
            # If conversion fails (e.g., 'N/A' or 'Invalid'), skip the row
            print(f"Skipping row {index}: DBH ('{raw_dbh}') or Height ('{raw_height}') could not be converted to a number.")
            return
        
        # 3. Check for zero values after successful conversion
        if dbh == 0.0 or height == 0.0:
            print(f"Skipping row {index}: DBH ({dbh}) or Height ({height}) is zero.")
            return

        # --- Parameters are safely converted to float here ---
        
        wood_parameter_1 = float(species_params.get("bhwood1", 0))
        wood_parameter_2 = float(species_params.get("bhwood2", 0))
        wood_parameter_3 = float(species_params.get("bhwood3", 0))

        branch_parameter_1 = float(species_params.get("bhbranches1", 0))
        branch_parameter_2 = float(species_params.get("bhbranches2", 0))
        branch_parameter_3 = float(species_params.get("bhbranches3", 0))

        bark_parameter_1 = float(species_params.get("bhbark1", 0))
        bark_parameter_2 = float(species_params.get("bhbark2", 0))
        bark_parameter_3 = float(species_params.get("bhbark3", 0))

        foliage_parameter_1 = float(species_params.get("bhfoliage1", 0))
        foliage_parameter_2 = float(species_params.get("bhfoliage2", 0))
        foliage_parameter_3 = float(species_params.get("bhfoliage3", 0))
        
        
        # --- Calculation Initialization (Kept for completeness, though print statements removed) ---
        
        wood_biomass = bark_biomass = branches_biomass = stem_biomass = crown_biomass = total_biomass = foliage_biomass = 0 
        
        # --- Biomass Calculation Logic (Unchanged) ---
        
        if "Wood" in self.selected_components:
            wood_biomass += self._calculate_dbh_and_height_based_biomass_for_wood(dbh, height, wood_parameter_1, wood_parameter_2, wood_parameter_3)
            data.at[index, 'Wood (KG)'] = float(round(wood_biomass, 4))

        if "Bark" in self.selected_components:
            bark_biomass += self._calculate_dbh_and_height_based_biomass_for_bark(dbh, height, bark_parameter_1, bark_parameter_2, bark_parameter_3)
            data.at[index, 'Bark (KG)'] = float(round(bark_biomass, 4))
            
        if "Branch" in self.selected_components:
            branches_biomass += self._calculate_dbh_and_height_based_biomass_for_branch(dbh, height, branch_parameter_1, branch_parameter_2, branch_parameter_3 )
            data.at[index, 'Branch (KG)'] = float(round(branches_biomass, 4))
            
        if "Foliage" in self.selected_components:
            foliage_biomass += self._calculate_dbh_and_height_based_biomass_for_foliage(dbh, height, foliage_parameter_1, foliage_parameter_2, foliage_parameter_3)
            data.at[index, 'Foliage (KG)'] = float(round(foliage_biomass, 4))
            
            
        if "Stem" in self.selected_components:
            stem_biomass += self._calculate_dbh_and_height_based_biomass_for_wood(dbh, height, wood_parameter_1, wood_parameter_2, wood_parameter_3)
            stem_biomass += self._calculate_dbh_and_height_based_biomass_for_bark(dbh, height, bark_parameter_1, bark_parameter_2, bark_parameter_3)  
            data.at[index, 'Stem (KG)'] = float(round(stem_biomass, 4))
            
        
        if "Crown" in self.selected_components:
            crown_biomass += self._calculate_dbh_and_height_based_biomass_for_foliage(dbh, height, foliage_parameter_1, foliage_parameter_2, foliage_parameter_3)
            crown_biomass += self._calculate_dbh_and_height_based_biomass_for_branch(dbh, height, branch_parameter_1, branch_parameter_2, branch_parameter_3 )
            data.at[index, 'Crown (KG)'] = float(round(crown_biomass, 4))
            
            
        if "Total" in self.selected_components:
            total_biomass += self._calculate_dbh_and_height_based_biomass_for_wood(dbh, height, wood_parameter_1, wood_parameter_2, wood_parameter_3)
            total_biomass += self._calculate_dbh_and_height_based_biomass_for_bark(dbh, height, bark_parameter_1, bark_parameter_2, bark_parameter_3)
            total_biomass += self._calculate_dbh_and_height_based_biomass_for_foliage(dbh, height, foliage_parameter_1, foliage_parameter_2, foliage_parameter_3)
            total_biomass += self._calculate_dbh_and_height_based_biomass_for_branch(dbh, height, branch_parameter_1, branch_parameter_2, branch_parameter_3 )
            data.at[index, 'Total (KG)'] = float(round(total_biomass, 4))
      
        # calculate for wood = wood1 * (DBH)^(bwood2) * (Height)^bwood3 
        
        
        # wood = 
    def _calculate_dbh_and_height_based_biomass_for_wood(self, dbh: float, height: float, wood_parameter_1: float, wood_parameter_2: float, wood_parameter_3: float) -> float:
        return float(wood_parameter_1 * (dbh ** wood_parameter_2) * (height ** wood_parameter_3))

    def _calculate_dbh_and_height_based_biomass_for_bark(self, dbh: float, height: float, bark_parameter_1: float, bark_parameter_2: float, bark_parameter_3: float) -> float:
        return float(bark_parameter_1 * (dbh ** bark_parameter_2) * (height ** bark_parameter_3))

    def _calculate_dbh_and_height_based_biomass_for_branch(self, dbh: float, height: float, branch_parameter_1: float, branch_parameter_2: float, branch_parameter_3: float) -> float:
        return float(branch_parameter_1 * (dbh ** branch_parameter_2) * (height ** branch_parameter_3))

    def _calculate_dbh_and_height_based_biomass_for_foliage(self, dbh: float, height: float, foliage_parameter_1: float, foliage_parameter_2: float, foliage_parameter_3: float) -> float:
        return float(foliage_parameter_1 * (dbh ** foliage_parameter_2) * (height ** foliage_parameter_3))
    
    def _calculate_dbh_based_biomass(self, data: pd.DataFrame, index: int, row: pd.Series, species_params: dict) -> None:
        """Calculate DBH-based biomass for all selected components."""
        dbh = row.get('dbh', 0)
         # 2. Attempt safe conversion to float (and handle missing/zero values)
        try:
            # Check if the values are truthy (not None, not empty string) and convert
            dbh = float(dbh) if dbh is not None and str(dbh).strip() != '' else 0.0
         
            
        except (ValueError, TypeError):
            # If conversion fails (e.g., 'N/A' or 'Invalid'), skip the row
            print(f"Skipping row {index}: DBH ('{dbh}') ")
            return
        
        # 3. Check for zero values after successful conversion
        if dbh == 0.0:
            print(f"Skipping row {index}: DBH ({dbh}) is 0")
            return


        self._calculate_individual_components(data, index, species_params, dbh)
        self._calculate_composite_components(data, index, species_params, dbh)

    def _calculate_individual_components(self, data: pd.DataFrame, index: int, species_params: dict, dbh: float) -> None:
        """Calculate biomass for individual tree components."""
        component_configs = [
            ("Wood", "wood", "bwood1", "bwood2"),
            ("Bark", "bark", "bbark1", "bbark2"), 
            ("Foliage", "foliage", "bfoliage1", "bfoliage2"),
            ("Branch", "branches", "bbranches1", "bbranches2")
        ]

        for display_name, component, param1, param2 in component_configs:
            if display_name in self.selected_components:
                self._calculate_component_biomass(data, index, species_params, dbh, component, param1, param2)

    def _calculate_composite_components(self, data: pd.DataFrame, index: int, species_params: dict, dbh: float) -> None:
        """Calculate biomass for composite tree components."""
        if "Crown" in self.selected_components:
            self._calculate_crown_biomass(data, index, species_params, dbh)
            
        if "Stem" in self.selected_components:
            self._calculate_stem_biomass(data, index, species_params, dbh)
            
        if "Total" in self.selected_components:
            self._calculate_total_biomass(data, index, species_params, dbh)

    def _calculate_component_biomass(self, data: pd.DataFrame, index: int, species_params: dict, 
                                   dbh: float, component: str, param1: str, param2: str) -> None:
        """Calculate biomass for a single component using the formula: param1 * (dbh ^ param2)."""
        param1_val = species_params.get(param1, 0)
        param2_val = species_params.get(param2, 0)
        if dbh == 0 and param1_val == 0 and param2_val == 0:
            return
    
        biomass = param1_val * (dbh ** param2_val)
        column_name = f"{component.title()} (KG)" if component != "branches" else "Branch (KG)"
        data.at[index, column_name] = float(round(biomass, 4))

    def _calculate_crown_biomass(self, data: pd.DataFrame, index: int, species_params: dict, dbh: float) -> None:
        """Calculate crown biomass as sum of foliage and branch components."""
        crown_biomass = 0.0
        # calculate foliage and branch biomass regardless of selection
        foliage_biomass = self._calculate_single_component(species_params, dbh, 'bfoliage1', 'bfoliage2')
        branch_biomass = self._calculate_single_component(species_params, dbh, 'bbranches1', 'bbranches2')

        if foliage_biomass:
            crown_biomass += foliage_biomass
        if branch_biomass:
            crown_biomass += branch_biomass
        
        if crown_biomass > 0:
            data.at[index, 'Crown (KG)'] = float(round(crown_biomass, 4))

    def _calculate_stem_biomass(self, data: pd.DataFrame, index: int, species_params: dict, dbh: float) -> None:
        """Calculate stem biomass as sum of wood and bark components."""
        stem_biomass = 0.0
        
        # Wood component
        wood_biomass = self._calculate_single_component(species_params, dbh, 'bwood1', 'bwood2')
        if wood_biomass:
            stem_biomass += wood_biomass

        # Bark component  
        bark_biomass = self._calculate_single_component(species_params, dbh, 'bbark1', 'bbark2')
        if bark_biomass:
            stem_biomass += bark_biomass

        if stem_biomass > 0:
            data.at[index, 'Stem (KG)'] = float(round(stem_biomass, 4))

    def _calculate_total_biomass(self, data: pd.DataFrame, index: int, species_params: dict, dbh: float) -> None:
        """Calculate total biomass as sum of all individual components."""
        total_biomass = 0.0
        
        # calculate all individual components regardless of selection
        wood_biomass = self._calculate_single_component(species_params, dbh, 'bwood1', 'bwood2')
        bark_biomass = self._calculate_single_component(species_params, dbh, 'bbark1', 'bbark2')
        foliage_biomass = self._calculate_single_component(species_params, dbh, 'bfoliage1', 'bfoliage2')
        branch_biomass = self._calculate_single_component(species_params, dbh, 'bbranches1', 'bbranches2')
        
        total_biomass = wood_biomass + bark_biomass + foliage_biomass + branch_biomass
        
        if total_biomass > 0:
            data.at[index, 'Total (KG)'] = float(round(total_biomass, 4))

    def _calculate_single_component(self, species_params: dict, dbh: float, param1: str, param2: str) -> float:
        """Calculate biomass for a single component using its parameters."""
        param1_val = species_params.get(param1, 0)
        param2_val = species_params.get(param2, 0)
        
        if dbh != 0 and param1_val != 0 and param2_val != 0:
            return param1_val * (dbh ** param2_val)
        return 0.0

    def _save_results(self, data: pd.DataFrame) -> None:
        """Save calculation results to JSON and text files."""
        # Save to JSON
        data.to_json("storage/biomass_results.json", orient='records')
        print("Biomass results saved to biomass_results.json")
        
        # Save to text file
        self._save_to_text_file(data)

    def _save_to_text_file(self, data: pd.DataFrame) -> None:
        """Save results to a tab-delimited text file."""
        try:
            records = data.to_dict('records')
            
            with open('storage/output.txt', 'w') as file:
                if records:
                    headers = list(records[0].keys())
                    file.write('\t'.join(headers) + '\n')
                    
                    for record in records:
                        row_values = [str(record.get(header, '')) for header in headers]
                        file.write('\t'.join(row_values) + '\n')

            print("Data successfully written to output.txt")
            
        except Exception as e:
            print(f"Error saving to text file: {e}")