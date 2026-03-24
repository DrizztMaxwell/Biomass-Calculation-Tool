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
        return "#1E1E1E" if self._is_dark else "#F0F4F8"

    def _surface_card(self):
        return "#2A2A2A" if self._is_dark else "#FFFFFF"

    def _border(self):
        return "#2E2E2E" if self._is_dark else "#E2E8F0"

    def _text_primary(self):
        return "#F5F5F5" if self._is_dark else "#1E293B"

    def _text_secondary(self):
        return "#AAAAAA" if self._is_dark else "#374151"

    def _accent(self):
        return "#6D28D9" if self._is_dark else "#8B5CF6"

    # ── Coloured flat cards (matching screenshot) ─────────────────────────────

    def _flat_card(self, icon, icon_color, card_bg, title_color, label, body_text) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, size=16, color=icon_color),
                        bgcolor=ft.Colors.with_opacity(0.18, icon_color),
                        border_radius=ft.border_radius.all(6),
                        width=30, height=30,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(label, size=14, weight=ft.FontWeight.W_700,
                            color=title_color),
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=8),
                ft.Text(body_text, size=13, color=self._text_secondary(),
                        selectable=True),
            ], spacing=0),
            bgcolor=card_bg,
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.all(16),
        )

    # ── Content sections ──────────────────────────────────────────────────────

    def _build_overview_card(self) -> ft.Container:
        card_bg  = "#DBEAFE" if not self._is_dark else "#1E3A5F"
        title_c  = "#1D4ED8" if not self._is_dark else "#60A5FA"
        icon_c   = "#2563EB"
        return self._flat_card(
            icon=ft.Icons.ANALYTICS_ROUNDED,
            icon_color=icon_c,
            card_bg=card_bg,
            title_color=title_c,
            label="Overview",
            body_text=(
                "This tool estimates aboveground biomass for Canadian tree species "
                "using national equations (Lambert et al. 2005). It converts standard "
                "forest inventory measurements into biomass estimates for carbon "
                "accounting and forest management. Biomass is calculated for individual "
                "tree components — wood, bark, branches, and foliage — with the sum "
                "equaling total aboveground biomass. Species-specific allometric models "
                "offer two precision levels: DBH-based equations (when height is "
                "unavailable) and more accurate DBH + height-based equations (when both "
                "measurements are provided)."
            ),
        )

    def _build_features_card(self) -> ft.Container:
        card_bg = "#DCFCE7" if not self._is_dark else "#14532D"
        title_c = "#15803D" if not self._is_dark else "#4ADE80"
        icon_c  = "#16A34A"
        return self._flat_card(
            icon=ft.Icons.SPEED_ROUNDED,
            icon_color=icon_c,
            card_bg=card_bg,
            title_color=title_c,
            label="Precision & Features",
            body_text=(
                "Estimates aboveground biomass for 33 Canadian tree species using "
                "national equations (Lambert et al. 2005). Calculates biomass for "
                "wood, bark, branches, and foliage — summing to total biomass. "
                "Choose between DBH-based or more accurate DBH + height-based "
                "equations."
            ),
        )

    def _build_audience_card(self) -> ft.Container:
        card_bg = "#EDE9FE" if not self._is_dark else "#2E1065"
        title_c = "#6D28D9" if not self._is_dark else "#A78BFA"
        icon_c  = "#7C3AED"
        return self._flat_card(
            icon=ft.Icons.GROUPS_ROUNDED,
            icon_color=icon_c,
            card_bg=card_bg,
            title_color=title_c,
            label="Intended For",
            body_text=(
                "Researchers, forest managers, and policy analysts requiring "
                "robust biomass estimates across Canada."
            ),
        )

    def _build_contact_card(self) -> ft.Container:
        def email_pill(name, email, icon_color, pill_bg):
            display = f"{name} ({email})"

            def open_email(e, _email=email):
                self.page.launch_url(f"mailto:{_email}")

            return ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.MAIL_OUTLINE_ROUNDED, size=14,
                                        color="#FFFFFF"),
                        bgcolor=icon_color,
                        border_radius=ft.border_radius.all(5),
                        width=26, height=26,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(display, size=12, color=self._text_primary(),
                            expand=True),
                ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=pill_bg,
                border_radius=ft.border_radius.all(8),
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                on_click=open_email,
                ink=True,
                url=f"mailto:{email}",
            )

        pill_bg_amber = "#FEF3C7" if not self._is_dark else "#3B2A00"
        pill_bg_blue  = "#DBEAFE" if not self._is_dark else "#1E3A5F"
        pill_bg_green = "#DCFCE7" if not self._is_dark else "#14532D"

        return ft.Container(
            content=ft.Column([
                ft.Text("Development & Contact", size=14,
                        weight=ft.FontWeight.W_700,
                        color=self._text_primary()),
                ft.Container(height=10),
                ft.Row([
                    email_pill(
                        "Jamshid Eslamdoust",
                        "Jamshid.Eslamdoust@ontario.ca",
                        "#F59E0B",
                        pill_bg_amber,
                    ),
                    email_pill(
                        "Christopher Stratton",
                        "Christopher.Stratton@ontario.ca",
                        "#2563EB",
                        pill_bg_blue,
                    ),
                ], spacing=10),
                ft.Container(height=8),
                ft.Row([
                    email_pill(
                        "Todd Little",
                        "Todd.Little@ontario.ca",
                        "#16A34A",
                        pill_bg_green,
                    ),
                ], spacing=10),
            ], spacing=0),
            bgcolor=self._surface_card(),
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.all(16),
            border=ft.border.all(1, self._border()),
        )

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