import os
import sys
import flet as ft
from controller.Select_Data_Controller import Select_Data_Controller
from views import Select_Data_View
from views.Modify_Species_View import Modify_Species_View
from views.Calculate_Biomass_View import  Calculate_Biomass_View
from model.Calculate_Biomass_Model import Calculate_Biomass_Model
from views.Create_Species_View import Create_Species_View
from controller.Create_Species_Controller import Create_Species_Controller
from controller.Calculate_Biomass_Controller import Calculate_Biomass_Controller
from views.Select_Data_View import Select_Data_View
from views.About_Dialog_View import About_Dialog_View
from widgets.Display_Nav_Item import Display_Nav_Item
from widgets.Display_Version_Number import Display_Version_Number
from widgets.Display_Exit_Dialog import Display_Exit_Dialog
from views.Settings_View import SettingsView
from helper_functions.Remove_Underscores_And_Add_Space_And_Capitalise_Words import Remove_Underscores_And_Add_Space_And_Capitalise_Words
from widgets.Supported_Species_Dialog import Supported_Species_Dialog
from widgets.LogFileTxt import logger
from controller.Settings_Controller import Settings_Controller
class SideNavbar_View:
    
    """Main application class for the Biomass Calculator"""
    
    # --- Configuration Constants ---
    SIDEBAR_BACKGROUND = "#1B2433"  # Dark background color from the image
    SIDEBAR_EXPANDED_WIDTH = 250
    SIDEBAR_COLLAPSED_WIDTH = 80
    PRIMARY_COLOR = ft.Colors.GREEN_500  # A bright, light green
    ACCENT_DISCLAIMER = ft.Colors.GREEN_700  # Bright green for the Disclaimer button
    ACCENT_ABOUT = "#8B5CF6"  # Purple for the About button
    ACTIVE_ITEM_BG = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)  # Subtle highlight for active item
    
    CALCULATE_BIOMASS_PAGE = "calculate_biomass"
    CREATE_SPECIES_PAGE = "create_species"
    SETTINGS_PAGE = "settings"
    MODIFY_SPECIES_PAGE = "modify_species"
    SELECT_DATA_PAGE = "select_data"
    EXIT_APPLICATION_PAGE = "exit_application"
    SUPPORTED_SPECIES_DIALOG = "supported_species_dialog"
    
    

    def __init__(self, page: ft.Page):
        self.page = page
        self._Initialise()
        

    def _Initialise(self):
        
        
        self.active__nav_item = self.SELECT_DATA_PAGE  # Default active item
        self.is_expanded_state = {'value': True}  # Initialize as True (expanded)
        
        
        self.Set_Data_Imported_Flag(False)
       

        self._Setup_initial_Views()
        
    def _Setup_initial_Views(self):
        
        
        self.select_data_view = Select_Data_View(page=self.page, controller=None)
        self.select_data_controller = Select_Data_Controller(self.page, self.Callback_To_Update_Sidebar_UI, self.select_data_view)
        self.select_data_view.controller = self.select_data_controller
        
        self.create_species_controller = Create_Species_Controller()
        self.create_species_view = Create_Species_View(self.page, self.create_species_controller)
        self.create_species_controller.view = self.create_species_view
        
        
        self.settings_controller = Settings_Controller(self.page)
        self.settings_view = SettingsView(self.page, self.settings_controller).build()
        
   
           
    def Set_Data_Imported_Flag(self, imported: bool):
        self.data_imported = imported
        
    def Callback_To_Update_Sidebar_UI(self, imported: bool):
        """Set the data imported status and update the UI"""
        self.Set_Data_Imported_Flag(imported)
        self.Refresh_Sidebar()
        
    def Refresh_Sidebar(self):
        """Refresh the sidebar to reflect current state (e.g., enabled/disabled items)"""
        self.sidebar_content.controls = self._build_sidebar_controls(
            self.is_expanded_state['value'], None
        )
        self.page.update()

    def show_about_dialog(self, e):
        self.about_dialog = About_Dialog_View(self.page)
        self.about_dialog.show()
        
    def navigate_to_page(self, page_name: str):
        """Navigate to the specified page and update the UI."""
    
        # Update active navigation item
        self.active__nav_item = page_name
        
        if page_name == self.EXIT_APPLICATION_PAGE:  
            logger.write("User chose to exit the application")
            self.page.open(Display_Exit_Dialog(self.page).get_dialog())
            return
        
        # Clear the main content area
        self.main_content_area.controls.clear()
        if page_name == self.CALCULATE_BIOMASS_PAGE:
            logger.write("User navigated to Calculate Biomass page")
            self.main_content_area.controls.append(self._Setup_Biomass_Calculation())
            
        elif page_name == self.CREATE_SPECIES_PAGE:
            logger.write("User navigated to Create Species page")
            self.main_content_area.controls.append(self.create_species_view.build())
            
        elif page_name == self.SETTINGS_PAGE:
            logger.write("User navigated to Settings page")
            self.main_content_area.controls.append(self.settings_view)
            
        elif page_name == self.MODIFY_SPECIES_PAGE:
            logger.write("User navigated to Modify Species page")
            self.modify_species_view = Modify_Species_View(self.page)
            self.main_content_area.controls.append(self.modify_species_view.build())
            
        elif page_name == self.SELECT_DATA_PAGE:
            logger.write("User navigated to Select Data page")
            self.main_content_area.controls.append(self.select_data_controller.build())
      
        # Refresh the sidebar to update active item highlighting
        self.Refresh_Sidebar()
   
    def _Setup_Biomass_Calculation(self) -> ft.Control:
        self.biomass_model = Calculate_Biomass_Model()
        self.biomass_view = Calculate_Biomass_View(None, page = self.page, selected_file_path=None)  # Pass None initially, set controller later
        self.biomass_controller = Calculate_Biomass_Controller(self.biomass_model, self.biomass_view, )
        self.biomass_view.controller = self.biomass_controller
        self.biomass_view.selected_file_path = self.select_data_controller.selected_file_path
        self.biomass_view_content = self.biomass_controller.build()
        return self.biomass_view_content

    def toggle_sidebar(self, e):
        """Toggle the sidebar state and update the UI."""
        # Determine the new state (toggle the existing state value)
        new_expanded_state = not self.is_expanded_state['value']
        self.is_expanded_state['value'] = new_expanded_state
        
        # Update the width on the Container reference
        self.sidebar.width = self.SIDEBAR_EXPANDED_WIDTH if new_expanded_state else self.SIDEBAR_COLLAPSED_WIDTH
        
        # Update the content (rebuild the control tree with the new state)
        self.sidebar_content.controls = self._build_sidebar_controls(new_expanded_state, e)
        
        
        # Animate the transition and update the page
        self.page.update()

    def _build_header_controls(self, is_expanded, on_click_handler):
        """Builds the logo/title header and the collapse button."""
        toggle_icon = ft.Icons.MENU_OPEN if is_expanded else ft.Icons.MENU
        
        # 1. Define the Toggle Row (Hamburger icon aligned right)
        toggle_row = ft.Row(
            controls=[
                ft.Container(expand=True),  # Pushes the icon to the right
                ft.IconButton(
                    icon=toggle_icon,
                    icon_color=ft.Colors.WHITE,
                    on_click=on_click_handler,
                    tooltip="Toggle Navigation",
                )
            ],
            alignment=ft.MainAxisAlignment.END,
            tight=True,  # Minimizes padding
        )

        # 2. Define the Logo/Title Row
        logo_title_row = ft.Row(
            controls=[
                # Icon stand-in for the Biomass Calculator logo
                ft.Icon(ft.Icons.FOREST, color=self.PRIMARY_COLOR, size=30),
                ft.Text("Biomass Calculator", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD, visible=is_expanded),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START if is_expanded else ft.MainAxisAlignment.CENTER,
        )
        
        # Container holding the header content and the toggle button
        return ft.Container(
            content=ft.Column(
                [
                    toggle_row,  # Hamburger icon (top)
                    logo_title_row,  # Logo/Title (middle)
                    Display_Version_Number(is_expanded=is_expanded),
                    ft.Divider(color=ft.Colors.WHITE24, height=1)  # Divider (bottom)
                ],
                tight=True,
                spacing=10
            ),
            padding=ft.padding.only(left=20, right=10, top=10, bottom=10)
        )

    def _build_sidebar_controls(self, is_expanded, e):
        """Builds all navigation items and footer buttons."""
        
        def create__nav_items():
            """Create navigation items based on page definitions"""
            
            # Define navigation items configuration
            navigation_config = [
                {
                    "page_id": self.SELECT_DATA_PAGE,
                    "icon": ft.Icons.RESTART_ALT,
                    "label": self.SELECT_DATA_PAGE,
                    "enabled": True,  # Always enabled
                },
                {
                    "page_id": self.CALCULATE_BIOMASS_PAGE,
                    "icon": ft.Icons.CALCULATE,
                    "label": self.CALCULATE_BIOMASS_PAGE,
                    "enabled": self.data_imported,  # Requires data import
                },
                {
                    "page_id": self.CREATE_SPECIES_PAGE,
                    "icon": ft.Icons.ADD_CIRCLE_OUTLINE,
                    "label": self.CREATE_SPECIES_PAGE,
                    "enabled": True,  # Always enabled
                },
                {
                    "page_id": self.MODIFY_SPECIES_PAGE,
                    "icon": ft.Icons.EDIT,
                    "label": self.MODIFY_SPECIES_PAGE,
                    "enabled": True,  # Always enabled
                },
                {
                    "page_id": self.SETTINGS_PAGE,
                    "icon": ft.Icons.SETTINGS,
                    "label": self.SETTINGS_PAGE,
                    "enabled": True,  # Always enabled
                },
                {
                    "page_id": self.EXIT_APPLICATION_PAGE,
                    "icon": ft.Icons.EXIT_TO_APP,
                    "label": self.EXIT_APPLICATION_PAGE,
                    "enabled": True,  # Always enabled
                },
            ]
            
            # Build navigation items from configuration
            nav_items = []
            for config in navigation_config:
                nav_item = Display_Nav_Item(
                    icon=config["icon"],
                    text=Remove_Underscores_And_Add_Space_And_Capitalise_Words(config["label"]),
                    is_expanded=is_expanded,
                    is_active=(self.active__nav_item == config["page_id"]),
                    on_click=lambda e, page_id=config["page_id"]: self.navigate_to_page(page_id),
                    enabled=config["enabled"]
                )
                nav_items.append(nav_item)
            
            return nav_items
        
        def create_footer_buttons():
            # About Button
            about_btn = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.INFO, color=ft.Colors.WHITE, size=20),
                        ft.Text("About", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, visible=is_expanded)
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START
                ),
                bgcolor=self.ACCENT_ABOUT,
                border_radius=10,
                padding=ft.padding.symmetric(vertical=12, horizontal=20),
                on_click=lambda e: About_Dialog_View(self.page).show(),
            )
            
            
            supported_species = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.SUPPORT, color=ft.Colors.WHITE, size=20),
                        ft.Text("Supported Species", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, visible=is_expanded)
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START
                ),
                bgcolor=ft.Colors.GREEN,
                border_radius=10,
                padding=ft.padding.symmetric(vertical=12, horizontal=20),
                on_click=lambda e: Supported_Species_Dialog(self.page).show(),
            )
            
            
            # Place buttons in a Column
            return ft.Column(
                [
                    ft.Divider(color=ft.Colors.WHITE24),
                    # Ensure alignment is correct for collapsed mode
                    ft.Container(
                        content=about_btn,
                        width=self.SIDEBAR_EXPANDED_WIDTH - 20 if is_expanded else self.SIDEBAR_COLLAPSED_WIDTH,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=supported_species,
                        width=self.SIDEBAR_EXPANDED_WIDTH - 20 if is_expanded else self.SIDEBAR_COLLAPSED_WIDTH,
                        alignment=ft.alignment.center
                    )
                ],
                spacing=15,
                tight=True
            )

        # The actual content column
        return [
            self._build_header_controls(is_expanded, self.toggle_sidebar),
            ft.Column(create__nav_items(), spacing=5),
            ft.Container(expand=True),
            ft.Container(content=create_footer_buttons(), padding=ft.padding.only(bottom=20, left=10, right=10))
        ]

    def build(self):
        """Build and return the main application layout"""
        
        self.sidebar_content = ft.Column(
            self._build_sidebar_controls(self.is_expanded_state['value'], None),
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )

        # --- Sidebar Container Definition ---
        self.sidebar = ft.Container(
            content=self.sidebar_content,
            width=self.SIDEBAR_EXPANDED_WIDTH,
            height=float('inf'),
            bgcolor=self.SIDEBAR_BACKGROUND,
            animate_size=100,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.BLACK54,
                offset=ft.Offset(2, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            )
        )

        # --- Main Content Area ---
        self.main_content_area = ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True
        )

        self.navigate_to_page("select_data")
        
        self.page.add(ft.Row(
                [
                    self.sidebar,
                    ft.VerticalDivider(width=1, color=ft.Colors.BLACK12),
                    self.main_content_area,
                ],
                expand=True,
                spacing=0,
                tight=True
            )
        )