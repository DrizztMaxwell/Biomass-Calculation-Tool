import flet as ft
from Main_View import Main_View
from model.Main_Model import Main_Model
from Create_Species import AddSpeciesForm
from controller.Create_Species_Controller import Create_Species_Controller


# --- Configuration Constants ---
SIDEBAR_BACKGROUND = "#1B2433" # Dark background color from the image
SIDEBAR_EXPANDED_WIDTH = 250
SIDEBAR_COLLAPSED_WIDTH = 80
PRIMARY_COLOR = "#34D399" # A bright, light green
ACCENT_DISCLAIMER = "#34D399" # Bright green for the Disclaimer button
ACCENT_ABOUT = "#8B5CF6" # Purple for the About button
ACTIVE_ITEM_BG = ft.Colors.with_opacity(0.1, ft.Colors.WHITE) # Subtle highlight for active item

# --- Custom Navigation Item Component ---
def NavItem(page, icon: str, text: str, is_expanded: bool, is_active: bool = False, on_click=None):
    
    """Creates a custom, responsive navigation item."""
    
    # Define the visual appearance of the item based on its state (expanded vs. collapsed)
    
    # 1. Base Content (Icon and Text)
    content = ft.Row(
        [
            ft.Icon(icon, color=ft.Colors.WHITE, size=24),
            ft.Text(text, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
        ],
        spacing=15,
        # The Text component's visibility is implicitly handled by the Row's overall width 
        # and the fact that NavItem is only called with the correct is_expanded state.
        visible=is_expanded 
    )

    # 2. Wrapper Container
    container = ft.Container(
        content=content if is_expanded else ft.Icon(icon, color=ft.Colors.WHITE, size=28),
        # Style/Coloring
        bgcolor=PRIMARY_COLOR if is_active else None,
        border_radius=10,
        ink=True,
        # Padding and Alignment
        padding=ft.padding.symmetric(vertical=12, horizontal=20) if is_expanded else ft.padding.symmetric(vertical=15),
        alignment=ft.alignment.center_left if is_expanded else ft.alignment.center,
        # Tooltip for collapsed state
        tooltip=text if not is_expanded else None,
        on_click=on_click,  # Use the passed on_click handler
        # If collapsed, give it a fixed width to ensure the icon is centered
        width=float('inf') if is_expanded else SIDEBAR_COLLAPSED_WIDTH 
    )

    return container

# --- About Dialog Component ---
def show_about_dialog(e, page):
    """Shows the About the Tool dialog as a modal popup."""
    
    def close_dialog(e):
        about_dialog.open = False
        page.update()
    
    # Header with gradient background and close button
    header = ft.Container(
        content=ft.Row([
            # Info icon and title
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.INFO, color=ft.Colors.WHITE, size=28),
                    padding=ft.padding.all(12),
                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                    border_radius=ft.border_radius.all(12),
                ),
                ft.Column([
                    ft.Text("About the Tool", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Biomass Calculator v1.0", size=14, color=ft.Colors.WHITE70),
                ], spacing=2)
            ], spacing=15),
            
            # Close button (X) at top right
            ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_color=ft.Colors.WHITE,
                on_click=close_dialog,
                tooltip="Close",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    side=ft.BorderSide(width=1, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                )
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.all(25),
        border_radius=ft.border_radius.only(top_left=15, top_right=15),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#4F46E5", "#7C3AED"]
        )
    )
    
    # Feature items with improved styling
    def create_feature_item(icon, text, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=color, size=18),
                ft.Text(text, size=14, color=ft.Colors.GREY_800, expand=True),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=8),
        )
    
    # Main content with increased padding and scroll
    about_content = ft.Container(
        content=ft.Column(
            [
                header,
                
                # Scrollable main content area
                ft.Container(
                    content=ft.Column([
                        # Introduction
                        ft.Text(
                            "This tool provides a reliable way to estimate the aboveground biomass of Canadian tree species by applying the national biomass equations developed by Lambert et al (2005). "
                            "These equations were designed to support carbon accounting and forest management by converting standard forest inventory measurements into biomass estimates.",
                            size=14,
                            color=ft.Colors.GREY_800,
                            text_align=ft.TextAlign.JUSTIFY
                        ),
                        
                        ft.Divider(height=30, color=ft.Colors.GREY_200),  # Increased height
                        
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
                            ], spacing=6),  # Increased spacing
                            padding=ft.padding.only(left=15, top=15, bottom=15, right=15),  # Increased padding
                            bgcolor=ft.Colors.GREY_50,
                            border_radius=ft.border_radius.all(10),
                            margin=ft.margin.symmetric(vertical=12)  # Increased margin
                        ),
                        
                        ft.Divider(height=30, color=ft.Colors.GREY_200),  # Increased height
                        
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
                            ], spacing=6),  # Increased spacing
                            padding=ft.padding.only(left=15, top=15, bottom=15, right=15),  # Increased padding
                            bgcolor=ft.Colors.GREY_50,
                            border_radius=ft.border_radius.all(10),
                            margin=ft.margin.symmetric(vertical=12)  # Increased margin
                        ),
                        
                        ft.Divider(height=30, color=ft.Colors.GREY_200),  # Increased height
                        
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
                            ], spacing=10),  # Increased spacing
                            padding=ft.padding.all(20),  # Increased padding
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
                    ], spacing=0),
                    padding=ft.padding.all(40),  # Increased from 35 to 40
                ),
                
               
            ],
            spacing=0
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(15),
        width=650,  # Slightly increased width to accommodate more padding
        height=600,  # Fixed height to enable scrolling
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=25,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            offset=ft.Offset(0, 10),
        )
    )
    
    # Make the main content area scrollable
    scrollable_content = ft.Container(
        bgcolor="white",
        content=ft.Column(
            [
                # Scrollable content area
                ft.Container(
                    bgcolor="white",
                    content=ft.Column([
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
                            bgcolor=ft.Colors.WHITE,
                            content=ft.Column([
                                create_feature_item(ft.Icons.TRENDING_UP, "Additional species and regional variations", "#10B981"),
                                create_feature_item(ft.Icons.CLOUD_UPLOAD, "Cloud-based calculations and data storage", "#3B82F6"),
                                create_feature_item(ft.Icons.SHARE, "Collaborative features and sharing capabilities", "#8B5CF6"),
                                create_feature_item(ft.Icons.AUTO_GRAPH, "Advanced visualization and reporting tools", "#F59E0B"),
                            ], spacing=6),
                            padding=ft.padding.only(left=15, top=15, bottom=15, right=15),
                           
                            border_radius=ft.border_radius.all(10),
                            margin=ft.margin.symmetric(vertical=12)
                        ),
                    ], spacing=0),
                    padding=ft.padding.all(40),
                ),
            ],
            scroll=ft.ScrollMode.ADAPTIVE,  # Enable scrolling
            expand=True,
        ),
        expand=True,
    )

    # Final dialog structure with header, scrollable content, and footer
       # Final dialog structure with header, scrollable content, and footer
    about_dialog = ft.AlertDialog(
        modal=True,
        bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.BLACK),  # Customize overlay color/opacity
        content=ft.Column(
            [
                header,
                ft.Container(
                    content=scrollable_content,
                    height=400,  # Fixed height for scrollable area
                    expand=True,
                ),
                # Close button container
               
            ],
            spacing=0,
            expand=True
        ),
        shape=ft.RoundedRectangleBorder(radius=15),
    )
    
    page.dialog = about_dialog
    about_dialog.open = True
    page.open(about_dialog)
    page.update()

