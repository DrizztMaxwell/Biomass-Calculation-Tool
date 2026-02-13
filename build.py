"""
Biomass Calculation Tool - Build Script (FIXED)
Creates a single executable (.exe) with all dependencies and files included.
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path
import re

# ============================================================================
# CONFIGURATION
# ============================================================================
ENTRY_POINT = "main.py"
APP_NAME = "BiomassCalculationTool"
DIST_DIR = "dist"
BUILD_DIR = "build"
SPEC_FILE = f"{APP_NAME}.spec"

# Directories to exclude from the build
EXCLUDE_DIRS = {
    DIST_DIR, BUILD_DIR, "__pycache__", ".git", ".github", 
    ".vscode", ".idea", "venv", "env", ".pytest_cache",
    "screenshots", "testing_dataset"
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clean_build_artifacts():
    """Remove previous build artifacts"""
    print("🧹 Cleaning previous build artifacts...")
    
    dirs_to_clean = [DIST_DIR, BUILD_DIR]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed: {dir_name}")
    
    if os.path.exists(SPEC_FILE):
        os.remove(SPEC_FILE)
        print(f"   Removed: {SPEC_FILE}")


def check_entry_point():
    """Verify the entry point exists"""
    if not os.path.exists(ENTRY_POINT):
        print(f"❌ ERROR: Entry point '{ENTRY_POINT}' not found!")
        print(f"   Current directory: {os.getcwd()}")
        sys.exit(1)
    print(f"✅ Entry point found: {ENTRY_POINT}")


def is_valid_package_name(name):
    """Check if a string is a valid Python package name"""
    if not name:
        return False
    # Package names should only contain letters, numbers, underscores, hyphens, and dots
    # Must not contain special characters or binary data
    pattern = r'^[a-zA-Z0-9_\-\.]+$'
    return bool(re.match(pattern, name)) and len(name) < 100


def collect_data_files(base_dir):
    """
    Collect all data files and folders that need to be included in the executable.
    Returns a list of tuples: (source_path, destination_path)
    """
    print("📦 Collecting data files and folders...")
    
    data_files = []
    base_path = Path(base_dir)
    
    # Walk through all directories
    for root, dirs, files in os.walk(base_dir):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        # Skip the base directory itself
        if root == base_dir:
            continue
        
        root_path = Path(root)
        rel_path = root_path.relative_to(base_path)
        
        # Check if directory has any files (not just subdirs)
        if files:
            # Add the entire folder
            data_files.append((str(root_path), str(rel_path)))
            print(f"   Adding folder: {rel_path}")
    
    # Also add specific important files from root if they exist
    important_root_files = [
        "requirements.txt",  # Only .txt, not .parquet
        "MyApp.spec", 
        "flet", 
        "connection_history",
        "data_set", 
        "BCT", 
        ".gitignore"
    ]
    
    for filename in important_root_files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                data_files.append((filepath, filename))
                print(f"   Adding file: {filename}")
    
    return data_files


def collect_hidden_imports(base_dir):
    """
    Collect Python packages that should be explicitly imported.
    This ensures all modules are found by PyInstaller.
    """
    print("🔍 Detecting Python packages...")
    
    hidden_imports = set()
    base_path = Path(base_dir)
    
    # Find all Python packages (directories with __init__.py)
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        if "__init__.py" in files:
            root_path = Path(root)
            
            # Skip the base directory
            if root_path == base_path:
                continue
            
            try:
                rel_path = root_path.relative_to(base_path)
                package_name = str(rel_path).replace(os.sep, ".")
                if is_valid_package_name(package_name):
                    hidden_imports.add(package_name)
                    print(f"   Found package: {package_name}")
            except ValueError:
                continue
    
    # Add common dependencies that might be missed
    common_imports = [
        "flet", 
        "flet_core", 
        "flet_runtime",
        "pandas", 
        "numpy", 
        "openpyxl",
        "pyodbc",
        "matplotlib", 
        "seaborn", 
        "plotly",
        "PIL", 
        "Pillow",
        # Add more based on your requirements.txt
    ]
    
    print("   Adding common dependencies...")
    for imp in common_imports:
        if is_valid_package_name(imp):
            hidden_imports.add(imp)
    
    return list(hidden_imports)


def get_requirements_from_file():
    """Parse requirements.txt ONLY (not .parquet files)"""
    hidden_imports = set()
    
    # ONLY read requirements.txt (text file)
    if os.path.exists("requirements.txt"):
        print(f"📋 Reading requirements.txt...")
        try:
            with open("requirements.txt", 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Extract package name (before ==, >=, etc.)
                    package = line.split('==')[0].split('>=')[0].split('<=')[0].split('[')[0].strip()
                    
                    # Only add if it's a valid package name
                    if is_valid_package_name(package):
                        hidden_imports.add(package)
                        print(f"   Added from requirements: {package}")
        except Exception as e:
            print(f"   Warning: Could not read requirements.txt: {e}")
    
    return list(hidden_imports)


def build_pyinstaller_command(data_files, hidden_imports):
    """Construct the PyInstaller command with all arguments"""
    
    separator = ";" if os.name == "nt" else ":"
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (GUI app)
        "--name", APP_NAME,             # Name of the executable
        "--clean",                      # Clean PyInstaller cache
        "--noconfirm",                  # Replace output directory without asking
    ]
    
    # Add data files
    for src, dest in data_files:
        cmd.extend(["--add-data", f"{src}{separator}{dest}"])
    
    # Add hidden imports (only valid package names)
    for module in hidden_imports:
        if is_valid_package_name(module):
            cmd.extend(["--hidden-import", module])
    
    # Add icon if it exists
    icon_files = ["icon.ico", "app.ico", "logo.ico"]
    for icon in icon_files:
        if os.path.exists(icon):
            cmd.extend(["--icon", icon])
            print(f"📷 Using icon: {icon}")
            break
    
    # Add the entry point
    cmd.append(ENTRY_POINT)
    
    return cmd


# ============================================================================
# MAIN BUILD PROCESS
# ============================================================================

def main():
    """Main build process"""
    
    print("=" * 70)
    print(f"  Building {APP_NAME}")
    print("=" * 70)
    print()
    
    # Step 1: Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✅ PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller is not installed!")
        print("   Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed successfully")
    
    print()
    
    # Step 2: Verify entry point
    check_entry_point()
    print()
    
    # Step 3: Clean previous builds
    clean_build_artifacts()
    print()
    
    # Step 4: Get current directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"📂 Working directory: {project_dir}")
    print()
    
    # Step 5: Collect data files
    data_files = collect_data_files(project_dir)
    print(f"   Total data entries: {len(data_files)}")
    print()
    
    # Step 6: Collect hidden imports
    hidden_imports = collect_hidden_imports(project_dir)
    requirements_imports = get_requirements_from_file()
    
    # Combine and filter to ensure all are valid
    all_imports = list(set(hidden_imports + requirements_imports))
    all_imports = [imp for imp in all_imports if is_valid_package_name(imp)]
    
    print(f"   Total hidden imports: {len(all_imports)}")
    print()
    
    # Step 7: Build the command
    cmd = build_pyinstaller_command(data_files, all_imports)
    
    # Step 8: Display and run the command
    print("=" * 70)
    print("🚀 Running PyInstaller...")
    print("=" * 70)
    print()
    print("Command preview:")
    print(f"   pyinstaller --onefile --windowed --name {APP_NAME} ...")
    print(f"   With {len(data_files)} data folders and {len(all_imports)} hidden imports")
    print()
    print("This may take several minutes...")
    print()
    
    try:
        subprocess.run(cmd, check=True)
        print()
        print("=" * 70)
        print("✅ BUILD SUCCESSFUL!")
        print("=" * 70)
        print()
        print(f"📦 Your executable is ready: {DIST_DIR}\\{APP_NAME}.exe")
        print(f"   Location: {os.path.join(project_dir, DIST_DIR)}")
        print()
        print("You can now distribute this single .exe file!")
        print()
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 70)
        print("❌ BUILD FAILED!")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print("Troubleshooting tips:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that main.py exists and runs without errors")
        print("3. Look at the error messages above for specific issues")
        print("4. Try running with administrator privileges")
        print()
        sys.exit(1)
    
    except KeyboardInterrupt:
        print()
        print("❌ Build cancelled by user")
        sys.exit(1)


if __name__ == "__main__":
    main()