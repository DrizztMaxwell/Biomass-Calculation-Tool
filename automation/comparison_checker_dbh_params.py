import json
import csv
import os
from colorama import Fore, Back, Style, init

# Initialize colorama for colored output
init(autoreset=True)

def load_json_data(json_file_path='data.json'):
    """Load JSON data from file"""
    try:
        with open(json_file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: JSON file '{json_file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Invalid JSON format in '{json_file_path}'.")
        return []

def load_csv_data(csv_file_path='table3.csv'):
    """Load CSV data from file and organize by species and parameter"""
    table_data = {}
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if not all(field in reader.fieldnames for field in ['Species', 'Parameter', 'Estimate']):
                print(f"{Fore.RED}Error: CSV must have 'Species', 'Parameter', and 'Estimate' columns.")
                return {}
            
            for row in reader:
                species = row['Species'].strip()
                param = row['Parameter'].strip()
                
                try:
                    value = float(row['Estimate'])
                except (ValueError, KeyError):
                    continue  # Skip rows with invalid values
                
                if species not in table_data:
                    table_data[species] = {}
                
                table_data[species][param] = value
                
        print(f"{Fore.GREEN}Loaded {sum(len(params) for params in table_data.values())} values from CSV.")
        return table_data
        
    except FileNotFoundError:
        print(f"{Fore.RED}Error: CSV file '{csv_file_path}' not found.")
        return {}

def normalize_species_name(name):
    """Normalize species names for comparison"""
    # Remove extra spaces, convert to lowercase, handle common variations
    name = name.strip().lower()
    
    # Handle common name variations
    variations = {
        'american basswood': 'basswood',
        'american beech': 'beech',
        'northern red oak': 'red oak',
        'american larch': 'tamarack larch',
        'eastern red cedar': 'eastern redcedar',
        'eastern white cedar': 'eastern white-cedar',
        'large-tooth aspen': 'largetooth aspen'
    }
    
    return variations.get(name, name)

def normalize_parameter_name(param):
    """Normalize parameter names for comparison"""
    param = param.strip().lower()
    
    # Map table parameter names to JSON keys
    param_mapping = {
        'b_wood1': 'bwood1',
        'b_wood2': 'bwood2',
        'b_bark1': 'bbark1',
        'b_bark2': 'bbark2',
        'b_branches1': 'bbranches1',
        'b_branches2': 'bbranches2',
        'b_foliage1': 'bfoliage1',
        'b_foliage2': 'bfoliage2',
        'wood1': 'bwood1',
        'wood2': 'bwood2',
        'bark1': 'bbark1',
        'bark2': 'bbark2',
        'branches1': 'bbranches1',
        'branches2': 'bbranches2',
        'foliage1': 'bfoliage1',
        'foliage2': 'bfoliage2'
    }
    
    # Try exact match first
    if param in param_mapping:
        return param_mapping[param]
    
    # Try partial match
    for table_param, json_key in param_mapping.items():
        if table_param.replace('_', '') == param.replace('_', ''):
            return json_key
    
    return param

def compare_values(json_data, table_data, tolerance=0.0001):
    """Compare JSON values with CSV table values"""
    comparison_results = []
    discrepancies = 0
    matches = 0
    not_found_in_table = 0
    not_found_in_json = 0
    
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}COMPARISON RESULTS")
    print(f"{Fore.CYAN}{'='*80}")
    
    # First, check all JSON entries against table
    for json_entry in json_data:
        species_name = json_entry.get('SpecCommon', '').strip()
        norm_species = normalize_species_name(species_name)
        
        print(f"\n{Fore.YELLOW}Species: {species_name}")
        print(f"{Fore.YELLOW}{'-' * 40}")
        
        # Find matching species in table
        table_species_match = None
        for table_species in table_data.keys():
            if normalize_species_name(table_species) == norm_species:
                table_species_match = table_species
                break
        
        if not table_species_match:
            print(f"{Fore.MAGENTA}  Species not found in CSV table")
            not_found_in_table += 1
            continue
        
        # Compare each parameter
        for json_key, json_value in json_entry.items():
            if json_key.startswith('b') and not json_key.startswith('bh'):  # Only compare base parameters
                if json_key in ['SpecCommon', 'SpeciesCode']:
                    continue
                    
                norm_param = normalize_parameter_name(json_key)
                table_value = None
                
                # Look for parameter in table
                for table_param, value in table_data[table_species_match].items():
                    if normalize_parameter_name(table_param) == norm_param:
                        table_value = value
                        break
                
                if table_value is None:
                    print(f"{Fore.MAGENTA}  {json_key}: {json_value} (not in table)")
                    not_found_in_json += 1
                elif abs(json_value - table_value) <= tolerance:
                    print(f"{Fore.GREEN}  ✓ {json_key}: {json_value} = {table_value}")
                    matches += 1
                else:
                    print(f"{Fore.RED}  ✗ {json_key}: {json_value} != {table_value} (diff: {abs(json_value - table_value):.6f})")
                    discrepancies += 1
    
    # Now check for table entries not in JSON
    print(f"\n{Fore.YELLOW}{'='*80}")
    print(f"{Fore.YELLOW}ITEMS IN CSV BUT NOT IN JSON:")
    print(f"{Fore.YELLOW}{'-' * 40}")
    
    for table_species, params in table_data.items():
        norm_table_species = normalize_species_name(table_species)
        
        # Check if species exists in JSON
        species_in_json = False
        for json_entry in json_data:
            if normalize_species_name(json_entry.get('SpecCommon', '')) == norm_table_species:
                species_in_json = True
                break
        
        if not species_in_json:
            print(f"{Fore.MAGENTA}{table_species}: Species not found in JSON")
            continue
        
        # Check each parameter
        for table_param, table_value in params.items():
            norm_table_param = normalize_parameter_name(table_param)
            
            # Find the JSON entry for this species
            json_entry_for_species = None
            for json_entry in json_data:
                if normalize_species_name(json_entry.get('SpecCommon', '')) == norm_table_species:
                    json_entry_for_species = json_entry
                    break
            
            if json_entry_for_species:
                param_found = False
                for json_key in json_entry_for_species.keys():
                    if json_key.startswith('b') and not json_key.startswith('bh'):
                        if normalize_parameter_name(json_key) == norm_table_param:
                            param_found = True
                            break
                
                if not param_found:
                    print(f"{Fore.MAGENTA}  {table_species} - {table_param}: {table_value} (parameter not in JSON)")
    
    # Print summary
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}SUMMARY")
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.GREEN}Matches: {matches}")
    print(f"{Fore.RED}Discrepancies: {discrepancies}")
    print(f"{Fore.MAGENTA}Not found in table: {not_found_in_table}")
    print(f"{Fore.MAGENTA}Not found in JSON: {not_found_in_json}")
    print(f"{Fore.CYAN}{'='*80}")
    
    return comparison_results

