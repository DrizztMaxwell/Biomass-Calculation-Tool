import flet as ft

class About_Dialog_View():
    def __init__(self, page: ft.Page):
        self.page = page
        self.container = self._create_about_container()
        self.overlay =  self._create_overlay()
        self.is_visible = False

    def show(self):
        """Show the about container with overlay"""
        self.page.overlay.append(self.overlay)
        self.page.overlay.append(self.container)
        self.page.update()
        print(self.page.overlay)
        


    def close(self, e=None):
        """Close the about container and remove overlay"""
        self.page.overlay.remove(self.overlay)
        self.page.overlay.remove(self.container)
        self.page.update()

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
        return ft.Column(
            [
                # Introduction
                ft.Text(
                    "This tool provides a reliable way to estimate the aboveground biomass of Canadian tree species by applying the national biomass equations developed by Lambert et al. (2005). "
                    "These equations were designed to support carbon accounting and forest management by converting standard forest inventory measurements into biomass estimates. The tool calculates biomass for individual tree components—wood, bark, branches, and foliage—and ensures that the sum of these components equals the total aboveground biomass. It uses species-specific allometric models based on diameter at breast height (DBH) and, when available, tree height, offering two levels of precision:",
                    size=14,
                    color=ft.Colors.GREY_800,
                    text_align=ft.TextAlign.JUSTIFY
                ),
            
                ft.Divider(height=30, color=ft.Colors.GREY_200),
            
                # Precision levels section
                ft.Text(
                    "Precision Types",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_900
                ),
            
                ft.Container(
                    content=ft.Column([
                        self._create_icon_with_text(ft.Icons.STRAIGHTEN, "DBH-based equations for situations where height data are unavailable.", "#10B981"),
                        self._create_icon_with_text(ft.Icons.HEIGHT, "DBH + height-based equations for improved accuracy when both measurements are provided.", "#3B82F6"),
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
                        self._create_icon_with_text(ft.Icons.PARK, "Covers 33 Canadian tree species, plus grouped equations for hardwoods, softwoods, and all species combined.", "#8B5CF6"),
                        self._create_icon_with_text(ft.Icons.ANALYTICS, "Provides outputs suitable for forest carbon budget estimation, ecological modeling, and operational planning.", "#F59E0B"),
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
                    margin=ft.margin.only(top=30),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=ft.border_radius.all(10),
                    border=ft.border.all(1, ft.Colors.BLUE_100)
                ),
            ], 
            spacing=0,
            scroll=ft.ScrollMode.ADAPTIVE,
            height=700,
           
        )
    
    def _create_icon_with_text(self, icon, text, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=color, size=18),
                ft.Text(text, size=14, color=ft.Colors.GREY_800, expand=True),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=8),
        )

    def _create_about_container(self):
        """Create the about section as a container"""
        return ft.Container(
            content=ft.Column(
                [
                    self._create_about_header(),
                    ft.Container(
                        padding=30,
                        content=self._create_about_content(),
                    ),
                ],
                spacing=0,
            ),
            bgcolor="white",
           
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            ),
            # Center the container on the screen
            top=100,
            left=0,
            right=0,
            margin=ft.margin.symmetric(horizontal=50),
            alignment=ft.alignment.center,
        )

    def update_view(self):
        """Update the view if needed"""
        self.page.update()