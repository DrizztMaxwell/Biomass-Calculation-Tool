"""
Biomass Calculation Tool - Build Script
Creates a single executable (.exe) with all dependencies and assets bundled inside
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
    "screenshots", "testing_dataset", "app_data"  # Exclude app_data as it's created at runtime
}

# CRITICAL: These folders will be BUNDLED INSIDE the executable
# They will be available at runtime via sys._MEIPASS
ASSETS_TO_BUNDLE = {
    "assets": "assets",  # Bundle entire assets folder
}

# Specific files that will be CREATED at runtime in AppData
# These should NOT be bundled - they'll be created on first run
RUNTIME_FILES = [
    "storage/localstorage.json",
    "data/create_species.json",
    "data/selected_database.json",
    "data/treeparameters.json",
]

# Python packages that must be included
REQUIRED_PACKAGES = [
    "views",
    "views.EULA",
    "controller",
    "config",
    "widgets",
    "data",
]

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
    pattern = r'^[a-zA-Z0-9_\-\.]+$'
    return bool(re.match(pattern, name)) and len(name) < 100


def verify_assets_for_bundling():
    """Verify that assets exist and will be bundled inside the executable"""
    print("🔍 Verifying assets for bundling...")
    
    all_assets_found = True
    
    for asset_folder, _ in ASSETS_TO_BUNDLE.items():
        if os.path.exists(asset_folder) and os.path.isdir(asset_folder):
            # Count all files in asset folder
            total_files = sum([len(files) for _, _, files in os.walk(asset_folder)])
            print(f"   ✅ Found '{asset_folder}/' - will be BUNDLED inside executable ({total_files} files)")
            
            # Check for subfolders
            if asset_folder == "assets":
                images_path = os.path.join(asset_folder, "images")
                fonts_path = os.path.join(asset_folder, "fonts")
                
                if os.path.exists(images_path):
                    img_count = len([f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f))])
                    print(f"      📷 images/ subfolder found ({img_count} files)")
                
                if os.path.exists(fonts_path):
                    font_count = len([f for f in os.listdir(fonts_path) if os.path.isfile(os.path.join(fonts_path, f))])
                    print(f"      🔤 fonts/ subfolder found ({font_count} files)")
        else:
            print(f"   ⚠️  Warning: '{asset_folder}/' not found - will not be bundled")
            all_assets_found = False
    
    if not all_assets_found:
        print("\n⚠️  Some asset folders are missing. The executable will still work,")
        print("   but may lack icons, images, or fonts.")
    
    return all_assets_found


def verify_runtime_files():
    """Verify runtime files structure (these will be created at runtime, not bundled)"""
    print("🔍 Checking runtime files structure...")
    print("   📝 The following files will be CREATED at runtime in %APPDATA%:")
    for file_path in RUNTIME_FILES:
        print(f"      - {file_path}")
    print("   ✅ No need to bundle these - they'll be created on first run")


def collect_bundle_files(base_dir):
    """
    Collect files that need to be BUNDLED INSIDE the executable.
    Returns a list of tuples: (source_path, destination_path)
    This version recursively collects ALL files in assets, preserving folder structure.
    """
    print("📦 Collecting files to BUNDLE inside executable...")
    
    data_files = []
    base_path = Path(base_dir)
    
    # Bundle assets folders recursively
    print("   Bundling asset folders INSIDE executable:")
    for src_folder, dest_folder in ASSETS_TO_BUNDLE.items():
        full_src_path = base_path / src_folder
        if full_src_path.exists() and full_src_path.is_dir():
            # Walk through all files recursively
            for file_path in full_src_path.rglob("*"):
                if file_path.is_file():
                    # Relative path inside project for destination
                    rel_path = file_path.relative_to(base_path).parent
                    data_files.append((str(file_path), str(rel_path)))
                    print(f"      ✔ {file_path.relative_to(base_path)}")
        else:
            print(f"   ⚠️  Warning: '{src_folder}/' not found - will not be bundled")
    
    # Bundle Python packages
    print("   Bundling Python packages:")
    for package in REQUIRED_PACKAGES:
        package_path = base_path / Path(package.replace('.', os.sep))
        if package_path.exists() and package_path.is_dir():
            py_files = list(package_path.rglob("*.py"))
            if py_files:
                data_files.append((str(package_path), package))
                print(f"      Bundled package: {package}/ ({len(py_files)} files)")
    
    # Also add important root files
    important_root_files = ["requirements.txt", ".gitignore"]
    for filename in important_root_files:
        filepath = base_path / filename
        if filepath.exists() and filepath.is_file():
            data_files.append((str(filepath), "."))
            print(f"      Bundled file: {filename}")
    
    print(f"\n   Total items bundled inside executable: {len(data_files)}")
    return data_files


def collect_hidden_imports(base_dir):
    """
    Collect Python packages that should be explicitly imported.
    This ensures all modules are found by PyInstaller.
    """
    print("🔍 Detecting Python packages for import...")
    
    hidden_imports = set()
    
    # Add required packages explicitly
    for package in REQUIRED_PACKAGES:
        hidden_imports.add(package)
        print(f"   Added required package: {package}")
    
    # Add common dependencies
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
        "json",
        "asyncio",
    ]
    
    for imp in common_imports:
        if is_valid_package_name(imp):
            hidden_imports.add(imp)
    
    return list(hidden_imports)


def get_requirements_from_file():
    """Parse requirements.txt"""
    hidden_imports = set()
    
    if os.path.exists("requirements.txt"):
        print(f"📋 Reading requirements.txt...")
        try:
            with open("requirements.txt", 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    package = line.split('==')[0].split('>=')[0].split('<=')[0].split('[')[0].strip()
                    
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
        # "--windowed",                   # No console window (GUI app)
        "--name", APP_NAME,             # Name of the executable
        "--clean",                      # Clean PyInstaller cache
        "--noconfirm",                  # Replace output directory without asking
        "--upx-dir", "upx",             # Enable UPX compression
    ]
    
    # Add data files to bundle inside executable
    for src, dest in data_files:
        cmd.extend(["--add-data", f"{src}{separator}{dest}"])
    cmd.extend(["--add-data", f"assets{separator}assets"])  # Add an extra dummy entry to ensure at least one --add-data is present assets folder

    
    # Add hidden imports
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
    print(f"  Building {APP_NAME} with ASSETS BUNDLED INSIDE")
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
    
    # Step 3: Verify assets for bundling
    verify_assets_for_bundling()
    print()
    
    # Step 4: Check runtime files (these will be created at runtime)
    verify_runtime_files()
    print()
    
    # Step 5: Clean previous builds
    clean_build_artifacts()
    print()
    
    # Step 6: Get current directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"📂 Working directory: {project_dir}")
    print()
    
    # Step 7: Collect files to bundle inside executable
    data_files = collect_bundle_files(project_dir)
    print(f"\n   Total items bundled inside executable: {len(data_files)}")
    print()
    
    # Step 8: Collect hidden imports
    hidden_imports = collect_hidden_imports(project_dir)
    requirements_imports = get_requirements_from_file()
    
    all_imports = list(set(hidden_imports + requirements_imports))
    all_imports = [imp for imp in all_imports if is_valid_package_name(imp)]
    
    print(f"   Total hidden imports: {len(all_imports)}")
    print()
    
    # Step 9: Build the command
    cmd = build_pyinstaller_command(data_files, all_imports)
    
    # Step 10: Display and run the command
    print("=" * 70)
    print("🚀 Running PyInstaller...")
    print("=" * 70)
    print()
    print("📦 ASSETS ARE BEING BUNDLED INSIDE THE EXECUTABLE")
    print("   They will be extracted to a temp folder at runtime")
    print()
    print(f"   Bundling {len(data_files)} data folders/files")
    print(f"   Including {len(all_imports)} hidden imports")
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
        print("🎯 ASSETS BUNDLED INSIDE THE EXECUTABLE:")
        for asset_folder in ASSETS_TO_BUNDLE.keys():
            print(f"   - {asset_folder}/ (entire folder)")
        
        print("\n📝 RUNTIME FILES (created on first run in %APPDATA%):")
        for file_path in RUNTIME_FILES[:3]:  # Show first 3
            print(f"   - {file_path}")
        if len(RUNTIME_FILES) > 3:
            print(f"   - ... and {len(RUNTIME_FILES)-3} more")
        
        print()
        print("✨ You can now distribute this single .exe file anywhere!")
        print("   The executable contains ALL assets inside it.")
        print("   User data will be stored in %APPDATA%/BiomassCalculationTool/")
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