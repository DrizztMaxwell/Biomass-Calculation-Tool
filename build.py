# build_pyinstaller.py
import os
import sys
import subprocess
import shutil
import glob
from pathlib import Path

def clean_previous_builds():
    """Remove previous build artifacts"""
    folders_to_remove = ['build', 'dist', '__pycache__', '*.spec']
    
    for folder in folders_to_remove[:3]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Cleaned: {folder}")
    
    # Remove .spec files
    for spec_file in glob.glob("*.spec"):
        os.remove(spec_file)
        print(f"Cleaned: {spec_file}")

def get_file_size(path):
    """Get file size in MB"""
    if os.path.exists(path):
        return os.path.getsize(path) / 1024 / 1024
    return 0

def optimize_imports():
    """Try to optimize imports for smaller size"""
    print("\nAnalyzing imports for optimization...")
    
    # Common large libraries and their alternatives
    large_libs = {
        'pandas': 'Consider using built-in csv module for simple CSV operations',
        'numpy': 'Use math module for basic math operations if possible',
        'matplotlib': 'Only include if plotting is essential',
        'scipy': 'Very large, avoid if possible',
        'sklearn': 'Very large, consider alternatives',
    }
    
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        for lib, suggestion in large_libs.items():
            if f'import {lib}' in content or f'from {lib}' in content:
                print(f"⚠️  Found {lib}: {suggestion}")
    except:
        pass

def create_spec_file():
    """Create optimized PyInstaller spec file"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include assets folder
        ('assets', 'assets'),
        # Include data files
        ('data/*.json', 'data'),
        ('storage/*', 'storage'),
        # Include any required DLLs or resources
    ],
    hiddenimports=[
        # Add any hidden imports here
        'pandas',
        'numpy',
        'pyodbc',
        'flet',
        'PIL',
        'tkinter',
        'json',
        'csv',
        'datetime',
        'os',
        'sys',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'matplotlib',
        'scipy',
        'sklearn',
        'notebook',
        'IPython',
        'tensorflow',
        'torch',
        'keras',
        'django',
        'flask',
        'sqlalchemy',
        # Development tools
        'pdb',
        'pytest',
        'unittest',
        'doctest',
        # GUI frameworks (if not using)
        'PyQt5',
        'PySide2',
        'wx',
        'tkinter',  # Only exclude if not using
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# UPX compression
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,          # Reduce size
    upx=True,           # Enable UPX compression
    upx_exclude=[],     # Files to exclude from UPX
    runtime_tmpdir=None,
    console=False,      # Change to True if you need console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)

# For onefile mode
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MyApp',
)
"""
    
    with open('myapp.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("Created optimized spec file: myapp.spec")

def build_onefile():
    """Build single executable file"""
    print("\nBuilding onefile executable...")
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--noconsole',  # Change to --console if you need terminal
        '--clean',
        '--noupx',  # We'll apply UPX separately for better control
        '--name', 'MyApp',
        '--distpath', 'dist',
        '--workpath', 'build',
        '--specpath', '.',
    ]
    
    # Add icon if exists
    if os.path.exists('assets/icon.ico'):
        cmd.extend(['--icon', 'assets/icon.ico'])
    
    # Add hidden imports
    for imp in ['pandas', 'pyodbc', 'flet', 'numpy', 'PIL', 'tkinter']:
        cmd.extend(['--hidden-import', imp])
    
    # Add data files
    data_dirs = ['assets', 'data', 'storage']
    for d in data_dirs:
        if os.path.exists(d):
            cmd.extend(['--add-data', f'{d}{os.pathsep}{d}'])
    
    # Add main script
    cmd.append('main.py')
    
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            exe_path = 'dist/MyApp.exe'
            if os.path.exists(exe_path):
                size = get_file_size(exe_path)
                print(f"✓ Onefile build successful: {size:.2f} MB")
                return exe_path
            else:
                print("✗ Executable not found")
        else:
            print(f"✗ Build failed: {result.stderr[:500]}")
            
    except Exception as e:
        print(f"✗ Error: {e}")
    
    return None

def build_onedir():
    """Build directory distribution (smaller, faster to build)"""
    print("\nBuilding onedir distribution...")
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onedir',
        '--noconsole',
        '--clean',
        '--noupx',
        '--name', 'MyApp',
        '--distpath', 'dist_dir',
        '--workpath', 'build',
    ]
    
    if os.path.exists('assets/icon.ico'):
        cmd.extend(['--icon', 'assets/icon.ico'])
    
    for imp in ['pandas', 'pyodbc', 'flet', 'numpy', 'PIL', 'tkinter']:
        cmd.extend(['--hidden-import', imp])
    
    data_dirs = ['assets', 'data', 'storage']
    for d in data_dirs:
        if os.path.exists(d):
            cmd.extend(['--add-data', f'{d}{os.pathsep}{d}'])
    
    cmd.append('main.py')
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            dir_path = 'dist_dir/MyApp'
            if os.path.exists(dir_path):
                # Calculate total size
                total_size = 0
                for path, dirs, files in os.walk(dir_path):
                    for f in files:
                        fp = os.path.join(path, f)
                        total_size += os.path.getsize(fp)
                size_mb = total_size / 1024 / 1024
                print(f"✓ Onedir build successful: {size_mb:.2f} MB")
                return dir_path
    except Exception as e:
        print(f"✗ Error: {e}")
    
    return None

