import json
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
