import flet as ft


class Display_Exit_Dialog:
    def __init__(self, page: ft.Page):
        self.page    = page
        self._overlay = None

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):             return "#1A1A1A" if self._is_dark else "#FFFFFF"
    def _border(self):         return "#2E2E2E" if self._is_dark else "#E2E8F0"
    def _text_primary(self):   return "#F5F5F5" if self._is_dark else "#0F172A"
    def _text_secondary(self): return "#888888" if self._is_dark else "#64748B"

    # ── Actions ───────────────────────────────────────────────────────────────

    def yes_clicked(self, e):
        self.page.window.destroy()

    def no_clicked(self, e):
        self.close_dialog()

    # ── Build overlay ─────────────────────────────────────────────────────────

    def _build_overlay(self) -> ft.Container:
        # ── Header ────────────────────────────────────────────────────────────
        header = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=20, color="#FFFFFF"),
                    bgcolor=ft.Colors.with_opacity(0.18, "#FFFFFF"),
                    border_radius=ft.border_radius.all(9),
                    width=40, height=40,
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text("Exit Application", size=16,
                            weight=ft.FontWeight.W_700, color="#FFFFFF"),
                    ft.Text("Are you sure you want to quit?",
                            size=12,
                            color=ft.Colors.with_opacity(0.80, "#FFFFFF")),
                ], spacing=2, tight=True, expand=True),
            ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=24, vertical=22),
            bgcolor="#DC2626",
            border_radius=ft.border_radius.only(top_left=14, top_right=14),
        )

        # ── Body ──────────────────────────────────────────────────────────────
        body = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=15, color="#D97706"),
                ft.Text("Any unsaved data will be lost when you exit.",
                        size=13, color=self._text_secondary(), expand=True),
            ], spacing=8),
            bgcolor=ft.Colors.with_opacity(0.08, "#D97706"),
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, "#D97706")),
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            margin=ft.margin.symmetric(horizontal=24, vertical=20),
        )

        # ── Actions ───────────────────────────────────────────────────────────
        def _btn(label, icon, on_click, bgcolor, text_color, border=None):
            return ft.Container(
                content=ft.Row([
                    ft.Icon(icon, size=14, color=text_color),
                    ft.Text(label, size=13, weight=ft.FontWeight.W_600,
                            color=text_color),
                ], spacing=6, tight=True),
                on_click=on_click,
                bgcolor=bgcolor,
                border=border,
                border_radius=ft.border_radius.all(8),
                padding=ft.padding.symmetric(horizontal=18, vertical=10),
                ink=True,
            )

        actions = ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                _btn("Stay", ft.Icons.ARROW_BACK_ROUNDED,
                     self.no_clicked,
                     ft.Colors.with_opacity(
                         0.06, ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK
                     ),
                     self._text_primary(),
                     border=ft.border.all(1, self._border())),
                ft.Container(width=8),
                _btn("Exit Anyway", ft.Icons.LOGOUT_ROUNDED,
                     self.yes_clicked, "#DC2626", "#FFFFFF"),
            ]),
            padding=ft.padding.only(left=24, right=24, bottom=22, top=12),
            bgcolor=self._bg(),
            border=ft.border.only(top=ft.BorderSide(1, self._border())),
            border_radius=ft.border_radius.only(bottom_left=14, bottom_right=14),
        )

        # ── Card ──────────────────────────────────────────────────────────────
        card = ft.Container(
            content=ft.Column([header, body, actions], spacing=0, tight=True),
            bgcolor=self._bg(),
            border_radius=ft.border_radius.all(14),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            shadow=ft.BoxShadow(
                blur_radius=40, spread_radius=0,
                color=ft.Colors.with_opacity(0.35, ft.Colors.BLACK),
                offset=ft.Offset(0, 10),
            ),
            width=440,
        )

        # ── Full-screen overlay ───────────────────────────────────────────────
        return ft.Container(
            content=card,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.65, ft.Colors.BLACK),
            expand=True,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def get_dialog(self):
        """Backwards compatible: opens the dialog and returns self."""
        self.open_dialog()
        return self

    def open_dialog(self):
        self._overlay = self._build_overlay()
        self.page.overlay.append(self._overlay)
        self.page.update()

    def close_dialog(self):
        if self._overlay and self._overlay in self.page.overlay:
            self.page.overlay.remove(self._overlay)
            self._overlay = None
        self.page.update()