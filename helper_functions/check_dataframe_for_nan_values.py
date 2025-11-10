
import pandas as pd

def check_dataframe_for_nan_values(data_frame: pd.DataFrame) -> tuple:
    """
    Check for NaN values in a DataFrame and generate error reports.

    Args:
        data_frame: pandas DataFrame to check

    Returns:
        tuple: (nan_detected, error_count, error_messages)
    """
    nan_detected = False
    error_count = 0
    error_messages = []

    for index, row in data_frame.iterrows():
        nan_columns = [data_frame.columns[col_idx] for col_idx, value in enumerate(row) if pd.isna(value)]

        if nan_columns:
            nan_detected = True
            error_count += 1
            
            # Extract clean row data without pandas metadata
            row_data_clean = {}
            for col_name, value in row.items():
                row_data_clean[col_name] = value
            
            error_msg = {
                "index": index,
                "row_data": row_data_clean,  # Clean dictionary instead of pandas Series
                "nan_columns": nan_columns
            }
            
            # Optional: Print formatted error message
            print(f"NaN found at row {index}, columns: {nan_columns}")
            error_messages.append(error_msg)

    return nan_detected, error_count, error_messages