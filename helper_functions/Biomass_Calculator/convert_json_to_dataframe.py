def convert_json_to_dataframe(json_file_path):
        """Convert JSON file to DataFrame (basic approach)"""
        try:
            import json
            import pandas as pd
            with open(json_file_path, 'r') as f:
                data = json.load(f)
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error converting JSON to DataFrame: {e}")
            return pd.DataFrame()