import json
import pandas as pd
from model.Calculate_Biomass_Model import Calculate_Biomass_Model
from widgets.Bar_Chart_Widget import Bar_Chart_Widget


class Calculate_Biomass_Controller:
    """Controller for calculating tree biomass based on selected components and equation types."""
    
    
    
    def __init__(self, model: Calculate_Biomass_Model, view):
        self.model = model
        self.view = view
        self.equation_type = "DBH-based"
        self.selected_components = []
    def json_to_dataframe_basic(self, json_file_path):
        """Convert JSON file to DataFrame (basic approach)"""
        try:
            with open(json_file_path, 'r') as f:
                data = json.load(f)
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error converting JSON to DataFrame: {e}")
            return pd.DataFrame()
    def reorder_by_species_code(self, data: pd.DataFrame) -> pd.DataFrame:
        """Reorder the DataFrame by 'speciescode' in ascending order."""
        if 'speccode' in data.columns:
            return data.sort_values(by='speccode').reset_index(drop=True)
        return data
    def _get_sum_of_component_for_specific_species(self, data: pd.DataFrame, species_code: int, component: str) -> float:
        """Get the sum of a specific component for a given species code."""
        print(type(data["speccode"]))
        filtered_data = data[data['speccode'].astype(str) == str(species_code)]
        print(f"filtered_data: {filtered_data}")
        component_column = f"{component} (KG)"
        if component_column in filtered_data.columns:
            return filtered_data[component_column].sum()
        return 0.0
    def _extract_all_species_codes(self, data: pd.DataFrame) -> list:
        """Extract all unique species codes from the DataFrame."""
        if 'speccode' in data.columns:
            return data['speccode'].unique().tolist()
        return []
    def _click_on_show_chart_button(self) -> None:
        """Handle the click event for the 'Show Chart' button."""
        print("Show Chart button clicked.")
        species_data_for_chart = []
        data = self.json_to_dataframe_basic("storage/biomass_results.json")
        data = self.reorder_by_species_code(data)
        species_codes = self._extract_all_species_codes(data)
        for species_code in species_codes:
            wood_sum = self._get_sum_of_component_for_specific_species(data, species_code, "Wood")
            bark_sum = self._get_sum_of_component_for_specific_species(data, species_code, "Bark")
            branch_sum = self._get_sum_of_component_for_specific_species(data, species_code, "Branch")
            foliage_sum = self._get_sum_of_component_for_specific_species(data, species_code, "Foliage")
            if wood_sum == 0 and bark_sum == 0 and branch_sum == 0 and foliage_sum == 0:
                continue
            species_data_for_chart.append({
                "species_code": species_code,
                "Wood": wood_sum,
                "Bark": bark_sum,
                "Branch": branch_sum,
                "Foliage": foliage_sum
            })
       
        
        # print(f"Wood Sum: {wood_sum}")
        # print(f"Bark Sum: {bark_sum}")
        # print(species_data_for_chart)
        return species_data_for_chart
        # Implement chart display logic here
        # self.reorder_by_species_code(data)
        
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
            df.columns = df.columns.str.lower()

    def lookup(self, data, species_code:int) -> dict:
        print(species_code)
        species_code_lookup = {int(dat["speciescode"]): dat for dat in data}
        print(species_code_lookup.get(species_code))
        
        if species_code_lookup.get(species_code) is None:
            return None
        
        # FIX: Return the species data using species_code, not species_code_lookup
        return species_code_lookup.get(species_code)

    def _process_biomass_calculations(self, local_data: pd.DataFrame, tree_params: pd.DataFrame) -> None:
        """Calculate biomass for each row in the dataset - most efficient version."""
        
        # 1. Precompute lookup dictionaries ONCE
        species_code_lookup = {}
        created_species_lookup = {}
        
        # Load from tree_params (existing)
        for _, row in tree_params.iterrows():
            try:
                code = row['speciescode']
                if pd.notna(code):
                    species_code_lookup[int(code)] = row.to_dict()
            except (ValueError, TypeError):
                continue
        
        # Load from created_species.json (new)
        try:
            with open("data/create_species.json", "r") as f:
                created_species_data = json.load(f)
            
            for species in created_species_data:
                try:
                    code = species.get('SpeciesCode')
                    if code and pd.notna(code):
                        created_species_lookup[int(code)] = species
                except (ValueError, TypeError):
                    continue
                    
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load created_species.json: {e}")
        
        # 2. Vectorized filtering of valid rows
        species_codes = pd.to_numeric(local_data['speccode'], errors='coerce')
        valid_mask = (species_codes.notna()) & (species_codes != 0)
        valid_indices = species_codes[valid_mask].index
        valid_codes = species_codes[valid_mask].astype(int)
        
        # 3. Process only valid rows - check both lookup sources
        for idx, species_code in zip(valid_indices, valid_codes):
            species_params = species_code_lookup.get(species_code)
            
            # If not found in tree_params, try created_species
            if not species_params:
                species_params = created_species_lookup.get(species_code)
            
            if species_params:
                self._calculate_row_biomass(local_data, idx, local_data.loc[idx], species_params)

    def _get_species_parameters(self, tree_params: pd.DataFrame, species_code: int) -> dict:
        """Retrieve parameters for a specific species code."""
        # Convert DataFrame to list of dictionaries for the lookup function
        data_as_dict = tree_params.to_dict('records')
        return self.lookup(data_as_dict, species_code)
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