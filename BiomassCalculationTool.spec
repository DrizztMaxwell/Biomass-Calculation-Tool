# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ssl_fixed_main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\mohib\\AppData\\Local\\Programs\\Python\\Python314\\Lib\\site-packages\\certifi\\cacert.pem', 'certifi'), ('assets', 'assets'), ('manual', 'manual'), ('data', 'data'), ('flet_client_cache', 'flet_client_cache')],
    hiddenimports=['flet', 'flet_core', 'flet_runtime', 'certifi', 'ssl', 'views', 'views.EULA', 'controller', 'config', 'widgets', 'data'],
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
