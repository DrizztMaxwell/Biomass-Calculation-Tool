import pandas as pd


def do_mandatory_columns_exist(data_frame: pd.DataFrame) -> bool:
   
    required_columns = ['plot', 'year', 'origin', 'tree status', 'tree number', 'dbh', 'height', 'speccode']
    
    # Get the actual column names from the DataFrame (in lowercase for case-insensitive comparison)
    actual_columns = [col.lower() for col in data_frame.columns]
    
    # Find missing columns
    missing_columns = [req_col for req_col in required_columns if req_col not in actual_columns]
    
    if missing_columns:
        # Create a helpful error message
        error_message = f"Missing required columns: {missing_columns}\n"
        error_message += f"Available columns: {list(data_frame.columns)}"
        raise ValueError(error_message)
    
    print(f"✓ All required columns are present: {required_columns}")
    return True