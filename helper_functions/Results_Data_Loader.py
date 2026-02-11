import json
import os
from widgets.LogFileTxt import logger

class Results_Data_Loader:
    """Load results data from JSON file."""
    
    _RESULTS_JSON_PATH = 'storage/biomass_results.json'
    
    def load(self):
        """Load results from JSON file."""
        try:
            if not os.path.exists(self._RESULTS_JSON_PATH):
                return []
            
            with open(self._RESULTS_JSON_PATH, 'r') as file:
                data = json.load(file)
                return data
        
        except json.JSONDecodeError as error:
            logger.write(f"Error parsing results JSON: {error}")
            return []
        except Exception as error:
            logger.write(f"Error loading results: {error}")
            return []