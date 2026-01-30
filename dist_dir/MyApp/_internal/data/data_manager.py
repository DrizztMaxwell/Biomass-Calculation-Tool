
#data_manager.py
import json
import os
from threading import Lock
from data.database_config import get_sql_server_odbc_driver


class DataManager:
    _instance = None
    _lock = Lock()
    _file_path = os.path.join("storage", "localstorage.json")
    _param_file_path = os.path.join("data", "treeparameters.json")
    _db_path: str | None = None  # store path to DB
    

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

    def set_database_path(self, db_name: str):
        """
        Save the database connection info and generate a full ODBC connection string.
        """
        driver = get_sql_server_odbc_driver()

        connection_string = (
            f"Driver={{{driver}}};"
            "Server=.\\SQLEXPRESS;"
            f"Database={db_name};"
            "Trusted_Connection=yes;"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )

        self._db_path = connection_string

        meta_file = os.path.join("storage", "metadata.json")
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "db_name": db_name,
                    "db_path": connection_string
                },
                f,
                indent=4
            )

        print(f"✅ Database connection saved for database: {db_name}")


    def get_database_path(self) -> str | None:
        """Return the last used database path from metadata.json."""

        # Try to load from metadata.json
        meta_file = os.path.join("storage", "metadata.json")
        if os.path.exists(meta_file):
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._db_path = data.get("db_path")
            except json.JSONDecodeError:
                print(f"⚠️ Failed to parse {meta_file}, database path unavailable.")
                self._db_path = None

        return self._db_path

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