def create_sample_csv():
    """Create a sample CSV file if it doesn't exist"""
    sample_data = """Species,Parameter,Estimate,SE
Alpine fir,b_wood1,0.0528,0.0046
Alpine fir,b_wood2,2.4309,0.0268
Alpine fir,b_bark1,0.0108,0.0026
Alpine fir,b_bark2,2.3876,0.0739
Alpine fir,b_branches1,0.0121,0.0033
Alpine fir,b_branches2,2.3519,0.0845
Alpine fir,b_foliage1,0.0251,0.0086
Alpine fir,b_foliage2,2.0389,0.1070
Balsam fir,b_wood1,0.0534,0.0017
Balsam fir,b_wood2,2.4030,0.0103"""
    
    with open('table3_sample.csv', 'w', newline='', encoding='utf-8') as f:
        f.write(sample_data)
    print(f"{Fore.YELLOW}Created sample CSV file: table3_sample.csv")

def main():
    """Main function to run the comparison"""
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}JSON vs CSV COMPARISON TOOL")
    print(f"{Fore.CYAN}{'='*80}")
    
    # File paths
    json_file = 'data.json'  # Save your JSON to this file
    csv_file = 'table3.csv'  # Your CSV file from the previous export
    
    # Check if files exist
    if not os.path.exists(json_file):
        print(f"{Fore.YELLOW}JSON file '{json_file}' not found.")
        print(f"{Fore.YELLOW}Please save your JSON data to '{json_file}'")
        return
    
    if not os.path.exists(csv_file):
        print(f"{Fore.YELLOW}CSV file '{csv_file}' not found.")
        choice = input(f"{Fore.YELLOW}Create a sample CSV file? (y/n): ")
        if choice.lower() == 'y':
            create_sample_csv()
            csv_file = 'table3_sample.csv'
        else:
            print(f"{Fore.RED}Please provide a CSV file for comparison.")
            return
    
    # Load data
    print(f"{Fore.GREEN}Loading JSON data from '{json_file}'...")
    json_data = load_json_data(json_file)
    
    if not json_data:
        return
    
    print(f"{Fore.GREEN}Loading CSV data from '{csv_file}'...")
    table_data = load_csv_data(csv_file)
    
    if not table_data:
        return
    
    # Compare values
    compare_values(json_data, table_data)

if __name__ == "__main__":
    main()