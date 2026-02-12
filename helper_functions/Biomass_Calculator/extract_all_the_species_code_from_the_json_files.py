def extract_all_the_species_code_from_the_json_files(json_file_path_1:str, json_file_path_2:str) -> list:
    """Extract all unique species codes from two JSON files."""
    species_codes = set()
    try:
        import json
        with open(json_file_path_1, 'r') as f1, open(json_file_path_2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
            # soem speciescode is ""
            species_codes.update((item['SpecCommon']) for item in data1 if 'SpecCommon' in item and item['SpecCommon'] != "")
            species_codes.update((item['SpecCommon']) for item in data2 if 'SpecCommon' in item and item['SpecCommon'] != "")
            species_codes.update((item['SpeciesCode']) for item in data1 if 'SpeciesCode' in item and item['SpeciesCode'] != "")
            species_codes.update((item['SpeciesCode']) for item in data2 if 'SpeciesCode' in item and item['SpeciesCode'] != "") 
            
            
    except Exception as e:
        print(f"Error extracting species codes: {e}")

    return list(species_codes)