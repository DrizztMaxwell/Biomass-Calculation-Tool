"""
Model for the Data Import Platform
Contains data structures and business logic.
"""

class ImportOption:
    """Data model for import options"""
    
    def __init__(self, icon_name: str, title: str, subtitle: str, color: str):
        self.icon_name = icon_name
        self.title = title
        self.subtitle = subtitle
        self.color = color

class AppState:
    """Manages application state"""
    
    def __init__(self):
        self.import_options = [
            ImportOption(
                icon_name="folder_open",
                title="Local File Import",
                subtitle="Upload CSV, TXT, or Excel files from your local storage with advanced parsing options.",
                color="blue_600"
            ),
            ImportOption(
                icon_name="storage",
                title="Database Connection",
                subtitle="Connect securely to SQL databases using JDBC/ODBC drivers with real-time data streaming.",
                color="indigo_600"
            )
        ]
    
    @staticmethod
    def get_page_configuration():
        """Returns page configuration settings"""
        return {
            "title": "Data Import Platform",
            "vertical_alignment": "center",
            "horizontal_alignment": "center", 
            "theme_mode": "light",
            "bgcolor": "blue_grey_50",
            "padding": 0
        }