import customtkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from Widgets.CustomErrorBox import CustomErrorBox
from Functions.App_Configuration import set_app_configurations
from Functions.Set_Column_Data_Types import set_column_data_types

# Constants
COLUMN_NAMES = ["Plot", "SubPlot", "Year", "Origin", "Tree", "Status", "Species", "Tree", "DBH", "Height"]
ERROR_COUNT = 0
app = None

# Validation ranges
DBH_MIN = 2.5
DBH_MAX = 100
HEIGHT_MIN = 1.3
HEIGHT_MAX = 50

def validate_dbh_height_values(df):
    """
    Validate DBH and Height values against acceptable ranges.

    Args:
        df: pandas DataFrame to validate

    Returns:
        list: Error messages for invalid DBH/Height values
    """
    error_messages = []

    for index, row in df.iterrows():
        dbh_value = row['DBH']
        height_value = row['Height']
        dbh_invalid = False
        height_invalid = False

        # Validate DBH (0 <= DBH < 100)
        if not pd.isna(dbh_value):
            if dbh_value < DBH_MIN or dbh_value >= DBH_MAX:
                dbh_invalid = True

        # Validate Height (1.5 <= Height <= 50)
        if not pd.isna(height_value):
            if height_value < HEIGHT_MIN or height_value > HEIGHT_MAX:
                height_invalid = True

        if dbh_invalid or height_invalid:
            error_msg = [
                "═══════════════════════════════════════════════════",
                f"🚨 RANGE ERROR: Record #{index + 2}",
                "═══════════════════════════════════════════════════",
                f"📊 Invalid Values Found:",
                f"   - DBH: {dbh_value} (Valid range: {DBH_MIN} <= DBH < {DBH_MAX})" if dbh_invalid else f"   - DBH: ✅ {dbh_value}",
                f"   - Height: {height_value} (Valid range: {HEIGHT_MIN} <= Height <= {HEIGHT_MAX})" if height_invalid else f"   - Height: ✅ {height_value}",
                "",
                "📋 Record Details:",
                "───────────────────────────────────────────────────"
            ]

            # Add all record details
            for col_name, col_value in row.items():
                value_display = "❌ ERROR" if pd.isna(col_value) else f"✅ {col_value}"
                error_msg.append(f"   {col_name:<12}: {value_display}")

            error_msg.append("───────────────────────────────────────────────────")
            error_msg.append("")

            error_messages.append("\n".join(error_msg))

    return error_messages


def get_nan_columns(row, columns):

    return [columns[col_idx] for col_idx, value in enumerate(row) if pd.isna(value)]


def create_error_message(index, row, nan_columns):

    error_msg = [
        "═══════════════════════════════════════════════════",
        f"🚨 ERROR: Record #{index + 2}",
        "═══════════════════════════════════════════════════",
        f"📊 Columns with NaN: {', '.join(nan_columns)}",
        "",
        "📋 Record Details:",
        "───────────────────────────────────────────────────"
    ]

    # Add row details
    for col_name, col_value in row.items():
        value_display = "❌ ERROR" if pd.isna(col_value) else f"✅ {col_value}"
        error_msg.append(f"   {col_name:<12}: {value_display}")

    error_msg.append("───────────────────────────────────────────────────")
    error_msg.append("")

    return "\n".join(error_msg)


def check_nan_values(df):
    """
    Check for NaN values in a DataFrame and generate error reports.

    Args:
        df: pandas DataFrame to check

    Returns:
        tuple: (nan_detected, error_count, error_messages)
    """
    nan_detected = False
    error_count = 0
    error_messages = []

    for index, row in df.iterrows():
        nan_columns = get_nan_columns(row, df.columns)

        if nan_columns:
            nan_detected = True
            error_count += 1
            error_msg = create_error_message(index, row, nan_columns)
            print(error_msg)
            error_messages.append(error_msg)

    return nan_detected, error_count, error_messages


def print_nan_summary(df):
    """Print a summary of NaN values by column."""
    print("\nNaN Summary by Column:")
    nan_summary = df.isna().sum()
    for col_name, nan_count in nan_summary.items():
        if nan_count > 0:
            print(f"   {col_name}: {nan_count} NaN values")


