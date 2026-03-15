import flet as ft


class Calculate_Biomass_Button:
    """Calculate Biomass action button — matches app Container + ink=True style."""

    def __init__(self, on_click_callback, is_disabled: bool = False):
        self.on_click_callback = on_click_callback
        self.is_disabled       = is_disabled
        self._container        = None

    def create(self) -> ft.Row:
        self._container = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CALCULATE_ROUNDED, size=18, color="#FFFFFF"),
                ft.Text("Calculate Biomass", size=15,
                        weight=ft.FontWeight.W_600, color="#FFFFFF"),
            ], spacing=8, tight=True),
            on_click=None if self.is_disabled else self.on_click_callback,
            bgcolor="#16A34A" if not self.is_disabled else "#4A4A4A",
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.symmetric(horizontal=28, vertical=14),
            ink=not self.is_disabled,
            opacity=1.0 if not self.is_disabled else 0.5,
            shadow=ft.BoxShadow(
                blur_radius=8, spread_radius=0,
                color=ft.Colors.with_opacity(
                    0.25 if not self.is_disabled else 0.0, "#16A34A"
                ),
                offset=ft.Offset(0, 3),
            ),
            animate_opacity=ft.Animation(200, ft.AnimationCurve.LINEAR),
        )
        return ft.Row(
            [self._container],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def disable(self):
        if self._container:
            self._container.bgcolor   = "#4A4A4A"
            self._container.opacity   = 0.5
            self._container.ink       = False
            self._container.on_click  = None
            self._container.shadow    = None
            self._container.update()

    def enable(self):
        if self._container:
            self._container.bgcolor   = "#16A34A"
            self._container.opacity   = 1.0
            self._container.ink       = True
            self._container.on_click  = self.on_click_callback
            self._container.shadow    = ft.BoxShadow(
                blur_radius=8, spread_radius=0,
                color=ft.Colors.with_opacity(0.25, "#16A34A"),
                offset=ft.Offset(0, 3),
            )
            self._container.update()