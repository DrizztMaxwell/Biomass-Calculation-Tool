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
        screen_height = self.page.height
        
        # Make the dialog larger to fit more content without scrolling
        dialog_width = min(max(screen_width * 0.85, 800), 1400)  # Increased max width
        dialog_height = min(max(screen_height * 0.90, 700), 1000)  # Increased height
        
        # Update container dimensions
        self.container.width = dialog_width
        self.container.height = dialog_height
        
        # Center the container
        self.container.left = (screen_width - dialog_width) / 2
        self.container.top = (screen_height - dialog_height) / 2

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
                            size=26, 
                            weight=ft.FontWeight.BOLD, 
                            color=ft.Colors.WHITE,
                            font_family="Poppins-Medium"
                        ),
                        ft.Text(
                            "Biomass Calculator", 
                            size=15, 
                            color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE),
                            font_family="Poppins-Regular"
                        ),
                    ], spacing=4)
                ], spacing=18),
                    
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

    def _create_about_content(self):
        """Create compact content section with reduced spacing"""
        return ft.Column(
            [
                # Introduction - reduced line spacing and smaller text
                ft.Text(
                    "This tool provides a reliable way to estimate the aboveground biomass of Canadian tree species by applying the national biomass equations developed by Lambert et al. (2005). "
                    "These equations were designed to support carbon accounting and forest management by converting standard forest inventory measurements into biomass estimates. The tool calculates biomass for individual tree components—wood, bark, branches, and foliage—and ensures that the sum of these components equals the total aboveground biomass. It uses species-specific allometric models based on diameter at breast height (DBH) and, when available, tree height, offering two levels of precision:",
                    size=13,  # Reduced from 14
                    color=ft.Colors.PRIMARY,
                    text_align=ft.TextAlign.JUSTIFY
                ),
            
                ft.Divider(height=20, color=ft.Colors.GREY_200),  # Reduced from 30
            
                # Precision levels section
                ft.Text(
                    "Precision Types",
                    size=15,  # Reduced from 16
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.PRIMARY
                ),
            
                ft.Container(
                    content=ft.Column([
                        self._create_icon_with_text(ft.Icons.STRAIGHTEN, "DBH-based equations for situations where height data are unavailable.", "#10B981"),
                        self._create_icon_with_text(ft.Icons.HEIGHT, "DBH + height-based equations for improved accuracy when both measurements are provided.", "#3B82F6"),
                    ], spacing=4),  # Reduced spacing
                    padding=ft.padding.only(left=12, top=10, bottom=10, right=12),  # Reduced padding
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=ft.border_radius.all(10),
                    margin=ft.margin.symmetric(vertical=8)  # Reduced margin
                ),
            
                ft.Divider(height=20, color=ft.Colors.GREY_200),  # Reduced from 30
            
                # Key features section
                ft.Text(
                    "Key Features",
                    size=15,  # Reduced from 16
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.PRIMARY
                ),
            
                ft.Container(
                    content=ft.Column([
                        self._create_icon_with_text(ft.Icons.PARK, "Covers 33 Canadian tree species, plus grouped equations for hardwoods, softwoods, and all species combined.", "#8B5CF6"),
                        self._create_icon_with_text(ft.Icons.ANALYTICS, "Provides outputs suitable for forest carbon budget estimation, ecological modeling, and operational planning.", "#F59E0B"),
                    ], spacing=4),  # Reduced spacing
                    padding=ft.padding.only(left=12, top=10, bottom=10, right=12),  # Reduced padding
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=ft.border_radius.all(10),
                    margin=ft.margin.symmetric(vertical=8)  # Reduced margin
                ),
            
                ft.Divider(height=20, color=ft.Colors.GREY_200),  # Reduced from 30
            
                # Target audience - made more compact
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Intended For",
                            size=15,  # Reduced from 16
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                        ft.Text(
                            "Researchers, forest managers, and policy analysts who require consistent and scientifically robust biomass estimates across Canada.",
                            size=13,  # Reduced from 14
                            color=ft.Colors.BLACK,
                            text_align=ft.TextAlign.JUSTIFY
                        ),
                    ], spacing=6),  # Reduced spacing
                    padding=ft.padding.all(15),  # Reduced padding
                    margin=ft.margin.only(top=15),  # Reduced margin
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=ft.border_radius.all(10),
                    border=ft.border.all(1, ft.Colors.BLUE_100)
                ),
                
                ft.Divider(height=20, color=ft.Colors.GREY_200),  # Reduced from 30
                
                # Development and Contact section - made more compact
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Development & Contact",
                            size=15,  # Reduced from 16
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.PRIMARY
                        ),
                        ft.Text(
                            "This biomass calculation tool was developed by the Ontario Ministry of Natural Resources and Forestry in collaboration with Trent University. For more information, please contact:",
                            size=13,  # Reduced from 14
                            color=ft.Colors.PRIMARY,
                            text_align=ft.TextAlign.JUSTIFY
                        ),
                        
                        # Email links container with reduced spacing
                        ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.MAIL_OUTLINED, color="#EA580C", size=16),  # Reduced icon size
                                        ft.Text(
                                            "Jamshid Eslamdoust",
                                            size=13,  # Reduced from 14
                                            color=ft.Colors.BLACK,
                                            weight=ft.FontWeight.W_500
                                        ),
                                    ], spacing=8),  # Reduced spacing
                                    padding=ft.padding.symmetric(vertical=6, horizontal=12),  # Reduced padding
                                    border_radius=ft.border_radius.all(8),
                                    bgcolor=ft.Colors.ORANGE_50,
                                    border=ft.border.all(1, ft.Colors.ORANGE_100),
                                    on_click=lambda e: self._open_email("Jamshid.Eslamdoust@ontario.ca"),
                                    data="Jamshid.Eslamdoust@ontario.ca",
                                    ink=True,
                                ),
                                
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.MAIL_OUTLINED, color="#0284C7", size=16),  # Reduced icon size
                                        ft.Text(
                                            "Christopher Stratton",
                                            size=13,  # Reduced from 14
                                            color=ft.Colors.BLACK,
                                            weight=ft.FontWeight.W_500
                                        ),
                                    ], spacing=8),  # Reduced spacing
                                    padding=ft.padding.symmetric(vertical=6, horizontal=12),  # Reduced padding
                                    border_radius=ft.border_radius.all(8),
                                    bgcolor=ft.Colors.BLUE_50,
                                    border=ft.border.all(1, ft.Colors.BLUE_100),
                                    on_click=lambda e: self._open_email("Christopher.Stratton@ontario.ca"),
                                    data="Christopher.Stratton@ontario.ca",
                                    ink=True,
                                ),
                            ], spacing=6),  # Reduced spacing
                            margin=ft.margin.only(top=10),  # Reduced margin
                        ),
                        
                        ft.Text(
                            "Click on any email address above to open your default email client.",
                            size=11,  # Reduced from 12
                            color=ft.Colors.GREY_600,
                            italic=True,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ], spacing=8),  # Reduced spacing between sections
                    padding=ft.padding.all(15),  # Reduced padding
                    margin=ft.margin.only(top=15),  # Reduced margin
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=ft.border_radius.all(10),
                    border=ft.border.all(1, ft.Colors.GREY_200)
                ),
            ], 
            spacing=0,  # No spacing between main sections
            scroll=ft.ScrollMode.AUTO,  # Keep AUTO scroll just in case, but with compact layout it shouldn't be needed
            expand=True,
        )
    
    def _open_email(self, email_address):
        """Open default email client with the specified email address"""
        self.page.launch_url(f"mailto:{email_address}")
        
    def _create_icon_with_text(self, icon, text, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=color, size=16),  # Reduced icon size
                ft.Text(text, size=13, color=ft.Colors.PRIMARY, expand=True),  # Reduced text size
            ], spacing=10),  # Reduced spacing
            padding=ft.padding.symmetric(vertical=6),  # Reduced padding
        )

    def _create_about_container(self):
        """Create the about section as a responsive container"""
        return ft.Container(
            content=ft.Column(
                [
                    self._create_about_header(),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=25, vertical=20),  # Reduced padding
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