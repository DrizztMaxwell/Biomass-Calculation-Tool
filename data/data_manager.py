import json
import os
from threading import Lock

class DataManager:
    _instance = None
    _lock = Lock()
    _file_path = os.path.join("storage", "localstorage.json")
    _param_file_path = os.path.join("data", "treeparameters.json")

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._data = []
                cls._instance._load()
            return cls._instance

    # ---------- Core Data Handling ----------
    def _load(self):
        """Load localstorage.json if it exists."""
        if os.path.exists(self._file_path):
            try:
                with open(self._file_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Corrupted localstorage.json — resetting.")
                self._data = []
        else:
            self._data = []

    def save(self):
        """Save current data to localstorage.json."""
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=4, ensure_ascii=False)

    def get_all(self):
        """Return all entries."""
        return self._data

    def set_all(self, new_data):
        """Overwrite entire dataset and save."""
        self._data = new_data
        self.save()

    def add_entry(self, entry):
        """Append one record and save."""
        self._data.append(entry)
        self.save()

    def clear(self):
        """Clear all data."""
        self._data = []
        self.save()

    def update_entry(self, index, updated_values: dict, save=True):
        """Update one entry with new key-value pairs. Optionally defer saving."""
        if 0 <= index < len(self._data):
            self._data[index].update(updated_values)
            if save:
                self.save()

    # ---------- Tree Parameters Merge ----------
    def add_parameters(self):
        """
        Merge treeparameters.json entries into localstorage.json based on SpecCommon (case-insensitive).
        Does not duplicate SpecCommon field.
        """
        if not os.path.exists(self._param_file_path):
            print(f"⚠️ No {self._param_file_path} found — skipping parameter merge.")
            return

        try:
            with open(self._param_file_path, "r", encoding="utf-8") as f:
                param_data = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ Failed to parse {self._param_file_path}.")
            return

        if not isinstance(param_data, list):
            print(f"⚠️ {self._param_file_path} must be a list of parameter objects.")
            return

        # Create a case-insensitive lookup for parameters
        param_lookup = {
            entry.get("SpecCommon", "").strip().lower(): entry
            for entry in param_data if "SpecCommon" in entry
        }

        updated_count = 0

        # Merge parameters into existing data
        for entry in self._data:
            spec_name = entry.get("SpecCommon", "").strip().lower()
            if spec_name in param_lookup:
                param_entry = param_lookup[spec_name].copy()
                param_entry.pop("SpecCommon", None)  # prevent duplication
                entry.update(param_entry)
                updated_count += 1

        self.save()
        print(f"✅ Added parameters to {updated_count} matching species from treeparameters.json.")
