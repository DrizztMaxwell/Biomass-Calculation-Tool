"""
Biomass Calculation Tool - Optimized Build Script
Creates a single optimized executable (.exe) using PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import re

# =============================================================================
# CONFIGURATION
# =============================================================================

ENTRY_POINT = "main.py"
APP_NAME = "BiomassCalculationTool"

DIST_DIR = "dist"
BUILD_DIR = "build"
SPEC_FILE = f"{APP_NAME}.spec"

# Folders bundled into the EXE
ASSETS_TO_BUNDLE = {
    "assets": "assets",
    "manual": "manual",
}

# Runtime files created in AppData
RUNTIME_FILES = [
    "storage/localstorage.json",
    "data/create_species.json",
    "data/selected_database.json",
    "data/treeparameters.json",
]

# Core project packages
REQUIRED_PACKAGES = [
    "views",
    "views.EULA",
    "controller",
    "config",
    "widgets",
    "data",
]

# Modules to EXCLUDE (reduces size)
EXCLUDED_MODULES = [
    "tkinter",
    "pytest",
    "IPython",
    "notebook",
    "jupyter",
    "matplotlib.tests",
    "numpy.tests",
    "pandas.tests",
    "scipy",
    "sympy",
    "torch",
    "tensorflow",
    "sklearn",
    "flet_cli",
    "flet.fastapi",
    "flet.auth",
    "tests",
    "test",
]

# Common imports required
COMMON_IMPORTS = [
    "flet",
    "pandas",
    "numpy",
    "openpyxl",
    "pyodbc",
    "PIL",
    "Pillow",
]

# =============================================================================
# HELPERS
# =============================================================================

def clean():
    """Remove previous builds"""
    print("🧹 Cleaning previous build artifacts")

    for folder in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   removed {folder}")

    if os.path.exists(SPEC_FILE):
        os.remove(SPEC_FILE)
        print(f"   removed {SPEC_FILE}")


def check_entry():
    """Verify entry point exists"""
    if not os.path.exists(ENTRY_POINT):
        print(f"❌ Entry point '{ENTRY_POINT}' not found")
        sys.exit(1)

    print(f"✅ Entry point found: {ENTRY_POINT}")


def is_valid_package(name):
    """Validate module names"""
    if not name:
        return False

    pattern = r"^[a-zA-Z0-9_\-.]+$"
    return bool(re.match(pattern, name))


def collect_assets(project_dir):
    """Collect assets to bundle"""
    print("📦 Collecting asset files")

    data_files = []
    project_dir = Path(project_dir)

    for src, dest in ASSETS_TO_BUNDLE.items():

        src_path = project_dir / src

        if not src_path.exists():
            print(f"⚠️ Missing folder: {src}")
            continue

        count = 0

        for file in src_path.rglob("*"):
            if file.is_file():

                relative_dest = file.relative_to(project_dir).parent
                data_files.append((str(file), str(relative_dest)))
                count += 1

        print(f"   bundled {count} files from {src}/")

    return data_files


def collect_hidden_imports():

    imports = set()

    for pkg in REQUIRED_PACKAGES:
        imports.add(pkg)

    for pkg in COMMON_IMPORTS:
        imports.add(pkg)

    return list(imports)


def read_requirements():
    """Read requirements.txt"""

    imports = set()

    if not os.path.exists("requirements.txt"):
        return []

    print("📋 Reading requirements.txt")

    with open("requirements.txt", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            pkg = line.split("==")[0].split(">=")[0].split("<=")[0]
            pkg = pkg.strip()

            if is_valid_package(pkg):
                imports.add(pkg)

    return list(imports)


def find_icon():
    """Find application icon"""

    icons = [
        "icon.ico",
        "app.ico",
        "logo.ico",
        "assets/icon.ico",
    ]

    for icon in icons:
        if os.path.exists(icon):
            print(f"🎨 Using icon: {icon}")
            return icon

    print("⚠️ No icon found")
    return None


# =============================================================================
# BUILD COMMAND
# =============================================================================

def build_command(data_files, hidden_imports):

    sep = ";" if os.name == "nt" else ":"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",

        "--onefile",
        "--windowed",

        "--name",
        APP_NAME,

        "--clean",
        "--noconfirm",

        "--strip",

        "--upx-dir",
        "upx",
    ]

    # data files
    for src, dest in data_files:
        cmd += ["--add-data", f"{src}{sep}{dest}"]

    # hidden imports
    for module in hidden_imports:
        cmd += ["--hidden-import", module]

    # exclusions
    for module in EXCLUDED_MODULES:
        cmd += ["--exclude-module", module]

    # icon
    icon = find_icon()

    if icon:
        cmd += ["--icon", icon]

    cmd.append(ENTRY_POINT)

    return cmd


# =============================================================================
# MAIN BUILD
# =============================================================================

def main():

    print("=" * 70)
    print(f"Building {APP_NAME}")
    print("=" * 70)

    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__}")
    except ImportError:

        print("Installing PyInstaller")

        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller"],
            check=True
        )

    check_entry()

    clean()

    project_dir = Path(__file__).parent.resolve()

    print(f"📂 Project dir: {project_dir}")

    # collect assets
    data_files = collect_assets(project_dir)

    # imports
    hidden_imports = collect_hidden_imports()
    hidden_imports += read_requirements()

    hidden_imports = list(set(hidden_imports))

    print(f"🔍 Hidden imports: {len(hidden_imports)}")

    # build command
    cmd = build_command(data_files, hidden_imports)

    print("\n🚀 Running PyInstaller\n")

    try:

        subprocess.run(cmd, check=True)

        print("\n" + "=" * 70)
        print("✅ BUILD SUCCESSFUL")
        print("=" * 70)

        exe_path = Path(DIST_DIR) / f"{APP_NAME}.exe"

        print(f"\nExecutable created:")
        print(exe_path)

        print("\nBundled folders:")

        for folder in ASSETS_TO_BUNDLE:
            print(f"   {folder}/")

        print("\nRuntime files (created on first run):")

        for file in RUNTIME_FILES:
            print(f"   {file}")

        print("\nYou can now distribute the EXE.")

    except subprocess.CalledProcessError as e:

        print("\n❌ BUILD FAILED\n")

        print(e)

        sys.exit(1)


if __name__ == "__main__":
    main()