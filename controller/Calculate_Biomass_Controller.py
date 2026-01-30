#Calculate_Biomass_Controller
import json
import os
from datetime import datetime
from model.Calculate_Biomass_Model import Calculate_Biomass_Model


class Calculate_Biomass_Controller:
    """Controller for calculating tree biomass based on selected components and equation types."""
    
    def lazy_imports(self):
        global pd, pyodbc, Bar_Chart_Widget
        import pandas as pd
        import pyodbc
        from widgets.Bar_Chart_Widget import Bar_Chart_Widget
    
    def __init__(self, model: Calculate_Biomass_Model, view):
        self.lazy_imports()
        
        self.model = model
        self.view = view
        self.equation_type = "DBH-based"
        self.local_storage_data = pd.read_json("storage/localstorage.json")
        self.tree_params_data = pd.read_json("data/treeparameters.json")
        self.selected_components = []
        self.hardwood_and_softwood_species_code_mapping = []
       
        # check to see if database is selected
        selected_db_path = 'data/selected_database.json'
        if os.path.exists(selected_db_path):
            with open(selected_db_path, 'r') as f:
                content = f.read().strip()
                if content and content != "{}":
                    print("Database selected for calculations.")
                    self.view.is_database_selected = True
                else:
                    print("No database selected for calculations.")
                    self.view.is_database_selected = False
                    
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
        if 'species' in data.columns:
            return data.sort_values(by='species').reset_index(drop=True)
        return data
    def _get_sum_of_component_for_specific_species(self, data: pd.DataFrame, species_code: int, component: str) -> float:
        """Get the sum of a specific component for a given species code."""
        #print(type(data["species"]))
        filtered_data = data[data['species'].astype(str) == str(species_code)]
        #print(f"filtered_data: {filtered_data}")
        component_column = f"{component} (KG)"
        if component_column in filtered_data.columns:
            return filtered_data[component_column].sum()
        return 0.0
   
    def _click_on_show_chart_button(self) -> None:
        """Handle the click event for the 'Show Chart' button."""
        #print("Show Chart button clicked.")
        species_data_for_chart = []
        data = self.json_to_dataframe_basic("storage/biomass_results.json")
       
        data = self.reorder_by_species_code(data)
        #print(f"Data loaded for chart: {data.head()}")
        species_codes = self._extract_all_species_codes(data)
        #print(f"Extracted species codes: {species_codes}")
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
    
    def _extract_all_species_codes(self, data: pd.DataFrame) -> list:
        """Extract all unique species codes from the DataFrame."""
        #print("Data COlumns=================================================================================")
        #print(data.columns)
        if 'species' in data.columns:
            #print("True found")
            return data['species'].unique().tolist()
        return []
     
    def set_equation_type(self, equation_type: str) -> None:
        """Set the equation type for biomass calculations."""
        self.equation_type = equation_type
        #print(f"Selected Equation Type: {equation_type}")

    def get_equation_type(self) -> str:
        """Get the currently selected equation type."""
        return self.equation_type
    
    def build(self):
        """Build the main view."""
        return self.view.build()

#     ###
#     # when i press calculate biomass button,

