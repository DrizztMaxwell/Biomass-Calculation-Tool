# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\icon.ico', 'assets'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\bark.png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\branch.png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\calculating.png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\crown.png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\foliage.png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\key.png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\list.png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\origin.png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\stem.png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\total.png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\wood (1).png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\wood (2).png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\images\\wood.png', 'assets\\images'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Black.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-BlackItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Bold.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-BoldItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-ExtraBold.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-ExtraBoldItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-ExtraLight.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-ExtraLightItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Italic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Light.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-LightItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Medium.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-MediumItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Regular.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-SemiBold.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-SemiBoldItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-Thin.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\assets\\fonts\\poppins\\Poppins-ThinItalic.ttf', 'assets\\fonts\\poppins'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\manual\\Biomass Calculation Tool Manual.pdf', 'manual'), ('C:\\Users\\sid\\Desktop\\biomass calc\\Biomass-Calculation-Tool\\manual\\MANUAL SOFTWARE EXAMPLE.pdf', 'manual')],
    hiddenimports=['config', 'controller', 'views', 'openpyxl', 'pyodbc', 'data', 'flet', 'pandas', 'PIL', 'widgets', 'views.EULA', 'numpy', 'Pillow'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'pytest', 'IPython', 'notebook', 'jupyter', 'matplotlib.tests', 'numpy.tests', 'pandas.tests', 'scipy', 'sympy', 'torch', 'tensorflow', 'sklearn', 'flet_cli', 'flet.fastapi', 'flet.auth', 'tests', 'test'],
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
    strip=True,
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
