import flet as ft
from controller.Settings_Controller import Settings_Controller
from constants.Settings_Constants import SettingsConstants
from .components.Build_Theme_Toggle_Switch import Build_Theme_Toggle_Switch


class SettingsView:
    """View for application settings and preferences."""

    def __init__(self, page: ft.Page, controller: Settings_Controller):
        self.page       = page
        self.controller = controller
        self.cnst       = SettingsConstants()

        # Persistent controls so we can rebuild on theme change
        self._content_col   = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)
        self._outer         = ft.Container(expand=True, margin=ft.margin.all(20))

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):           return "#1A1A1A" if self._is_dark else "#FFFFFF"
    def _surface(self):      return "#222222" if self._is_dark else "#F8FAFC"
    def _surface_card(self): return "#2A2A2A" if self._is_dark else "#FFFFFF"
    def _border(self):       return "#2E2E2E" if self._is_dark else "#E2E8F0"
    def _divider(self):      return "#333333" if self._is_dark else "#F1F5F9"
    def _text_primary(self): return "#F5F5F5" if self._is_dark else "#0F172A"
    def _text_secondary(self): return "#888888" if self._is_dark else "#64748B"

    # ── Rebuild on theme toggle ───────────────────────────────────────────────

    def _on_theme_toggle(self, e):
        """Toggle theme then immediately repaint the settings view."""
        self.controller.toggle_theme(e)
        self._repaint()

    def _repaint(self):
        """Rebuild all controls with fresh theme colors."""
        self._apply_to_outer()
        self._outer.update()

    def _apply_to_outer(self):
        self._outer.bgcolor       = self._bg()
        self._outer.border        = ft.border.all(1, self._border())
        self._outer.border_radius = ft.border_radius.all(12)
        self._outer.clip_behavior = ft.ClipBehavior.ANTI_ALIAS
        self._outer.shadow        = ft.BoxShadow(
            spread_radius=0, blur_radius=10,
            color=ft.Colors.with_opacity(0.3 if self._is_dark else 0.06, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        )
        self._outer.content = ft.Container(
            content=self._build_inner_column(),
            padding=ft.padding.all(28),
            bgcolor=self._bg(),
            expand=True,
        )

    def _build_inner_column(self) -> ft.Column:
        return ft.Column([
            self._page_header(),
            self._section_label("Appearance"),
            self._build_appearance_card(),
            ft.Container(height=40),
        ], spacing=0)

    # ── Page header ───────────────────────────────────────────────────────────

    def _page_header(self) -> ft.Container:
        icon  = getattr(self.cnst, 'SETTINGS_ICON', ft.Icons.SETTINGS_OUTLINED)
        title = getattr(self.cnst, 'TITLE',         "Settings")
        desc  = getattr(self.cnst, 'DESCRIPTION',   "Manage your application preferences")
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, size=22, color="#FFFFFF"),
                        bgcolor="#16A34A",
                        border_radius=ft.border_radius.all(10),
                        width=44, height=44,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column([
                        ft.Text(title, size=18, weight=ft.FontWeight.W_700,
                                color=self._text_primary()),
                        ft.Text(desc,  size=12, color=self._text_secondary()),
                    ], spacing=2, expand=True),
                ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=1, bgcolor=self._border(),
                             margin=ft.margin.only(top=14)),
            ], spacing=0),
            margin=ft.margin.only(bottom=20),
        )

    # ── Section label ─────────────────────────────────────────────────────────

    def _section_label(self, text: str) -> ft.Container:
        return ft.Container(
            content=ft.Text(text.upper(), size=10, weight=ft.FontWeight.W_700,
                            color=self._text_secondary()),
            padding=ft.padding.only(left=2, bottom=8, top=4),
        )

    # ── Setting row ───────────────────────────────────────────────────────────

    def _setting_row(self, icon, icon_color, title, subtitle,
                     trailing, is_last=False) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=15, color=icon_color),
                    bgcolor=ft.Colors.with_opacity(0.12, icon_color),
                    border_radius=ft.border_radius.all(6),
                    width=30, height=30,
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text(title, size=13, weight=ft.FontWeight.W_600,
                            color=self._text_primary()),
                    ft.Text(subtitle, size=11, color=self._text_secondary()),
                ], spacing=1, tight=True, expand=True),
                trailing,
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=self._surface_card(),
            padding=ft.padding.symmetric(horizontal=16, vertical=14),
            border=ft.border.only(
                bottom=ft.BorderSide(1, self._divider()) if not is_last
                       else None,
            ),
        )

    # ── Appearance card ───────────────────────────────────────────────────────

    def _build_appearance_card(self) -> ft.Container:
        appearance_title = getattr(self.cnst, 'APPEARANCE_TITLE', "Appearance")
        appearance_sub   = getattr(self.cnst, 'APPEARANCE_SUBTITLE', "Visual preferences")

        # Use our own toggle wrapper so we can repaint after switch
        toggle = ft.Switch(
            value=self._is_dark,
            on_change=self._on_theme_toggle,
            active_color="#16A34A",
            inactive_thumb_color="#888888",
            inactive_track_color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
        )

        card_header = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.PALETTE_OUTLINED, size=15, color="#2563EB"),
                    bgcolor=ft.Colors.with_opacity(0.12, "#2563EB"),
                    border_radius=ft.border_radius.all(7),
                    width=30, height=30,
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text(appearance_title, size=13, weight=ft.FontWeight.W_700,
                            color=self._text_primary()),
                    ft.Text(appearance_sub,   size=11, color=self._text_secondary()),
                ], spacing=1, tight=True),
            ], spacing=10),
            padding=ft.padding.only(left=16, right=16, top=14, bottom=12),
            bgcolor=self._surface(),
        )

        return ft.Container(
            content=ft.Column([
                card_header,
                ft.Container(height=1, bgcolor=self._border()),
                self._setting_row(
                    icon=ft.Icons.DARK_MODE_OUTLINED,
                    icon_color="#7C3AED",
                    title="Dark Mode",
                    subtitle="Switch between light and dark interface",
                    trailing=toggle,
                    is_last=True,
                ),
            ], spacing=0),
            bgcolor=self._surface_card(),
            border=ft.border.all(1, self._border()),
            border_radius=ft.border_radius.all(10),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=8,
                color=ft.Colors.with_opacity(
                    0.3 if self._is_dark else 0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

    # ── Build ─────────────────────────────────────────────────────────────────

    def build(self) -> ft.Container:
        self._apply_to_outer()
        return self._outer