def convert_columns_to_lowercase(data_frame):
    """
    Convert all column names in the DataFrame to lowercase.
    
    Args:
        data_frame (pd.DataFrame): The DataFrame whose column names need to be converted
        
    Returns:
        pd.DataFrame: DataFrame with all column names in lowercase
    """
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = data_frame.copy()
    
    # Convert all column names to lowercase
    df_copy.columns = [col.lower() for col in df_copy.columns]
    print("Converted column names to lowercase:")
    print(df_copy)
    return df_copy