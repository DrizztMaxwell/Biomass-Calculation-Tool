import pandas as pd
import pyarrow.parquet as pq
import os

def convert_text_file_into_dataframe(selected_file_path: str) -> pd.DataFrame:
    try:
        # Read with regex separator that handles multiple spaces but preserves "Natural Stand"
        df = pd.read_csv(selected_file_path, sep='\t', header=0)
        
        print("Dataset loaded successfully:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(df.head())
        
        # Convert to Parquet
        parquet_path = selected_file_path.replace('.txt', '.parquet').replace('.csv', '.parquet')
        df.to_parquet(parquet_path, index=False)
        
        # Compare file sizes
        original_size = os.path.getsize(selected_file_path) / 1024 / 1024  # MB
        parquet_size = os.path.getsize(parquet_path) / 1024 / 1024  # MB
        
        print(f"\nParquet conversion completed!")
        print(f"Original file size: {original_size:.2f} MB")
        print(f"Parquet file size: {parquet_size:.2f} MB")
        print(f"Size reduction: {(1 - parquet_size/original_size)*100:.1f}%")
        print(f"Parquet file saved as: {parquet_path}")
        return pd.read_parquet(parquet_path)
        
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Usage example:
# df = convert_text_file_into_dataframe("your_file.txt")