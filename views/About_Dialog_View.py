from widgets.LogFileTxt import logger
import flet as ft

class About_Dialog_View():
    def __init__(self, page: ft.Page):
        self.page = page
        self.container = self._create_about_container()
        self.overlay = self._create_overlay()
        self.is_visible = False

    def show(self):
        """Show the about container with overlay"""
        self.page.overlay.append(self.overlay)
        self.page.overlay.append(self.container)
        self.is_visible = True
        self._update_container_size()  # Update size based on current screen
        logger.write("Displayed About Dialog")
        self.page.update()
        
    def close(self, e=None):
        """Close the about container and remove overlay"""
        self.page.overlay.remove(self.overlay)
        self.page.overlay.remove(self.container)
        self.is_visible = False
        logger.write("Closed About Dialog")
        self.page.update()
    
    def _update_container_size(self):
        """Update container size based on current page dimensions"""
        # Calculate responsive width and height
        screen_width = self.page.width
        screen_height = self.page.height - 50  # Leave some vertical space for margins and potential taskbar
        
        # Use more of the screen, but leave margins
        dialog_width = min(max(screen_width * 0.90, 800), 1600)  # Increased max width
        dialog_height = min(max(screen_height * 0.95, 600), 1200)  # Use more height
        
        # Update container dimensions
        self.container.width = dialog_width
        self.container.height = dialog_height
        
        # Center the container
        self.container.left = (screen_width - dialog_width) / 2
        self.container.top = (screen_height - dialog_height) / 2
        
        # Update font sizes based on container height
        self._update_content_font_sizes(dialog_height)

    def _update_content_font_sizes(self, dialog_height):
        """Dynamically adjust font sizes based on available height"""
        # Base font sizes that will scale with dialog height
        base_height = 800  # Reference height
        
        # Calculate scale factor
        scale_factor = min(dialog_height / base_height, 1.2)  # Cap scaling at 1.2x
        
        # Update all text elements with scaled sizes
        self._update_text_sizes(scale_factor)

    def _update_text_sizes(self, scale_factor):
        """Update all text sizes in the content"""
        # This would need to be implemented by modifying the text widgets
        # or recreating the content with new sizes
        pass

    def _create_overlay(self):
        """Create a dimmed overlay background"""
        return ft.Container(
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            expand=True,
            on_click=lambda e: self.close(),
        )

    def _create_about_header(self):
        return ft.Container(
            content=ft.Row([
                # Info icon and title with elegant styling
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.INFO_ROUNDED, color="#34D399", size=32),
                        padding=ft.padding.all(8),
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
                            size=24,  # Reduced from 26
                            weight=ft.FontWeight.BOLD, 
                            color=ft.Colors.WHITE,
                        ),
                        ft.Text(
                            "Biomass Calculator", 
                            size=14,  # Reduced from 15
                            color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE),
                        ),
                    ], spacing=2)  # Reduced spacing
                ], spacing=14),  # Reduced spacing
                    
                # Close button
                ft.Container(
                    content=ft.Icon(ft.Icons.CLOSE_ROUNDED, color=ft.Colors.WHITE70, size=24),
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    ink=True,
                    on_click=lambda e: self.close(),
                    tooltip="Close",
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=25, vertical=20),  # Reduced padding
            border_radius=ft.border_radius.only(top_left=20, top_right=20),
            bgcolor="#1B2433",
        )

    def _create_about_content(self):
        """Create compact content section that fits without scrolling"""
        return ft.Container(
        padding=ft.padding.all(20)
        ,
            content=
    ft.Column(
            [
                # Introduction - very compact
                ft.Container(
                    content=ft.Text(
                        "This tool provides a reliable way to estimate the aboveground biomass of Canadian tree species by applying the national biomass equations developed by Lambert et al. (2005). "
                        "These equations were designed to support carbon accounting and forest management by converting standard forest inventory measurements into biomass estimates. The tool calculates biomass for individual tree components—wood, bark, branches, and foliage—and ensures that the sum of these components equals the total aboveground biomass. It uses species-specific allometric models based on diameter at breast height (DBH) and, when available, tree height, offering two levels of precision:",
                        size=12,  # Reduced further
                        color=ft.Colors.PRIMARY,
                        text_align=ft.TextAlign.JUSTIFY
                    ),
                    padding=ft.padding.all(12),
                    margin=ft.margin.only(bottom=8),
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=ft.border_radius.all(8),
                ),
            
                # Precision levels section - more compact
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Precision Types",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.PRIMARY,
                         
                        ),
                        self._create_compact_icon_with_text(ft.Icons.STRAIGHTEN, "DBH-based equations for situations where height data are unavailable.", "#10B981"),
                        self._create_compact_icon_with_text(ft.Icons.HEIGHT, "DBH + height-based equations for improved accuracy when both measurements are provided.", "#3B82F6"),
                    ], spacing=2),
                    padding=ft.padding.all(12),
                    margin=ft.margin.only(bottom=8),
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=ft.border_radius.all(8),
                ),
            
                # Key features section - more compact
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Key Features",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.PRIMARY,
                            # margin=ft.margin.only(bottom=6)
                        ),
                        self._create_compact_icon_with_text(ft.Icons.PARK, "Covers 33 Canadian tree species, plus grouped equations for hardwoods, softwoods, and all species combined.", "#8B5CF6"),
                        self._create_compact_icon_with_text(ft.Icons.ANALYTICS, "Provides outputs suitable for forest carbon budget estimation, ecological modeling, and operational planning.", "#F59E0B"),
                    ], spacing=2),
                    padding=ft.padding.all(12),
                    margin=ft.margin.only(bottom=8),
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=ft.border_radius.all(8),
                ),
            
                # Target audience - made more compact
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Intended For",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK,
                            # margin=ft.margin.only(bottom=6)
                        ),
                        ft.Text(
                            "Researchers, forest managers, and policy analysts who require consistent and scientifically robust biomass estimates across Canada.",
                            size=12,
                            color=ft.Colors.BLACK,
                            text_align=ft.TextAlign.JUSTIFY
                        ),
                    ], spacing=4),
                    padding=ft.padding.all(12),
                    margin=ft.margin.only(bottom=8),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=ft.border_radius.all(8),
                    border=ft.border.all(1, ft.Colors.BLUE_100)
                ),
                
                # Development and Contact section - made more compact
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Development & Contact",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.PRIMARY,
                            #   margin=ft.margin.only(bottom=6)
                        ),
                        ft.Container(height=4),  # Small spacer
                        ft.Text(
                            "This biomass calculation tool was developed by the Ontario Ministry of Natural Resources and Forestry in collaboration with Trent University. For more information, please contact:",
                            size=12,
                            color=ft.Colors.PRIMARY,
                            text_align=ft.TextAlign.JUSTIFY,
                           # margin=ft.margin.only(bottom=8)
                        ),
                        ft.Container(height=8),  # Small spacer
                        
                        # Email links container with minimal spacing
                        ft.Column([
                            self._create_compact_email_item("Jamshid Eslamdoust", "Jamshid.Eslamdoust@ontario.ca", "#EA580C"),
                            self._create_compact_email_item("Christopher Stratton", "Christopher.Stratton@ontario.ca", "#0284C7"),
                        ], spacing=4),
                        
                        ft.Text(
                            "Click on any email address above to open your default email client.",
                            size=10,
                            color=ft.Colors.GREY_600,
                            italic=True,
                            text_align=ft.TextAlign.CENTER,
                            # margin=ft.margin.only(top=8)
                        ),
                        ft.Container(height=4),  # Small spacer
                    ], spacing=4),
                    padding=ft.padding.all(12),
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=ft.border_radius.all(8),
                    border=ft.border.all(1, ft.Colors.GREY_200)
                ),
            ], 
            spacing=4,  # Very small spacing between sections
            expand=True,
        )
    )
    
    def _create_compact_icon_with_text(self, icon, text, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=color, size=14),  # Smaller icon
                ft.Text(text, size=11, color=ft.Colors.PRIMARY, expand=True),  # Smaller text
            ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.START),  # Reduced spacing
            padding=ft.padding.symmetric(vertical=3),  # Minimal padding
        )
    
    def _create_compact_email_item(self, name, email, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.MAIL_OUTLINED, color=color, size=14),  # Smaller icon
                ft.Column([
                    ft.Text(
                        name,
                        size=11,  # Smaller text
                        color=ft.Colors.PRIMARY,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Text(
                        email,
                        size=10,  # Smaller text
                        color=ft.Colors.GREY_600,
                    ),
                ], spacing=1)
            ], spacing=10),  # Reduced spacing
            padding=ft.padding.symmetric(vertical=5, horizontal=10),  # Reduced padding
            border_radius=ft.border_radius.all(6),
            bgcolor=ft.Colors.with_opacity(0.1, color),
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, color)),
            on_click=lambda e: self._open_email(email),
            margin=ft.margin.only(bottom=4),  # Small margin between email items
            ink=True,
        )
    
    def _open_email(self, email_address):
        """Open default email client with the specified email address"""
        self.page.launch_url(f"mailto:{email_address}")

    def _create_about_container(self):
        """Create the about section as a responsive container"""
        return ft.Container(
            content=ft.Column(
                [
                    self._create_about_header(),
                    ft.Container(
                        padding=ft.padding.all(15),  # Reduced padding
                        content=self._create_about_content(),
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            ),
            # Initial dimensions - will be updated in show() method
            width=800,
            height=700,
            top=0,
            left=0,
        )

    def update_view(self):
        """Update the view if needed"""
        self.page.update()