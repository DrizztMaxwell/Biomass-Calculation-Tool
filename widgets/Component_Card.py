import flet as ft
from typing import Dict, Callable

def Component_Card(item: Dict, on_hover_handler: Callable, on_click_handler: Callable) -> ft.Container:
    """
    A reusable Flet functional component for displaying a component card.

    It handles the visual layout based on the item data and attaches
    controller event handlers for hover and click interactions.
    """
    
    title = item.get("title", "Unknown")
    image_src = item.get("image_src", "./assets/images/default.png")
    is_selected = item.get("is_selected", False)

    initial_bgcolor = "#A3FFDA" if is_selected else "white"

    # Create and configure the ft.Container
    return ft.Container(
        # The data property is crucial for the controller to identify which card was clicked/hovered
        data=title,
        bgcolor=initial_bgcolor,
        margin=10,
        padding=10,
        width=150,
        height=150,
        
        # Attach controller methods
        on_hover=on_hover_handler,
        on_click=on_click_handler,
        
        # Styling and animation
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
            offset=ft.Offset(0, 3),
        ),
        animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),

        # Card Content Layout
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Image(
                    src=image_src,
                    width=50,
                    height=50,
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                ),
                ft.Text(title, color="black", font_family="Arial", size=18, weight=ft.FontWeight.W_600)
            ]
        )
    )
