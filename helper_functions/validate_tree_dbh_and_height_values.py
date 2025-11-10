import pandas as pd

def validate_tree_dbh_and_height_values(data_frame: pd.DataFrame, dbh_min: float = 2.5, dbh_max: float = 100, height_min: float = 1.3, height_max: float = 50):
    """
    Validate DBH and Height values against acceptable ranges and return errors in structured format.
    
    Args:
        data_frame: pandas DataFrame to validate
        dbh_min: Minimum valid DBH value
        dbh_max: Maximum valid DBH value  
        height_min: Minimum valid Height value
        height_max: Maximum valid Height value
        
    Returns:
        list: Error messages in structured format [{'index': int, 'row_data': dict, 'nan_columns': list}]
    """
    error_messages = []

    for index, row in data_frame.iterrows():
        dbh_value = row['DBH']
        height_value = row['Height']
        dbh_invalid = False
        height_invalid = False

        # Validate DBH range
        if not pd.isna(dbh_value):
            if dbh_value < dbh_min or dbh_value >= dbh_max:
                dbh_invalid = True

        # Validate Height range
        if not pd.isna(height_value):
            if height_value < height_min or height_value > height_max:
                height_invalid = True

        if dbh_invalid or height_invalid:
            # Convert row to dictionary (removes pandas metadata)
            row_data = row.to_dict()
            
            # Determine which columns are invalid
            invalid_columns = []
            if dbh_invalid:
                invalid_columns.append('DBH')
            if height_invalid:
                invalid_columns.append('Height')
            
            # Create structured error message
            error_msg = {
                'index': index,
                'row_data': row_data,
                'nan_columns': invalid_columns  # Using same key name for consistency
            }
            
            error_messages.append(error_msg)
    
    print(f"Found {len(error_messages)} DBH/Height validation errors")
    return error_messages