import flet as ft

class Header:
    def __init__(self, close_callback, page: ft.Page):
        self.close_callback = close_callback
        self.page = page
        self._init_colors()
        
    def _init_colors(self):
        """Initialize colors based on current theme mode"""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.bg_color = "#1A202C"  # Deep slate for light mode
            self.title_color = ft.Colors.WHITE
            self.subtitle_color = ft.Colors.BLUE_200
            self.icon_color = ft.Colors.BLUE_400
            self.close_icon_color = ft.Colors.WHITE70
            self.close_overlay_color = ft.Colors.WHITE10
        else:
            self.bg_color = "#0F1219"  # Even darker for dark mode
            self.title_color = ft.Colors.WHITE
            self.subtitle_color = ft.Colors.PURPLE_300
            self.icon_color = ft.Colors.PURPLE_400
            self.close_icon_color = ft.Colors.WHITE60
            self.close_overlay_color = ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_400)
        
    def update_colors(self):
        """Update colors when theme changes"""
        self._init_colors()
        
    def create(self):
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(
                        ft.Icons.SETTINGS_SUGGEST_ROUNDED, 
                        color=self.icon_color, 
                        size=28
                    ),
                    ft.Column([
                        ft.Text(
                            "About This Tool", 
                            size=18, 
                            weight=ft.FontWeight.W_800, 
                            color=self.title_color
                        ),
                        ft.Text(
                            "Biomass Calculator | MNRF & Trent University", 
                            size=11, 
                            color=self.subtitle_color
                        ),
                    ], spacing=0)
                ], spacing=15),
                ft.IconButton(
                    icon=ft.Icons.CLOSE_ROUNDED,
                    icon_color=self.close_icon_color,
                    on_click=lambda _: self.close_callback(),
                    style=ft.ButtonStyle(overlay_color=self.close_overlay_color)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=25, vertical=15),
            bgcolor=self.bg_color,
            border_radius=ft.border_radius.only(top_left=15, top_right=15)
        )