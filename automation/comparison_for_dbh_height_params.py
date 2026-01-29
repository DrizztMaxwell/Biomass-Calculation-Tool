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

def load_csv_data(csv_file_path='table4.csv'):
    """Load CSV data from file and organize by species and parameter"""
    table_data = {}
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Check required columns
            required_columns = ['Species', 'Parameter', 'Estimate']
            if not all(field in reader.fieldnames for field in required_columns):
                print(f"{Fore.RED}Error: CSV must have {required_columns} columns.")
                print(f"{Fore.RED}Found columns: {list(reader.fieldnames)}")
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
                
        total_values = sum(len(params) for params in table_data.values())
        print(f"{Fore.GREEN}Loaded {total_values} parameter values for {len(table_data)} species from CSV.")
        return table_data
        
    except FileNotFoundError:
        print(f"{Fore.RED}Error: CSV file '{csv_file_path}' not found.")
        return {}

def normalize_species_name(name):
    """Normalize species names for comparison"""
    if not name:
        return ""
    
    name = name.strip().lower()
    
    # Handle common name variations
    variations = {
        'alpine fir': 'alpine fir',
        'balsam fir': 'balsam fir',
        'balsam poplar': 'balsam poplar',
        'american basswood': 'basswood',
        'american beech': 'beech',
        'black ash': 'black ash',
        'black cherry': 'black cherry',
        'black spruce': 'black spruce',
        'eastern hemlock': 'eastern hemlock',
        'eastern red cedar': 'eastern redcedar',
        'eastern white cedar': 'eastern white-cedar',
        'eastern white pine': 'eastern white pine',
        'grey birch': 'grey birch',
        'hickory': 'hickory',
        'hop-hornbeam': 'hop-hornbeam',
        'jack pine': 'jack pine',
        'large-tooth aspen': 'largetooth aspen',
        'lodgepole pine': 'lodgepole pine',
        'red ash': 'red ash',
        'red maple': 'red maple',
        'northern red oak': 'red oak',
        'red pine': 'red pine',
        'red spruce': 'red spruce',
        'silver maple': 'silver maple',
        'sugar maple': 'sugar maple',
        'american larch': 'tamarack larch',
        'trembling aspen': 'trembling aspen',
        'white ash': 'white ash',
        'white birch': 'white birch',
        'white elm': 'white elm',
        'white oak': 'white oak',
        'white spruce': 'white spruce',
        'yellow birch': 'yellow birch',
        'hardwood': 'hardwood',
        'softwood': 'softwood',
        'all': 'all'
    }
    
    # Try exact match first
    for key, normalized in variations.items():
        if name == key.lower():
            return normalized
    
    # Try partial match
    for key, normalized in variations.items():
        if key.lower() in name or name in key.lower():
            return normalized
    
    return name

def normalize_parameter_name(param):
    """Normalize parameter names for comparison"""
    param = param.strip().lower()
    
    # Map JSON bh parameters to table parameter names
    param_mapping = {
        'bhwood1': 'b_wood1',
        'bhwood2': 'b_wood2',
        'bhwood3': 'b_wood3',
        'bhbark1': 'b_bark1',
        'bhbark2': 'b_bark2',
        'bhbark3': 'b_bark3',
        'bhbranches1': 'b_branches1',
        'bhbranches2': 'b_branches2',
        'bhbranches3': 'b_branches3',
        'bhfoliage1': 'b_foliage1',
        'bhfoliage2': 'b_foliage2',
        'bhfoliage3': 'b_foliage3'
    }
    
    # Try exact match first
    if param in param_mapping:
        return param_mapping[param]
    
    # Try removing 'h' from 'bh' parameters
    if param.startswith('bh'):
        base_param = param[1:]  # Remove the 'h'
        if base_param in param_mapping:
            return param_mapping[base_param]
    
    # Try with underscore variations
    for json_param, table_param in param_mapping.items():
        if json_param.replace('_', '').lower() == param.replace('_', '').lower():
            return table_param
    
    return param

