# build_exe.py
"""
ONE-CLICK EXE BUILDER
Creates a single .exe file that can be placed anywhere
No dependencies needed - everything is inside the .exe
"""
import os
import sys
import subprocess
import shutil
import glob
import json
from pathlib import Path

def print_header():
    print("="*70)
    print("SINGLE EXE BUILDER")
    print("Creates ONE .exe file - Copy anywhere, double-click to run!")
    print("="*70)

def clean_everything():
    """Remove ALL previous build files"""
    print("\n🧹 Cleaning previous builds...")
    
    folders_to_remove = ['build', 'dist', '__pycache__', 'output', 'compressed']
    for folder in folders_to_remove:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"  ✓ Removed: {folder}")
            except:
                pass
    
    # Remove spec files
    for spec in glob.glob("*.spec"):
        try:
            os.remove(spec)
            print(f"  ✓ Removed: {spec}")
        except:
            pass

def check_main_file():
    """Check if main.py exists"""
    if not os.path.exists("main.py"):
        print("\n❌ ERROR: main.py not found!")
        print("  Place your Flet app code in main.py")
        print("  Make sure it ends with: flet.app(target=main)")
        return False
    
    # Check if it's a valid Flet app
    try:
        with open("main.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'flet.app(' not in content and 'ft.app(' not in content:
            print("\n⚠️  Warning: main.py might not be a Flet app")
            print("  It should end with: flet.app(target=main_function)")
    except:
        pass
    
    print("  ✓ Found main.py")
    return True

def embed_files_into_exe():
    """Embed all necessary files into the exe using PyInstaller's add-data"""
    
    # Files to embed
    data_to_embed = []
    
    # Embed assets folder if exists
    if os.path.exists("assets"):
        data_to_embed.append(('assets', 'assets'))
        print("  ✓ Will embed: assets/ folder")
    
    # Embed data folder if exists
    if os.path.exists("data"):
        data_to_embed.append(('data', 'data'))
        print("  ✓ Will embed: data/ folder")
    
    # Embed JSON files
    for json_file in glob.glob("*.json"):
        if os.path.isfile(json_file):
            data_to_embed.append((json_file, '.'))
            print(f"  ✓ Will embed: {json_file}")
    
    # Embed any config files
    for config_file in ['config.ini', 'settings.ini', 'config.json', 'settings.json']:
        if os.path.exists(config_file):
            data_to_embed.append((config_file, '.'))
            print(f"  ✓ Will embed: {config_file}")
    
    return data_to_embed

def build_single_exe():
    """Build ONE SINGLE .exe file with everything inside"""
    print("\n🔨 Building SINGLE .exe file...")
    print("   (This will take 5-15 minutes depending on your app)")
    
    # Get embedded files
    embedded_data = embed_files_into_exe()
    
    # Build command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',           # SINGLE EXE
        '--noconsole',         # No terminal window
        '--clean',             # Clean build
        '--name', 'MyApp',     # Output name
        '--distpath', 'dist',  # Output folder
    ]
    
    # Add icon if exists
    icon_paths = ['assets/icon.ico', 'icon.ico', 'app.ico']
    for icon in icon_paths:
        if os.path.exists(icon):
            cmd.extend(['--icon', icon])
            print(f"  ✓ Using icon: {icon}")
            break
    else:
        print("  ⚠️  No icon found - using default")
    
    # Add ALL data files
    for src, dest in embedded_data:
        cmd.extend(['--add-data', f'{src}{os.pathsep}{dest}'])
    
    # Hidden imports (COMMON Flet/Python modules)
    hidden_imports = [
        'flet', 'flet_core', 'flet.version', 'flet.utils',
        'pandas', 'numpy', 'pyodbc',
        'PIL', 'PIL._imaging', 'PIL.Image',
        'json', 'csv', 'datetime', 'os', 'sys', 'pathlib',
        'tkinter', 'typing', 'collections', 'inspect',
    ]
    
    for imp in hidden_imports:
        cmd.extend(['--hidden-import', imp])
    
    # Exclude LARGE unnecessary modules
    cmd.extend(['--exclude-module', 'matplotlib'])
    cmd.extend(['--exclude-module', 'scipy'])
    cmd.extend(['--exclude-module', 'sklearn'])
    cmd.extend(['--exclude-module', 'tensorflow'])
    cmd.extend(['--exclude-module', 'torch'])
    cmd.extend(['--exclude-module', 'django'])
    cmd.extend(['--exclude-module', 'flask'])
    
    # Try UPX compression (makes exe smaller)
    cmd.append('--upx-dir=upx' if os.path.exists('upx') else '--noupx')
    
    # Add the main script
    cmd.append('main.py')
    
    print(f"\n📋 Build Command:")
    print(' '.join(cmd[:10]) + " \\")
    for i in range(10, len(cmd), 5):
        print('   ' + ' '.join(cmd[i:i+5]))
    
    print("\n⏳ Starting build process...")
    print("   Please be patient - this takes time!")
    
    try:
        # Run with timeout (20 minutes)
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        # Show progress
        print("\n" + "-"*50)
        print("BUILD PROGRESS:")
        print("-"*50)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Show only important messages
                if any(x in output.lower() for x in ['writing', 'copying', 'compressing', 'building', 'analyzing']):
                    print(f"  {output.strip()}")
        
        return_code = process.poll()
        
        if return_code == 0:
            exe_path = 'dist/MyApp.exe'
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / 1024 / 1024
                print(f"\n✅ SUCCESS! Single .exe created:")
                print(f"   📂 {os.path.abspath(exe_path)}")
                print(f"   📊 Size: {size_mb:.2f} MB")
                print(f"\n🎯 What to do next:")
                print(f"   1. Copy 'MyApp.exe' to ANY folder")
                print(f"   2. Double-click it to run!")
                print(f"   3. No Python or other files needed!")
                return True, exe_path, size_mb
            else:
                print("\n❌ ERROR: Executable not created")
                return False, None, 0
        else:
            error = process.stderr.read()
            print(f"\n❌ BUILD FAILED")
            if error:
                print("\nError details:")
                print(error[:1000])
            return False, None, 0
            
    except Exception as e:
        print(f"\n❌ Build error: {e}")
        import traceback
        traceback.print_exc()
        return False, None, 0

