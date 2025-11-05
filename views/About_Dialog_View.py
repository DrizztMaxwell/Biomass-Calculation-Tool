import flet as ft

class About_Dialog_View():
    def __init__(self, page: ft.Page):
        self.page = page
        self.dialog = None

    def open_dialog(self, e=None):
        """Open the about dialog"""
        self.dialog = self.display_about_dialog()
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.open(self.dialog)
        
    def close_dialog(self, e):
        """Close the about dialog"""
        if self.dialog:
            self.dialog.open = False
            self.dialog.modal = False
            self.page.close(self.dialog)
        print(self.dialog)

    def _display_about_dialog_header(self):
        return ft.Container(
            content=ft.Row([
                # Info icon and title with elegant styling
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.INFO_ROUNDED, color="#34D399", size=32),
                        padding=ft.padding.all(0),
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
                    
                # Close button with hover effect
                ft.Container(
                    content=ft.Icon(ft.Icons.CLOSE_ROUNDED, color=ft.Colors.WHITE70, size=24),
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    ink=True,
                    on_click=lambda e: self.close_dialog(e),
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

    def _display_about_section_content(self):
        return ft.Column(
            [
                # Introduction
                ft.Text(
                    "This tool provides a reliable way to estimate the aboveground biomass of Canadian tree species by applying the national biomass equations developed by Lambert et al. (2005)."
                    "These equations were designed to support carbon accounting and forest management by converting standard forest inventory measurements into biomass estimates. The tool calculates biomass for individual tree components—wood, bark, branches, and foliage—and ensures that the sum of these components equals the total aboveground biomass. It uses species-specific allometric models based on diameter at breast height (DBH) and, when available, tree height, offering two levels of precision:",
                    size=14,
                    color=ft.Colors.GREY_800,
                    text_align=ft.TextAlign.JUSTIFY
                ),
            
                ft.Divider(height=30, color=ft.Colors.GREY_200),
            
                # Precision levels section
                # ft.Text(
                #     "Calculation Methodology",
                #     size=16,
                #     weight=ft.FontWeight.BOLD,
                #     color=ft.Colors.GREY_900
                # ),
                # ft.Text(
                #     "The tool calculates biomass for individual tree components—wood, bark, branches, and foliage—and ensures that the sum equals total aboveground biomass. "
                #     "It uses species-specific allometric models offering two precision levels:",
                #     size=14,
                #     color=ft.Colors.GREY_700,
                #     text_align=ft.TextAlign.JUSTIFY
                # ),
            

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
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=ft.border_radius.all(10),
                    border=ft.border.all(1, ft.Colors.BLUE_100)
                ),

                # Additional content to demonstrate scrolling
                ft.Divider(height=30, color=ft.Colors.GREY_200),
            
                # ft.Text(
                #     "Technical Details",
                #     size=16,
                #     weight=ft.FontWeight.BOLD,
                #     color=ft.Colors.GREY_900
                # ),
            
                # ft.Container(
                #     content=ft.Column([
                #         self._create_icon_with_text(ft.Icons.CODE, "Built with modern Python and Flet framework", "#06B6D4"),
                #         self._create_icon_with_text(ft.Icons.DATASET, "Uses validated scientific equations and coefficients", "#84CC16"),
                #         self._create_icon_with_text(ft.Icons.SECURITY, "Ensures data integrity and calculation accuracy", "#DC2626"),
                #         self._create_icon_with_text(ft.Icons.ACCESSIBILITY, "User-friendly interface for both technical and non-technical users", "#7C3AED"),
                #         self._create_icon_with_text(ft.Icons.UPLOAD_FILE, "Supports multiple input formats and export capabilities", "#F97316"),
                #     ], spacing=6),
                #     padding=ft.padding.only(left=15, top=15, bottom=15, right=15),
                #     bgcolor=ft.Colors.GREY_50,
                #     border_radius=ft.border_radius.all(10),
                #     margin=ft.margin.symmetric(vertical=12)
                # ),

                # ft.Divider(height=30, color=ft.Colors.GREY_200),
            
                # ft.Text(
                #     "Future Enhancements",
                #     size=16,
                #     weight=ft.FontWeight.BOLD,
                #     color=ft.Colors.GREY_900
                # ),
            
                # ft.Container(
                #     content=ft.Column([
                #         self._create_icon_with_text(ft.Icons.TRENDING_UP, "Additional species and regional variations", "#10B981"),
                #         self._create_icon_with_text(ft.Icons.CLOUD_UPLOAD, "Cloud-based calculations and data storage", "#3B82F6"),
                #         self._create_icon_with_text(ft.Icons.SHARE, "Collaborative features and sharing capabilities", "#8B5CF6"),
                #         self._create_icon_with_text(ft.Icons.AUTO_GRAPH, "Advanced visualization and reporting tools", "#F59E0B"),
                #     ], spacing=6),
                #     padding=ft.padding.only(left=15, top=15, bottom=15, right=15),
                #     bgcolor=ft.Colors.GREY_50,
                #     border_radius=ft.border_radius.all(10),
                #     margin=ft.margin.symmetric(vertical=12)
                # ),
            ], 
            spacing=0,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
    
    def _create_icon_with_text(self, icon, text, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=color, size=18),
                ft.Text(text, size=14, color=ft.Colors.GREY_800, expand=True),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=8),
        )

    def display_about_dialog(self):
        return ft.AlertDialog(
            # modal=True,
            bgcolor="white",
            content=ft.Column(
                [
                    self._display_about_dialog_header(),
                    ft.Container(
                        padding=40,
                        content=self._display_about_section_content(),
                        expand=True
                        # padding=ft.padding.all(25),
                    ),
                ],
                spacing=0,
                tight=True,
            ),
        )

    def update_view(self):
        self.page.update()