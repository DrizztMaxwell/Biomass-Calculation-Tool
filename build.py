import os
import subprocess
import sys
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
ENTRY_POINT = "main.py"
DIST_DIR = "dist"
EXCLUDE_DIRS = [DIST_DIR, "build", "__pycache__", ".git"]

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def collect_asset_folders(base_dir, exclude_dirs=None):
    """
    Recursively collect folders that contain assets (non-Python files) to include with --add-data
    """
    if exclude_dirs is None:
        exclude_dirs = EXCLUDE_DIRS

    add_data = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Skip root folder itself
        if root == base_dir:
            continue

        # Include ALL non-Python files AND Python modules (for proper packaging)
        if files:  # Only if directory has files
            rel_path = os.path.relpath(root, base_dir)
            add_data.append((root, rel_path))
            
            # Also include __init__.py files for package structure
            if "__init__.py" in files:
                init_file = os.path.join(root, "__init__.py")
                add_data.append((init_file, os.path.join(rel_path, "__init__.py")))

    return add_data

def collect_python_packages(base_dir):
    """Collect all Python packages to ensure they're properly included"""
    packages = set()
    for root, dirs, files in os.walk(base_dir):
        if "__init__.py" in files:
            rel_path = os.path.relpath(root, base_dir)
            if rel_path == ".":
                continue
            package_name = rel_path.replace(os.sep, ".")
            packages.add(package_name)
    return packages

# -----------------------------
# BUILD --add-data ARGS
# -----------------------------
project_dir = os.path.dirname(os.path.abspath(__file__))
asset_folders = collect_asset_folders(project_dir)

add_data_args = []
for src, dest in asset_folders:
    sep = ";" if os.name == "nt" else ":"
    add_data_args.extend(["--add-data", f"{src}{sep}{dest}"])

# -----------------------------
# ADD PYTHON PACKAGES AS DATA
# -----------------------------
# This ensures package structure is maintained
packages = collect_python_packages(project_dir)
for package in packages:
    add_data_args.extend(["--hidden-import", package])

# -----------------------------
# IMPORTANT: Add the entire project as data
# -----------------------------
# This ensures all Python files are included
sep = ";" if os.name == "nt" else ":"
add_data_args.extend(["--add-data", f"{project_dir}{sep}."])

# -----------------------------
# FINAL PYINSTALLER COMMAND
# -----------------------------
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", "BiomassCalculationTool",  # Custom name for your exe
    "--clean",  # Clean cache before building
    *add_data_args,
    ENTRY_POINT
]

print("Running PyInstaller with command:")
print(" ".join(cmd))

# -----------------------------
# RUN BUILD
# -----------------------------
try:
    subprocess.run(cmd, check=True)
    print(f"\n✅ Build complete! Check the {DIST_DIR} folder for your exe.")
except subprocess.CalledProcessError as e:
    print(f"\n❌ Build failed: {e}")