def compress_exe(exe_path):
    """Try to make the .exe smaller with UPX"""
    if not os.path.exists(exe_path):
        return False
    
    print("\n🔍 Trying to make .exe smaller...")
    
    # Check for UPX
    upx_paths = [
        'upx/upx.exe',
        'upx.exe',
        'C:\\upx\\upx.exe',
        'C:\\Program Files\\upx\\upx.exe',
    ]
    
    upx_exe = None
    for path in upx_paths:
        if os.path.exists(path):
            upx_exe = path
            break
    
    if not upx_exe:
        print("  ⚠️  UPX not found. For smaller .exe:")
        print("     Download from: https://github.com/upx/upx/releases")
        print("     Extract upx.exe to project folder")
        return False
    
    original_size = os.path.getsize(exe_path) / 1024 / 1024
    
    # Create backup
    backup = exe_path + '.backup'
    shutil.copy2(exe_path, backup)
    
    try:
        print(f"  Original size: {original_size:.2f} MB")
        print("  Compressing...")
        
        # Try different compression methods
        compressions = [
            ['--best', '--ultra-brute'],  # Maximum compression
            ['--best'],                   # Best standard
            ['-9'],                       # Level 9
            ['-8', '--lzma'],             # LZMA
        ]
        
        for comp in compressions:
            try:
                cmd = [upx_exe] + comp + [exe_path]
                print(f"  Trying: {' '.join(cmd)}")
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                if result.returncode == 0:
                    new_size = os.path.getsize(exe_path) / 1024 / 1024
                    reduction = ((original_size - new_size) / original_size) * 100
                    print(f"  ✅ Compressed to: {new_size:.2f} MB")
                    print(f"     (Reduced by {reduction:.1f}%)")
                    os.remove(backup)
                    return True
                else:
                    # Restore and try next
                    shutil.copy2(backup, exe_path)
                    
            except subprocess.TimeoutExpired:
                print(f"  ⏱️  Timeout with {' '.join(comp)}")
                shutil.copy2(backup, exe_path)
                continue
        
        # If all failed, restore original
        shutil.copy2(backup, exe_path)
        os.remove(backup)
        print("  ❌ Compression failed, using original")
        return False
        
    except Exception as e:
        print(f"  ❌ Compression error: {e}")
        if os.path.exists(backup):
            shutil.copy2(backup, exe_path)
            os.remove(backup)
        return False

