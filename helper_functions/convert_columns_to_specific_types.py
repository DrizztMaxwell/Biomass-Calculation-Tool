import pandas as pd
import numpy as np

def convert_columns_to_specific_types(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Enhanced version with better error handling and validation.
    """
    try:
        # Create mapping from lowercase to original column names
        col_mapping = {str(col).lower(): col for col in data_frame.columns}
        
        # print("Starting data type conversion...")
        
        # Track conversion results
        conversion_results = {}
        
        # Integer columns with specific types
        int16_columns = ['year', 'tree number']
        for col in int16_columns:
            if col in col_mapping:
                original_col = col_mapping[col]
                before_dtype = data_frame[original_col].dtype
                data_frame[original_col] = pd.to_numeric(data_frame[original_col], errors='coerce').astype('Int16')
                after_dtype = data_frame[original_col].dtype
                conversion_results[original_col] = f"{before_dtype} → {after_dtype}"
        
        # Speccode as Int64
        if 'speccode' in col_mapping:
            original_col = col_mapping['speccode']
            before_dtype = data_frame[original_col].dtype
            data_frame[original_col] = pd.to_numeric(data_frame[original_col], errors='coerce').astype('Int64')
            after_dtype = data_frame[original_col].dtype
            conversion_results[original_col] = f"{before_dtype} → {after_dtype}"

        # String columns
        string_columns = ['origin', 'tree status', 'plot']
        for col in string_columns:
            if col in col_mapping:
                original_col = col_mapping[col]
                before_dtype = data_frame[original_col].dtype
                data_frame[original_col] = data_frame[original_col].astype(str)
                after_dtype = data_frame[original_col].dtype
                conversion_results[original_col] = f"{before_dtype} → {after_dtype}"

        # Float32 columns
        if 'dbh' in col_mapping:
            original_col = col_mapping['dbh']
            before_dtype = data_frame[original_col].dtype
            data_frame[original_col] = pd.to_numeric(data_frame[original_col], errors='coerce').round(1).astype('float32')
            after_dtype = data_frame[original_col].dtype
            conversion_results[original_col] = f"{before_dtype} → {after_dtype}"

        if 'height' in col_mapping:
            original_col = col_mapping['height']
            before_dtype = data_frame[original_col].dtype
            data_frame[original_col] = pd.to_numeric(data_frame[original_col], errors='coerce').round(2).astype('float32')
            after_dtype = data_frame[original_col].dtype
            conversion_results[original_col] = f"{before_dtype} → {after_dtype}"
        
        # # Print conversion summary
        # print("\n" + "="*50)
        # print("DATA TYPE CONVERSION SUMMARY")
        # print("="*50)
        # for col, conversion in conversion_results.items():
        #     print(f"✓ {col:15} : {conversion}")
        print(data_frame)
        print("DATADKSK:DJ:DW:KWDKO:WK")
        return data_frame
        
    except Exception as e:
        print(f"Error converting DataFrame columns: {e}")
        raise e
