# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\icon.ico', 'assets'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\bark.png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\branch.png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\calculating.png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\crown.png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\foliage.png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\key.png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\list.png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\origin.png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\stem.png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\total.png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\wood (1).png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\wood (2).png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\images\\wood.png', 'assets\\images'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Black.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-BlackItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Bold.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-BoldItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-ExtraBold.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-ExtraBoldItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-ExtraLight.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-ExtraLightItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Italic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Light.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-LightItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Medium.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-MediumItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Regular.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-SemiBold.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-SemiBoldItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Thin.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-ThinItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\manual\\Biomass Calculation Tool Manual.pdf', 'manual'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\manual\\MANUAL SOFTWARE EXAMPLE.pdf', 'manual'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\views', 'views'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\views\\EULA', 'views.EULA'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\controller', 'controller'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\config', 'config'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\widgets', 'widgets'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\data', 'data'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\requirements.txt', '.'), ('C:\\Users\\mohib\\OneDrive\\Documents\\Biomass Calculator\\Biomass-Calculation-Tool\\.gitignore', '.')],
    hiddenimports=['widgets', 'openpyxl', 'seaborn', 'plotly', 'pyarrow', 'controller', 'flet_core', 'asyncio', 'PIL', 'Pillow', 'views', 'pandas', 'flet_runtime', 'config', 'matplotlib', 'numpy', 'flet', 'views.EULA', 'data', 'pyautogui', 'pyodbc', 'json'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BiomassCalculationTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