# --- Main Application Logic ---
def main(page: ft.Page):
    # Set up the page appearance
    page.title = "Biomass Calculator"
    page.bgcolor = ft.Colors.WHITE
    page.window_height = 800
    page.window_width = 1200
    page.padding = 0

    # --- State Management ---
    is_sidebar_expanded = ft.Ref[ft.Container]()
    is_expanded_state = {'value': True} # Initialize as True (expanded)
    current_page = ft.Ref[ft.Control]()  # Reference to track current page
    active_nav_item = ft.Ref[str]()  # Track which nav item is active

    # Initialize controllers and forms
    main_controller = Main_Controller(Main_Model(), Main_View())
    create_species_controller = Create_Species_Controller()
    add_species_form = AddSpeciesForm(create_species_controller)

    def navigate_to_page(page_name: str):
        """Navigate to the specified page and update the UI."""
        # Update active navigation item
        active_nav_item.current = page_name
        
        # Clear the main content area
        main_content_area.controls.clear()
        
        # Add the appropriate page based on selection
        if page_name == "calculate_biomass":
            # Render Main_View page
            main_view_content = main_controller.build()
            main_content_area.controls.append(main_view_content)
        elif page_name == "create_species":
            # Render Create Species page
            create_species_content = add_species_form.build(page=page)
            main_content_area.controls.append(create_species_content)
        elif page_name == "settings":
            # Render Settings page (placeholder)
            main_content_area.controls.append(
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
            main_content_area.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("Re-Import Dataset", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Dataset re-import functionality coming soon...")
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    expand=True,
                    alignment=ft.alignment.center
                )
            )
        elif page_name == "exit_application":
            # Exit application
            print("Exiting application...")
            # You can add proper exit logic here
            return
        
        # Update the sidebar to reflect active state
        sidebar_content.controls = build_sidebar_controls(is_expanded_state['value'], None)
        
        # Update the page
        page.update()

    def toggle_sidebar(e):
        """Toggle the sidebar state and update the UI."""
        
        # 1. Determine the new state (toggle the existing state value)
        new_expanded_state = not is_expanded_state['value']
        is_expanded_state['value'] = new_expanded_state # Update the stored state
        
        # 2. Update the width on the Container reference
        is_sidebar_expanded.current.width = SIDEBAR_EXPANDED_WIDTH if new_expanded_state else SIDEBAR_COLLAPSED_WIDTH
        
        # 3. Update the content (rebuild the control tree with the new state)
        sidebar_content.controls = build_sidebar_controls(new_expanded_state, e)
        
        # 4. Animate the transition and update the page
        page.update()

    # --- Header and Toggle ---
    def build_header_controls(is_expanded, on_click_handler):
        """Builds the logo/title header and the collapse button."""
        toggle_icon = ft.Icons.MENU_OPEN if is_expanded else ft.Icons.MENU
        
        # 1. Define the Toggle Row (Hamburger icon aligned right)
        toggle_row = ft.Row(
            controls=[
                ft.Container(expand=True), # Pushes the icon to the right
                ft.IconButton(
                    icon=toggle_icon,
                    icon_color=ft.Colors.WHITE,
                    on_click=on_click_handler,
                    tooltip="Toggle Navigation",
                )
            ],
            alignment=ft.MainAxisAlignment.END,
            tight=True, # Minimizes padding
        )

        # 2. Define the Logo/Title Row
        logo_title_row = ft.Row(
            controls=[
                # Icon stand-in for the Biomass Calculator logo
                ft.Icon(ft.Icons.FOREST, color=PRIMARY_COLOR, size=30),
                ft.Text("Biomass Calculator", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD, visible=is_expanded)
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START if is_expanded else ft.MainAxisAlignment.CENTER,
        )
        
        # Container holding the header content and the toggle button
        return ft.Container(
            content=ft.Column(
                [
                    toggle_row, # Hamburger icon (top)
                    logo_title_row, # Logo/Title (middle)
                    ft.Divider(color=ft.Colors.WHITE24, height=1) # Divider (bottom)
                ],
                tight=True,
                spacing=10
            ),
            # Keep padding for overall spacing
            padding=ft.padding.only(left=20, right=10, top=10, bottom=10)
        )

    # --- Sidebar Content (Navigation and Footer) ---
    def build_sidebar_controls(is_expanded, e):
        """Builds all navigation items and footer buttons."""
        
        # A utility to recreate NavItems based on the current state
        def create_nav_items():
            return [
                NavItem(
                    page, 
                    ft.Icons.CALCULATE, 
                    "Calculate Biomass", 
                    is_expanded, 
                    is_active=(active_nav_item.current == "calculate_biomass"),
                    on_click=lambda e: navigate_to_page("calculate_biomass")
                ),
                NavItem(
                    page, 
                    ft.Icons.ADD_CIRCLE_OUTLINE, 
                    "Create Species", 
                    is_expanded,
                    is_active=(active_nav_item.current == "create_species"),
                    on_click=lambda e: navigate_to_page("create_species")
                ),
                NavItem(
                    page, 
                    ft.Icons.SETTINGS, 
                    "Settings", 
                    is_expanded,
                    is_active=(active_nav_item.current == "settings"),
                    on_click=lambda e: navigate_to_page("settings")
                ),
                NavItem(
                    page, 
                    ft.Icons.RESTART_ALT, 
                    "Re-Import Dataset", 
                    is_expanded,
                    is_active=(active_nav_item.current == "reimport_dataset"),
                    on_click=lambda e: navigate_to_page("reimport_dataset")
                ),
                NavItem(
                    page, 
                    ft.Icons.EXIT_TO_APP, 
                    "Exit Application", 
                    is_expanded,
                    is_active=(active_nav_item.current == "exit_application"),
                    on_click=lambda e: navigate_to_page("exit_application")
                ),
            ]
        
        # A utility to recreate Footer Buttons based on the current state
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
                bgcolor=ACCENT_ABOUT,
                border_radius=10,
                padding=ft.padding.symmetric(vertical=12, horizontal=20),
                on_click=lambda e: show_about_dialog(e, page),
            )
            
            # Place buttons in a Column
            return ft.Column(
                [
                    # Add divider above the About button
                    ft.Divider(color=ft.Colors.WHITE24),
                    
                    # The About button
                    about_btn if is_expanded else ft.Container(content=about_btn, width=SIDEBAR_COLLAPSED_WIDTH * 0.8),
                ],
                spacing=15,
                tight=True
            )

        # The actual content column
        return [
            build_header_controls(is_expanded, toggle_sidebar),
            ft.Column(create_nav_items(), spacing=5),
            ft.Container(expand=True),
            ft.Container(content=create_footer_buttons(), padding=ft.padding.only(bottom=20, left=10, right=10))
        ]

    # Initialize the sidebar content as expanded
    sidebar_content = ft.Column(
        build_sidebar_controls(is_expanded_state['value'], None),
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
    )

    # --- Sidebar Container Definition ---
    sidebar = ft.Container(
        ref=is_sidebar_expanded,
        content=sidebar_content,
        width=SIDEBAR_EXPANDED_WIDTH,
        height=float('inf'),
        bgcolor=SIDEBAR_BACKGROUND,
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
    main_content_area = ft.Column(
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
                sidebar,
                ft.VerticalDivider(width=1, color=ft.Colors.BLACK12),
                main_content_area,
            ],
            expand=True,
            spacing=0,
            tight=True
        )
    )

    # Set initial page to Calculate Biomass
    active_nav_item.current = "calculate_biomass"
    navigate_to_page("calculate_biomass")

if __name__ == "__main__":
    ft.app(target=main)