import flet as ft


def DescriptionText(
    message: str,
    size: int = 13,
    color: str = None,
    font_weight=ft.FontWeight.W_400,
) -> ft.Text:
    """Muted description text — uses ON_SURFACE_VARIANT to adapt to dark/light mode."""
    return ft.Text(
        message,
        size=size,
        weight=font_weight,
        color=color or ft.Colors.ON_SURFACE_VARIANT,
    )