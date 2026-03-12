import flet as ft
import asyncio
from data.data_manager import DataManager
from views.EULA.EULA_View import EULA_View
from views.SideNavbar_View import SideNavbar_View
from controller.SideNavbar_Controller import SideNavbar_Controller
from config.App_Config import AppConfig
from widgets.LogFileTxt import logger
import sys
import os
from pathlib import Path
import json
from constants.Json_File_Path_Constants import json_paths

def get_base_path():
    """Get the base path for the application (works for both dev and PyInstaller)"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return sys._MEIPASS
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def get_app_data_path():
    """
    Get the path for application data (user-specific)
    For executable: Uses %APPDATA%/BiomassCalculationTool/
    For development: Uses ./app_data/
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable - use AppData folder
        if os.name == 'nt':  # Windows
            app_data = os.environ.get('APPDATA', '')
            if not app_data:
                app_data = os.path.expanduser('~')
            data_path = os.path.join(app_data, 'BiomassCalculationTool')
        else:  # Linux/Mac
            data_path = os.path.join(os.path.expanduser('~'), '.biomass_calc')
    else:
        # Running as script - use local folder
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_data')
    
    # Create the directory if it doesn't exist
    os.makedirs(data_path, exist_ok=True)
    return data_path

def get_resource_path(relative_path):
    """Get absolute path to resource (read-only files from the executable)"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def get_user_data_path(relative_path):
    """
    Get path for user-specific data files (read-write)
    These files will be stored in the user's AppData folder
    """
    app_data_path = get_app_data_path()
    full_path = os.path.join(app_data_path, relative_path)
    
    # Create subdirectories if needed
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path

def initialize_json_files():
    """Initialize JSON files according to specific rules:
    - treeparameters.json: Always create fresh (empty array)
    - selected_database.json: Always create fresh (empty object)
    - localstorage.json: Always create fresh (empty object)
    - create_species.json: Only create if doesn't exist (preserve if exists)
    """
    logger.write("Initializing JSON files...")
    
    # Files that should be created fresh every time (overwrite if exists)
    fresh_files = {
        "storage/localstorage.json": {},  # Empty object
        "data/treeparameters.json": 
            [
  {
    "SpecCommon": "Alpine fir",
    "SpeciesCode": "",
    "bwood1": 0.0528,
    "bwood2": 2.4309,
    "bbark1": 0.0108,
    "bbark2": 2.3876,
    "bbranches1": 0.0121,
    "bbranches2": 2.3519,
    "bfoliage1": 0.0251,
    "bfoliage2": 2.0389,
    "bhwood1": 0.0268,
    "bhwood2": 1.7579,
    "bhwood3": 0.9871,
    "bhbark1": 0.0009,
    "bhbark2": 1.446,
    "bhbark3": 1.8839,
    "bhbranches1": 0.047,
    "bhbranches2": 2.9288,
    "bhbranches3": -1.1588,
    "bhfoliage1": 0.0551,
    "bhfoliage2": 1.7585,
    "bhfoliage3": 0
  },
  {
    "SpecCommon": "Balsam fir",
    "SpeciesCode": 20,
    "bwood1": 0.0534,
    "bwood2": 2.403,
    "bbark1": 0.0115,
    "bbark2": 2.3484,
    "bbranches1": 0.007,
    "bbranches2": 2.5406,
    "bfoliage1": 0.084,
    "bfoliage2": 1.6695,
    "bhwood1": 0.0294,
    "bhwood2": 1.8357,
    "bhwood3": 0.864,
    "bhbark1": 0.0053,
    "bhbark2": 2.0876,
    "bhbark3": 0.5842,
    "bhbranches1": 0.0117,
    "bhbranches2": 3.5097,
    "bhbranches3": -1.3006,
    "bhfoliage1": 0.1245,
    "bhfoliage2": 2.523,
    "bhfoliage3": -1.123
  },
  {
    "SpecCommon": "Balsam poplar",
    "SpeciesCode": 73,
    "bwood1": 0.051,
    "bwood2": 2.4529,
    "bbark1": 0.0297,
    "bbark2": 2.1131,
    "bbranches1": 0.012,
    "bbranches2": 2.4165,
    "bfoliage1": 0.0276,
    "bfoliage2": 1.6215,
    "bhwood1": 0.0117,
    "bhwood2": 1.7757,
    "bhwood3": 1.2555,
    "bhbark1": 0.018,
    "bhbark2": 1.8131,
    "bhbark3": 0.5144,
    "bhbranches1": 0.0112,
    "bhbranches2": 3.0861,
    "bhbranches3": -0.7164,
    "bhfoliage1": 0.0617,
    "bhfoliage2": 1.8615,
    "bhfoliage3": -0.5375
  },
  {
    "SpecCommon": "American Basswood",
    "SpeciesCode": 51,
    "bwood1": 0.0562,
    "bwood2": 2.4102,
    "bbark1": 0.0302,
    "bbark2": 2.0976,
    "bbranches1": 0.023,
    "bbranches2": 2.2382,
    "bfoliage1": 0.0288,
    "bfoliage2": 1.6378,
    "bhwood1": 0.0168,
    "bhwood2": 1.9844,
    "bhwood3": 0.8989,
    "bhbark1": 0.0057,
    "bhbark2": 1.5881,
    "bhbark3": 1.1472,
    "bhbranches1": 0.0039,
    "bhbranches2": 2.0084,
    "bhbranches3": 0.8588,
    "bhfoliage1": 0.0147,
    "bhfoliage2": 1.83,
    "bhfoliage3": 0.0
  },
  {
    "SpecCommon": "American beech",
    "SpeciesCode": 44,
    "bwood1": 0.1478,
    "bwood2": 2.2986,
    "bbark1": 0.012,
    "bbark2": 2.2388,
    "bbranches1": 0.037,
    "bbranches2": 2.368,
    "bfoliage1": 0.0376,
    "bfoliage2": 1.6164,
    "bhwood1": 0.0432,
    "bhwood2": 2.0378,
    "bhwood3": 0.7,
    "bhbark1": 0.0049,
    "bhbark2": 1.9057,
    "bhbark3": 0.677,
    "bhbranches1": 0.0355,
    "bhbranches2": 2.3749,
    "bhbranches3": 0.0,
    "bhfoliage1": 0.0452,
    "bhfoliage2": 1.5567,
    "bhfoliage3": 0
  },
  {
    "SpecCommon": "Black ash",
    "SpeciesCode": 45,
    "bwood1": 0.0941,
    "bwood2": 2.3491,
    "bbark1": 0.0323,
    "bbark2": 2.0761,
    "bbranches1": 0.0448,
    "bbranches2": 1.9771,
    "bfoliage1": 0.0538,
    "bfoliage2": 1.3584,
    "bhwood1": 0.0306,
    "bhwood2": 2.1836,
    "bhwood3": 0.574,
    "bhbark1": 0.0897,
    "bhbark2": 2.2634,
    "bhbark3": -0.567,
    "bhbranches1": 0.0994,
    "bhbranches2": 2.163,
    "bhbranches3": -0.4809,
    "bhfoliage1": 0.0124,
    "bhfoliage2": 1.0325,
    "bhfoliage3": 0.8747
  },
  {
    "SpecCommon": "Black cherry",
    "SpeciesCode": 58,
    "bwood1": 0.3743,
    "bwood2": 1.9406,
    "bbark1": 0.0679,
    "bbark2": 1.8377,
    "bbranches1": 0.0796,
    "bbranches2": 2.0103,
    "bfoliage1": 0.084,
    "bfoliage2": 1.2319,
    "bhwood1": 0.0181,
    "bhwood2": 1.7013,
    "bhwood3": 1.3057,
    "bhbark1": 0.0101,
    "bhbark2": 1.5956,
    "bhbark3": 0.919,
    "bhbranches1": 0.0005,
    "bhbranches2": 2.8004,
    "bhbranches3": 0.8603,
    "bhfoliage1": 0.1976,
    "bhfoliage2": 1.4421,
    "bhfoliage3": -0.5264
  },
  {
    "SpecCommon": "Black spruce",
    "SpeciesCode": 13,
    "bwood1": 0.0477,
    "bwood2": 2.5147,
    "bbark1": 0.0153,
    "bbark2": 2.2429,
    "bbranches1": 0.0278,
    "bbranches2": 2.0839,
    "bfoliage1": 0.1648,
    "bfoliage2": 1.4143,
    "bhwood1": 0.0309,
    "bhwood2": 1.7527,
    "bhwood3": 1.0014,
    "bhbark1": 0.0115,
    "bhbark2": 1.7405,
    "bhbark3": 0.6589,
    "bhbranches1": 0.038,
    "bhbranches2": 3.2558,
    "bhbranches3": -1.4218,
    "bhfoliage1": 0.2048,
    "bhfoliage2": 2.5754,
    "bhfoliage3": -1.3704
  },
  {
    "SpecCommon": "Eastern hemlock",
    "SpeciesCode": 19,
    "bwood1": 0.0619,
    "bwood2": 2.3821,
    "bbark1": 0.0139,
    "bbark2": 2.3282,
    "bbranches1": 0.0217,
    "bbranches2": 2.2653,
    "bfoliage1": 0.0776,
    "bfoliage2": 1.6995,
    "bhwood1": 0.0257,
    "bhwood2": 1.9277,
    "bhwood3": 0.8576,
    "bhbark1": 0.0118,
    "bhbark2": 1.9893,
    "bhbark3": 0.47,
    "bhbranches1": 0.0215,
    "bhbranches2": 2.6553,
    "bhbranches3": -0.4682,
    "bhfoliage1": 0.1471,
    "bhfoliage2": 2.0108,
    "bhfoliage3": -0.608
  },
  {
    "SpecCommon": "Eastern red cedar",
    "SpeciesCode": 23,
    "bwood1": 0.1277,
    "bwood2": 1.9778,
    "bbark1": 0.0377,
    "bbark2": 1.6064,
    "bbranches1": 0.0254,
    "bbranches2": 2.2884,
    "bfoliage1": 0.055,
    "bfoliage2": 1.8656,
    "bhwood1": 0.052,
    "bhwood2": 1.7731,
    "bhwood3": 0.7054,
    "bhbark1": 0.0283,
    "bhbark2": 1.7079,
    "bhbark3": 0.0,
    "bhbranches1": 0.0219,
    "bhbranches2": 2.3585,
    "bhbranches3": 0.0,
    "bhfoliage1": 0.2575,
    "bhfoliage2": 2.5136,
    "bhfoliage3": -1.5565
  },
  {
    "SpecCommon": "Eastern white cedar",
    "SpeciesCode": 22,
    "bwood1": 0.0654,
    "bwood2": 2.2121,
    "bbark1": 0.0114,
    "bbark2": 2.1432,
    "bbranches1": 0.0335,
    "bbranches2": 1.9367,
    "bfoliage1": 0.0499,
    "bfoliage2": 1.7278,
    "bhwood1": 0.0295,
    "bhwood2": 1.7026,
    "bhwood3": 0.9428,
    "bhbark1": 0.0076,
    "bhbark2": 1.7861,
    "bhbark3": 0.6132,
    "bhbranches1": 0.0501,
    "bhbranches2": 2.5165,
    "bhbranches3": -0.8774,
    "bhfoliage1": 0.0813,
    "bhfoliage2": 2.218,
    "bhfoliage3": -0.7907
  },
  {
    "SpecCommon": "Eastern white pine",
    "SpeciesCode": 1,
    "bwood1": 0.0997,
    "bwood2": 2.2709,
    "bbark1": 0.0192,
    "bbark2": 2.2038,
    "bbranches1": 0.0056,
    "bbranches2": 2.6011,
    "bfoliage1": 0.0284,
    "bfoliage2": 1.9375,
    "bhwood1": 0.017,
    "bhwood2": 1.7779,
    "bhwood3": 1.137,
    "bhbark1": 0.0069,
    "bhbark2": 1.6589,
    "bhbark3": 0.9582,
    "bhbranches1": 0.0184,
    "bhbranches2": 3.1968,
    "bhbranches3": -1.0876,
    "bhfoliage1": 0.0584,
    "bhfoliage2": 2.2389,
    "bhfoliage3": -0.5968
  },
  {
    "SpecCommon": "Grey birch",
    "SpeciesCode": "",
    "bwood1": 0.072,
    "bwood2": 2.3885,
    "bbark1": 0.0168,
    "bbark2": 2.2569,
    "bbranches1": 0.0088,
    "bbranches2": 2.5689,
    "bfoliage1": 0.0099,
    "bfoliage2": 1.8985,
    "bhwood1": 0.0295,
    "bhwood2": 1.9064,
    "bhwood3": 0.9139,
    "bhbark1": 0.0148,
    "bhbark2": 1.8433,
    "bhbark3": 0.5021,
    "bhbranches1": 0.015,
    "bhbranches2": 3.0347,
    "bhbranches3": -0.7629,
    "bhfoliage1": 0.0455,
    "bhfoliage2": 2.6447,
    "bhfoliage3": -1.4955
  },
  {
    "SpecCommon": "Hickory",
    "SpeciesCode": "",
    "bwood1": 0.2116,
    "bwood2": 2.2013,
    "bbark1": 0.0365,
    "bbark2": 2.1133,
    "bbranches1": 0.0087,
    "bbranches2": 2.8927,
    "bfoliage1": 0.0173,
    "bfoliage2": 1.983,
    "bhwood1": 0.0139,
    "bhwood2": 1.5913,
    "bhwood3": 1.508,
    "bhbark1": 0.0081,
    "bhbark2": 1.4943,
    "bhbark3": 1.1324,
    "bhbranches1": 0.005,
    "bhbranches2": 3.0463,
    "bhbranches3": 0.0,
    "bhfoliage1": 0.0121,
    "bhfoliage2": 2.0865,
    "bhfoliage3": 0.0
  },
  {
    "SpecCommon": "Hop-hornbeam",
    "SpeciesCode": "",
    "bwood1": 0.1929,
    "bwood2": 1.9672,
    "bbark1": 0.0671,
    "bbark2": 1.5911,
    "bbranches1": 0.0278,
    "bbranches2": 2.1336,
    "bfoliage1": 0.0293,
    "bfoliage2": 1.9502,
    "bhwood1": 0.0083,
    "bhwood2": 1.6534,
    "bhwood3": 1.7479,
    "bhbark1": 0.0012,
    "bhbark2": 1.1486,
    "bhbark3": 2.2903,
    "bhbranches1": 0.0009,
    "bhbranches2": 1.9152,
    "bhbranches3": 1.7769,
    "bhfoliage1": 0.0247,
    "bhfoliage2": 2.0056,
    "bhfoliage3": 0.0
  },
  {
    "SpecCommon": "Jack pine",
    "SpeciesCode": 3,
    "bwood1": 0.0804,
    "bwood2": 2.4041,
    "bbark1": 0.0184,
    "bbark2": 2.0703,
    "bbranches1": 0.0079,
    "bbranches2": 2.4155,
    "bfoliage1": 0.0389,
    "bfoliage2": 1.729,
    "bhwood1": 0.0199,
    "bhwood2": 1.6883,
    "bhwood3": 1.2456,
    "bhbark1": 0.0141,
    "bhbark2": 1.5994,
    "bhbark3": 0.5957,
    "bhbranches1": 0.0185,
    "bhbranches2": 3.0584,
    "bhbranches3": -0.9816,
    "bhfoliage1": 0.0325,
    "bhfoliage2": 1.7879,
    "bhfoliage3": 0.0
  },
  {
    "SpecCommon": "Large-tooth aspen",
    "SpeciesCode": 70,
    "bwood1": 0.0959,
    "bwood2": 2.343,
    "bbark1": 0.0308,
    "bbark2": 2.224,
    "bbranches1": 0.0047,
    "bbranches2": 2.653,
    "bfoliage1": 0.008,
    "bfoliage2": 2.0149,
    "bhwood1": 0.0128,
    "bhwood2": 2.0633,
    "bhwood3": 0.9516,
    "bhbark1": 0.024,
    "bhbark2": 2.3055,
    "bhbark3": 0,
    "bhbranches1": 0.0131,
    "bhbranches2": 3.1274,
    "bhbranches3": -0.8379,
    "bhfoliage1": 0.0382,
    "bhfoliage2": 2.1673,
    "bhfoliage3": -0.6842
  },
  {
    "SpecCommon": "Lodgepole pine",
    "SpeciesCode": "",
    "bwood1": 0.0475,
    "bwood2": 2.5437,
    "bbark1": 0.0186,
    "bbark2": 2.0807,
    "bbranches1": 0.0198,
    "bbranches2": 2.1287,
    "bfoliage1": 0.0432,
    "bfoliage2": 1.7166,
    "bhwood1": 0.0202,
    "bhwood2": 1.7179,
    "bhwood3": 1.2078,
    "bhbark1": 0.0099,
    "bhbark2": 1.6049,
    "bhbark3": 0.7456,
    "bhbranches1": 0.044,
    "bhbranches2": 3.719,
    "bhbranches3": -2.0399,
    "bhfoliage1": 0.0785,
    "bhfoliage2": 2.5377,
    "bhfoliage3": -1.1213
  },
  {
    "SpecCommon": "Red ash",
    "SpeciesCode": 47,
    "bwood1": 0.1571,
    "bwood2": 2.1817,
    "bbark1": 0.0416,
    "bbark2": 2.0509,
    "bbranches1": 0.0177,
    "bbranches2": 2.337,
    "bfoliage1": 0.1041,
    "bfoliage2": 1.2185,
    "bhwood1": 0.0224,
    "bhwood2": 1.7845,
    "bhwood3": 1.066,
    "bhbark1": 0.0219,
    "bhbark2": 1.419,
    "bhbark3": 0.8963,
    "bhbranches1": 0.0176,
    "bhbranches2": 2.3313,
    "bhbranches3": 0.0,
    "bhfoliage1": 0.0761,
    "bhfoliage2": 1.3077,
    "bhfoliage3": 0.0
  },
  {
    "SpecCommon": "Red maple",
    "SpeciesCode": 32,
    "bwood1": 0.1014,
    "bwood2": 2.3448,
    "bbark1": 0.0291,
    "bbark2": 2.0893,
    "bbranches1": 0.0175,
    "bbranches2": 2.4846,
    "bfoliage1": 0.0515,
    "bfoliage2": 1.5198,
    "bhwood1": 0.0315,
    "bhwood2": 2.0342,
    "bhwood3": 0.7485,
    "bhbark1": 0.0283,
    "bhbark2": 2.0907,
    "bhbark3": 0.0,
    "bhbranches1": 0.0225,
    "bhbranches2": 2.4106,
    "bhbranches3": 0.0,
    "bhfoliage1": 0.0571,
    "bhfoliage2": 1.4898,
    "bhfoliage3": 0.0
  },
  {
    "SpecCommon": "Northern Red Oak",
    "SpeciesCode": 41,
    "bwood1": 0.1754,
    "bwood2": 2.1616,
    "bbark1": 0.0381,
    "bbark2": 2.0991,
    "bbranches1": 0.0085,
    "bbranches2": 2.779,
    "bfoliage1": 0.0373,
    "bfoliage2": 1.674,
    "bhwood1": 0.0285,
    "bhwood2": 1.8501,
    "bhwood3": 1.0204,
    "bhbark1": 0.0326,
    "bhbark2": 1.81,
    "bhbark3": 0.4153,
    "bhbranches1": 0.0013,
    "bhbranches2": 3.0637,
    "bhbranches3": 0.3153,
    "bhfoliage1": 0.0582,
    "bhfoliage2": 1.5438,
    "bhfoliage3": 0.0
  },
  {
    "SpecCommon": "Red pine",
    "SpeciesCode": 2,
    "bwood1": 0.0564,
    "bwood2": 2.4465,
    "bbark1": 0.0188,
    "bbark2": 2.0527,
    "bbranches1": 0.0033,
    "bbranches2": 2.7515,
    "bfoliage1": 0.0212,
    "bfoliage2": 2.069,
    "bhwood1": 0.0106,
    "bhwood2": 1.7725,
    "bhwood3": 1.3285,
    "bhbark1": 0.0277,
    "bhbark2": 1.5192,
    "bhbark3": 0.4645,
    "bhbranches1": 0.0125,
    "bhbranches2": 3.3865,
    "bhbranches3": -1.1939,
    "bhfoliage1": 0.0731,
    "bhfoliage2": 2.3439,
    "bhfoliage3": -0.7378
  },
  {
    "SpecCommon": "Red spruce",
    "SpeciesCode": 14,
    "bwood1": 0.0989,
    "bwood2": 2.2814,
    "bbark1": 0.022,
    "bbark2": 2.0908,
    "bbranches1": 0.0005,
    "bbranches2": 3.275,
    "bfoliage1": 0.0066,
    "bfoliage2": 2.4213,
    "bhwood1": 0.0143,
    "bhwood2": 1.6441,
    "bhwood3": 1.4065,
    "bhbark1": 0.0274,
    "bhbark2": 2.0188,
    "bhbark3": 0.0,
    "bhbranches1": 0.0005,
    "bhbranches2": 3.3136,
    "bhbranches3": 0.0,
    "bhfoliage1": 0.0106,
    "bhfoliage2": 2.2709,
    "bhfoliage3": 0.0
  },
  {
    "SpecCommon": "Silver maple",
    "SpeciesCode": 33,
    "bwood1": 0.2324,
    "bwood2": 2.1,
    "bbark1": 0.0278,
    "bbark2": 2.0433,
    "bbranches1": 0.0028,
    "bbranches2": 3.102,
    "bfoliage1": 0.143,
    "bfoliage2": 1.258,
    "bhwood1": 0.0274,
    "bhwood2": 1.7126,
    "bhwood3": 1.1086,
    "bhbark1": 0.0123,
    "bhbark2": 1.825,
    "bhbark3": 0.501,
    "bhbranches1": 0.0543,
    "bhbranches2": 3.7343,
    "bhbranches3": -1.6497,
    "bhfoliage1": 6.6808,
    "bhfoliage2": 2.1092,
    "bhfoliage3": -2.1697
  },
  {
    "SpecCommon": "Sugar maple",
    "SpeciesCode": 30,
    "bwood1": 0.1315,
    "bwood2": 2.3129,
    "bbark1": 0.0631,
    "bbark2": 1.9241,
    "bbranches1": 0.033,
    "bbranches2": 2.3741,
    "bfoliage1": 0.0393,
    "bfoliage2": 1.693,
    "bhwood1": 0.0301,
    "bhwood2": 2.0313,
    "bhwood3": 0.8171,
    "bhbark1": 0.0103,
    "bhbark2": 1.7111,
    "bhbark3": 0.8509,
    "bhbranches1": 0.0661,
    "bhbranches2": 2.594,
    "bhbranches3": -0.4933,
    "bhfoliage1": 2.5019,
    "bhfoliage2": 2.4527,
    "bhfoliage3": -2.3008
  },
  {
    "SpecCommon": "American Larch",
    "SpeciesCode": 25,
    "bwood1": 0.0625,
    "bwood2": 2.4475,
    "bbark1": 0.0174,
    "bbark2": 2.1109,
    "bbranches1": 0.0196,
    "bbranches2": 2.2652,
    "bfoliage1": 0.0801,
    "bfoliage2": 1.4875,
    "bhwood1": 0.0276,
    "bhwood2": 1.6724,
    "bhwood3": 1.1443,
    "bhbark1": 0.012,
    "bhbark2": 1.7059,
    "bhbark3": 0.5811,
    "bhbranches1": 0.0336,
    "bhbranches2": 3.1335,
    "bhbranches3": -1.1559,
    "bhfoliage1": 0.1324,
    "bhfoliage2": 2.114,
    "bhfoliage3": -0.8781
  },
  {
    "SpecCommon": "Trembling aspen",
    "SpeciesCode": 74,
    "bwood1": 0.0605,
    "bwood2": 2.475,
    "bbark1": 0.0168,
    "bbark2": 2.3949,
    "bbranches1": 0.008,
    "bbranches2": 2.5214,
    "bfoliage1": 0.0261,
    "bfoliage2": 1.6304,
    "bhwood1": 0.0142,
    "bhwood2": 1.9389,
    "bhwood3": 1.0572,
    "bhbark1": 0.0063,
    "bhbark2": 2.0819,
    "bhbark3": 0.6617,
    "bhbranches1": 0.0137,
    "bhbranches2": 2.927,
    "bhbranches3": -0.6221,
    "bhfoliage1": 0.027,
    "bhfoliage2": 1.6183,
    "bhfoliage3": 0.0
  },
  {
    "SpecCommon": "White ash",
    "SpeciesCode": 46,
    "bwood1": 0.1861,
    "bwood2": 2.1665,
    "bbark1": 0.0406,
    "bbark2": 1.9946,
    "bbranches1": 0.0461,
    "bbranches2": 2.2291,
    "bfoliage1": 0.1106,
    "bfoliage2": 1.2277,
    "bhwood1": 0.0224,
    "bhwood2": 1.7438,
    "bhwood3": 1.1899,
    "bhbark1": 0.0126,
    "bhbark2": 1.6456,
    "bhbark3": 0.7893,
    "bhbranches1": 0.0354,
    "bhbranches2": 2.3046,
    "bhbranches3": 0.0,
    "bhfoliage1": 0.0195,
    "bhfoliage2": 1.0509,
    "bhfoliage3": 0.7836
  },
  {
    "SpecCommon": "White birch",
    "SpeciesCode": 38,
    "bwood1": 0.0593,
    "bwood2": 2.5026,
    "bbark1": 0.0135,
    "bbark2": 2.4053,
    "bbranches1": 0.0135,
    "bbranches2": 2.5532,
    "bfoliage1": 0.0546,
    "bfoliage2": 1.6351,
    "bhwood1": 0.0338,
    "bhwood2": 2.0702,
    "bhwood3": 0.6876,
    "bhbark1": 0.008,
    "bhbark2": 1.9754,
    "bhbark3": 0.6659,
    "bhbranches1": 0.0257,
    "bhbranches2": 3.1754,
    "bhbranches3": -0.9417,
    "bhfoliage1": 0.1415,
    "bhfoliage2": 2.3074,
    "bhfoliage3": -1.1189
  },
  {
    "SpecCommon": "White elm",
    "SpeciesCode": 50,
    "bwood1": 0.0402,
    "bwood2": 2.5804,
    "bbark1": 0.0073,
    "bbark2": 2.4859,
    "bbranches1": 0.0401,
    "bbranches2": 2.1826,
    "bfoliage1": 0.075,
    "bfoliage2": 1.3436,
    "bhwood1": 0.0207,
    "bhwood2": 2.2276,
    "bhwood3": 0.6488,
    "bhbark1": 0.0078,
    "bhbark2": 2.454,
    "bhbark3": 0.0,
    "bhbranches1": 0.0393,
    "bhbranches2": 2.188,
    "bhbranches3": 0.0,
    "bhfoliage1": 0.0516,
    "bhfoliage2": 1.4511,
    "bhfoliage3": 0.0
  },
  {
    "SpecCommon": "White oak",
    "SpeciesCode": 40,
    "bwood1": 0.0762,
    "bwood2": 2.3335,
    "bbark1": 0.0338,
    "bbark2": 1.9845,
    "bbranches1": 0.0113,
    "bbranches2": 2.6211,
    "bfoliage1": 0.0188,
    "bfoliage2": 1.7881,
    "bhwood1": 0.0442,
    "bhwood2": 1.6818,
    "bhwood3": 1.031,
    "bhbark1": 0.0308,
    "bhbark2": 1.7479,
    "bhbark3": 0.3504,
    "bhbranches1": 0.0022,
    "bhbranches2": 2.0165,
    "bhbranches3": 1.3953,
    "bhfoliage1": 0.0053,
    "bhfoliage2": 1.2822,
    "bhfoliage3": 1.1323
  },
  {
    "SpecCommon": "White spruce",
    "SpeciesCode": 12,
    "bwood1": 0.0359,
    "bwood2": 2.5775,
    "bbark1": 0.0116,
    "bbark2": 2.3022,
    "bbranches1": 0.0283,
    "bbranches2": 2.0823,
    "bfoliage1": 0.1601,
    "bfoliage2": 1.467,
    "bhwood1": 0.0265,
    "bhwood2": 1.7952,
    "bhwood3": 0.9733,
    "bhbark1": 0.0124,
    "bhbark2": 1.6962,
    "bhbark3": 0.6489,
    "bhbranches1": 0.0325,
    "bhbranches2": 2.8573,
    "bhbranches3": -0.9127,
    "bhfoliage1": 0.202,
    "bhfoliage2": 2.3802,
    "bhfoliage3": -1.1103
  },
  {
    "SpecCommon": "Yellow birch",
    "SpeciesCode": 37,
    "bwood1": 0.1932,
    "bwood2": 2.1569,
    "bbark1": 0.0192,
    "bbark2": 2.2475,
    "bbranches1": 0.0305,
    "bbranches2": 2.4044,
    "bfoliage1": 0.1119,
    "bfoliage2": 1.3973,
    "bhwood1": 0.0259,
    "bhwood2": 1.9044,
    "bhwood3": 0.9715,
    "bhbark1": 0.0069,
    "bhbark2": 2.0834,
    "bhbark3": 0.5371,
    "bhbranches1": 0.0325,
    "bhbranches2": 2.3851,
    "bhbranches3": 0,
    "bhfoliage1": 0.1683,
    "bhfoliage2": 1.2764,
    "bhfoliage3": 0
  },
  {
    "SpecCommon": "Hardwood",
    "SpeciesCode": "",
    "bwood1": 0.0871,
    "bwood2": 2.3702,
    "bbark1": 0.0241,
    "bbark2": 2.1969,
    "bbranches1": 0.0167,
    "bbranches2": 2.4807,
    "bfoliage1": 0.039,
    "bfoliage2": 1.6229,
    "bhwood1": 0.0359,
    "bhwood2": 2.0263,
    "bhwood3": 0.6987,
    "bhbark1": 0.0094,
    "bhbark2": 1.8677,
    "bhbark3": 0.6985,
    "bhbranches1": 0.0433,
    "bhbranches2": 2.6817,
    "bhbranches3": -0.5731,
    "bhfoliage1": 0.0859,
    "bhfoliage2": 1.8485,
    "bhfoliage3": -0.5383
  },
  {
    "SpecCommon": "Softwood",
    "SpeciesCode": "",
    "bwood1": 0.0648,
    "bwood2": 2.3927,
    "bbark1": 0.0162,
    "bbark2": 2.1959,
    "bbranches1": 0.0156,
    "bbranches2": 2.2916,
    "bfoliage1": 0.0861,
    "bfoliage2": 1.6261,
    "bhwood1": 0.0284,
    "bhwood2": 1.6894,
    "bhwood3": 1.0857,
    "bhbark1": 0.01,
    "bhbark2": 1.8463,
    "bhbark3": 0.5616,
    "bhbranches1": 0.0301,
    "bhbranches2": 3.0038,
    "bhbranches3": -1.052,
    "bhfoliage1": 0.1554,
    "bhfoliage2": 2.4021,
    "bhfoliage3": -1.1043
  },
  {
    "SpecCommon": "All",
    "SpeciesCode": "",
    "bwood1": 0.0787,
    "bwood2": 2.3702,
    "bbark1": 0.0185,
    "bbark2": 2.2159,
    "bbranches1": 0.023,
    "bbranches2": 2.2678,
    "bfoliage1": 0.0767,
    "bfoliage2": 1.572,
    "bhwood1": 0.0348,
    "bhwood2": 1.9235,
    "bhwood3": 0.7829,
    "bhbark1": 0.0139,
    "bhbark2": 1.5429,
    "bhbark3": 0.8189,
    "bhbranches1": 0.0346,
    "bhbranches2": 2.6706,
    "bhbranches3": -0.6033,
    "bhfoliage1": 0.1822,
    "bhfoliage2": 2.2864,
    "bhfoliage3": -1.1203
  }
]
            }
    
    # Track created/updated files
    created_files = []
    
    # Create fresh files (always overwrite)
    for file_path, default_content in fresh_files.items():
        user_file_path = get_user_data_path(file_path)
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(user_file_path), exist_ok=True)
            
            # Always write fresh content (overwrite if exists)
            with open(user_file_path, 'w', encoding='utf-8') as f:
                json.dump(default_content, f, indent=2, ensure_ascii=False)
            
            logger.write(f"   Created/Updated: {file_path}")
            created_files.append(file_path)
        except Exception as e:
            logger.write(f"   Error creating {file_path}: {str(e)}")
    
    # Handle create_species.json - only create if it doesn't exist
    create_species_path = get_user_data_path(json_paths.CREATED_SPECIES_PATH)
    
    if not os.path.exists(create_species_path):
        try:
            # Create empty file if it doesn't exist
            os.makedirs(os.path.dirname(create_species_path), exist_ok=True)
            with open(create_species_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii=False)  # Empty array
            logger.write(f"   Created: {json_paths.CREATED_SPECIES_PATH} (new file)")
            created_files.append(json_paths.CREATED_SPECIES_PATH)
        except Exception as e:
            logger.write(f"   Error creating {json_paths.CREATED_SPECIES_PATH}: {str(e)}")
    else:
        logger.write(f"   Preserved existing: {json_paths.CREATED_SPECIES_PATH}")
    
    if created_files:
        logger.write(f"Initialized {len(created_files)} JSON files")
    else:
        logger.write("All JSON files are ready")

    # Handle selected_database.json - only create if it doesn't exist
    selected_db_path = get_user_data_path(json_paths.SELECTED_DATABASE_PATH)
    if not os.path.exists(selected_db_path):
        try:
            # Create empty file if it doesn't exist
            os.makedirs(os.path.dirname(selected_db_path), exist_ok=True)
            with open(selected_db_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2, ensure_ascii=False)  # Empty object
            logger.write(f"   Created: {json_paths.SELECTED_DATABASE_PATH} (new file)")
            created_files.append(json_paths.SELECTED_DATABASE_PATH)
        except Exception as e:
            logger.write(f"   Error creating {json_paths.SELECTED_DATABASE_PATH}: {str(e)}")
    else:
        logger.write(f"   Preserved existing: {json_paths.SELECTED_DATABASE_PATH}")
    
    connection_history_path = get_user_data_path(json_paths.CONNECTION_HISTORY_PATH)
    if not os.path.exists(connection_history_path):
        try:
            # Create empty file if it doesn't exist
            os.makedirs(os.path.dirname(connection_history_path), exist_ok=True)
            with open(connection_history_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii=False)  # Empty array
            logger.write(f"   Created: {json_paths.CONNECTION_HISTORY_PATH} (new file)")
            created_files.append(json_paths.CONNECTION_HISTORY_PATH)
        except Exception as e:
            logger.write(f"   Error creating {json_paths.CONNECTION_HISTORY_PATH}: {str(e)}")
    else:
        logger.write(f"   Preserved existing: {json_paths.CONNECTION_HISTORY_PATH}")

def setup_paths():
    """Setup paths for both development and compiled environments"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        project_root = Path(sys._MEIPASS)
        app_data_path = get_app_data_path()
        logger.write(f"Running as compiled executable")
        logger.write(f"   Program path: {sys._MEIPASS}")
        logger.write(f"   Data path: {app_data_path}")
    else:
        # Running as script
        project_root = Path(__file__).parent
        app_data_path = get_app_data_path()
        logger.write(f"Running as script")
        logger.write(f"   Program path: {project_root}")
        logger.write(f"   Data path: {app_data_path}")
    
    # Add to sys.path if not already there
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Initialize JSON files
    initialize_json_files()
    
    return project_root, app_data_path

