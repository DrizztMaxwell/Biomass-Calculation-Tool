import os
import sys
from pathlib import Path

class Assets_Helper:
    def __init__(self):
        self.cache = {}
        self.debug = False  # Set to True for debugging
    
    def is_production(self):
        """Check if running in production mode"""
        return getattr(sys, 'frozen', False)
    
    def get_base_path(self):
        """Get the base path for the current execution context"""
        if self.is_production():
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            if hasattr(sys, '_MEIPASS'):
                return sys._MEIPASS
            # Fallback to executable directory
            return os.path.dirname(sys.executable)
        else:
            # Development mode - get project root
            return str(Path(__file__).parent.parent.parent)
    
    def get_asset_path(self, relative_path):
        """Get absolute path to asset, with caching"""
        print(f"Getting asset path for: {relative_path}")
        if relative_path in self.cache:
            return self.cache[relative_path]
        
        path = self._find_asset(relative_path)
        self.cache[relative_path] = path
        return path
    
    def _find_asset(self, relative_path):
        """Find asset in various possible locations"""
        print(f"Finding asset: {relative_path}")
        # Clean the path
        if relative_path.startswith('./'):
            relative_path = relative_path[2:]
        
        # Remove 'assets/' prefix for consistent searching
        if relative_path.startswith('assets/'):
            asset_subpath = relative_path[7:]  # Remove 'assets/'
        elif relative_path.startswith('assets\\'):
            asset_subpath = relative_path[8:]  # Remove 'assets\\'
        else:
            asset_subpath = relative_path
        
        # Get base path
        base_path = self.get_base_path()
        print(f"Base path: {base_path}")
        # Possible paths to try
        possible_paths = []
        
        if self.is_production():
            print("Running in production mode. Checking for assets in bundled locations...")
            # Production mode paths
            possible_paths = [
                # In _MEIPASS with assets folder structure
                os.path.join(base_path, relative_path),
                os.path.join(base_path, 'assets', asset_subpath),
                # Next to executable
                os.path.join(os.path.dirname(sys.executable), relative_path),
                os.path.join(os.path.dirname(sys.executable), 'assets', asset_subpath),
                # Current working directory
                os.path.join(os.getcwd(), relative_path),
                os.path.join(os.getcwd(), 'assets', asset_subpath),
            ]
        else:
            # Development mode paths
            possible_paths = [
                os.path.join(base_path, relative_path),
                os.path.join(base_path, 'assets', asset_subpath),
                os.path.join(os.getcwd(), relative_path),
                os.path.join(os.getcwd(), 'assets', asset_subpath),
            ]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_paths = []
        for path in possible_paths:
            if path not in seen:
                seen.add(path)
                unique_paths.append(path)
        
        # Try each path
        for path in unique_paths:
            if os.path.exists(path):
                print(f"✅ Found asset at: {path}")
                return path
                if self.debug:
                    print(f"✅ Found asset at: {path}")
                return path
        
        # If not found, log warning and return None
        if self.debug:
            print(f"⚠️ Asset not found: {relative_path}")
            print("   Tried paths:")
            for path in unique_paths:
                print(f"      - {path}")
        
        # Return None to indicate asset not found
        return None

# Create singleton
asset_helper = Assets_Helper()

# Optional: Set debug mode to True for troubleshooting
# asset_helper.debug = True