def compare_bh_values(json_data, table_data, tolerance=0.0001):
    """Compare JSON bh (dbh+height) values with CSV table values"""
    comparison_results = []
    discrepancies = 0
    matches = 0
    not_found_in_table = 0
    not_found_in_json = 0
    
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}COMPARISON OF DBH+HEIGHT PARAMETERS (bh*)")
    print(f"{Fore.CYAN}{'='*80}")
    
    # Define which parameters to compare (all bh* parameters)
    bh_parameters = ['bhwood1', 'bhwood2', 'bhwood3', 
                     'bhbark1', 'bhbark2', 'bhbark3',
                     'bhbranches1', 'bhbranches2', 'bhbranches3',
                     'bhfoliage1', 'bhfoliage2', 'bhfoliage3']
    
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
        
        # Compare each bh parameter
        for param in bh_parameters:
            if param in json_entry:
                json_value = json_entry[param]
                norm_param = normalize_parameter_name(param)
                table_value = None
                
                # Look for parameter in table
                for table_param, value in table_data[table_species_match].items():
                    if normalize_parameter_name(table_param) == norm_param:
                        table_value = value
                        break
                
                if table_value is None:
                    print(f"{Fore.MAGENTA}  {param}: {json_value} (not in table)")
                    not_found_in_json += 1
                elif abs(json_value - table_value) <= tolerance:
                    print(f"{Fore.GREEN}  ✓ {param}: {json_value} = {table_value}")
                    matches += 1
                else:
                    diff = abs(json_value - table_value)
                    print(f"{Fore.RED}  ✗ {param}: {json_value} != {table_value} (diff: {diff:.6f})")
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
                for param in bh_parameters:
                    if normalize_parameter_name(param) == norm_table_param:
                        param_found = True
                        break
                
                if not param_found:
                    print(f"{Fore.MAGENTA}  {table_species} - {table_param}: {table_value} (parameter not in JSON)")
    
    # Print summary
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}SUMMARY FOR DBH+HEIGHT PARAMETERS")
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.GREEN}Matches: {matches}")
    print(f"{Fore.RED}Discrepancies: {discrepancies}")
    print(f"{Fore.MAGENTA}Not found in table: {not_found_in_table}")
    print(f"{Fore.MAGENTA}Not found in JSON: {not_found_in_json}")
    print(f"{Fore.CYAN}Total parameters checked: {matches + discrepancies + not_found_in_json}")
    print(f"{Fore.CYAN}{'='*80}")
    
    return comparison_results

def create_table4_csv():
    """Create a CSV file for Table 4 data from the PDF"""
    # This is sample data - you should replace with actual Table 4 data
    table4_data = """Species,Parameter,Estimate,SE
Alpine fir,bwood1,0.0268,0.0023
Alpine fir,bwood2,1.7579,0.0577
Alpine fir,bwood3,0.9871,0.0794
Alpine fir,bbark1,0.0009,0.0004
Alpine fir,bbark2,1.4460,0.2504
Alpine fir,bbark3,1.8839,0.3653
Alpine fir,bbranches1,0.0470,0.0085
Alpine fir,bbranches2,2.9288,0.2044
Alpine fir,bbranches3,-1.1588,0.2155
Alpine fir,bfoliage1,0.0551,0.0151
Alpine fir,bfoliage2,1.7585,0.0885
Balsam fir,bwood1,0.0294,0.0008
Balsam fir,bwood2,1.8357,0.0163
Balsam fir,bwood3,0.8640,0.0213
Balsam fir,bbark1,0.0053,0.0004
Balsam fir,bbark2,2.0876,0.0388
Balsam fir,bbark3,0.5842,0.0506
Balsam fir,bbranches1,0.0117,0.0008
Balsam fir,bbranches2,3.5097,0.0667
Balsam fir,bbranches3,-1.3006,0.0773
Balsam fir,bfoliage1,0.1245,0.0073
Balsam fir,bfoliage2,2.5230,0.0750
Balsam fir,bfoliage3,-1.1230,0.0878"""
    
    with open('table4_sample.csv', 'w', newline='', encoding='utf-8') as f:
        f.write(table4_data)
    print(f"{Fore.YELLOW}Created sample Table 4 CSV file: table4_sample.csv")

def main():
    """Main function to run the comparison for dbh+height parameters"""
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}JSON vs CSV COMPARISON - DBH+HEIGHT PARAMETERS (bh*)")
    print(f"{Fore.CYAN}{'='*80}")
    
    # File paths
    json_file = 'data.json'  # Your JSON data file
    csv_file = 'table4.csv'  # CSV file with Table 4 data
    
    # Check if files exist
    if not os.path.exists(json_file):
        print(f"{Fore.YELLOW}JSON file '{json_file}' not found.")
        print(f"{Fore.YELLOW}Please save your JSON data to '{json_file}'")
        return
    
    if not os.path.exists(csv_file):
        print(f"{Fore.YELLOW}CSV file '{csv_file}' not found.")
        print(f"{Fore.YELLOW}Table 4 contains dbh+height parameters from the PDF.")
        print(f"{Fore.YELLOW}You need to extract Table 4 data from the PDF into CSV format.")
        choice = input(f"{Fore.YELLOW}Create a sample CSV file? (y/n): ")
        if choice.lower() == 'y':
            create_table4_csv()
            csv_file = 'table4_sample.csv'
        else:
            print(f"{Fore.RED}Please provide a CSV file with Table 4 data for comparison.")
            print(f"{Fore.YELLOW}Table 4 should contain parameters like bwood1, bwood2, bwood3, etc.")
            return
    
    # Load data
    print(f"{Fore.GREEN}Loading JSON data from '{json_file}'...")
    json_data = load_json_data(json_file)
    
    if not json_data:
        print(f"{Fore.RED}No JSON data loaded. Please check your JSON file.")
        return
    
    print(f"{Fore.GREEN}Loading CSV data from '{csv_file}'...")
    table_data = load_csv_data(csv_file)
    
    if not table_data:
        print(f"{Fore.RED}No CSV data loaded. Please check your CSV file.")
        return
    
    # Compare dbh+height values
    compare_bh_values(json_data, table_data, tolerance=0.001)

if __name__ == "__main__":
    main()