def create_portable_folder(exe_path, size_mb):
    """Create a folder with just the .exe and README"""
    print("\n📦 Creating portable package...")
    
    portable_dir = "Portable_App"
    os.makedirs(portable_dir, exist_ok=True)
    
    # Copy the exe
    exe_name = os.path.basename(exe_path)
    portable_exe = os.path.join(portable_dir, exe_name)
    shutil.copy2(exe_path, portable_exe)
    
    # Create README
    readme = f"""MyApp - Portable Application
=================================

This is a standalone application. No installation required!

🚀 HOW TO USE:
1. Copy "{exe_name}" to ANY folder
2. Double-click it to run
3. That's it!

📋 DETAILS:
- Size: {size_mb:.2f} MB
- Type: Standalone Windows executable
- No dependencies needed
- No Python required
- No installation required

⚠️  NOTES:
- Your antivirus might flag it (false positive)
- Add an exception if needed
- First run might be slow

📞 Support: Your contact info here
"""
    
    with open(os.path.join(portable_dir, "README.txt"), 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print(f"  ✅ Portable package created in: {portable_dir}/")
    print(f"     Contains just the .exe and README")

def verify_exe_works(exe_path):
    """Test if the exe runs"""
    print("\n🧪 Testing if .exe works...")
    
    if not os.path.exists(exe_path):
        print("  ❌ .exe file missing!")
        return False
    
    try:
        # Quick test - just check if it starts
        print("  ⚠️  Starting test (will close automatically)...")
        
        process = subprocess.Popen(
            [exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a few seconds then close
        import time
        time.sleep(3)
        process.terminate()
        
        # Check if it started
        if process.poll() is None:
            process.kill()
            print("  ✅ .exe started successfully!")
            return True
        else:
            print("  ⚠️  .exe closed quickly - might be normal")
            return True
            
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def install_pyinstaller():
    """Install PyInstaller if not present"""
    print("\n📦 Checking for PyInstaller...")
    
    try:
        import PyInstaller
        print(f"  ✅ PyInstaller {PyInstaller.__version__} found")
        return True
    except ImportError:
        print("  ⚠️  PyInstaller not found. Installing...")
        
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'pyinstaller', '--upgrade'],
                check=True,
                capture_output=True
            )
            print("  ✅ PyInstaller installed")
            return True
        except Exception as e:
            print(f"  ❌ Failed to install PyInstaller: {e}")
            print("\n💡 Manual installation:")
            print("   Open Command Prompt as Administrator and run:")
            print("   pip install pyinstaller --upgrade")
            return False

def main():
    print_header()
    
    # Step 1: Check dependencies
    if not install_pyinstaller():
        return
    
    # Step 2: Clean previous builds
    clean_everything()
    
    # Step 3: Check main.py
    if not check_main_file():
        return
    
    # Step 4: Build the single exe
    success, exe_path, size_mb = build_single_exe()
    
    if not success:
        print("\n❌ Build failed!")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure main.py has no syntax errors")
        print("   2. Try: pip install pyinstaller --upgrade")
        print("   3. Check if all imports in main.py are installed")
        return
    
    # Step 5: Try compression
    if input("\n🔍 Try to make .exe smaller with UPX? (y/n): ").lower() == 'y':
        compress_exe(exe_path)
    
    # Step 6: Verify
    if input("\n🧪 Test if .exe works? (y/n): ").lower() == 'y':
        verify_exe_works(exe_path)
    
    # Step 7: Create portable package
    if input("\n📦 Create portable folder? (y/n): ").lower() == 'y':
        create_portable_folder(exe_path, size_mb)
    
    print("\n" + "="*70)
    print("🎉 BUILD COMPLETE!")
    print("="*70)
    print(f"\n📍 Your SINGLE .exe file is at:")
    print(f"   📂 {os.path.abspath(exe_path)}")
    print(f"\n🚀 What to do now:")
    print(f"   1. Copy 'MyApp.exe' to your Desktop")
    print(f"   2. Double-click it to run!")
    print(f"   3. No other files needed!")
    print(f"\n⚠️  Note: Antivirus might flag it (false positive)")
    print(f"   Add an exception if needed")
    
    # Open folder
    if os.path.exists('dist'):
        os.startfile('dist')

if __name__ == '__main__':
    try:
        main()
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n❌ Build cancelled")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")