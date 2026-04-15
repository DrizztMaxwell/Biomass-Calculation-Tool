"""
Biomass Calculation Tool - Build Script
Pre-downloads Flet client and bundles it with SSL certificates
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path
import re
import urllib.request
import certifi
import ssl

# ============================================================================
# CONFIGURATION
# ============================================================================
ENTRY_POINT = "main.py"
APP_NAME = "BiomassCalculationTool"
DIST_DIR = "dist"
BUILD_DIR = "build"
FLET_CLIENT_DIR = "flet_client_cache"

# ============================================================================
# PRE-DOWNLOAD FLET CLIENT
# ============================================================================

def download_flet_client():
    """Pre-download the Flet client to bundle with the executable"""
    print("📥 Pre-downloading Flet client...")
    
    # Create SSL context with certifi certificates
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    # Flet client download URL (adjust version as needed)
    import flet
    flet_version = "0.28.3"
    
    # Determine platform
    if sys.platform == "win32":
        platform = "windows"
        file_ext = "zip"
    elif sys.platform == "darwin":
        platform = "macos"
        file_ext = "zip"
    else:
        platform = "linux"
        file_ext = "tar.gz"
    
    download_url = f"https://github.com/flet-dev/flet/releases/download/v{flet_version}/flet_client-{platform}.{file_ext}"
    
    # Create cache directory
    os.makedirs(FLET_CLIENT_DIR, exist_ok=True)
    
    # Download client
    client_path = os.path.join(FLET_CLIENT_DIR, f"flet_client.{file_ext}")
    
    try:
        if not os.path.exists(client_path):
            print(f"   Downloading from: {download_url}")
            req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ssl_context) as response:
                with open(client_path, 'wb') as f:
                    f.write(response.read())
            print(f"   ✅ Downloaded to: {client_path}")
        
        # Extract the client
        if file_ext == "zip":
            import zipfile
            with zipfile.ZipFile(client_path, 'r') as zip_ref:
                zip_ref.extractall(FLET_CLIENT_DIR)
        else:
            import tarfile
            with tarfile.open(client_path, 'r:gz') as tar_ref:
                tar_ref.extractall(FLET_CLIENT_DIR)
        
        print(f"   ✅ Extracted Flet client to: {FLET_CLIENT_DIR}")
        return True
    except Exception as e:
        print(f"   ⚠️ Could not pre-download Flet client: {e}")
        return False

# ============================================================================
# SSL FIX FOR MAIN.PY
# ============================================================================

def create_ssl_fixed_main():
    """Create a temporary main file with SSL fix"""
    print("🔧 Creating SSL-fixed main file...")
    
    ssl_fix_code = '''
# SSL FIX FOR PACKAGED APPLICATION
import os
import sys
import ssl

# Fix SSL certificate verification
if hasattr(sys, '_MEIPASS'):
    # Running from PyInstaller bundle
    cert_path = os.path.join(sys._MEIPASS, 'certifi', 'cacert.pem')
    if os.path.exists(cert_path):
        os.environ['SSL_CERT_FILE'] = cert_path
        os.environ['REQUESTS_CA_BUNDLE'] = cert_path
        os.environ['CURL_CA_BUNDLE'] = cert_path
        
        # For Python's ssl module
        try:
            ssl._create_default_https_context = ssl.create_default_context
        except:
            pass
        
        print(f"SSL certificates loaded from: {cert_path}")
    else:
        # Try alternative path
        alt_cert = os.path.join(sys._MEIPASS, 'cacert.pem')
        if os.path.exists(alt_cert):
            os.environ['SSL_CERT_FILE'] = alt_cert
            print(f"SSL certificates loaded from: {alt_cert}")

# Import your actual main module
if __name__ == "__main__":
    # Import and run your real main
    import main as real_main
    if hasattr(real_main, 'main'):
        import flet as ft
        ft.app(target=real_main.main)
    else:
        print("ERROR: main function not found")
'''
    
    # Write temporary SSL wrapper
    with open("ssl_fixed_main.py", "w") as f:
        f.write(ssl_fix_code)
    
    print("   ✅ Created ssl_fixed_main.py wrapper")
    return "ssl_fixed_main.py"

# ============================================================================
# MAIN BUILD PROCESS
# ============================================================================

def main():
    """Main build process with SSL fix"""
    
    print("=" * 70)
    print(f"  Building {APP_NAME} with FLET CLIENT PRE-DOWNLOAD")
    print("=" * 70)
    print()
    
    # Step 1: Install required packages
    required_packages = ['certifi', 'flet', 'pyinstaller']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
    
    print()
    
    # Step 2: Pre-download Flet client
    download_flet_client()
    print()
    
    # Step 3: Create SSL-fixed main file
    entry_point = create_ssl_fixed_main()
    
    # Step 4: Build with PyInstaller
    print("🚀 Building with PyInstaller...")
    
    separator = ";" if os.name == "nt" else ":"
    
    # Get certifi path
    import certifi
    cert_path = certifi.where()
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", APP_NAME,
        "--clean",
        "--noconfirm",
        "--add-data", f"{cert_path}{separator}certifi",
    ]
    
    # Add data folders if they exist
    for folder in ["assets", "manual", "data"]:
        if os.path.exists(folder):
            cmd.extend(["--add-data", f"{folder}{separator}{folder}"])
            print(f"   Added folder: {folder}")
    
    # Add Flet client cache if exists
    if os.path.exists(FLET_CLIENT_DIR):
        cmd.extend(["--add-data", f"{FLET_CLIENT_DIR}{separator}{FLET_CLIENT_DIR}"])
        print(f"   Added Flet client cache")
    
    # Add hidden imports
    hidden_imports = [
        "flet", "flet_core", "flet_runtime", "certifi", "ssl",
        "views", "views.EULA", "controller", "config", "widgets", "data"
    ]
    
    for module in hidden_imports:
        cmd.extend(["--hidden-import", module])
    
    # Add icon
    if os.path.exists("icon.ico"):
        cmd.extend(["--icon", "icon.ico"])
    
    # Add entry point
    cmd.append(entry_point)
    
    # Run PyInstaller
    try:
        subprocess.run(cmd, check=True)
        print()
        print("=" * 70)
        print("✅ BUILD SUCCESSFUL!")
        print("=" * 70)
        print()
        print(f"📦 Executable: {DIST_DIR}\\{APP_NAME}.exe")
        print()
        print("🔧 SSL CERTIFICATES INCLUDED")
        print("📦 FLET CLIENT INCLUDED")
        print()
        
        # Clean up temporary file
        if os.path.exists("ssl_fixed_main.py"):
            os.remove("ssl_fixed_main.py")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()