def read_json_file(file_path):
    """Read a JSON file from user data directory"""
    try:
        user_file_path = get_user_data_path(file_path)
        if os.path.exists(user_file_path):
            with open(user_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.write(f"File not found: {file_path}")
            return None
    except Exception as e:
        logger.write(f"Error reading {file_path}: {str(e)}")
        return None

def write_json_file(file_path, data):
    """Write data to a JSON file in user data directory"""
    try:
        user_file_path = get_user_data_path(file_path)
        with open(user_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.write(f"Successfully wrote to {file_path}")
        return True
    except Exception as e:
        logger.write(f"Error writing to {file_path}: {str(e)}")
        return False

def main(page: ft.Page):
    """Main entry point for the Biomass Calculation Tool application."""
    
    try:
        # Setup paths first
        project_root, app_data_path = setup_paths()
        logger.write("Application starting...")
        
        # Configure the page with AppConfig
        AppConfig(page).configure_page()
        logger.write("Page configured")
        
        async def show_splash_and_proceed():
            """Show splash screen and then proceed to EULA"""
            try:
                # Create splash screen content
                splash_content = ft.Container(
                    content=ft.Column(
                        [
                            # App Logo/Icon
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.NATURE,
                                    size=80,
                                    color=ft.Colors.GREEN_700
                                ),
                                width=120,
                                height=120,
                                border_radius=60,
                                bgcolor=ft.Colors.GREEN_50,
                                alignment=ft.alignment.center,
                                border=ft.border.all(2, ft.Colors.GREEN_200),
                            ),
                            
                            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                            
                            # App Name
                            ft.Text(
                                "Biomass Calculation Tool",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_800
                            ),
                            
                            ft.Text(
                                "Professional Edition",
                                size=16,
                                color=ft.Colors.GREY_600
                            ),
                            
                            ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                            
                            # Loading indicator
                            ft.Column(
                                [
                                    ft.ProgressRing(
                                        color=ft.Colors.GREEN_700,
                                        stroke_width=4
                                    ),
                                    ft.Text(
                                        "Loading application...",
                                        size=14,
                                        color=ft.Colors.GREY_600
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15
                            ),
                            
                            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                            
                            # Version/Footer
                            ft.Text(
                                f"Version 1.0 | Data: {app_data_path}",
                                size=10,
                                color=ft.Colors.GREY_400
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    padding=20,
                    animate_opacity=300,
                )
                
                # Add splash screen to page
                page.add(splash_content)
                page.update()
                
                logger.write("Splash screen displayed")
                
                # Simulate loading time (2 seconds)
                await asyncio.sleep(2)
                
                # Fade out animation
                splash_content.opacity = 0
                page.update()
                await asyncio.sleep(0.3)
                
                # Clear splash screen
                page.controls.clear()
                page.update()
                
                logger.write("Splash screen cleared")
                
                # Now proceed with the rest of the application
                DataManager().clear()
                logger.write("DataManager cleared, proceeding to EULA")
                
                # Create and show EULA view
                eula_view = EULA_View(page=page, controller=None)
                eula_view.get_eula_view()
                
                page.update()
                logger.write("EULA view displayed")
                
            except Exception as e:
                logger.write(f"Error in splash_and_proceed: {str(e)}")
                # Show error on page
                page.add(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.ERROR_OUTLINE, size=60, color=ft.Colors.RED_400),
                                ft.Text("Application Error", size=24, color=ft.Colors.RED_700),
                                ft.Text(str(e), size=14, color=ft.Colors.GREY_700),
                                ft.Text("Check logs for details", size=12, color=ft.Colors.GREY_500),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        expand=True,
                        alignment=ft.alignment.center,
                        padding=20
                    )
                )
                page.update()
        
        # Start the splash screen sequence
        page.run_task(show_splash_and_proceed)
        
    except Exception as e:
        logger.write(f"Error in main: {str(e)}")
        # Show error message
        page.add(
            ft.Text(f"Fatal Error: {str(e)}", color=ft.Colors.RED_700)
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)