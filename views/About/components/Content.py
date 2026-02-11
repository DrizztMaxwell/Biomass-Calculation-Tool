import flet as ft

class Content:
    def __init__(self, email_callback):
        self.email_callback = email_callback
        
    def create(self):
        return ft.Column([
            # Introduction
            self._create_section(
                "This tool provides a reliable way to estimate the aboveground biomass of Canadian tree species by applying the national biomass equations developed by Lambert et al. (2005). "
                "These equations were designed to support carbon accounting and forest management by converting standard forest inventory measurements into biomass estimates. The tool calculates biomass for individual tree components—wood, bark, branches, and foliage—and ensures that the sum of these components equals the total aboveground biomass. It uses species-specific allometric models based on diameter at breast height (DBH) and, when available, tree height, offering two levels of precision:",
                None,
                bgcolor=ft.Colors.SECONDARY_CONTAINER
            ),
            
            # Precision levels section
            self._create_section(
                None,
                ft.Column([
                    ft.Text("Precision Types", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                    self._create_icon_with_text(ft.Icons.STRAIGHTEN, "DBH-based equations for situations where height data are unavailable.", "#10B981"),
                    self._create_icon_with_text(ft.Icons.HEIGHT, "DBH + height-based equations for improved accuracy when both measurements are provided.", "#3B82F6"),
                ], spacing=2),
                bgcolor=ft.Colors.SECONDARY_CONTAINER
            ),
            
            # Key features section
            self._create_section(
                None,
                ft.Column([
                    ft.Text("Key Features", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                    self._create_icon_with_text(ft.Icons.PARK, "Covers 33 Canadian tree species, plus grouped equations for hardwoods, softwoods, and all species combined.", "#8B5CF6"),
                    self._create_icon_with_text(ft.Icons.ANALYTICS, "Provides outputs suitable for forest carbon budget estimation, ecological modeling, and operational planning.", "#F59E0B"),
                ], spacing=2),
                bgcolor=ft.Colors.SECONDARY_CONTAINER
            ),
            
            # Target audience
            self._create_section(
                "Researchers, forest managers, and policy analysts who require consistent and scientifically robust biomass estimates across Canada.",
                ft.Text("Intended For", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.BLUE_50,
                border=ft.border.all(1, ft.Colors.BLUE_100),
                text_color=ft.Colors.BLACK
            ),
            
            # Development and Contact section
            self._create_contact_section(),
            
        ], spacing=4, expand=True)
    
    def _create_section(self, text_content, header_content, **kwargs):
        bgcolor = kwargs.get('bgcolor', ft.Colors.SECONDARY_CONTAINER)
        border = kwargs.get('border', None)
        text_color = kwargs.get('text_color', ft.Colors.PRIMARY)
        
        content = []
        
        if header_content:
            content.append(header_content)
            
        if text_content:
            content.append(
                ft.Text(
                    text_content,
                    size=12,
                    color=text_color,
                    text_align=ft.TextAlign.JUSTIFY
                )
            )
        
        return ft.Container(
            content=ft.Column(content, spacing=4 if text_content and header_content else 0),
            padding=ft.padding.all(12),
            margin=ft.margin.only(bottom=8),
            bgcolor=bgcolor,
            border_radius=ft.border_radius.all(8),
            border=border
        )
    
    def _create_icon_with_text(self, icon, text, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=color, size=14),
                ft.Text(text, size=11, color=ft.Colors.PRIMARY, expand=True),
            ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.START),
            padding=ft.padding.symmetric(vertical=3),
        )
    
    def _create_email_item(self, name, email, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.MAIL_OUTLINED, color=color, size=14),
                ft.Column([
                    ft.Text(name, size=11, color=ft.Colors.PRIMARY, weight=ft.FontWeight.W_500),
                    ft.Text(email, size=10, color=ft.Colors.GREY_600),
                ], spacing=1)
            ], spacing=10),
            padding=ft.padding.symmetric(vertical=5, horizontal=10),
            border_radius=ft.border_radius.all(6),
            bgcolor=ft.Colors.with_opacity(0.1, color),
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, color)),
            on_click=lambda e: self.email_callback(email),
            margin=ft.margin.only(bottom=4),
            ink=True,
        )
    
    def _create_contact_section(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Development & Contact", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                ft.Container(height=4),
                ft.Text(
                    "This biomass calculation tool was developed by the Ontario Ministry of Natural Resources and Forestry in collaboration with Trent University. For more information, please contact:",
                    size=12,
                    color=ft.Colors.PRIMARY,
                    text_align=ft.TextAlign.JUSTIFY,
                ),
                ft.Container(height=8),
                
                ft.Column([
                    self._create_email_item("Jamshid Eslamdoust", "Jamshid.Eslamdoust@ontario.ca", "#EA580C"),
                    self._create_email_item("Christopher Stratton", "Christopher.Stratton@ontario.ca", "#0284C7"),
                ], spacing=4),
                
                ft.Text(
                    "Click on any email address above to open your default email client.",
                    size=10,
                    color=ft.Colors.GREY_600,
                    italic=True,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=4),
            ], spacing=4),
            padding=ft.padding.all(12),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(1, ft.Colors.GREY_200)
        )