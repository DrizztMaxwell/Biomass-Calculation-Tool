import flet as ft

def Display_Nav_Item(icon: str, text: str, is_expanded: bool, is_active: bool = False, on_click=None, bgcolor="#34D399", SIDEBAR_COLLAPSED_WIDTH=80, enabled: bool = True) -> ft.Container:
    """Creates a custom, responsive navigation item."""
    print(f"Nav Item: {text}, Active: {is_active}, Enabled: {enabled}")
    
    # Determine colors based on enabled state
    if enabled:
        icon_color = ft.Colors.WHITE
        text_color = ft.Colors.WHITE
        active_bgcolor = bgcolor if is_active else None
    else:
        icon_color = ft.Colors.GREY_500  # Grey for disabled
        text_color = ft.Colors.GREY_500  # Grey for disabled
        active_bgcolor = None  # No active background when disabled

    # 1. Base Content (Icon and Text)
    content = ft.Row(
        [
            ft.Icon(icon, color=icon_color, size=24),
            ft.Text(text, color=text_color, weight=ft.FontWeight.W_500)
        ],
        spacing=15,
        visible=is_expanded 
    )

    # 2. Wrapper Container
    container = ft.Container(
        content=content if is_expanded else ft.Icon(icon, color=icon_color, size=28),
        bgcolor=active_bgcolor,
        border_radius=10,
        ink=True,
        margin=ft.margin.only(left=10, top=0, right=10, bottom=5),
        padding=ft.padding.symmetric(vertical=10, horizontal=15) if is_expanded else ft.padding.symmetric(vertical=15),
        alignment=ft.alignment.center_left if is_expanded else ft.alignment.center,
        tooltip=text if not is_expanded else (f"{text} (Import data first)" if not enabled else text),
        on_click=on_click if enabled else None,
        width=float('inf') if is_expanded else SIDEBAR_COLLAPSED_WIDTH,
        opacity=0.6 if not enabled else 1.0,  # Additional visual indication
        disabled=not enabled  # Properly disable the container
    )

    return container