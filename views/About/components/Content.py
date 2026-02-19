import flet as ft

class Content:
    def __init__(self, email_callback, page: ft.Page):
        self.email_callback = email_callback
        self.page = page
        self._init_colors()
        
    def _init_colors(self):
        """Initialize colors based on current theme mode"""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            # Light theme colors
            self.bg_color = ft.Colors.WHITE
            self.section_bg_1 = ft.Colors.BLUE_50
            self.section_bg_2 = ft.Colors.GREEN_50
            self.section_bg_3 = ft.Colors.YELLOW_50
            self.contact_bg = ft.Colors.BLUE_GREY_50
            
            self.title_color = ft.Colors.BLUE_900
            self.text_color = ft.Colors.BLUE_GREY_800
            self.icon_color = ft.Colors.BLUE_GREY_400
            self.contact_title_color = ft.Colors.BLUE_GREY_900
            
            self.chip_border_color = ft.Colors.BLACK12
            self.chip_text_color = ft.Colors.BLUE_GREY_900
            
            self.email_pill_bg = ft.Colors.WHITE
            self.email_pill_border_opacity = 0.1
            
            self.email_color_1 = ft.Colors.ORANGE_800
            self.email_color_2 = ft.Colors.BLUE_800
            
        else:
            # Dark theme colors
            self.bg_color = ft.Colors.GREY_900
            self.section_bg_1 = ft.Colors.with_opacity(0.15, ft.Colors.BLUE_900)
            self.section_bg_2 = ft.Colors.with_opacity(0.15, ft.Colors.GREEN_900)
            self.section_bg_3 = ft.Colors.with_opacity(0.15, ft.Colors.YELLOW_900)
            self.contact_bg = ft.Colors.with_opacity(0.2, ft.Colors.ORANGE_900)
            
            self.title_color = ft.Colors.BLUE_200
            self.text_color = ft.Colors.GREY_300
            self.icon_color = ft.Colors.BLUE_GREY_300
            self.contact_title_color = ft.Colors.BLUE_100
            
            self.chip_border_color = ft.Colors.with_opacity(0.2, ft.Colors.WHITE)
            self.chip_text_color = ft.Colors.GREY_300
            
            self.email_pill_bg = ft.Colors.GREY_800
            self.email_pill_border_opacity = 0.3
            
            self.email_color_1 = ft.Colors.ORANGE_400
            self.email_color_2 = ft.Colors.BLUE_300
        
    def update_colors(self):
        """Update colors when theme changes"""
        self._init_colors()
        
    def create(self):
        return ft.Column([
            # Section 1: Intro (The "Lead")
            self._create_stack_item(
                "Overview",
                "This tool estimates aboveground biomass for Canadian tree species using national equations (Lambert et al. 2005). It converts standard forest inventory measurements into biomass estimates for carbon accounting and forest management. Biomass is calculated for individual tree components—wood, bark, branches, and foliage—with the sum equaling total aboveground biomass. Species-specific allometric models offer two precision levels: DBH-based equations (when height is unavailable) and more accurate DBH + height-based equations (when both measurements are provided).",
                ft.Icons.ANALYTICS_ROUNDED,
                self.section_bg_1
            ),
            
            # Section 2: Precision & Features
            self._create_stack_item(
                "Precision & Features",
                "Estimates aboveground biomass for 33 Canadian tree species using national equations (Lambert et al. 2005). Calculates biomass for wood, bark, branches, and foliage—summing to total biomass. Choose between DBH-based or more accurate DBH + height-based equations.",
                ft.Icons.SPEED_ROUNDED,
                self.section_bg_2
            ),
           
            # Section 3: Target Audience
            self._create_stack_item(
                "Intended For",
                "Researchers, forest managers, and policy analysts requiring robust biomass estimates across Canada.",
                ft.Icons.GROUPS_ROUNDED,
                self.section_bg_3
            ),
            
            # Section 4: Contact (Streamlined)
            ft.Container(
                margin=ft.margin.only(top=5),
                content=ft.Column([
                    ft.Text(
                        "Development & Contact", 
                        size=13, 
                        weight=ft.FontWeight.BOLD, 
                        color=self.contact_title_color
                    ),
                    ft.Row([
                        self._create_email_pill("Jamshid Eslamdoust", "Jamshid.Eslamdoust@ontario.ca", self.email_color_1),
                        self._create_email_pill("Christopher Stratton", "Christopher.Stratton@ontario.ca", self.email_color_2),
                    ], spacing=10, alignment=ft.MainAxisAlignment.START),
                ], spacing=8),
                padding=12,
                bgcolor=self.contact_bg,
                border_radius=10,
            ),
        ], spacing=12, alignment=ft.MainAxisAlignment.START, expand=True)

    def _create_stack_item(self, title, text, icon, bgcolor):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=20, color=self.icon_color),
                ft.Column([
                    ft.Text(
                        title, 
                        size=16, 
                        weight=ft.FontWeight.BOLD, 
                        color=self.title_color
                    ),
                    ft.Text(
                        text, 
                        size=13, 
                        color=self.text_color, 
                        width=700
                    ),
                ], spacing=2, expand=True)
            ], vertical_alignment=ft.CrossAxisAlignment.START),
            padding=12,
            bgcolor=bgcolor,
            border_radius=10,
        )

    def _create_info_chip(self, icon, label, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=14, color=color),
                ft.Text(
                    label, 
                    size=13, 
                    weight=ft.FontWeight.W_500, 
                    color=self.chip_text_color
                ),
            ], spacing=5),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border=ft.border.all(1, self.chip_border_color),
            border_radius=20,
        )

    def _create_email_pill(self, name, email, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.MAIL_ROUNDED, size=14, color=color),
                ft.Text(
                    f"{name} ({email})", 
                    size=13, 
                    weight=ft.FontWeight.W_500,
                    color=self.text_color,
                ),
            ], spacing=8),
            on_click=lambda _: self.email_callback(email),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            bgcolor=self.email_pill_bg,
            border=ft.border.all(1, ft.Colors.with_opacity(self.email_pill_border_opacity, color)),
            border_radius=8,
            ink=True,
            ink_color=ft.Colors.with_opacity(0.2, color),
        )