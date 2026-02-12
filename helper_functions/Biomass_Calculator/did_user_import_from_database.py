
import os


def did_user_import_from_database():
        """Check if a database is selected for calculations."""
        from constants.Biomass_Config import Biomass_Config
        # check to see if database is selected
        selected_db_path = Biomass_Config.SELECTED_DB_PATH
        if os.path.exists(selected_db_path):
            with open(selected_db_path, 'r') as f:
                content = f.read().strip()
                if content and content != "{}":
                    print("Database selected for calculations.")
                    return True
                else:
                    print("No database selected for calculations.")
                    return False
        else:
            print("Selected database file does not exist.")
            return False