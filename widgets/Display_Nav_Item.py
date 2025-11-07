import flet as ft

def Display_Nav_Item( icon: str, text: str, is_expanded: bool, is_active: bool = False, on_click=None, bgcolor="#34D399", SIDEBAR_COLLAPSED_WIDTH=80):
        """Creates a custom, responsive navigation item."""
        print(is_active)
        # 1. Base Content (Icon and Text)
        content = ft.Row(
            [
                ft.Icon(icon, color=ft.Colors.WHITE, size=24),
                ft.Text(text, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)
            ],
            spacing=15,
            visible=is_expanded 
        )

        # 2. Wrapper Container
        container = ft.Container(
                
            content=content if is_expanded else ft.Icon(icon, color=ft.Colors.WHITE, size=28),
            bgcolor=bgcolor if is_active else None,
            border_radius=10,
            ink=True,
            margin=ft.margin.only(left=10, top=0, right=10, bottom=5), # Applies specific margins,
            padding=ft.padding.symmetric(vertical=10, horizontal=15) if is_expanded else ft.padding.symmetric(vertical=15),
            alignment=ft.alignment.center_left if is_expanded else ft.alignment.center,
            tooltip=text if not is_expanded else None,
            on_click=on_click,
            width=float('inf') if is_expanded else SIDEBAR_COLLAPSED_WIDTH 
        )

        return container