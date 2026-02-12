# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\.github', '.github'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\assets\\fonts\\poppins', 'assets\\fonts\\poppins'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\assets\\images', 'assets\\images'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\automation', 'automation'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\data', 'data'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\log', 'log'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\manual', 'manual'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\screenshots', 'screenshots'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\storage', 'storage'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\TEST OTUTPUTS', 'TEST OTUTPUTS'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\testing_dataset', 'testing_dataset'), ('C:\\Users\\mohib\\Desktop\\BIOMASS L\\Biomass-Calculation-Tool\\testing_dataset\\Client_Testing_Files', 'testing_dataset\\Client_Testing_Files')],
    hiddenimports=['helper_functions.convert_columns_to_specific_types', 'views.Settings.components.Build_Appearance_Content', 'views.Create_Species.components.Preview_Handler', 'data.database_config', 'views.Calculate_Biomass.Calculate_Biomass_View', 'views.EULA.components.Create_Button', 'constants.EULA_Constants', 'widgets.Display_Version_Number', 'controller.Create_Species_Controller', 'views.Select_Data.components.Warning_Banner', 'automation.comparison_checker_dbh_params', 'views.Modify_Species.Modify_Species_View', 'helper_functions.print_file_content', 'widgets.Delete_Dialog', 'views.Modify_Species.components.Action_Buttons', 'model.Create_Species_Model', 'views.Select_Data.components.Connection_History_Manager', 'data.components_data_2', 'views.Create_Species.components.Parameter_Input', 'helper_functions.validate_tree_dbh_and_height_values', 'views.EULA.components.Create_Section', 'views.Select_Data.components.File_Status', 'views.Calculate_Biomass.components.Results_Buttons', 'constants.Modify_Species_Constants', 'data.data_manager', 'views.Select_Data.components.Import_Buttons', 'views.Create_Species.Create_Species_View', 'views.Create_Species.components.Parameter_Section', 'helper_functions.convert_text_file_into_dataframe', 'views.EULA.components.Create_Header', 'widgets.View_Dialog', 'views.Settings.components.Build_Header', 'widgets.Equation_Card_Formula_Text', 'widgets.Bar_Chart_Widget', 'widgets.text_widget', 'views.Calculate_Biomass.components.Layout', 'views.Create_Species.components.Submit_Button', 'constants.Json_File_Path_Constants', 'data.import_dataset_helper', 'widgets.button_widget', 'widgets.Connect_To_Database_Dialog_Widget', 'views.Settings.Settings_View', 'widgets.Warning_Dialog_Header', 'widgets.Custom_Alert_Dialog', 'controller.SideNavbar_Controller', 'views.EULA.EULA_View', 'views.EULA.components.Create_Exit_Content', 'controller.Calculate_Biomass_Controller', 'helper_functions.check_dataframe_for_nan_values', 'widgets.Create_Section_Buttons', 'views.Modify_Species.components.Pagination_Controls', 'widgets.Calculate_Biomass_Button', 'automation.comparison_for_dbh_height_params', 'controller.Select_Data_Controller', 'views.About.components.Header', 'views.Select_Data.components.Page_Header', 'helper_functions.do_mandatory_columns_exist', 'widgets.Equation_Type_Card', 'widgets.TitleTextWidget', 'helper_functions.Remove_Underscores_And_Add_Space_And_Capitalise_Words', 'widgets.Equation_Card_Description_Text', 'views.About.components.Content', 'widgets.DescriptionText', 'widgets.container_widget', 'model.SideNavbar_Model', 'widgets.Hardwood_or_Softwood_Dialog', 'data.calculate_biomass_helper', 'widgets.Display_Nav_Item', 'helper_functions.set_first_row_as_header', 'views.Settings.components.Build_Appearance_Header', 'data.constants', 'widgets.Display_Error_Dialog', 'views.Calculate_Biomass.components.Components_Section', 'controller.Import_Data_Controller', 'widgets.Edit_Dialog', 'widgets.Error_Alert_Import_Data_Dialog', 'views.Settings.components.Build_Theme_Toggle_Switch', 'widgets.Create_Species_Preview_Modal', 'widgets.Supported_Species_Dialog', 'constants.Settings_Constants', 'views.Modify_Species.components.Search_Field', 'widgets.LogFileTxt', 'widgets.Loading_Spinner_Widget', 'controller.Modify_Species_Controller', 'widgets.input_widget', 'widgets.Display_Exit_Dialog', 'widgets.Create_Label_With_Icon', 'widgets.Equation_Card_Title_Text', 'data.components_data', 'views.Calculate_Biomass.components.Results_Table', 'views.Modify_Species.components.No_Search_Results_Display', 'widgets.Warning_Dialog_Display_Errors_Header', 'widgets.Parameter_Section', 'build', 'views.Modify_Species.components.Species_Data_Table', 'views.Calculate_Biomass.components.File_Exporter_Handler', 'widgets.Create_Title_And_Description_Widget', 'views.Create_Species.components.Species_Metadata_Row', 'views.About.About_Dialog_View', 'widgets.Select_Components_Widget', 'views.Select_Data.components.Database_Dialog', 'controller.Settings_Controller', 'widgets.Component_Card', 'widgets.Import_Option_card', 'widgets.Display_Warning_Dialog', 'views.Select_Data.Select_Data_View', 'views.SideNavbar_View', 'widgets.Title_With_Icon', 'config.App_Config', 'views.Calculate_Biomass.components.Equation_Section', 'model.__init__', 'model.Import_Data_Model', 'widgets.Equation_Type_Widget', 'views.Modify_Species.components.No_Data_Display', 'helper_functions.convert_columns_to_lowercase', 'helper_functions.Results_Data_Loader'],
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
    name='main',
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
