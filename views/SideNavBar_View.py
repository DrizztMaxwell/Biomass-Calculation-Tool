import flet as ft
from views import Import_Data_View
from views.Main_View import Main_View
from model.Main_Model import Main_Model
from views.Create_Species import AddSpeciesForm
from controller.Create_Species_Controller import Create_Species_Controller
from controller.Main_Controller import Main_Controller
from views.Import_Data_View import ImportDataComponents

class BiomassCalculatorApp:
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
        self.page = None
        self.is_expanded_state = {'value': True}  # Initialize as True (expanded)
        self.active_nav_item = None
        self.sidebar = None
        self.sidebar_content = None
        self.main_content_area = None
        
        # Initialize controllers and forms
        self.main_controller = Main_Controller(Main_Model(), Main_View())
        self.create_species_controller = Create_Species_Controller()
        self.add_species_form = AddSpeciesForm(self.create_species_controller)

    def nav_item(self, icon: str, text: str, is_expanded: bool, is_active: bool = False, on_click=None):
        """Creates a custom, responsive navigation item."""
        
        # 1. Base Content (Icon and Text)
        content = ft.Row(
            [
                ft.Icon(icon, color=ft.Colors.WHITE, size=24),
                ft.Text(text, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
            ],
            spacing=15,
            visible=is_expanded 
        )

        # 2. Wrapper Container
        container = ft.Container(
            content=content if is_expanded else ft.Icon(icon, color=ft.Colors.WHITE, size=28),
            bgcolor=self.PRIMARY_COLOR if is_active else None,
            border_radius=10,
            ink=True,
            padding=ft.padding.symmetric(vertical=12, horizontal=20) if is_expanded else ft.padding.symmetric(vertical=15),
            alignment=ft.alignment.center_left if is_expanded else ft.alignment.center,
            tooltip=text if not is_expanded else None,
            on_click=on_click,
            width=float('inf') if is_expanded else self.SIDEBAR_COLLAPSED_WIDTH 
        )

        return container

    def show_about_dialog(self, e):
        """Shows the About the Tool dialog as a modal popup."""
        print("ℹ️ Showing About the Tool dialog")
        def close_dialog(e):
            # Close the dialog
            if self.page.dialog:
                self.page.dialog.open = False
                self.page.update()
    
        # Header with gradient background and close button
        header = ft.Container(
    content=ft.Row([
        # Info icon and title with elegant styling
        ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.INFO_ROUNDED, color="#34D399", size=32),
                padding=ft.padding.all(14),
                bgcolor=ft.Colors.with_opacity(0.15, "#34D399"),
                border_radius=ft.border_radius.all(16),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color=ft.Colors.with_opacity(0.3, "#34D399"),
                    offset=ft.Offset(0, 2),
                )
            ),
            ft.Column([
                ft.Text(
                    "About the Tool", 
                    size=26, 
                    weight=ft.FontWeight.BOLD, 
                    color=ft.Colors.WHITE,
                    font_family="Poppins-Medium"
                ),
                ft.Text(
                    "Biomass Calculator v1.0", 
                    size=15, 
                    color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE),
                    font_family="Poppins-Regular"
                ),
            ], spacing=4)
        ], spacing=18),
            
        # Close button with hover effect
        ft.Container(
            content=ft.Icon(ft.Icons.CLOSE_ROUNDED, color=ft.Colors.WHITE70, size=24),
            padding=ft.padding.all(10),
            border_radius=ft.border_radius.all(10),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
            ink=True,
            on_click=close_dialog,
            tooltip="Close",
        )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    padding=ft.padding.symmetric(horizontal=30, vertical=28),
    border_radius=ft.border_radius.only(top_left=20, top_right=20),
    bgcolor="#1B2433",
    shadow=ft.BoxShadow(
        spread_radius=0,
        blur_radius=20,
        color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
        offset=ft.Offset(0, 4),
    )
)
    
    
        def create_feature_item(icon, text, color):
            return ft.Container(
                content=ft.Row([
                    ft.Icon(icon, color=color, size=18),
                    ft.Text(text, size=14, color=ft.Colors.GREY_800, expand=True),
                ], spacing=12),
                padding=ft.padding.symmetric(vertical=8),
            )
    
        # Scrollable main content area
        scrollable_content = ft.Column(
            [
                # Introduction
                ft.Text(
                    "This tool provides a reliable way to estimate the aboveground biomass of Canadian tree species by applying the national biomass equations developed by Lambert et al (2005). "
                    "These equations were designed to support carbon accounting and forest management by converting standard forest inventory measurements into biomass estimates.",
                    size=14,
                    color=ft.Colors.GREY_800,
                    text_align=ft.TextAlign.JUSTIFY
                ),
            
                ft.Divider(height=30, color=ft.Colors.GREY_200),
            
                # Precision levels section
                ft.Text(
                    "Calculation Methodology",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_900
                ),
                ft.Text(
                    "The tool calculates biomass for individual tree components—wood, bark, branches, and foliage—and ensures that the sum equals total aboveground biomass. "
                    "It uses species-specific allometric models offering two precision levels:",
                    size=14,
                    color=ft.Colors.GREY_700,
                    text_align=ft.TextAlign.JUSTIFY
                ),
            
                ft.Container(
                    content=ft.Column([
                        create_feature_item(ft.Icons.STRAIGHTEN, "DBH-based equations for basic estimation", "#10B981"),
                        create_feature_item(ft.Icons.HEIGHT, "DBH + height-based equations for improved accuracy", "#3B82F6"),
                    ], spacing=6),
                    padding=ft.padding.only(left=15, top=15, bottom=15, right=15),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=ft.border_radius.all(10),
                    margin=ft.margin.symmetric(vertical=12)
                ),
            
                ft.Divider(height=30, color=ft.Colors.GREY_200),
            
                # Key features section
                ft.Text(
                    "Key Features",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_900
                ),
            
                ft.Container(
                    content=ft.Column([
                        create_feature_item(ft.Icons.PARK, "Covers 33 Canadian tree species with grouped equations", "#8B5CF6"),
                        create_feature_item(ft.Icons.ANALYTICS, "Outputs for carbon budget estimation and ecological modeling", "#F59E0B"),
                        create_feature_item(ft.Icons.SCIENCE, "Scientifically robust biomass estimates across Canada", "#EF4444"),
                    ], spacing=6),
                    padding=ft.padding.only(left=15, top=15, bottom=15, right=15),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=ft.border_radius.all(10),
                    margin=ft.margin.symmetric(vertical=12)
                ),
            
                ft.Divider(height=30, color=ft.Colors.GREY_200),
            
                # Target audience
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Intended For",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_900
                        ),
                        ft.Text(
                            "Researchers, forest managers, and policy analysts who require consistent and scientifically robust biomass estimates across Canada.",
                            size=14,
                            color=ft.Colors.GREY_700,
                            text_align=ft.TextAlign.JUSTIFY
                        ),
                    ], spacing=10),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=ft.border_radius.all(10),
                    border=ft.border.all(1, ft.Colors.BLUE_100)
                ),

                # Additional content to demonstrate scrolling
                ft.Divider(height=30, color=ft.Colors.GREY_200),
            
                ft.Text(
                    "Technical Details",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_900
                ),
            
                ft.Container(
                    content=ft.Column([
                        create_feature_item(ft.Icons.CODE, "Built with modern Python and Flet framework", "#06B6D4"),
                        create_feature_item(ft.Icons.DATASET, "Uses validated scientific equations and coefficients", "#84CC16"),
                        create_feature_item(ft.Icons.SECURITY, "Ensures data integrity and calculation accuracy", "#DC2626"),
                        create_feature_item(ft.Icons.ACCESSIBILITY, "User-friendly interface for both technical and non-technical users", "#7C3AED"),
                        create_feature_item(ft.Icons.UPLOAD_FILE, "Supports multiple input formats and export capabilities", "#F97316"),
                    ], spacing=6),
                    padding=ft.padding.only(left=15, top=15, bottom=15, right=15),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=ft.border_radius.all(10),
                    margin=ft.margin.symmetric(vertical=12)
                ),

                ft.Divider(height=30, color=ft.Colors.GREY_200),
            
                ft.Text(
                    "Future Enhancements",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_900
                ),
            
                ft.Container(
                    content=ft.Column([
                        create_feature_item(ft.Icons.TRENDING_UP, "Additional species and regional variations", "#10B981"),
                        create_feature_item(ft.Icons.CLOUD_UPLOAD, "Cloud-based calculations and data storage", "#3B82F6"),
                        create_feature_item(ft.Icons.SHARE, "Collaborative features and sharing capabilities", "#8B5CF6"),
                        create_feature_item(ft.Icons.AUTO_GRAPH, "Advanced visualization and reporting tools", "#F59E0B"),
                    ], spacing=6),
                    padding=ft.padding.only(left=15, top=15, bottom=15, right=15),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=ft.border_radius.all(10),
                    margin=ft.margin.symmetric(vertical=12)
                ),
            ], 
            spacing=0,
            scroll=ft.ScrollMode.ADAPTIVE,
        )


        # Final dialog structure
        about_dialog = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            content=ft.Column(
                [
                    header,
                    ft.Container(
                        content=scrollable_content,
                        height=400,
                        padding=ft.padding.all(25),
                    ),
                ],
                spacing=0,
                tight=True,
            ),
        )
    
        # Set the dialog and open it
        self.page.dialog = about_dialog
        about_dialog.open = True
        self.page.add(about_dialog)
        self.page.update()

    def navigate_to_page(self, page_name: str):
        """Navigate to the specified page and update the UI."""
        # Update active navigation item
        self.active_nav_item = page_name
        
        # Clear the main content area
        self.main_content_area.controls.clear()
        
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
        elif page_name == "reimport_dataset":
            # Render Re-Import Dataset page (placeholder)
            self.main_content_area.controls.append(
              ImportDataComponents.create_main_layout()
            )
        elif page_name == "exit_application":
            # Exit application
            print("Exiting application...")
            # You can add proper exit logic here
            return
        
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
                ft.Text("Biomass Calculator", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD, visible=is_expanded)
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
                    ft.Divider(color=ft.Colors.WHITE24, height=1)  # Divider (bottom)
                ],
                tight=True,
                spacing=10
            ),
            padding=ft.padding.only(left=20, right=10, top=10, bottom=10)
        )

    def _build_sidebar_controls(self, is_expanded, e):
        """Builds all navigation items and footer buttons."""
        
        def create_nav_items():
            return [
                self.nav_item(
                    ft.Icons.CALCULATE, 
                    "Calculate Biomass", 
                    is_expanded, 
                    is_active=(self.active_nav_item == "calculate_biomass"),
                    on_click=lambda e: self.navigate_to_page("calculate_biomass")
                ),
                self.nav_item(
                    ft.Icons.ADD_CIRCLE_OUTLINE, 
                    "Create Species", 
                    is_expanded,
                    is_active=(self.active_nav_item == "create_species"),
                    on_click=lambda e: self.navigate_to_page("create_species")
                ),
                self.nav_item(
                    ft.Icons.SETTINGS, 
                    "Settings", 
                    is_expanded,
                    is_active=(self.active_nav_item == "settings"),
                    on_click=lambda e: self.navigate_to_page("settings")
                ),
                self.nav_item(
                    ft.Icons.RESTART_ALT, 
                    "Re-Import Dataset", 
                    is_expanded,
                    is_active=(self.active_nav_item == "reimport_dataset"),
                    on_click=lambda e: self.navigate_to_page("reimport_dataset")
                ),
                self.nav_item(
                    ft.Icons.EXIT_TO_APP, 
                    "Exit Application", 
                    is_expanded,
                    is_active=(self.active_nav_item == "exit_application"),
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
            ft.Column(create_nav_items(), spacing=5),
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
        self.active_nav_item = "calculate_biomass"
        self.navigate_to_page("calculate_biomass")