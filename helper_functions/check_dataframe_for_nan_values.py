
import pandas as pd
import numpy as np
def check_dataframe_for_nan_values(data_frame: pd.DataFrame) -> tuple:
    """
    Check for NaN values in a DataFrame and generate error reports.

    Args:
        data_frame: pandas DataFrame to check

    Returns:
        tuple: (nan_detected, error_count, error_messages)
    """
   # Check for any NaN values in the entire dataframe
    nan_detected = data_frame.isna().any().any()
    
    if not nan_detected:
        return False, 0, []
    
    # Find rows with NaN values (vectorized - much faster)
    nan_rows = data_frame.isna().any(axis=1)
    error_count = nan_rows.sum()
    
    # Get indices of rows with NaN
    nan_indices = nan_rows[nan_rows].index.tolist()
    
    # Generate error messages efficiently
    error_messages = []
    for idx in nan_indices:
        nan_columns = data_frame.columns[data_frame.loc[idx].isna()].tolist()
        row_data_clean = data_frame.loc[idx].replace({np.nan: None}).to_dict()
        
        error_msg = {
            "index": idx,
            "row_data": row_data_clean,
            "nan_columns": nan_columns
        }
        error_messages.append(error_msg)
    
    print(f"Found {error_count} rows with NaN values")
    return nan_detected, error_count, error_messages