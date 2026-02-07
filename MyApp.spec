# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('data', 'data'), ('connection_history.json', '.'), ('flet.json', '.')],
    hiddenimports=['flet', 'flet_core', 'flet.version', 'flet.utils', 'pandas', 'numpy', 'pyodbc', 'PIL', 'PIL._imaging', 'PIL.Image', 'json', 'csv', 'datetime', 'os', 'sys', 'pathlib', 'tkinter', 'typing', 'collections', 'inspect'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'sklearn', 'tensorflow', 'torch', 'django', 'flask'],
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
    name='MyApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
