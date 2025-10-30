import csv
import os
from data.data_manager import DataManager


def csv_to_json(csv_file):
    """Convert a CSV (comma or tab-delimited) into JSON using DataManager."""
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        return

    with open(csv_file, "r", encoding="utf-8-sig") as f:
        first_line = f.readline()
        f.seek(0)
        delimiter = "\t" if "\t" in first_line else ","

        reader = csv.DictReader(f, delimiter=delimiter)
        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        data = []
        for row in reader:
            clean_row = {k.strip(): v.strip() for k, v in row.items()}
            data.append(clean_row)

    # Store data via DataManager
    manager = DataManager()
    manager.set_all(data)

    print(f"✅ Imported {len(data)} entries from {csv_file} into localDataset.json")
