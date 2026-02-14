# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\assets\\fonts\\poppins', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\assets\\images', 'assets\\images'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views', 'views'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\EULA', 'views.EULA'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\controller', 'controller'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\config', 'config'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\widgets', 'widgets'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\data', 'data'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\requirements.txt', '.'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\.gitignore', '.')],
    hiddenimports=['flet_core', 'views', 'flet', 'asyncio', 'plotly', 'controller', 'Pillow', 'views.EULA', 'numpy', 'pyodbc', 'matplotlib', 'openpyxl', 'seaborn', 'flet_runtime', 'data', 'PIL', 'widgets', 'config', 'json', 'pandas'],
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
)
