import flet as ft


def Create_Label_With_Icon(page: ft.Page, label_text: str = "", icon_src: str = "", width: int = 27, height: int = 27):
    """Create a label with an icon that adapts to light/dark mode"""
    # Determine image color based on theme
    image_color = ft.Colors.WHITE if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLACK
    
    return ft.Column([
        ft.Row([
            ft.Text(
                label_text, 
                font_family="Poppins-Medium",  
                weight=ft.FontWeight.W_700, 
                color=ft.Colors.PRIMARY, 
                size=15
            ),
            ft.Image(
                src=icon_src,
                width=width,
                height=height,
                fit=ft.ImageFit.CONTAIN,
                color=image_color
            )
        ]),
    ])