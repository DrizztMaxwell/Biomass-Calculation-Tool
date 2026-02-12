def extract_all_species_codes_from_local_storage_json(local_storage_data) -> list:
        """Extract all unique species codes from the local storage DataFrame."""
        species_codes = set()
        import pandas as pd
        try:
            for item in local_storage_data['Species']:
                # print(item)
                if item != "" and pd.notna(item):  # Also check for NaN
                    try:
                   
                        int_value = int(item)
                       
                        species_codes.add(int_value)  # Use add() for single values
                    except ValueError:
          
                        species_codes.add(str(item))  # Use add() for single values
        except Exception as e:
            print(f"Error extracting species codes from local storage: {e}")
        
        # Sort the species codes before returning
        species_codes = sorted(species_codes, key=lambda x: str(x))  # Convert to string for mixed type sorting
        return list(species_codes)