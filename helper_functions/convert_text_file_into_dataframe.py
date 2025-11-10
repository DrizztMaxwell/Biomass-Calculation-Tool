import pandas as pd


def convert_text_file_into_dataframe(selected_file_path: str) -> pd.DataFrame:
    try:
        # Read with regex separator that handles multiple spaces but preserves "Natural Stand"
        df = pd.read_csv(selected_file_path, sep='\t', header=0)
        
        print("Dataset loaded successfully:")
        print(df)
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        return None