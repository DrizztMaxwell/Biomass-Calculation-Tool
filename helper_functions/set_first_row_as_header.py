import pandas as pd

def set_first_row_as_header(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Promote the first row of the DataFrame to be the column headers
    and remove that row from the data.
    
    Only use this if your DataFrame doesn't have proper column names.
    """
    # Check if we already have proper column names (like 'Plot', 'SubPlot', etc.)
    expected_columns = ['Plot', 'SubPlot', 'Year', 'Origin', 'TreeStatus', 'Species', 'Tree', 'DBH', 'Height']
    
    if all(col in data_frame.columns for col in expected_columns):
        print("✅ DataFrame already has proper column headers - no need to set first row as header")
        print(f"📝 Current columns: {data_frame.columns.tolist()}")
        return data_frame
    
    print("Dataset Information:")
    print(f"Number of columns: {len(data_frame.columns)}")
    print(f"Current columns: {data_frame.columns.tolist()}")
    print(f"Data types: {data_frame.dtypes}")
    
    # Fix: Use proper iloc indexing to avoid the warning
    column_names = [data_frame.iloc[0].iloc[i] for i in range(len(data_frame.columns))]
    print(f"Extracted column names: {column_names}")
    print("===================================")

    # Set column names and remove the first row
    data_frame.columns = column_names
    data_frame = data_frame.iloc[1:].reset_index(drop=True)
    return data_frame