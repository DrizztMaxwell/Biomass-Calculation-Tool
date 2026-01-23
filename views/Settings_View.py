import flet as ft
from widgets.LogFileTxt import logger
class SettingsView:
    def __init__(self, page: ft.Page):
        self.page = page
        
  
        
    def toggle_theme(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        logger.write(f"Theme toggled to: {self.page.theme_mode}")
        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.bgcolor = ft.Colors.BLACK
        else:
            self.page.bgcolor = ft.Colors.WHITE
        self.page.update()
    
    def build(self):
        # logger.write(f"Current Theme Mode: {self.page.theme_mode}")
        # Header Section
        header = ft.Container(
            content=ft.Column([
                ft.Text("Settings", color=ft.Colors.PRIMARY, size=32, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Customize your experience and application preferences", 
                    color=ft.Colors.PRIMARY,
                    size=14
                ),
            ], spacing=8),
            margin=ft.margin.only(bottom=30),
        )

        # Appearance Card
        appearance_card = ft.Container(
           
            content=ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PALETTE_OUTLINED, color=ft.Colors.BLUE_700, size=28),
                    title=ft.Text("Appearance", color=ft.Colors.ON_PRIMARY_CONTAINER, size=18, weight=ft.FontWeight.W_600),
                    subtitle=ft.Text("Change the look and feel of the app",  color=ft.Colors.ON_PRIMARY_CONTAINER, size=13),
                    content_padding=ft.padding.all(16),
                ),
                ft.Divider(height=1, thickness=1, color=ft.Colors.GREY_300),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.DARK_MODE_OUTLINED, size=20, color=ft.Colors.GREY_700),
                            ft.Container(width=12),
                            ft.Switch(
                                label="Dark Theme", 
                                label_style=ft.TextStyle(color=ft.Colors.PRIMARY),
                                value=True if self.page.theme_mode == ft.ThemeMode.DARK else False,
                                on_change=self.toggle_theme,
                                active_color=ft.Colors.TERTIARY,
                            ),
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=16),
                    ], spacing=12),
                    padding=ft.padding.all(20),
                )
            ], spacing=0),
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_300),
          
  bgcolor=ft.Colors.SECONDARY_CONTAINER,

            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

      
        # Main container with padding
        main_content = ft.Container(
            
            bgcolor= ft.Colors.SECONDARY,
            content=ft.Column([
                header,
                appearance_card,
                ft.Container(height=20),
              
            ], spacing=0),
            padding=ft.padding.all(40),
            expand=True,
        )
        
        # Scrollable wrapper
        return ft.Container(
            content=ft.Column([
            
            main_content
        ], scroll=ft.ScrollMode.ADAPTIVE, expand=True)
        , expand=True
        )

