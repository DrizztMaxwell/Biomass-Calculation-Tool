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
        """Save species data to JSON file"""
        try:
            with open(json_paths.CREATED_SPECIES_PATH, "w") as f:
                json.dump(self.get_species_data(), f, indent=4)
            
            logger.write("Species data saved successfully.")    
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
        """Load species list from a .species file and overwrite JSON"""
        try:
            with open(file_path, "r") as f:
                imported_data = json.load(f)

            self.set_species_data(imported_data)
            self.save_species_data()  # overwrite JSON file

            logger.write(f"Species imported successfully from {file_path}")
            return True
        except Exception as e:
            logger.write(f"Error importing species file: {e}")
            return False