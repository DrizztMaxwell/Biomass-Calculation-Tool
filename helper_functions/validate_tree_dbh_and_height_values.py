import pandas as pd
import numpy as np

def validate_tree_dbh_and_height_values(data_frame: pd.DataFrame, dbh_min: float = 2.5, dbh_max: float = 100, height_min: float = 1.3, height_max: float = 50):
    """
    Vectorized validation for DBH and Height values - MUCH faster than iterrows().
    """
    # Create lowercase mapping for case-insensitive column access
    column_mapping = {col.lower(): col for col in data_frame.columns}
    
    # Check if required columns exist
    required_lower = ['dbh', 'height']
    missing_columns = [col for col in required_lower if col not in column_mapping]
    
    if missing_columns:
        # print(f"Warning: Missing required columns: {missing_columns}")
        return []

    # Get original column names
    dbh_col = column_mapping['dbh']
    height_col = column_mapping['height']
    
    # Vectorized validation (much faster than iterrows)
    dbh_values = data_frame[dbh_col]
    height_values = data_frame[height_col]
    
    # Create boolean masks for invalid values
    dbh_invalid_mask = (~dbh_values.isna()) & ((dbh_values < dbh_min) | (dbh_values >= dbh_max))
    height_invalid_mask = (~height_values.isna()) & ((height_values < height_min) | (height_values > height_max))
    
    # Combine masks to find rows with any invalid values
    invalid_rows_mask = dbh_invalid_mask | height_invalid_mask
    
    if not invalid_rows_mask.any():
        # print("✓ No DBH/Height validation errors found")
        return []
    
    # Get indices of invalid rows
    invalid_indices = invalid_rows_mask[invalid_rows_mask].index
    
    # Generate error messages efficiently
    error_messages = []
    for idx in invalid_indices:
        invalid_columns = []
        if dbh_invalid_mask.loc[idx]:
            invalid_columns.append(dbh_col)
        if height_invalid_mask.loc[idx]:
            invalid_columns.append(height_col)
        
        # Convert only the problematic row to dict (more efficient)
        row_data = data_frame.loc[idx].to_dict()
        
        error_msg = {
            'index': idx,
            'row_data': row_data,
            'nan_columns': invalid_columns
        }
        error_messages.append(error_msg)
    
    # print(f"Found {len(error_messages)} DBH/Height validation errors")
    return error_messages