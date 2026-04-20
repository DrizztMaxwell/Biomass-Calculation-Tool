#modify species controller

import json
import shutil
import os
from widgets.LogFileTxt import logger
from constants.Json_File_Path_Constants import json_paths
class Modify_Species_Controller:
    """Controller for handling species modification logic."""
    
    def __init__(self):
        self.__species_data = []
        pass
    def get_species_data(self):
        """Return the current species data."""
        return self.__species_data
    def set_species_data(self, data):        
        """Set the species data."""
        self.__species_data = data
    def load_species_data(self):
        """Load species data from JSON file"""
        try:
            print(f"Attempting to load species data from: {json_paths.CREATED_SPECIES_PATH}")
            with open(json_paths.CREATED_SPECIES_PATH, "r") as f:
                self.set_species_data(json.load(f))
                print(f"Loaded species data: {self.get_species_data()}")
                logger.write("Species data loaded successfully.")
        except (FileNotFoundError, json.JSONDecodeError):
            self.set_species_data([])


    def save_species_data(self):
        """Save species data to JSON file (appends to existing data)"""
        try:
            # Load existing data if file exists
            existing_data = []
            if os.path.exists(json_paths.CREATED_SPECIES_PATH):
                with open(json_paths.CREATED_SPECIES_PATH, "r") as f:
                    existing_data = json.load(f)
                    # Ensure existing_data is a list
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data]
            
            # Get new data
            new_data = self.get_species_data()
            
            # Append new data (assuming new_data is a dict or list)
            if isinstance(new_data, list):
                existing_data.extend(new_data)
            else:
                existing_data.append(new_data)
            
            # Write combined data back to file
            with open(json_paths.CREATED_SPECIES_PATH, "w") as f:
                json.dump(existing_data, f, indent=4)
            
            logger.write("Species data appended successfully.")    
            return True
        except Exception as e:
            logger.write(f"Error saving data: {e}")
            return False

    # ─────────────────────────────────────────────────────────────
    # Export species to .species file
    # ─────────────────────────────────────────────────────────────
    def export_species_file(self, file_path):
        """Save current species list to a .species file"""
        try:
            with open(file_path, "w") as f:
                json.dump(self.get_species_data(), f, indent=4)

            logger.write(f"Species exported successfully to {file_path}")
            return True
        except Exception as e:
            logger.write(f"Error exporting species file: {e}")
            return False

    # ─────────────────────────────────────────────────────────────
    # Import species from .species file
    # ─────────────────────────────────────────────────────────────
    def import_species_file(self, file_path):
        """Load species list from a .species file and append only unique species (case-insensitive)
        
        Returns:
            tuple: (success: bool, appended_count: int, duplicate_count: int)
        """
        try:
            with open(file_path, "r") as f:
                imported_data = json.load(f)
            
            # Ensure imported_data is a list
            if not isinstance(imported_data, list):
                imported_data = [imported_data]
            
            # Load existing data
            existing_data = self.get_species_data()
            if not isinstance(existing_data, list):
                existing_data = []
            
            # Create sets of existing identifiers for quick lookup (case-insensitive)
            existing_species_codes = set()
            existing_spec_common = set()
            
            for species in existing_data:
                if isinstance(species, dict):
                    # Add SpeciesCode if it exists (convert to lower case)
                    if "SpeciesCode" in species and species["SpeciesCode"]:
                        existing_species_codes.add(species["SpeciesCode"].lower())
                    # Add SpecCommon if it exists (convert to lower case)
                    if "SpecCommon" in species and species["SpecCommon"]:
                        existing_spec_common.add(species["SpecCommon"].lower())
            
            # Track new unique species
            new_species = []
            duplicate_count = 0
            
            for species in imported_data:
                if not isinstance(species, dict):
                    continue
                    
                species_code = species.get("SpeciesCode", "")
                spec_common = species.get("SpecCommon", "")
                
                # Convert to lower case for comparison
                species_code_lower = species_code.lower() if species_code else ""
                spec_common_lower = spec_common.lower() if spec_common else ""
                
                # Check if this species already exists
                is_duplicate = False
                
                if species_code_lower and species_code_lower in existing_species_codes:
                    is_duplicate = True
                    logger.write(f"Duplicate found - SpeciesCode '{species_code}' already exists. Skipping import.")
                elif spec_common_lower and spec_common_lower in existing_spec_common:
                    is_duplicate = True
                    logger.write(f"Duplicate found - SpecCommon '{spec_common}' already exists. Skipping import.")
                
                if not is_duplicate:
                    new_species.append(species)
                    # Add to existing sets to catch duplicates within the import file itself
                    if species_code_lower:
                        existing_species_codes.add(species_code_lower)
                    if spec_common_lower:
                        existing_spec_common.add(spec_common_lower)
                else:
                    duplicate_count += 1
            
            # Append only new unique species
            appended_count = len(new_species)
            
            if new_species:
                existing_data.extend(new_species)
                self.set_species_data(existing_data)
                self.save_species_data()
                logger.write(f"Imported {appended_count} new unique species from {file_path}. Skipped {duplicate_count} duplicates.")
            else:
                logger.write(f"No new unique species found in {file_path}. All {duplicate_count} items were duplicates.")
            
            return True, appended_count, duplicate_count
            
        except Exception as e:
            logger.write(f"Error importing species file: {e}")
            return False, 0, 0
        
    def overwrite_species_data(self):
        """Overwrite the species file with current in-memory data (no append)."""
        try:
            with open(json_paths.CREATED_SPECIES_PATH, "w") as f:
                json.dump(self.__species_data, f, indent=4)
            logger.write("Species data overwritten successfully.")
            return True
        except Exception as e:
            logger.write(f"Error overwriting species data: {e}")
            return False
    def clear_species_data(self):
        """Clear all species data from memory and file."""
        try:
            self.set_species_data([])
            with open(json_paths.CREATED_SPECIES_PATH, "w") as f:
                json.dump([], f, indent=4)
            logger.write("All species data cleared successfully.")
            return True
        except Exception as e:
            logger.write(f"Error clearing species data: {e}")
            return False