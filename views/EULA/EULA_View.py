from widgets.LogFileTxt import logger
import flet as ft
from controller.SideNavbar_Controller import SideNavbar_Controller
from views.SideNavbar_View import SideNavbar_View
from constants.EULA_Constants import EULA_Constants


class EULA_View:
    def __init__(self, page: ft.Page, controller):
        self.page       = page
        self.controller = controller
        self.constants  = EULA_Constants()

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):          return "#1A1A1A" if self._is_dark else "#FFFFFF"
    def _surface(self):     return "#222222" if self._is_dark else "#F8FAFC"
    def _surface_card(self):return "#2A2A2A" if self._is_dark else "#FFFFFF"
    def _border(self):      return "#2E2E2E" if self._is_dark else "#E2E8F0"
    def _divider(self):     return "#333333" if self._is_dark else "#F1F5F9"
    def _text_primary(self):return "#F5F5F5" if self._is_dark else "#0F172A"
    def _text_secondary(self): return "#888888" if self._is_dark else "#64748B"

    # ── Public entry ──────────────────────────────────────────────────────────

    def get_eula_view(self) -> None:
        self._display_on_page(self._build_eula_layout())

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.GAVEL_ROUNDED, size=22, color="#FFFFFF"),
                    width=44, height=44,
                    bgcolor=ft.Colors.with_opacity(0.18, "#FFFFFF"),
                    border_radius=ft.border_radius.all(10),
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text("End User Licence Agreement", size=18,
                            weight=ft.FontWeight.W_700, color="#FFFFFF"),
                    ft.Text("Biomass Calculator v1.0 — please read carefully",
                            size=12,
                            color=ft.Colors.with_opacity(0.75, "#FFFFFF")),
                ], spacing=2, expand=True),
            ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#16A34A",
            padding=ft.padding.symmetric(horizontal=28, vertical=18),
            border_radius=ft.border_radius.only(top_left=14, top_right=14),
        )

    # ── Section card ──────────────────────────────────────────────────────────

    def _build_section(self, icon, icon_color, heading, content_text) -> ft.Container:
        header = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=15, color=icon_color),
                    bgcolor=ft.Colors.with_opacity(0.10, icon_color),
                    border_radius=ft.border_radius.all(7),
                    width=30, height=30,
                    alignment=ft.alignment.center,
                ),
                ft.Text(heading, size=13, weight=ft.FontWeight.W_700,
                        color=self._text_primary()),
            ], spacing=10),
            padding=ft.padding.only(left=16, right=16, top=14, bottom=12),
            bgcolor=self._surface(),
        )
        body = ft.Container(
            content=ft.Text(
                content_text,
                size=13,
                color=self._text_secondary(),
                selectable=True,
            ),
            padding=ft.padding.all(16),
            bgcolor=self._surface_card(),
        )
        return ft.Container(
            content=ft.Column([
                header,
                ft.Container(height=1, bgcolor=self._border()),
                body,
            ], spacing=0),
            bgcolor=self._surface_card(),
            border=ft.border.all(1, self._border()),
            border_radius=ft.border_radius.all(10),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

    # ── Scrollable body ───────────────────────────────────────────────────────

    def _build_body(self) -> ft.Container:
        c = self.constants
        sections = [
            self._build_section(
                ft.Icons.DESCRIPTION_OUTLINED, "#2563EB",
                c.TERMS_HEADING, c.TERMS_CONTENT,
            ),
            self._build_section(
                ft.Icons.VERIFIED_OUTLINED, "#16A34A",
                c.ACCEPTANCE_HEADING, c.ACCEPTANCE_CONTENT,
            ),
            self._build_section(
                ft.Icons.WARNING_AMBER_ROUNDED, "#D97706",
                c.DISCLAIMER_HEADING, c.DISCLAIMER_CONTENT,
            ),
        ]
        return ft.Container(
            content=ft.ListView(
                controls=[
                    ft.Container(height=16),
                    *[ctrl for s in sections
                      for ctrl in (s, ft.Container(height=12))],
                    ft.Container(height=4),
                ],
                spacing=0,
                auto_scroll=False,
            ),
            expand=True,
            padding=ft.padding.symmetric(horizontal=24),
            bgcolor=self._bg(),
        )

    # ── Actions bar ───────────────────────────────────────────────────────────

    def _build_actions(self) -> ft.Container:
        def _btn(label, icon, bgcolor, on_click):
            return ft.Container(
                content=ft.Row([
                    ft.Icon(icon, size=15, color="#FFFFFF"),
                    ft.Text(label, size=13, weight=ft.FontWeight.W_600,
                            color="#FFFFFF"),
                ], spacing=7, tight=True),
                on_click=on_click,
                bgcolor=bgcolor,
                border_radius=ft.border_radius.all(9),
                padding=ft.padding.symmetric(horizontal=24, vertical=12),
                ink=True,
            )

        return ft.Container(
            content=ft.Row([
                _btn(self.constants.DISAGREE_BUTTON,
                     ft.Icons.CLOSE_ROUNDED,
                     "#DC2626",
                     lambda e: self._handle_user_choice(e, agreed=False)),
                ft.Container(width=12),
                _btn(self.constants.AGREE_BUTTON,
                     ft.Icons.CHECK_ROUNDED,
                     "#16A34A",
                     lambda e: self._handle_user_choice(e, agreed=True)),
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.only(left=24, right=24, top=16, bottom=20),
            bgcolor=self._bg(),
            border=ft.border.only(top=ft.BorderSide(1, self._border())),
            border_radius=ft.border_radius.only(bottom_left=14, bottom_right=14),
        )

    # ── Layout assembly ───────────────────────────────────────────────────────

    def _build_eula_layout(self) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                self._build_header(),
                self._build_body(),
                self._build_actions(),
            ], spacing=0, expand=True),
            bgcolor=self._bg(),
            border_radius=ft.border_radius.all(14),
            border=ft.border.all(1, self._border()),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            shadow=ft.BoxShadow(
                blur_radius=24, spread_radius=0,
                color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
            ),
            expand=True,
        )

    def _display_on_page(self, layout: ft.Container) -> None:
        self.page.add(
            ft.Container(
                content=layout,
                margin=ft.margin.all(30),
                expand=True,
            )
        )

    # ── Handlers ─────────────────────────────────────────────────────────────

    def _handle_user_choice(self, event, agreed: bool) -> None:
        if agreed:
            logger.write("User agreed to EULA — proceeding")
            self._proceed_to_application()
        else:
            logger.write("User rejected EULA")
            self._show_exit_view()

    def _proceed_to_application(self) -> None:
        self.page.clean()
        SideNavbar_Controller(SideNavbar_View(self.page)).build()
        self.page.update()

    def _show_exit_view(self) -> None:
        self.page.clean()
        self._display_exit_view()
        self.page.update()

    def _display_exit_view(self) -> None:
        self.page.add(self._build_exit_layout())

    def _build_exit_layout(self) -> ft.Container:
        return ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=self._bg(),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(ft.Icons.DO_NOT_DISTURB_ON_OUTLINED,
                                        size=40, color="#DC2626"),
                        bgcolor=ft.Colors.with_opacity(0.08, "#DC2626"),
                        border_radius=ft.border_radius.all(32),
                        width=72, height=72,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=16),
                    ft.Text("Application Cannot Continue", size=18,
                            weight=ft.FontWeight.W_700,
                            color=self._text_primary(),
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(height=8),
                    ft.Text(
                        "You must accept the EULA to use this application.\n"
                        "Please restart and accept the terms to proceed.",
                        size=13, color=self._text_secondary(),
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=24),
                    ft.Row([
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CLOSE_ROUNDED, size=15,
                                        color="#FFFFFF"),
                                ft.Text("Close Application", size=13,
                                        weight=ft.FontWeight.W_600,
                                        color="#FFFFFF"),
                            ], spacing=7, tight=True),
                            on_click=lambda e: self.page.window.close(),
                            bgcolor="#DC2626",
                            border_radius=ft.border_radius.all(9),
                            padding=ft.padding.symmetric(horizontal=22, vertical=11),
                            ink=True,
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0, tight=True),
                bgcolor=self._bg(),
                border=ft.border.all(1, self._border()),
                border_radius=ft.border_radius.all(14),
                width=440,
                padding=ft.padding.symmetric(horizontal=48, vertical=40),
                shadow=ft.BoxShadow(
                    blur_radius=20, spread_radius=0,
                    color=ft.Colors.with_opacity(0.10, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4),
                ),
            ),
        )