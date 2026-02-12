# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\.github', '.github'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\assets\\fonts\\poppins', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\assets\\images', 'assets\\images'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\automation', 'automation'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\config', 'config'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\constants', 'constants'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\controller', 'controller'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\data', 'data'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\helper_functions', 'helper_functions'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\log', 'log'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\manual', 'manual'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\model', 'model'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\model\\__init__.py', 'model\\__init__.py'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\screenshots', 'screenshots'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\storage', 'storage'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\TEST OTUTPUTS', 'TEST OTUTPUTS'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\testing_dataset', 'testing_dataset'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\testing_dataset\\Client_Testing_Files', 'testing_dataset\\Client_Testing_Files'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views', 'views'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\About', 'views\\About'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\About\\components', 'views\\About\\components'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\Calculate_Biomass', 'views\\Calculate_Biomass'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\Calculate_Biomass\\components', 'views\\Calculate_Biomass\\components'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\Create_Species', 'views\\Create_Species'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\Create_Species\\components', 'views\\Create_Species\\components'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\EULA', 'views\\EULA'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\EULA\\components', 'views\\EULA\\components'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\Modify_Species', 'views\\Modify_Species'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\Modify_Species\\components', 'views\\Modify_Species\\components'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\Select_Data', 'views\\Select_Data'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\Select_Data\\components', 'views\\Select_Data\\components'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\Settings', 'views\\Settings'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\views\\Settings\\components', 'views\\Settings\\components'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\widgets', 'widgets'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool', '.')],
    hiddenimports=['model'],
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
