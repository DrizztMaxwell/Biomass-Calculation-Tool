import flet as ft


class Custom_Alert_Dialog:
    def __init__(
        self,
        page: ft.Page,
        title_icon: ft.Icons,
        title_color: ft.Color,
        title_icon_color: ft.Color,
        title: str = "Error",
        message: str = "",
        solution: str = "",
        button_text: str = "I Understand",
    ):
        self.page = page
        self._dialog = None

        # Derive accent color from title_icon_color for theming
        self._icon       = title_icon
        self._icon_color = title_icon_color
        self._title      = title
        self._message    = message
        self._solution   = solution
        self._btn_text   = button_text

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):
        return "#1A1A1A" if self._is_dark else "#FFFFFF"

    def _surface(self):
        return "#222222" if self._is_dark else "#F8FAFC"

    def _border(self):
        return "#2E2E2E" if self._is_dark else "#E2E8F0"

    def _text_primary(self):
        return "#F5F5F5" if self._is_dark else "#0F172A"

    def _text_secondary(self):
        return "#888888" if self._is_dark else "#64748B"

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build(self) -> ft.AlertDialog:
        # Resolve icon color to a hex string if it's a Flet color token
        # We'll use it for the icon badge bg
        icon_color = self._icon_color

        # Icon badge
        icon_badge = ft.Container(
            content=ft.Icon(self._icon, size=22, color=icon_color),
            bgcolor=ft.Colors.with_opacity(0.12, icon_color),
            border_radius=ft.border_radius.all(10),
            width=44, height=44,
            alignment=ft.alignment.center,
        )

        # Header
        header = ft.Container(
            content=ft.Row([
                icon_badge,
                ft.Column([
                    ft.Text(
                        self._title, size=16,
                        weight=ft.FontWeight.W_700,
                        color=self._text_primary(),
                    ),
                ], spacing=0, tight=True, expand=True),
                # Close X
                ft.Container(
                    content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=15,
                                    color=self._text_secondary()),
                    on_click=lambda e: self._close(),
                    bgcolor=ft.Colors.with_opacity(
                        0.06, ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK
                    ),
                    border_radius=ft.border_radius.all(7),
                    padding=ft.padding.all(5),
                    ink=True,
                    tooltip="Close",
                ),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(left=20, right=20, top=18, bottom=14),
            bgcolor=self._surface(),
            border_radius=ft.border_radius.only(top_left=12, top_right=12),
        )

        # Body
        body_controls = [
            ft.Text(self._message, size=13, color=self._text_secondary()),
        ]
        if self._solution:
            body_controls += [
                ft.Container(height=8),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.LIGHTBULB_OUTLINE_ROUNDED, size=13,
                                color=icon_color),
                        ft.Text(self._solution, size=12,
                                weight=ft.FontWeight.W_500,
                                color=self._text_secondary(), expand=True),
                    ], spacing=8),
                    bgcolor=ft.Colors.with_opacity(0.07, icon_color),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.15, icon_color)),
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                ),
            ]

        body = ft.Container(
            content=ft.Column(body_controls, spacing=0, tight=True),
            padding=ft.padding.symmetric(horizontal=20, vertical=14),
            bgcolor=self._bg(),
        )

        # Divider
        divider = ft.Container(height=1, bgcolor=self._border())

        # Actions
        actions = ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_ROUNDED, size=14, color="#FFFFFF"),
                        ft.Text(self._btn_text, size=13,
                                weight=ft.FontWeight.W_600, color="#FFFFFF"),
                    ], spacing=6, tight=True),
                    on_click=lambda e: self._close(),
                    bgcolor=icon_color,
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.symmetric(horizontal=18, vertical=9),
                    ink=True,
                ),
            ]),
            padding=ft.padding.only(left=20, right=20, top=12, bottom=16),
            bgcolor=self._bg(),
            border=ft.border.only(top=ft.BorderSide(1, self._border())),
        )

        main = ft.Container(
            content=ft.Column([
                header,
                ft.Container(height=1, bgcolor=self._border()),
                body,
                actions,
            ], spacing=0, tight=True),
            width=400,
            bgcolor=self._bg(),
            border_radius=ft.border_radius.all(12),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            shadow=ft.BoxShadow(
                blur_radius=24, spread_radius=0,
                color=ft.Colors.with_opacity(0.18, ft.Colors.BLACK),
                offset=ft.Offset(0, 6),
            ),
        )

        return ft.AlertDialog(
            modal=True,
            content=main,
            content_padding=ft.padding.all(0),
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor=ft.Colors.TRANSPARENT,
            inset_padding=ft.padding.symmetric(horizontal=40, vertical=20),
            alignment=ft.alignment.center,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def show(self):
        self._dialog = self._build()
        self.page.open(self._dialog)

    def _close(self):
        if self._dialog:
            self.page.close(self._dialog)

    def close_alert(self, e):
        self._close()