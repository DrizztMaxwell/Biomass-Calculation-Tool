import os
from datetime import datetime

class LogFileTxt:
    _instance = None

    def __new__(cls):
        """Singleton pattern: ensures only one instance exists."""
        if cls._instance is None:
            cls._instance = super(LogFileTxt, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Sets up the folder and file name once."""
        self.folder_name = "log"
        
        # Create folder if it doesn't exist
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
        
        # Format: Log_YYYY-MM-DD_HH-MM-SS.txt
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.file_name = f"Log_{timestamp}.txt"
        self.file_path = os.path.join(self.folder_name, self.file_name)
        
        # Optional: Write an initial line
        self.write("--- Log Session Started ---")

    def write(self, message: str):
        """Appends a timestamped message to the log file."""
        now = datetime.now().strftime("%H:%M:%S")
        with open(self.file_path, "a") as f:
            f.write(f"[{now}] {message}\n")

# Instantiate it once at the module level
logger = LogFileTxt()