def apply_upx_compression(exe_path):
    """Apply UPX compression for smaller size"""
    if not os.path.exists(exe_path):
        return False
    
    print(f"\nApplying UPX compression to {exe_path}...")
    
    original_size = get_file_size(exe_path)
    
    # Try to find UPX
    upx_paths = [
        'upx',
        'C:\\upx\\upx.exe',
        'C:\\Program Files\\upx\\upx.exe',
        os.path.join(os.getcwd(), 'upx.exe'),
    ]
    
    upx_found = None
    for path in upx_paths:
        try:
            subprocess.run([path, '--version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
            upx_found = path
            print(f"Found UPX at: {path}")
            break
        except:
            continue
    
    if not upx_found:
        print("UPX not found. Download from: https://upx.github.io/")
        print("Place upx.exe in your project folder or C:\\upx\\")
        return False
    
    # Try different compression levels
    levels = [
        ['--best'],          # Best compression
        ['-9'],              # Level 9
        ['-8'],              # Level 8
        ['--lzma'],          # LZMA compression
    ]
    
    backup_path = exe_path.replace('.exe', '_backup.exe')
    shutil.copy2(exe_path, backup_path)
    
    for level in levels:
        try:
            cmd = [upx_found] + level + [exe_path]
            print(f"Trying: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True,
                                  timeout=300)  # 5 minute timeout
            
            if result.returncode == 0:
                new_size = get_file_size(exe_path)
                reduction = ((original_size - new_size) / original_size) * 100
                print(f"✓ Compressed: {new_size:.2f} MB ({reduction:.1f}% reduction)")
                return True
            else:
                # Restore backup and try next level
                shutil.copy2(backup_path, exe_path)
                
        except subprocess.TimeoutExpired:
            print(f"  Timeout with {level}, trying next...")
            shutil.copy2(backup_path, exe_path)
            continue
        except Exception as e:
            print(f"  Error: {e}")
            shutil.copy2(backup_path, exe_path)
            continue
    
    # Restore original if all compression failed
    shutil.copy2(backup_path, exe_path)
    os.remove(backup_path)
    print("✗ UPX compression failed, using original")
    return False

def optimize_with_pip_auto():
    """Use pip-auto to remove unused imports"""
    print("\nOptimizing imports with pip-auto...")
    
    try:
        # Install pip-auto if not present
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pip-auto'], 
                      capture_output=True)
        
        # Create requirements.txt if not exists
        if not os.path.exists('requirements.txt'):
            subprocess.run([sys.executable, '-m', 'pip', 'freeze'], 
                          capture_output=True)
        
        # Use pip-auto to clean
        subprocess.run([sys.executable, '-m', 'pip_auto', 'requirements.txt'], 
                      capture_output=True)
        
        print("✓ Imports optimized")
        return True
    except:
        print("⚠️  pip-auto not available, skipping import optimization")
        return False

def install_dependencies():
    """Install required packages"""
    print("\nInstalling PyInstaller...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 
                       'pyinstaller', '--upgrade'], 
                      check=True, capture_output=True)
        
        # Install UPX for compression
        print("\nFor best compression, download UPX from:")
        print("https://github.com/upx/upx/releases")
        print("Place upx.exe in C:\\upx\\ or project folder")
        
        return True
    except Exception as e:
        print(f"✗ Failed to install PyInstaller: {e}")
        return False

def main():
    print("="*60)
    print("PyInstaller Build System")
    print("Optimized for Small Size")
    print("="*60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except:
        print("PyInstaller not found. Installing...")
        if not install_dependencies():
            return
    
    # Clean previous builds
    clean_previous_builds()
    
    # Optimize imports
    optimize_imports()
    
    # Ask for build type
    print("\nSelect build type:")
    print("1. Onefile (single .exe) - Larger size")
    print("2. Onedir (folder) - Smaller size, faster")
    print("3. Both")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    exe_path = None
    dir_path = None
    
    # Build
    if choice in ['1', '3']:
        exe_path = build_onefile()
        if exe_path and input("\nApply UPX compression? (y/n): ").lower() == 'y':
            apply_upx_compression(exe_path)
    
    if choice in ['2', '3']:
        dir_path = build_onedir()
    
    # Show results
    print("\n" + "="*60)
    print("BUILD RESULTS")
    print("="*60)
    
    if exe_path and os.path.exists(exe_path):
        size = get_file_size(exe_path)
        print(f"✓ Onefile: {exe_path} ({size:.2f} MB)")
    
    if dir_path and os.path.exists(dir_path):
        total_size = sum(os.path.getsize(os.path.join(dir_path, f)) 
                        for f in os.listdir(dir_path) 
                        if os.path.isfile(os.path.join(dir_path, f)))
        size_mb = total_size / 1024 / 1024
        print(f"✓ Onedir: {dir_path} ({size_mb:.2f} MB total)")
    
    if not exe_path and not dir_path:
        print("✗ No builds were successful")
    
    print("\nFor even smaller size:")
    print("1. Remove unnecessary imports from your code")
    print("2. Use UPX compression (already attempted)")
    print("3. Consider using --exclude-module for unused libraries")
    print("4. Use virtual environment with only required packages")

if __name__ == '__main__':
    main()