
import os
import sys
from pathlib import Path

def setup_paths():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        os.environ['FLET_VIEW_PATH'] = base_path

setup_paths()