def print_range_violation_summary(df):
    """Print a summary of DBH and Height range violations."""
    dbh_violations = 0
    height_violations = 0

    for index, row in df.iterrows():
        dbh_value = row['DBH']
        height_value = row['Height']

        if not pd.isna(dbh_value) and (dbh_value < DBH_MIN or dbh_value >= DBH_MAX):
            dbh_violations += 1

        if not pd.isna(height_value) and (height_value < HEIGHT_MIN or height_value > HEIGHT_MAX):
            height_violations += 1

    if dbh_violations > 0 or height_violations > 0:
        print("\n📏 Range Violation Summary:")
        if dbh_violations > 0:
            print(f"   DBH: {dbh_violations} values outside range ({DBH_MIN} <= DBH < {DBH_MAX})")
        if height_violations > 0:
            print(f"   Height: {height_violations} values outside range ({HEIGHT_MIN} <= Height <= {HEIGHT_MAX})")


def read_text_file_dataset(file_path):
    """
    Read a text file dataset into a pandas DataFrame.

    Args:
        file_path: Path to the text file

    Returns:
        pandas DataFrame or None if error occurs
    """
    try:
        df = pd.read_csv(file_path, delim_whitespace=True, header=None)
        print("Dataset loaded successfully:")
        print(df)
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def process_dataframe(df):
    """
    Process the DataFrame by setting column names and data types.

    Args:
        df: Raw pandas DataFrame

    Returns:
        pandas DataFrame: Processed DataFrame
    """
    # Extract column names from first row
    column_names = [df.iloc[0][i] for i in range(len(df.columns))]

    print("Dataset Information:")
    print(f"Number of columns: {len(df.columns)}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Data types: {df.dtypes}")
    print(f"Extracted column names: {column_names}")
    print("===================================")

    # Set column names and remove the first row
    df.columns = column_names
    df = df.iloc[1:].reset_index(drop=True)

    # Set data types
    set_column_data_types(data_frame=df)

    print("\nAfter conversion:")
    print(df.info())
    print(df.head())

    return df


def open_text_file(file_path):
    """
    Open and process a text file, checking for data quality issues.

    Args:
        file_path: Path to the text file
    """
    global ERROR_COUNT, app

    # Read the dataset
    df = read_text_file_dataset(file_path)
    if df is None:
        messagebox.showerror("Error", "Failed to read the dataset. Please check if the file is valid.")
        return

    # Process the DataFrame
    df = process_dataframe(df)

    # Check for NaN values
    nan_detected, nan_error_count, nan_error_messages = check_nan_values(df)

    # Check for DBH/Height range violations
    range_error_messages = validate_dbh_height_values(df)
    range_error_count = len(range_error_messages)

    # Combine all errors
    all_error_messages = nan_error_messages + range_error_messages
    total_error_count = nan_error_count + range_error_count
    ERROR_COUNT += total_error_count

    # Print range error messages
    for error_msg in range_error_messages:
        print(error_msg)

    # Report results
    if not nan_detected and range_error_count == 0:
        print("✅ No data quality issues detected in the dataset")
    else:
        if nan_detected:
            print(f"\n🚨 TOTAL RECORDS WITH NaN VALUES: {df.isna().any(axis=1).sum()}")
            print_nan_summary(df)

        if range_error_count > 0:
            print_range_violation_summary(df)

        print(f"\n🚨 TOTAL ERRORS FOUND: {total_error_count}")

    # Show error dialog if errors found
    if total_error_count >= 1:
        CustomErrorBox(
            app,
            title="Data Quality Issues",
            message=f"Found {total_error_count} data quality issues in the dataset. Please fix them.",
            details=all_error_messages
        )


def on_import_button_click():
    """
    Handle import button click event.

    Returns:
        str or None: File path if selected, None otherwise
    """
    file_path = filedialog.askopenfilename(
        title="Select Text File Dataset",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if file_path:
        print(f"Selected file: {file_path}")
        open_text_file(file_path)
        return file_path

    return None


def create_main_ui(root):
    """
    Create the main user interface.

    Args:
        root: The main application window
    """
    # Instruction label
    instruction_label = tk.CTkLabel(
        root,
        text="To begin please import your dataset as a text file (.txt)."
    )
    instruction_label.pack(pady=10)

    # Import button
    import_button = tk.CTkButton(
        root,
        command=on_import_button_click,
        text="Import File",
        text_color="white",
        fg_color="#D71919",
        hover_color="red"
    )
    import_button.pack(pady=5)

    # Begin process button
    begin_button = tk.CTkButton(
        root,
        text="Begin Process",
        fg_color="black",
        text_color="white",
        hover_color="gray"
    )
    begin_button.pack(pady=5)


def main():
    """Main function to initialize and run the application."""
    global app
    app = tk.CTk()

    # Configure application
    set_app_configurations(root=app)

    # Create UI
    create_main_ui(app)

    # Start main loop
    app.mainloop()


if __name__ == "__main__":
    main()