import json
import os
from threading import Lock

class DataManager:
    _instance = None
    _lock = Lock()
    _file_path = "localstorage.json"  # match your previous references

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._data = []
                cls._instance._load()
            return cls._instance

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