import flet as ft


class Parameter_Input:
    """Helper for parameter input fields."""

    @staticmethod
    def create(label: str, controller=None) -> ft.TextField:

        def on_blur(e):
            val = (e.control.value or "").strip()
            if not val:
                e.control.value = "0.000000"
                e.control.error_text = None
            else:
                try:
                    e.control.value = f"{float(val):.6f}"
                    e.control.error_text = None
                except ValueError:
                    e.control.error_text = "Invalid"
            e.control.update()

        control = ft.TextField(
            label=label,
            hint_text="0.000000",
            height=54,
            text_size=14,
            text_align=ft.TextAlign.CENTER,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=12),
            border_radius=8,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_lines=1,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_color=ft.Colors.OUTLINE_VARIANT,
            focused_border_color=ft.Colors.PRIMARY,
            focused_border_width=2,
            border_width=1,
            color=ft.Colors.ON_SURFACE,
            label_style=ft.TextStyle(
                size=13,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.ON_SURFACE_VARIANT,
            ),
            hint_style=ft.TextStyle(size=13, color=ft.Colors.OUTLINE),
            error_style=ft.TextStyle(size=11, color=ft.Colors.ERROR),
            on_blur=on_blur,
        )

        if controller:
            controller.set_param_controls({control})

        return control