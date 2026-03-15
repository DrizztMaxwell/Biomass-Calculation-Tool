import flet as ft


def Create_Label_With_Icon(
    page: ft.Page,
    label_text: str = "",
    icon_src: str = "",
    width: int = 16,
    height: int = 16,
) -> ft.Row:
    """
    Field label with optional small icon beside it.
    Uses ON_SURFACE color so it adapts to dark/light mode automatically.
    """
    controls = [
        ft.Text(
            label_text,
            size=13,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.ON_SURFACE,
        ),
    ]

    if icon_src:
        controls.append(
            ft.Image(
                src=icon_src,
                width=width,
                height=height,
                fit=ft.ImageFit.CONTAIN,
                color=ft.Colors.ON_SURFACE,
            )
        )

    return ft.Row(
        controls,
        spacing=6,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )