import pandas as pd
import pandas as pd

def convert_columns_to_specific_types(data_frame: pd.DataFrame) -> pd.DataFrame:
    
    """
    Simplified version that handles case-insensitive column names.
    """
    try:
        # Create mapping from lowercase to original column names
        col_mapping = {str(col).lower(): col for col in data_frame.columns}
        
        # Integer columns (nullable) - handle case variations
        integer_columns = ['year', 'tree number', 'speccode']  # Added SpecCode as integer
        for col in integer_columns:
            if col in col_mapping:
                original_col = col_mapping[col]
                data_frame[original_col] = pd.to_numeric(data_frame[original_col], errors='coerce').astype('Int64')

        # String columns - handle case variations (plot is now alphanumeric/string)
        string_columns = ['origin', 'tree status', 'plot']  # Plot as string instead of integer
        for col in string_columns:
            if col in col_mapping:
                original_col = col_mapping[col]
                data_frame[original_col] = data_frame[original_col].astype(str)

        # DBH: Float with 1 decimal - handle case variations
        if 'dbh' in col_mapping:
            original_dbh = col_mapping['dbh']
            data_frame[original_dbh] = pd.to_numeric(data_frame[original_dbh], errors='coerce').round(1)

        # Height: Float with 2 decimals - handle case variations
        if 'height' in col_mapping:
            original_height = col_mapping['height']
            data_frame[original_height] = pd.to_numeric(data_frame[original_height], errors='coerce').round(2)
        
        print("DataFrame columns converted to specific types.")
        return data_frame
    except Exception as e:
        print(f"Error converting DataFrame columns: {e}")
        raise e 