from typing import Dict, List
from widgets.LogFileTxt import logger
from constants.Biomass_Config import Biomass_Config
def export_to_text_file(file_path) -> bool:
        """Export data to a formatted text file."""
        try:
            data  = []
            # read the data from biomass_results.json
            import json
            with open(Biomass_Config.BIOMASS_RESULTS_PATH, 'r') as f:
                data = json.load(f)
                print(f"Data loaded for export: {data}")
                
            import datetime
            with open(file_path, 'w') as file:
                
                file.write("BIOMASS CALCULATION RESULTS\n")
                file.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Total records: {len(data)}\n\n")
                
                if data:
                    headers = list(data[0].keys())
                    header_line = "\t".join(headers)
                    file.write(header_line + "\n")
                    
                    # Write data rows
                    for item in data:
                        row_values = []
                        for header in headers:
                            value = item.get(header, "")
                            if isinstance(value, (int, float)) and value is not None:
                                if header in Biomass_Config.BIOMASS_COLUMNS:
                                    display_value = f"{value:.4f}" if value is not None else "N/A"
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
    