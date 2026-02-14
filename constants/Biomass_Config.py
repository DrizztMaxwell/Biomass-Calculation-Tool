from typing import Dict, List, Tuple
from .Json_File_Path_Constants import json_paths
class Biomass_Config:
    """Configuration constants for biomass calculations."""
    
    # File paths
    LOCAL_STORAGE_PATH = json_paths.LOCAL_STORAGE_PATH
    TREE_PARAMS_PATH = json_paths.TREE_PARAMS_PATH
    CREATED_SPECIES_PATH = json_paths.CREATED_SPECIES_PATH
    BIOMASS_RESULTS_PATH = json_paths.BIOMASS_RESULTS_PATH
    OUTPUT_TEXT_PATH = "storage/output.txt"
    SELECTED_DB_PATH = json_paths.SELECTED_DATABASE_PATH
    
    # Database
    OUTPUT_TABLE_NAME = "tCalcBiomassOutput"
    
    # Component definitions
    INDIVIDUAL_COMPONENTS: List[Tuple[str, str, str, str]] = [
        ("Wood", "wood", "bwood1", "bwood2"),
        ("Bark", "bark", "bbark1", "bbark2"),
        ("Foliage", "foliage", "bfoliage1", "bfoliage2"),
        ("Branch", "branches", "bbranches1", "bbranches2")
    ]
    
    COMPOSITE_COMPONENTS: List[str] = ["Crown", "Stem", "Total"]
    
    # Biomass columns for display
    BIOMASS_COLUMNS: List[str] = [
        'Wood (KG)', 'Bark (KG)', 'Foliage (KG)', 'Branch (KG)',
        'Crown (KG)', 'Stem (KG)', 'Total (KG)'
    ]
    
    # Equation types
    EQUATION_TYPES: Dict[str, str] = {
        "DBH_BASED": "DBH-based",
        "DBH_HEIGHT_BASED": "DBH + Height-based"
    }