#  if not species code does not exist in both json data/treeparameters.json and data/created_species.json files then 
# display alert dialog box where user has to select which of the non existent species code is hard wood or softwood
#     display a checkbox list (select species for hardwood)
#     display a checkbox list (select species for softwood)
# based on those values set the parameters to the prefixed value depending what is selected
# Note at bottom: If you have parameters then please cancel this and add it in  the create species
#     # ###
#     def 
    def checkbox(self):
        pass
    def check_if_species_code_exists_within_the_json_files(self, species_code:int, json_file_path_1:str, json_file_path_2:str) -> bool:
        """Check if a species code exists within two JSON files."""
        try:
            with open(json_file_path_1, 'r') as f1, open(json_file_path_2, 'r') as f2:
                data1 = json.load(f1)
                data2 = json.load(f2)
                
                species_codes_1 = {int(item['SpeciesCode']) for item in data1 if 'SpeciesCode' in item}
                species_codes_2 = {int(item['SpeciesCode']) for item in data2 if 'SpeciesCode' in item}
                
                return species_code in species_codes_1 or species_code in species_codes_2
        except Exception as e:
            print(f"Error checking species code existence: {e}")
            return False
    
    def _extract_all_the_species_code_from_the_json_files(self, json_file_path_1:str, json_file_path_2:str) -> list:
        """Extract all unique species codes from two JSON files."""
        species_codes = set()
        try:
            with open(json_file_path_1, 'r') as f1, open(json_file_path_2, 'r') as f2:
                data1 = json.load(f1)
                data2 = json.load(f2)
                # soem speciescode is ""
                species_codes.update((item['SpecCommon']) for item in data1 if 'SpecCommon' in item and item['SpecCommon'] != "")
                species_codes.update((item['SpecCommon']) for item in data2 if 'SpecCommon' in item and item['SpecCommon'] != "")
                species_codes.update((item['SpeciesCode']) for item in data1 if 'SpeciesCode' in item and item['SpeciesCode'] != "")
                species_codes.update((item['SpeciesCode']) for item in data2 if 'SpeciesCode' in item and item['SpeciesCode'] != "") 
                
                
        except Exception as e:
            print(f"Error extracting species codes: {e}")
        
        #reorder species codes before returning
        # species_codes = sorted(species_codes)
        #print(f"Species Codes Extracted: {species_codes}")
        return list(species_codes)
    
    def _extract_all_species_codes_from_local_storage_json(self, local_storage_data: pd.DataFrame) -> list:
        """Extract all unique species codes from the local storage DataFrame."""
        species_codes = set()
        #print("----------------------------------------------------------------------------------------------------------------------")
        
        try:
            for item in local_storage_data['Species']:
                # print(item)
                if item != "" and pd.notna(item):  # Also check for NaN
                    try:
                        # Try to convert to int
                        int_value = int(item)
                        # print("INT FOUND")
                        species_codes.add(int_value)  # Use add() for single values
                    except ValueError:
                        # If conversion fails, keep as string
                        # print("STRING FOUND")
                        species_codes.add(str(item))  # Use add() for single values
        except Exception as e:
            print(f"Error extracting species codes from local storage: {e}")
        
        # Sort the species codes before returning
        species_codes = sorted(species_codes, key=lambda x: str(x))  # Convert to string for mixed type sorting
        return list(species_codes)
    def _create_hardwood_softwood_species_code_mapping(self, hardwood_species_codes: list, softwood_species_codes: list) -> dict:
        """Create a mapping of species codes to their type (hardwood or softwood)."""
        mapping = {}
        for code in hardwood_species_codes:
            mapping[code] = "hardwood"
        for code in softwood_species_codes:
            mapping[code] = "softwood"
        return mapping
    
    
    
    
    def _apply_species_type_mapping(self, species_type_mapping):
        """Apply the species type mapping to set parameters."""
        #print("Applying species type mapping...")
        #print(f"Species Type Mapping: {species_type_mapping}")
        # Example: For each species code in the mapping, set appropriate parameters
        for species_code, wood_type in species_type_mapping.items():
            #print(f"Setting species code {species_code} as {wood_type}")
            
            # Here you would add logic to set the parameters based on wood type
            # For example, you might set default parameters for hardwood vs softwood
            if wood_type == "Hardwood":
                # Set hardwood parameters
                self._set_hardwood_parameters(species_code)
            elif wood_type == "Softwood":
                # Set softwood parameters
                self._set_softwood_parameters(species_code)
        
        # You might also need to update your tree_params_data DataFrame
        # with the new species codes and their corresponding parameters

    def _set_hardwood_parameters(self, species_code):
        """Set default parameters for hardwood species."""
        
        # First, let's see what we're working with
        #print(f"Setting hardwood parameters for species code {species_code}")
        
        # Get hardwood records from tree_params_data
        hardwood_records = self.tree_params_data.loc[self.tree_params_data['SpecCommon'] == 'Hardwood'].to_dict('records')
        
        if not hardwood_records:
            print("No hardwood records found in tree_params_data")
            return
        
        # Now we need to update each record with the species code
        for record in hardwood_records:
            record['SpeciesCode'] = species_code
        
        # Append the updated records to the mapping
        self.hardwood_and_softwood_species_code_mapping.append(hardwood_records)
        
        #print(f"Added {len(hardwood_records)} hardwood record(s) for species code {species_code}")
        #print(f"Updated mapping: {self.hardwood_and_softwood_species_code_mapping}")
    def _set_softwood_parameters(self, species_code):
        """Set default parameters for softwood species."""
        
        # First, let's see what we're working with
        #print(f"Setting softwood parameters for species code {species_code}")
        
        # Get softwood records from tree_params_data
        softwood_records = self.tree_params_data.loc[self.tree_params_data['SpecCommon'] == 'Softwood'].to_dict('records')
        
        if not softwood_records:
            #print("No softwood records found in tree_params_data")
            return
        
        # Now we need to update each record with the species code
        for record in softwood_records:
            record['SpeciesCode'] = species_code
        
        # Append the updated records to the mapping
        self.hardwood_and_softwood_species_code_mapping.append(softwood_records)
        
        #print(f"Added {len(softwood_records)} softwood record(s) for species code {species_code}")
        #print(f"Updated mapping: {self.hardwood_and_softwood_species_code_mapping}")
    
    
    
    
    
    
    async def calculate_biomass(self) -> None:
        """Calculate biomass based on selected parameters and equation type."""
        #print("Calculate Biomass button clicked.")
        self.hardwood_and_softwood_species_code_mapping = []
        
        self.selected_components = self.view.get_selected_components()
        self.equation_type = self.get_equation_type()
        #print(f"Selected Components: {self.selected_components}")
        #print(f"Equation Type: {self.equation_type}")

        try:
            self.local_storage_data = pd.read_json("storage/localstorage.json")
            self.tree_params_data = pd.read_json("data/treeparameters.json")
            # if not self.check_if_species_code_exists_within_the_json_files(101, "data/treeparameters.json", "data/create_species.json"):
            #print("Checking for missing species codes...")
            datasets_species_code_list = self._extract_all_the_species_code_from_the_json_files("data/treeparameters.json", "data/create_species.json")
            
            #print(f"Datasets Species Code List: {datasets_species_code_list}")
            #Get the dataset species code list from the local storage data
            local_storage_species_code_list = self._extract_all_species_codes_from_local_storage_json(self.local_storage_data)
            #print(f"Local Storage Species Code List: {local_storage_species_code_list}")
                # Compare both lists to find missing species codes
            #convert to lower string if possible
            datasets_species_code_list = [str(code).lower() for code in datasets_species_code_list]
            #print(f"Datasets Species Code List (Lowercase): {datasets_species_code_list}")
            local_storage_species_code_list = [str(code).lower() for code in local_storage_species_code_list]
            #print(f"Local Storage Species Code List (Lowercase): {local_storage_species_code_list}")
        
            missing_species_codes = set(local_storage_species_code_list) - set(datasets_species_code_list)
            #print(f"Missing Species Codes: {missing_species_codes}")
            
            if missing_species_codes:
                # Display dialog to user to select hardwood or softwood for missing species codes
                # This will wait until the user clicks submit
                species_type_mapping = await self.view.show_species_code_dialog(missing_species_codes)
                
                if species_type_mapping is None:
                
                    #print("Dialog was cancelled. Aborting biomass calculation.")
                    
                    raise Exception("Dialog cancelled by user")
                print(species_type_mapping)
                #print(f"Species type mapping received: {species_type_mapping}")
                # Now you can use the mapping to set parameters
                self._apply_species_type_mapping(species_type_mapping)
                #print(f"Hardwood and Softwood Species Code Mapping: {self.hardwood_and_softwood_species_code_mapping}")
            print(self.hardwood_and_softwood_species_code_mapping)
            self._lower_column_names(self.local_storage_data, self.tree_params_data)
            self._process_biomass_calculations(self.local_storage_data, self.tree_params_data)
            self._save_results(self.local_storage_data)
            return True
            
        except Exception as e:
            print(f"Error calculating biomass: {e}")
            return False
            # self.view.show_error_dialog(str(e))  # Uncomment for user error display
   
    def _lower_column_names(self, *dataframes) -> None:
        """Convert all column names to lowercase for consistency."""
        for df in dataframes:
            df.columns = df.columns.str.lower()

    def lookup(self, data, species_code:int) -> dict:
        # print(species_code)
        species_code_lookup = {int(dat["speciescode"]): dat for dat in data}
        # print(species_code_lookup.get(species_code))
        
        if species_code_lookup.get(species_code) is None:
            return None
        
        # FIX: Return the species data using species_code, not species_code_lookup
        return species_code_lookup.get(species_code)

    
    def _process_biomass_calculations(self, local_data: pd.DataFrame, tree_params: pd.DataFrame) -> None:
        """Calculate biomass for each row in the dataset - most efficient version."""
        
        # 1. Precompute lookup dictionaries ONCE
        species_code_lookup = {}  # For looking up by species code (int)
        species_name_lookup = {}  # For looking up by species name (str)
        created_species_code_lookup = {}  # For created species by code
        created_species_name_lookup = {}  # For created species by name
        hardwood_and_softwood_species_code_mapping_lookup = {}
        
        # Load from tree_params (existing)
        for _, row in tree_params.iterrows():
           
                code = row['speciescode']
                if code and pd.notna(code):
                    # print(f"Adding species code to lookup: {code}")
                    species_code_lookup[int(code)] = row.to_dict()
               
                    # Store by species name (str) - adjust column name if needed
                name = row.get('speccommon')
                if name and pd.notna(name):
                    #print(f"Adding species name to lookup: {name}")
                    species_name_lookup[str(name).lower().strip()] = row.to_dict()
        
        # Load from created_species.json (new)
        try:
            with open("data/create_species.json", "r") as f:
                created_species_data = json.load(f)
            # print("Created Species Data Loaded:")
            # print(created_species_data)
            for species in created_species_data:
                try:
                    code = species.get('SpeciesCode')
                    if code and pd.notna(code):
                        created_species_code_lookup[int(code)] = species
                        
                    name = species.get('SpecCommon')
                    if name and pd.notna(name):
                        created_species_name_lookup[str(name).lower().strip()] = species
                except (ValueError, TypeError):
                    continue
            # print("Species Lookups Created:")
            # print("================================")
                
            # print("Created Species Code Lookup:")
            # print(created_species_code_lookup)
            # print("================================")
            # print("Created Species Name Lookup:")
            # print(created_species_name_lookup)
            # print("================================")
            
            # print("Species Code Lookup:")
            # print(species_code_lookup)
            # print("================================")
            
            # print("Species Name Lookup:")
            # print(species_name_lookup)     
            # print("================================")
                # for keys in species_name_lookup:
                #     print(f"Finding Jack pine : {keys}")
            # print(f"Finding Jack pine : {specie\s_name_lookup.get('jack pine')}")
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load created_species.json: {e}")
        
      
        # check self.hardwood_and_softwood_species_code_mapping to see if species code
        for species_list in self.hardwood_and_softwood_species_code_mapping:
            for species in species_list:
                try:
                    code = species.get('SpeciesCode')
                    if code.isdigit():
                        code = int(code)
                    else:
                        code = str(code).lower().strip()
                    # print(f"Adding species code from mapping: {code}")
                    if code and pd.notna(code):
                        print(f"Looking up hardwood/softwood mapping for species name 2'{code}': {species}")
                        hardwood_and_softwood_species_code_mapping_lookup[(code)] = species
                except (ValueError, TypeError):
                    continue
        print("Hardwood and Softwood Species Code Mapping Lookup:")
        print(hardwood_and_softwood_species_code_mapping_lookup)
        # 2. Vectorized filtering of valid rows\
            #check alphanumeric species codes and name
            
        for idx, row in local_data.iterrows():
            species_value = row.get('species')  # assuming 'species' column
            # if pd.isna(species_value):
            #     continue  # Skip if species is NaN
            
            species_params = None
            
            # First try: Convert to int (treat as species code)
            try:
                species_code = int(species_value)
                # print(f"Row {idx}: Treating '{species_value}' as code {species_code}")
                
                # Try to find by code in tree_params
                species_params = species_code_lookup.get(species_code)
                
                # If not found, try created_species by code
                
                if not species_params:
                    
                    species_params = created_species_code_lookup.get(species_code)
                if not species_params:
                    species_params = hardwood_and_softwood_species_code_mapping_lookup.get(species_code)
                    print(f"Looking up hardwood/softwood mapping for species name 1'{species_code}': {hardwood_and_softwood_species_code_mapping_lookup.get(species_code)}")
                    
                    
            except (ValueError, TypeError):
                # Conversion to int failed, so treat as string (species name)
                species_name = str(species_value).lower().strip()
            
                # print(f"Processing row {idx} with species value: {species_value.lower().strip()}")
                # print(f"Row {idx}: Treating '{species_value}' as name '{species_name}'")
                
                # Try to find by name in tree_params
                species_params = species_name_lookup.get(species_name)
                
                # If not found, try created_species by name
                if not species_params:
                    if species_name == "aw2":
                        print("HERE")
                    species_params = created_species_name_lookup.get(species_name)
                    print(f"Looking up created species name '{species_name}': {created_species_name_lookup.get(species_name)}")
                    
                if not species_params:
                    species_params = hardwood_and_softwood_species_code_mapping_lookup.get(species_name)
                    print(f"Looking up hardwood/softwood mapping for species name '{species_name}': {hardwood_and_softwood_species_code_mapping_lookup.get(species_name)}")
            # print(f"Processing row {idx} with species value: {species_params}")

            # If we found species parameters, calculate biomass
            if species_params:
               # print("Found species parameters:")
                # print(species_params)
                # print(f"Row {idx}: Found species params for '{species_value}'")
                self._calculate_row_biomass(local_data, idx, row, species_params)
            else:
                pass
                # print(f"Row {idx}: Species '{species_value}' not found in any lookup table")
            # print(species_params)
        

          
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
            # print(f"Skipping row {index}: DBH ('{raw_dbh}') or Height ('{raw_height}') could not be converted to a number.")
            return
        
        # 3. Check for zero values after successful conversion
        if dbh == 0.0 or height == 0.0:
            # print(f"Skipping row {index}: DBH ({dbh}) or Height ({height}) is zero.")
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
      
        try:
            # Check if the values are truthy (not None, not empty string) and convert
            dbh = float(dbh) if dbh is not None and str(dbh).strip() != '' else 0.0
         
            
        except (ValueError, TypeError):
            # If conversion fails (e.g., 'N/A' or 'Invalid'), skip the row
           # print(f"Skipping row {index}: DBH ('{dbh}') ")
            return
        
        # 3. Check for zero values after successful conversion
        if dbh == 0.0:
            # print(f"Skipping row {index}: DBH ({dbh}) is 0")
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
        # print("Biomass results saved to biomass_results.json")
        
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

            # print("Data successfully written to output.txt")
            
        except Exception as e:
            print(f"Error saving to text file: {e}")

    def _normalize_biomass_row(self, row: dict) -> dict:
        plot = row.get("Plot") or row.get("plot")
        year = row.get("Year") or row.get("year")
        tree_number = row.get("Tree_number") or row.get("Tree Number") or row.get("tree_number")
        species = row.get("Species") or row.get("species") or row.get("SpecCode")

        if not plot or year is None or tree_number is None or species is None:
            raise ValueError(f"Missing required fields in row: {row}")

        return {
            "plot": plot,
            "year": int(year),
            "species": int(species),
            "tree_number": int(tree_number),
            "dbh": row.get("DBH") or row.get("dbh"),
            "height": row.get("Height") or row.get("height"),
            "wood_kg": row.get("Wood_kg") or row.get("Wood (KG)") or row.get("wood_kg"),
            "bark_kg": row.get("Bark_kg") or row.get("Bark (KG)") or row.get("bark_kg"),
            "foliage_kg": row.get("Foliage_kg") or row.get("Foliage (KG)") or row.get("foliage_kg"),
            "branch_kg": row.get("Branch_kg") or row.get("Branch (KG)") or row.get("branch_kg"),
            "crown_kg": row.get("Crown_kg") or row.get("Crown (KG)") or row.get("crown_kg"),
            "stem_kg": row.get("Stem_kg") or row.get("Stem (KG)") or row.get("stem_kg"),
            "total_kg": row.get("Total_kg") or row.get("Total (KG)") or row.get("total_kg"),
            "coefficient_source": row.get("CoefficientSource") or row.get("coefficient_source")
        }


    def write_results_to_database(self):
        """Write the biomass results from JSON to SQL Server database using new schema."""
        try:
            from data.data_manager import DataManager

            dm = DataManager()
            db_path = dm.get_database_path()
            conn = pyodbc.connect(db_path)
            cursor = conn.cursor()

            # Ensure output table exists (new schema)
            create_table_sql = """
            IF NOT EXISTS (
                SELECT 1 FROM sys.tables t
                JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE t.name = 'tCalcBiomassOutput' AND s.name = 'dbo'
            )
            CREATE TABLE dbo.tCalcBiomassOutput
            (
                Plot               VARCHAR(100) NOT NULL,
                Year               INT          NOT NULL,
                Species            INT          NOT NULL,
                Tree_number        INT          NOT NULL,
                DBH                DECIMAL(4,1)  NOT NULL,
                Height             DECIMAL(4,2)  NULL,
                Wood_kg            NUMERIC(10,3),
                Bark_kg            NUMERIC(10,3),
                Foliage_kg         NUMERIC(10,3),
                Branch_kg          NUMERIC(10,3),
                Crown_kg           NUMERIC(10,3),
                Stem_kg            NUMERIC(10,3),
                Total_kg           NUMERIC(10,3),
                CoefficientSource  VARCHAR(100)  NULL,
                processed_at       DATETIMEOFFSET NOT NULL DEFAULT SYSUTCDATETIME()
            );
            """
            cursor.execute(create_table_sql)
            conn.commit()

            # Remove existing records to avoid duplicates
            delete_sql = "DELETE FROM dbo.tCalcBiomassOutput"
            cursor.execute(delete_sql)
            conn.commit()
            
            
            # Load JSON results
            with open('storage/biomass_results.json', 'r') as f:
                data = json.load(f)

            # Insert SQL matching new schema
            insert_sql = """
            INSERT INTO dbo.tCalcBiomassOutput
            (Plot, Year, Species, Tree_number, DBH, Height,
            Wood_kg, Bark_kg, Foliage_kg, Branch_kg, Crown_kg,
            Stem_kg, Total_kg, CoefficientSource)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.fast_executemany = True

            for row in data:
                r = self._normalize_biomass_row(row)

                cursor.execute(
                    insert_sql,
                    r["plot"],
                    r["year"],
                    r["species"],
                    r["tree_number"],
                    r["dbh"],
                    r["height"],
                    r["wood_kg"],
                    r["bark_kg"],
                    r["foliage_kg"],
                    r["branch_kg"],
                    r["crown_kg"],
                    r["stem_kg"],
                    r["total_kg"],
                    r.get("coefficient_source")  # optional
                )

            conn.commit()
            cursor.close()
            conn.close()
            return True

        except Exception as e:
            print(f"Database write error: {e}")
            return False
