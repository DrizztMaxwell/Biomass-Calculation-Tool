import flet as ft

class Parameter_Input:
    """Helper for parameter input fields."""
    
    @staticmethod
    def create(label: str, controller=None) -> ft.TextField:
        """Create a parameter input field."""
        
        def on_blur(e):
            if not e.control.value or e.control.value.strip() == "":
                e.control.value = "0.00"
                e.control.update()
        
        control = ft.TextField(
            label=label,
            height=50,
            width=120,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=5,
            keyboard_type=ft.KeyboardType.NUMBER,
            error_text=None,
            max_lines=1,
            text_align=ft.TextAlign.CENTER,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_color=ft.Colors.PRIMARY,
            focused_border_color=ft.Colors.PRIMARY,
            focused_border_width=2,
            border_width=1,
            label_style=ft.TextStyle(
                size=12,
                weight=ft.FontWeight.W_500,
                color=ft.Colors.PRIMARY,
            ),
            error_style=ft.TextStyle(
                size=11,
                color=ft.Colors.RED_600
            ),
            hint_text="0.00",
            hint_style=ft.TextStyle(
                size=13,
                color=ft.Colors.ON_PRIMARY_CONTAINER
            ),
            on_blur=on_blur,
        )
        
        if controller:
            controller.set_param_controls({control})
        
        return control