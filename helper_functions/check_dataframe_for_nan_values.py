import pandas as pd
import numpy as np

def check_dataframe_for_nan_values(data_frame: pd.DataFrame) -> tuple:
    numeric_columns = {
        'year': 'Int16',
        'tree number': 'Int16',
        'speccode': 'Int64',
        'dbh': 'float',
        'height': 'float'
    }
    
    # Create mapping from lowercase to original column names
    col_mapping = {str(col).lower(): col for col in data_frame.columns}
    
    error_messages = []
    error_count = 0
    
    # Check each row for errors
    for idx in data_frame.index:
        row_errors = []
        nan_columns = []
        row_data = data_frame.loc[idx]
        
        # Check numeric columns for conversion errors
        for col_lower, expected_type in numeric_columns.items():
            if col_lower in col_mapping:
                original_col = col_mapping[col_lower]
                value = row_data[original_col]
                
                # Skip if value is already NaN (will be handled separately)
                if pd.isna(value):
                    nan_columns.append(original_col)
                    continue
                
                # Check if value can be converted to numeric
                is_error = False
                try:
                    if expected_type in ['Int16', 'Int64']:
                        # Check if it's a valid integer
                        numeric_val = pd.to_numeric(value, errors='raise')
                        if not np.isnan(numeric_val):
                            int_val = int(numeric_val)
                            if numeric_val != int_val:
                                is_error = True
                    elif expected_type == 'float':
                        # Check if it's a valid float
                        numeric_val = pd.to_numeric(value, errors='raise')
                        # For float, we just need to check if conversion succeeds
                        # Additional range validation can be added here if needed
                except (ValueError, TypeError):
                    is_error = True
                
                if is_error:
                    nan_columns.append(original_col)
                    row_errors.append(f"{original_col}: '{value}' cannot be converted to {expected_type}")
        
        # If there are errors in this row, add to error messages
        if row_errors or nan_columns:
            error_count += 1
            
            # Convert row data to dictionary, keeping None for NaN values
            row_data_dict = {}
            for col in data_frame.columns:
                val = row_data[col]
                if pd.isna(val):
                    row_data_dict[col] = None
                else:
                    row_data_dict[col] = val
            
            error_msg = {
                "index": int(idx),
                "row_data": row_data_dict,
                "nan_columns": nan_columns  # List of columns with errors/NaN
            }
            error_messages.append(error_msg)
    
    errors_detected = error_count > 0
    
    if errors_detected:
        print(f"\n{'='*60}")
        print(f"VALIDATION ERRORS FOUND: {error_count} rows with issues")
        print(f"{'='*60}")
        print("\nSample errors (first 3 rows):")
        for i, error in enumerate(error_messages[:3]):
            print(f"\n  Row {error['index'] + 1}:")
            print(f"    Columns with errors: {', '.join(error['nan_columns'])}")
    else:
        print("\n✓ No validation errors found - all data types are valid!")
    
    return errors_detected, error_count, error_messages