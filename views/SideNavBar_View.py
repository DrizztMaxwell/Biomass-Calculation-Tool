import os
import sys
import flet as ft
from views import Import_Data_View
from views.Main_View import Main_View
from model.Main_Model import Main_Model
from views.Create_Species import AddSpeciesForm
from controller.Create_Species_Controller import Create_Species_Controller
from controller.Main_Controller import Main_Controller
from views.Import_Data_View import ImportDataComponents
from views.About_Dialog_View import About_Dialog_View
from widgets.Display_Nav_Item import Display_Nav_Item
from widgets.Display_Version_Number import Display_Version_Number
from widgets.Display_Exit_Dialog import Display_Exit_Dialog

class SideNavBar_View:
    """Main application class for the Biomass Calculator"""
    
    # --- Configuration Constants ---
    SIDEBAR_BACKGROUND = "#1B2433"  # Dark background color from the image
    SIDEBAR_EXPANDED_WIDTH = 250
    SIDEBAR_COLLAPSED_WIDTH = 80
    PRIMARY_COLOR = "#34D399"  # A bright, light green
    ACCENT_DISCLAIMER = "#34D399"  # Bright green for the Disclaimer button
    ACCENT_ABOUT = "#8B5CF6"  # Purple for the About button
    ACTIVE_ITEM_BG = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)  # Subtle highlight for active item

    def __init__(self):
        self._initialise()

    def _initialise(self):
        self.page = None
        self.is_expanded_state = {'value': True}  # Initialize as True (expanded)
        self.active__nav_item = None
        self.sidebar = None
        self.sidebar_content = None
        self.main_content_area = None
      
        
        # Initialize controllers and forms
        self.main_controller = Main_Controller(Main_Model(), Main_View())
        self.create_species_controller = Create_Species_Controller()
        self.add_species_form = AddSpeciesForm(self.create_species_controller)

    def show_about_dialog(self,e):
        about_dialog = About_Dialog_View(self.page)
        about_dialog.open_dialog()
        
    def _exit_application_direct(self):
        """Exit application without any UI interactions that could cause recursion."""
        print("Exiting application...")

        exit_dialog = Display_Exit_Dialog(self.yes_clicked, self.no_clicked)
        self.exit_dialog = exit_dialog
        self.page.open(exit_dialog)
        # Close window directly without page.update()
        # self.page.window.destroy()


    def yes_clicked(self,e):
        self.page.window.destroy()

    # Handle the "No" button click - close the dialog
    def no_clicked(self,e):
        self.page.dialog = self.exit_dialog
        self.page.close(self.exit_dialog)


    def navigate_to_page(self, page_name: str):
        """Navigate to the specified page and update the UI."""
    
        # Update active navigation item
        self.active__nav_item = page_name
        
        # Clear the main content area
        self.main_content_area.controls.clear()
        if page_name == "exit_application":
            self._exit_application_direct()
            return

        # Add the appropriate page based on selection
        if page_name == "calculate_biomass":
            # Render Main_View page
            main_view_content = self.main_controller.build()
            self.main_content_area.controls.append(main_view_content)
        elif page_name == "create_species":
            # Render Create Species page
            create_species_content = self.add_species_form.build(page=self.page)
            self.main_content_area.controls.append(create_species_content)
        elif page_name == "settings":
            # Render Settings page (placeholder)
            self.main_content_area.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("Settings Page", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Settings functionality coming soon...")
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    expand=True,
                    alignment=ft.alignment.center
                )
            )
        elif page_name == "select_data":
            # Render Re-Import Dataset page (placeholder)
            self.main_content_area.controls.append(
            ImportDataComponents.create_main_layout()
            )
        # elif page_name == "exit_application":
            

           
        #     # self.page.window.destroy()
        #     # # Add an alert giving option Yes or No
        #     # return # <--- THIS IS THE KEY FIX
            
        #     #
        
        # Update the sidebar to reflect active state
        self.sidebar_content.controls = self._build_sidebar_controls(self.is_expanded_state['value'], None)
        
        # Update the page
        self.page.update()
    


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
            return [
                Display_Nav_Item(
                    ft.Icons.RESTART_ALT, 
                    "Select Data", 
                    is_expanded,
                    is_active=(self.active__nav_item == "select_data"),

                    on_click=lambda e: self.navigate_to_page("select_data")
                 
                ),
                Display_Nav_Item(
                    ft.Icons.CALCULATE, 
                    "Calculate Biomass", 
                    is_expanded, 
                    is_active=(self.active__nav_item == "calculate_biomass"),
                    on_click=lambda e: self.navigate_to_page("calculate_biomass")
                )
            ,
               Display_Nav_Item(ft.Icons.ADD_CIRCLE_OUTLINE, 
                    "Create Species", 
                    is_expanded,
                    is_active=(self.active__nav_item == "create_species"),
                    on_click=lambda e: self.navigate_to_page("create_species"))
,
                Display_Nav_Item(
                    ft.Icons.SETTINGS, 
                    "Settings", 
                    is_expanded,
                    is_active=(self.active__nav_item == "settings"),
                    on_click=lambda e: self.navigate_to_page("settings")
                ),
               
                Display_Nav_Item(
                    ft.Icons.EXIT_TO_APP, 
                    "Exit Application", 
                    is_expanded,
                    is_active=(self.active__nav_item == "exit_application"),
                    on_click=lambda e: self.navigate_to_page("exit_application")
                ),
            ]
        
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
                on_click=self.show_about_dialog,
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

    

    def main(self, page: ft.Page):
        """Main application entry point"""
        self.page = page
        
        # Set up the page appearance
        page.title = "Biomass Calculator"
        page.bgcolor = ft.Colors.WHITE
        page.window_height = 800
        page.window_width = 1200
        page.padding = 0

        # Initialize the sidebar content as expanded
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

        # Set fonts
        page.fonts = {
            "Poppins-Medium": "./assets/fonts/poppins/Poppins-Medium.ttf",
            "Poppins-Regular": "./assets/fonts/poppins/Poppins-Regular.ttf" 
        }

        # --- Final Layout ---
        page.add(
            ft.Row(
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
           # Set initial page to Calculate Biomass
        self.active__nav_item = "select_data"
        self.navigate_to_page("select_data")

       