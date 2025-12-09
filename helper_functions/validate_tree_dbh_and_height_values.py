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
    
    # Function to check if values can be converted to float
    def can_convert_to_float(series):
        def is_convertible(value):
            if pd.isna(value):
                return True  # NaN is considered valid for conversion check
            try:
                float(value)
                return True
            except (ValueError, TypeError):
                return False
        return series.apply(is_convertible)
    
    # Check if DBH and Height values can be converted to float
    dbh_convertible_mask = can_convert_to_float(data_frame[dbh_col])
    height_convertible_mask = can_convert_to_float(data_frame[height_col])
    
    # Vectorized validation for numeric ranges (only for convertible values)
    dbh_values_numeric = pd.to_numeric(data_frame[dbh_col], errors='coerce')
    height_values_numeric = pd.to_numeric(data_frame[height_col], errors='coerce')
    
    # Create boolean masks for invalid values
    dbh_range_invalid_mask = (~dbh_values_numeric.isna()) & ((dbh_values_numeric < dbh_min) | (dbh_values_numeric >= dbh_max))
    height_range_invalid_mask = (~height_values_numeric.isna()) & ((height_values_numeric < height_min) | (height_values_numeric > height_max))
    
    # Combine masks to find rows with any invalid values
    conversion_errors_mask = (~dbh_convertible_mask) | (~height_convertible_mask)
    range_errors_mask = dbh_range_invalid_mask | height_range_invalid_mask
    invalid_rows_mask = conversion_errors_mask | range_errors_mask
    
    if not invalid_rows_mask.any():
        # print("✓ No DBH/Height validation errors found")
        return []
    
    # Get indices of invalid rows
    invalid_indices = invalid_rows_mask[invalid_rows_mask].index
    
    # Generate error messages efficiently
    error_messages = []
    for idx in invalid_indices:
        conversion_errors = []
        range_errors = []
        
        # Check conversion errors
        if not dbh_convertible_mask.loc[idx]:
            conversion_errors.append(dbh_col)
        if not height_convertible_mask.loc[idx]:
            conversion_errors.append(height_col)
        
        # Check range errors (only if values are convertible)
        if dbh_convertible_mask.loc[idx] and dbh_range_invalid_mask.loc[idx]:
            range_errors.append(dbh_col)
        if height_convertible_mask.loc[idx] and height_range_invalid_mask.loc[idx]:
            range_errors.append(height_col)
        
        # Convert only the problematic row to dict (more efficient)
        row_data = data_frame.loc[idx].to_dict()
        
        error_msg = {
            'index': idx,
            'row_data': row_data,
            'conversion_errors': conversion_errors,
            'range_errors': range_errors
        }
        error_messages.append(error_msg)
    
    # print(f"Found {len(error_messages)} DBH/Height validation errors")
    return error_messages