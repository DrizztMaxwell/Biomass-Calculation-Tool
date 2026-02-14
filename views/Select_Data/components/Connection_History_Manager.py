import os
import json
from datetime import datetime
from constants.Json_File_Path_Constants import json_paths
class Connection_History_Manager:
    """Manages database connection history persistence"""
    
    def __init__(self, history_file=json_paths.CONNECTION_HISTORY_PATH):
        self.history_file = history_file
        self.connection_history = []
        self._load_history()
    
    def _load_history(self):
        """Load connection history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    self.connection_history = json.load(f)
            except Exception:
                self.connection_history = []
    
    def _save_history(self):
        """Save connection history to file"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, "w") as f:
            json.dump(self.connection_history, f, indent=2)
    
    def add_connection(self, server, database):
        """
        Add a new connection to history
        
        Args:
            server: Server name
            database: Database name
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Remove existing entry if present
        self.connection_history = [
            c for c in self.connection_history 
            if not (c["server"] == server and c["database"] == database)
        ]
        
        # Add to beginning
        self.connection_history.insert(0, {
            "server": server, 
            "database": database, 
            "last_used": now
        })
        
        # Keep only last 10
        self.connection_history = self.connection_history[:10]
        self._save_history()
    
    def clear_history(self):
        """Clear all connection history"""
        self.connection_history.clear()
        self._save_history()
    
    def get_history(self):
        """Get the connection history list"""
        return self.connection_history