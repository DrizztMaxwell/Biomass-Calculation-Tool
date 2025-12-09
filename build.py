import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main.py',
    '--name=MyApp',
    '--onefile',
    '--windowed',
    '--add-data=assets;assets',
    '--add-data=assets/images;assets/images',
    '--add-data=assets/fonts;assets/fonts',
    '--hidden-import=pandas',
    '--hidden-import=numpy', 
    '--hidden-import=sklearn',
    '--hidden-import=PIL',
    '--hidden-import=PIL._imaging',
    '--hidden-import=flet',
    '--hidden-import=flet.core',
    # '--icon=assets/icon.ico',  # optional
])