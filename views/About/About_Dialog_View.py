import flet as ft


class About_Dialog_View:
    def __init__(self, page: ft.Page):
        self.page = page
        self.is_visible = False
        self._current_dialog = None

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self) -> bool:
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):
        return "#1A1A1A" if self._is_dark else "#F8FAFC"

    def _surface(self):
        return "#222222" if self._is_dark else "#F8FAFC"

    def _surface_card(self):
        return "#2A2A2A" if self._is_dark else "#FFFFFF"

    def _border(self):
        return "#2E2E2E" if self._is_dark else "#E2E8F0"

    def _divider(self):
        return "#333333" if self._is_dark else "#F1F5F9"

    def _text_primary(self):
        return "#F5F5F5" if self._is_dark else "#0F172A"

    def _text_secondary(self):
        return "#888888" if self._is_dark else "#64748B"
    def _accent(self):
        return "#6D28D9" if self._is_dark else "#8B5CF6"


    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=22,
                                    color="#FFFFFF"),
                    width=44, height=44,
                    bgcolor=ft.Colors.with_opacity(0.18, "#FFFFFF"),
                    border_radius=ft.border_radius.all(10),
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text("About This Tool", size=18,
                            weight=ft.FontWeight.W_700, color="#FFFFFF"),
                    ft.Text("Biomass Calculator v1.0", size=12,
                            color=ft.Colors.with_opacity(0.75, "#FFFFFF")),
                ], spacing=2, expand=True),
                ft.Container(
                    content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=16,
                                    color="#FFFFFF"),
                    on_click=lambda e: self.close(),
                    bgcolor=ft.Colors.with_opacity(0.15, "#FFFFFF"),
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.all(6),
                    ink=True,
                    tooltip="Close",
                ),
            ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=self._accent(),
            padding=ft.padding.symmetric(horizontal=24, vertical=18),
            border_radius=ft.border_radius.only(top_left=14, top_right=14),
        )

    # ── Card wrapper ──────────────────────────────────────────────────────────

    def _card(self, icon, icon_color, label, content) -> ft.Container:
        header = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=15, color=icon_color),
                    bgcolor=ft.Colors.with_opacity(0.10, icon_color),
                    border_radius=ft.border_radius.all(7),
                    width=30, height=30,
                    alignment=ft.alignment.center,
                ),
                ft.Text(label, size=13, weight=ft.FontWeight.W_600,
                        color=self._text_primary()),
            ], spacing=10),
            padding=ft.padding.only(left=16, right=16, top=14, bottom=12),
            bgcolor=self._surface(),
        )
        return ft.Container(
            content=ft.Column([
                header,
                ft.Container(height=1, bgcolor=self._border()),
                content,
            ], spacing=0),
            bgcolor=self._surface_card(),
            border=ft.border.all(1, self._border()),
            border_radius=ft.border_radius.all(10),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

    # ── Content sections ──────────────────────────────────────────────────────

    def _build_overview_card(self) -> ft.Container:
        return self._card(
            icon=ft.Icons.ANALYTICS_ROUNDED,
            icon_color="#2563EB",
            label="Overview",
            content=ft.Container(
                content=ft.Text(
                    "This tool estimates aboveground biomass for Canadian tree species "
                    "using national equations (Lambert et al. 2005). It converts standard "
                    "forest inventory measurements into biomass estimates for carbon "
                    "accounting and forest management. Biomass is calculated for individual "
                    "tree components — wood, bark, branches, and foliage — with the sum "
                    "equaling total aboveground biomass.",
                    size=13,
                    color=self._text_secondary(),
                ),
                padding=ft.padding.all(16),
            ),
        )

    def _build_features_card(self) -> ft.Container:
        features = [
            (ft.Icons.FOREST_OUTLINED,      self._accent(), "33 Canadian tree species supported"),
            (ft.Icons.DEVICE_HUB_ROUNDED,   "#2563EB", "Biomass for wood, bark, branches & foliage"),
            (ft.Icons.TRENDING_UP_ROUNDED,  "#F59E0B", "DBH-based & DBH + height-based equations"),
            (ft.Icons.BALANCE_ROUNDED,      "#8B5CF6", "Carbon accounting & forest management ready"),
        ]

        rows = []
        for i, (icon, color, text) in enumerate(features):
            is_last = (i == len(features) - 1)
            rows.append(ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, size=14, color=color),
                        bgcolor=ft.Colors.with_opacity(0.10, color),
                        border_radius=ft.border_radius.all(6),
                        width=28, height=28,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(text, size=13, color=self._text_secondary(), expand=True),
                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.symmetric(horizontal=16, vertical=11),
                border=ft.border.only(
                    bottom=ft.BorderSide(1, self._divider()) if not is_last else ft.BorderSide(0)
                ),
            ))

        return self._card(
            icon=ft.Icons.SPEED_ROUNDED,
            icon_color="#F59E0B",
            label="Precision & Features",
            content=ft.Column(rows, spacing=0),
        )

    def _build_audience_card(self) -> ft.Container:
        return self._card(
            icon=ft.Icons.GROUPS_ROUNDED,
            icon_color="#8B5CF6",
            label="Intended For",
            content=ft.Container(
                content=ft.Text(
                    "Researchers, forest managers, and policy analysts requiring "
                    "robust biomass estimates across Canada.",
                    size=13,
                    color=self._text_secondary(),
                ),
                padding=ft.padding.all(16),
            ),
        )

    def _build_contact_card(self) -> ft.Container:
        def email_pill(name, email, color):
            return ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.MAIL_OUTLINE_ROUNDED, size=14,
                                        color=color),
                        bgcolor=ft.Colors.with_opacity(0.10, color),
                        border_radius=ft.border_radius.all(6),
                        width=28, height=28,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column([
                        ft.Text(name, size=13, weight=ft.FontWeight.W_600,
                                color=self._text_primary()),
                        ft.Text(email, size=11, color=self._text_secondary()),
                    ], spacing=1, expand=True),
                    ft.Icon(ft.Icons.OPEN_IN_NEW_ROUNDED, size=13,
                            color=self._text_secondary()),
                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                on_click=lambda _, e=email: self.page.launch_url(f"mailto:{e}"),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                border=ft.border.only(bottom=ft.BorderSide(1, self._divider())),
                ink=True,
                ink_color=ft.Colors.with_opacity(0.05, color),
            )

        contacts = ft.Column([
            email_pill("Jamshid Eslamdoust",
                       "Jamshid.Eslamdoust@ontario.ca", "#F59E0B"),
            ft.Container(  # last item — no bottom border override
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.MAIL_OUTLINE_ROUNDED, size=14,
                                        color="#2563EB"),
                        bgcolor=ft.Colors.with_opacity(0.10, "#2563EB"),
                        border_radius=ft.border_radius.all(6),
                        width=28, height=28,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column([
                        ft.Text("Christopher Stratton", size=13,
                                weight=ft.FontWeight.W_600,
                                color=self._text_primary()),
                        ft.Text("Christopher.Stratton@ontario.ca", size=11,
                                color=self._text_secondary()),
                    ], spacing=1, expand=True),
                    ft.Icon(ft.Icons.OPEN_IN_NEW_ROUNDED, size=13,
                            color=self._text_secondary()),
                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                on_click=lambda _: self.page.launch_url(
                    "mailto:Christopher.Stratton@ontario.ca"),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                ink=True,
                ink_color=ft.Colors.with_opacity(0.05, "#2563EB"),
            ),
        ], spacing=0)

        return self._card(
            icon=ft.Icons.ALTERNATE_EMAIL_ROUNDED,
            icon_color="#2563EB",
            label="Development & Contact",
            content=contacts,
        )

    # ── Actions bar ───────────────────────────────────────────────────────────

    def _build_actions(self) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CLOSE_ROUNDED, size=14, color="#FFFFFF"),
                        ft.Text("Close", size=13, weight=ft.FontWeight.W_600,
                                color="#FFFFFF"),
                    ], spacing=6),
                    on_click=lambda e: self.close(),
                    bgcolor=self._accent(),
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    ink=True,
                ),
            ]),
            padding=ft.padding.only(left=24, right=24, top=12, bottom=16),
            bgcolor=self._surface(),
            border=ft.border.only(top=ft.BorderSide(1, self._border())),
        )

    # ── Dialog assembly ───────────────────────────────────────────────────────

    def _build_dialog(self) -> ft.AlertDialog:
        scrollable_body = ft.Container(
            content=ft.Column([
                ft.Container(height=16),
                self._build_overview_card(),
                ft.Container(height=12),
                self._build_features_card(),
                ft.Container(height=12),
                self._build_audience_card(),
                ft.Container(height=12),
                self._build_contact_card(),
                ft.Container(height=16),
            ], scroll=ft.ScrollMode.AUTO, spacing=0, tight=True, expand=True),
            padding=ft.padding.symmetric(horizontal=22),
            expand=True,
            bgcolor=self._surface(),
        )

        width  = min((self.page.width  or 860) * 0.9, 860)
        height = min((self.page.height or 700) * 0.88, 700)

        main = ft.Container(
            content=ft.Column([
                self._build_header(),
                scrollable_body,
                self._build_actions(),
            ], spacing=0, tight=True),
            width=width,
            height=height,
            bgcolor=self._surface(),
            border_radius=ft.border_radius.all(14),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            shadow=ft.BoxShadow(
                blur_radius=30,
                spread_radius=0,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            ),
        )

        return ft.AlertDialog(
            modal=True,
            content=main,
            content_padding=ft.padding.all(0),
            shape=ft.RoundedRectangleBorder(radius=14),
            bgcolor=ft.Colors.TRANSPARENT,
            surface_tint_color=ft.Colors.TRANSPARENT,
            inset_padding=ft.padding.symmetric(horizontal=20, vertical=20),
            alignment=ft.alignment.center,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def show(self):
        self._current_dialog = self._build_dialog()
        self.is_visible = True
        self.page.open(self._current_dialog)

    def close(self, e=None):
        if self._current_dialog:
            self.page.close(self._current_dialog)
        self.is_visible = False

    def handle_theme_change(self):
        """Rebuild dialog if visible after theme change."""
        if self.is_visible:
            self.close()
            self.show()