from typing import Dict, List
from widgets.LogFileTxt import logger
from constants.Biomass_Config import Biomass_Config

def export_to_text_file(file_path) -> bool:
    """Export data to a formatted text file."""
    try:
        data = []
        # read the data from biomass_results.json
        import json
        with open(Biomass_Config.BIOMASS_RESULTS_PATH, 'r') as f:
            data = json.load(f)
        
        import datetime
        with open(file_path, 'w') as file:
            
            file.write("BIOMASS CALCULATION RESULTS\n")
            file.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Total records: {len(data)}\n\n")
            
            if data:
                # Define biomass columns to be placed at the end
                biomass_columns = [
                    'Wood (KG)', 'Bark (KG)', 'Branch (KG)', 'Foliage (KG)',
                    'Stem (KG)', 'Crown (KG)', 'Total (KG)'
                ]
                
                # Get all columns from the first record
                all_columns = list(data[0].keys())
                
                # Separate columns: non-biomass first (in original order), then biomass columns
                non_biomass_columns = [col for col in all_columns if col not in biomass_columns]
                biomass_columns_existing = [col for col in biomass_columns if col in all_columns]
                
                # Final headers order: all non-biomass columns first, then biomass columns
                headers = non_biomass_columns + biomass_columns_existing
                
                header_line = "\t".join(headers)
                file.write(header_line + "\n")
                
                # Write data rows
                for item in data:
                    row_values = []
                    for header in headers:
                        value = item.get(header, "")
                        if isinstance(value, (int, float)) and value is not None:
                            if header in biomass_columns:
                                display_value = f"{value:.1f}" if value is not None else "N/A"
                            else:
                                display_value = str(value)
                        else:
                            display_value = str(value) if value is not None else "N/A"
                        row_values.append(display_value)
                    
                    file.write("\t".join(row_values) + "\n")
            
                return True
            return False
    
    except Exception as error:
        print(f"Export error: {error}")
        logger.write(f"[Error] - Failed to export to {file_path}: {error}")
        raise error