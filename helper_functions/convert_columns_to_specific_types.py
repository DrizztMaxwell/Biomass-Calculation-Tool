import pandas as pd

def convert_columns_to_specific_types(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Convert DataFrame columns to specific data types using column names.
    """
    # Integer columns (nullable)
    integer_columns = ['Plot', 'SubPlot', 'Year', 'Tree']
    for col in integer_columns:
        data_frame[col] = pd.to_numeric(data_frame[col], errors='coerce').astype('Int64')

    # String columns
    string_columns = ['Origin', 'TreeStatus', 'Species']
    for col in string_columns:
        data_frame[col] = data_frame[col].astype(str)

    # DBH: Float with 1 decimal
    data_frame['DBH'] = pd.to_numeric(data_frame['DBH'], errors='coerce').round(1)

    # Height: Float with 2 decimals
    data_frame['Height'] = pd.to_numeric(data_frame['Height'], errors='coerce').round(2)
    
    return data_frame