import os
import sys

class Json_File_Path_Constants:
    """Constants for JSON file paths used in the application."""
    
    def __init__(self):
        # Determine if running in production (frozen) or development
        self.is_production = self.check_frozen()
        
        # Get the appropriate base path
        if self.is_production:
            # Production: Use AppData folder for writable files
            self.base_path = self._get_app_data_path()
            self.resource_path = self._get_resource_path()
        else:
            # Development: Use project root (two levels up from config folder)
            # This puts data/storage at the same level as main.py
            self.base_path = self._get_project_root()
            self.resource_path = self.base_path
        
        # Initialize paths as instance variables
        self.CREATED_SPECIES_PATH = os.path.join(self.base_path, "data/create_species.json")
        self.BIOMASS_CALCULATIONS_PATH = os.path.join(self.base_path, "data/biomass_calculations.json")
        self.LOCAL_STORAGE_PATH = os.path.join(self.base_path, "storage/localstorage.json")
        self.SELECTED_DATABASE_PATH = os.path.join(self.base_path, "data/selected_database.json")
        self.BIOMASS_RESULTS_PATH = os.path.join(self.base_path, "storage/biomass_results.json")
        self.TREE_PARAMS_PATH = os.path.join(self.base_path, "data/treeparameters.json")
        self.OUTPUT_TEXT_PATH = os.path.join(self.base_path, "storage/output.txt")
        self.CONNECTION_HISTORY_PATH = os.path.join(self.base_path, "data/connection_history.json")
<<<<<<< HEAD
        self.INPUT_TEXT_FILE_NAME = os.path.join(self.base_path, "data/input_text_file_name.json")
=======
        
>>>>>>> 86feff1736be1803160fdf9b18c7c4b2a70faffa
        # Print paths for debugging
        print(f"📂 Development mode - Files stored in: {self.base_path}")
        print(f"   Data folder: {os.path.join(self.base_path, 'data')}")
        print(f"   Storage folder: {os.path.join(self.base_path, 'storage')}")
        print(f"   Connection history file: {self.CONNECTION_HISTORY_PATH}")
<<<<<<< HEAD
        print(f"   Input text file name: {self.INPUT_TEXT_FILE_NAME}")
=======
>>>>>>> 86feff1736be1803160fdf9b18c7c4b2a70faffa
        # Create necessary directories
        self._create_directories()
    
    def check_frozen(self):
        """Check if execution environment is frozen (e.g., PyInstaller)"""
        return getattr(sys, 'frozen', False)
    
    def _get_resource_path(self):
        """Get path for read-only resources (only relevant in production)"""
        if self.check_frozen():
            return sys._MEIPASS  # PyInstaller's temporary folder
        return os.path.dirname(os.path.abspath(__file__))
    
    def _get_app_data_path(self):
        """Get AppData path for production (writable files)"""
        if os.name == 'nt':  # Windows
            app_data = os.environ.get('APPDATA', '')
            if not app_data:
                app_data = os.path.expanduser('~')
            return os.path.join(app_data, 'BiomassCalculationTool')
        else:  # Linux/Mac
            return os.path.join(os.path.expanduser('~'), '.biomass_calc')
    
    def _get_project_root(self):
        """
        Get project root directory (where main.py is located)
        Assumes this file is in config/ folder: project_root/config/this_file.py
        """
        # Get the directory of this file (config folder)
        config_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to get project root
        project_root = os.path.dirname(config_dir)
        return project_root
    
    def _get_dev_path(self):
        """Legacy method - kept for compatibility"""
        return self._get_project_root()
    
    def _create_directories(self):
        """Create all necessary directories"""
        directories = [
            os.path.dirname(self.CREATED_SPECIES_PATH),
            os.path.dirname(self.BIOMASS_CALCULATIONS_PATH),
            os.path.dirname(self.LOCAL_STORAGE_PATH),
            os.path.dirname(self.SELECTED_DATABASE_PATH),
            os.path.dirname(self.BIOMASS_RESULTS_PATH),
            os.path.dirname(self.TREE_PARAMS_PATH),
            os.path.dirname(self.OUTPUT_TEXT_PATH),
<<<<<<< HEAD
            os.path.dirname(self.CONNECTION_HISTORY_PATH),
            os.path.dirname(self.INPUT_TEXT_FILE_NAME)

=======
            os.path.dirname(self.CONNECTION_HISTORY_PATH)
>>>>>>> 86feff1736be1803160fdf9b18c7c4b2a70faffa
        ]
        
        for directory in set(directories):
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Ensured directory: {directory}")
    
    def get_resource_path(self, relative_path):
        """Get path to a read-only resource (for files bundled with the executable)"""
        if self.is_production:
            return os.path.join(self.resource_path, relative_path)
        else:
            return os.path.join(self.base_path, relative_path)

# Create a singleton instance
json_paths = Json_File_Path_Constants()