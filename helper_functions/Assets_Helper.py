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
    
    def get_asset_path(self, relative_path):
        """Get absolute path to asset, with caching"""
        if relative_path in self.cache:
            return self.cache[relative_path]
        
        path = self._find_asset(relative_path)
        self.cache[relative_path] = path
        return path
    
    def _find_asset(self, relative_path):
        """Find asset in various possible locations"""
        
        # Clean the path
        if relative_path.startswith('./'):
            relative_path = relative_path[2:]
        
        # Remove 'assets/' prefix for searching
        asset_name = relative_path.replace('assets/', '').replace('assets\\', '')
        
        # Possible base paths to search
        possible_paths = []
        
        if self.is_production():
            # Production mode - multiple possible locations
            possible_paths.extend([
                # Next to executable
                os.path.join(os.path.dirname(sys.executable), relative_path),
                # In a nested assets folder next to executable
                os.path.join(os.path.dirname(sys.executable), 'assets', asset_name),
                # In temp directory (Nuitka sometimes extracts here)
                os.path.join(os.environ.get('TEMP', ''), 'nuitka', 'assets', asset_name),
                # In the current working directory
                os.path.join(os.getcwd(), relative_path),
            ])
        else:
            # Development mode
            # Get project root (assuming this file is in utils folder)
            project_root = Path(__file__).parent.parent
            possible_paths.extend([
                os.path.join(project_root, relative_path),
                os.path.join(project_root, 'assets', asset_name),
                os.path.join(os.getcwd(), relative_path),
            ])
        
        # Try each path
        for path in possible_paths:
            if os.path.exists(path):
                if self.debug:
                    print(f"✅ Found asset at: {path}")
                return path
        
        # If not found, return a fallback and log warning
        if self.debug:
            print(f"⚠️ Asset not found: {relative_path}")
            print("   Tried paths:")
            for path in possible_paths:
                print(f"      - {path}")
        
        # Return original path as fallback (might work in some cases)
        return relative_path

# Create singleton
asset_helper = Assets_Helper()

# Optional: Set debug mode
# asset_helper.debug = True