# output_generator.py
import csv
from data_manager import DataManager

def generate_csv_output(file_path="biomass_output.csv"):
    """
    Loads data from DataManager and writes selected fields to a CSV file.
    """
    headers = ["SpecCommon", "PlotName", "DBH", "HtTot", "bio_wood", "bio_bark", "bio_foilage", "bio_branches"]

    # Load all entries from DataManager
    manager = DataManager()
    data = manager.get_all()

    if not data:
        print("⚠️ No data available to export.")
        return

    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for entry in data:
                # Only include the selected fields
                row = {key: entry.get(key, "") for key in headers}
                writer.writerow(row)
        print(f"✅ CSV output generated at: {file_path}")
    except Exception as e:
        print(f"❌ Failed to generate CSV: {e}")
