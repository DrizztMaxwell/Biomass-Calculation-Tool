import pandas as pd
import numpy as np

def convert_columns_to_specific_types(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Enhanced version with better error handling and validation.
    Preserves original values when conversion fails instead of using NaN.
    """
    try:
        # Create mapping from lowercase to original column names
        col_mapping = {str(col).lower(): col for col in data_frame.columns}
        
        # Track conversion results
        conversion_results = {}
        
        # Integer columns with specific types
        int16_columns = ['year', 'tree number']
        for col in int16_columns:
            if col in col_mapping:
                original_col = col_mapping[col]
                before_dtype = data_frame[original_col].dtype
        
                
                # Convert only valid values, keep original for invalid ones
                converted = pd.to_numeric(data_frame[original_col], errors='coerce')
                mask = converted.notna()
                data_frame.loc[mask, original_col] = converted[mask].astype('Int16')
                
                after_dtype = data_frame[original_col].dtype
                conversion_results[original_col] = f"{before_dtype} → {after_dtype}"
                print(f"Converted column '{original_col}' to Int16 where possible. Invalid entries preserved as original.")
        # Species as alphanumeric
        if 'species' in col_mapping:
            original_col = col_mapping['species']
            before_dtype = data_frame[original_col].dtype
            
            converted = pd.to_numeric(data_frame[original_col], errors='coerce')
            mask = converted.notna()
            data_frame.loc[mask, original_col] = converted[mask].astype('Int64')
            
            after_dtype = data_frame[original_col].dtype
            conversion_results[original_col] = f"{before_dtype} → {after_dtype}"

        # String columns
        string_columns = [ 'plot']
        print("CHECKING FOR PLOT")
        for col in string_columns:
            print("AFTYER PLOT")
            print("Coluimns plot detected: ", col)
            if col in col_mapping:
                original_col = col_mapping[col]
                print(f"Converting column '{original_col}' to string...")
                before_dtype = data_frame[original_col].dtype
                data_frame[original_col] = data_frame[original_col].astype('str')
                after_dtype = data_frame[original_col].dtype
                conversion_results[original_col] = f"{before_dtype} → {after_dtype}"

        # Float32 columns
        if 'dbh' in col_mapping:
            original_col = col_mapping['dbh']
            before_dtype = data_frame[original_col].dtype
            
            converted = pd.to_numeric(data_frame[original_col], errors='coerce')
            mask = converted.notna()
            data_frame.loc[mask, original_col] = converted[mask].round(1).astype('float32')
            
            after_dtype = data_frame[original_col].dtype
            conversion_results[original_col] = f"{before_dtype} → {after_dtype}"

        if 'height' in col_mapping:
            original_col = col_mapping['height']
            before_dtype = data_frame[original_col].dtype
            
            converted = pd.to_numeric(data_frame[original_col], errors='coerce')
            mask = converted.notna()
            data_frame.loc[mask, original_col] = converted[mask].round(2).astype('float32')
            
            after_dtype = data_frame[original_col].dtype
            conversion_results[original_col] = f"{before_dtype} → {after_dtype}"
        
        print(data_frame)
        print("DATADKSK:DJ:DW:KWDKO:WK")
        print(data_frame)
        return data_frame
        
    except Exception as e:
        print(f"Error converting DataFrame columns: {e}")
        raise e