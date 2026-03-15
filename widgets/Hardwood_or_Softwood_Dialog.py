import flet as ft
import asyncio


class HardwoodOrSoftwoodDialog:
    """
    Multi-step dialog for classifying missing species codes as Hardwood or Softwood.
    """

    def __init__(self, page: ft.Page, missing_species_codes: set):
        self.page = page
        self.missing_species_codes = missing_species_codes
        self.user_selections  = {}
        self.selected_types   = {code: None for code in missing_species_codes}
        self.submitted        = False
        self.result_future    = None
        self.current_step     = [0]
        self.main_column      = None
        self.dialog           = None

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):
        return "#1A1A1A" if self._is_dark else "#FFFFFF"

    def _surface(self):
        return "#222222" if self._is_dark else "#F8FAFC"

    def _surface_card(self):
        return "#2A2A2A" if self._is_dark else "#FFFFFF"

    def _border(self):
        return "#2E2E2E" if self._is_dark else "#E2E8F0"

    def _text_primary(self):
        return "#F5F5F5" if self._is_dark else "#0F172A"

    def _text_secondary(self):
        return "#888888" if self._is_dark else "#64748B"

    def _step_color(self, step):
        """Hardwood = amber, Softwood = blue."""
        return "#D97706" if step == 0 else "#2563EB"

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self) -> ft.Container:
        step      = self.current_step[0]
        color     = self._step_color(step)
        icon      = ft.Icons.PARK_OUTLINED if step == 0 else ft.Icons.FOREST_OUTLINED
        title     = "Classify as Hardwood" if step == 0 else "Classify as Softwood"
        subtitle  = f"Step {step + 1} of 2 — select species codes below"

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=22, color="#FFFFFF"),
                    width=44, height=44,
                    bgcolor=ft.Colors.with_opacity(0.18, "#FFFFFF"),
                    border_radius=ft.border_radius.all(10),
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text(title, size=17, weight=ft.FontWeight.W_700, color="#FFFFFF"),
                    ft.Text(subtitle, size=12,
                            color=ft.Colors.with_opacity(0.75, "#FFFFFF")),
                ], spacing=2, expand=True),
                # Step pill
                ft.Container(
                    content=ft.Text(f"{step + 1}/2", size=12,
                                    weight=ft.FontWeight.W_700, color="#FFFFFF"),
                    bgcolor=ft.Colors.with_opacity(0.20, "#FFFFFF"),
                    border_radius=ft.border_radius.all(20),
                    padding=ft.padding.symmetric(horizontal=12, vertical=5),
                ),
            ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=color,
            padding=ft.padding.symmetric(horizontal=24, vertical=18),
            border_radius=ft.border_radius.only(top_left=14, top_right=14),
        )

    # ── Species card ──────────────────────────────────────────────────────────

    def create_species_card(self, code, species_type: str) -> ft.Container:
        is_selected = self.selected_types.get(code) == species_type
        step        = self.current_step[0]
        color       = self._step_color(step)

        def on_tap(e):
            self.selected_types[code] = None if self.selected_types.get(code) == species_type else species_type
            self.main_column.controls = self._get_current_step_content(self.current_step[0])
            self.page.update()

        return ft.Container(
            content=ft.Row([
                # Check circle
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.CHECK_ROUNDED if is_selected else ft.Icons.CIRCLE_OUTLINED,
                        size=16,
                        color=color if is_selected else self._text_secondary(),
                    ),
                    width=32, height=32,
                    bgcolor=ft.Colors.with_opacity(0.10 if is_selected else 0.0, color),
                    border_radius=ft.border_radius.all(16),
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text(str(code), size=14, weight=ft.FontWeight.W_700,
                            color=color if is_selected else self._text_primary()),
                    ft.Text(f"Classify as {species_type}", size=12,
                            color=self._text_secondary()),
                ], spacing=2, expand=True),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=on_tap,
            bgcolor=ft.Colors.with_opacity(0.06, color) if is_selected else self._surface_card(),
            border=ft.border.all(
                1.5 if is_selected else 1,
                ft.Colors.with_opacity(0.4 if is_selected else 0.15, color),
            ),
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            ink=True,
            animate=ft.Animation(150, ft.AnimationCurve.LINEAR),
            margin=ft.margin.only(bottom=8),
        )

    # ── Step content ──────────────────────────────────────────────────────────

    def _get_current_step_content(self, step: int):
        species_type    = "Hardwood" if step == 0 else "Softwood"
        color           = self._step_color(step)
        available_codes = list(self.missing_species_codes) if step == 0 else [
            c for c in self.missing_species_codes
            if self.selected_types.get(c) != "Hardwood"
        ]

        if step == 1 and not available_codes:
            body = ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                        size=32, color="#16A34A"),
                        bgcolor=ft.Colors.with_opacity(0.08, "#16A34A"),
                        border_radius=ft.border_radius.all(24),
                        width=56, height=56,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=10),
                    ft.Text("All codes classified as Hardwood", size=14,
                            weight=ft.FontWeight.W_700,
                            color=self._text_primary(),
                            text_align=ft.TextAlign.CENTER),
                    ft.Text("Press Submit to confirm, or Back to review.",
                            size=12, color=self._text_secondary(),
                            text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                   spacing=0, tight=True),
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(vertical=30),
            )
        else:
            # Info hint for step 2
            hint = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=13,
                            color=color),
                    ft.Text("Hardwood selections are removed from this list.",
                            size=11, color=self._text_secondary()),
                ], spacing=6),
                visible=(step == 1),
                margin=ft.margin.only(bottom=10),
            )

            cards = [self.create_species_card(c, species_type) for c in available_codes]
            body  = ft.Column([
                hint,
                ft.Column(
                    cards,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    spacing=0,
                ),
            ], spacing=0)

        return [body]

    # ── Actions bar ───────────────────────────────────────────────────────────

    def _build_actions(self, on_next, on_back, on_submit, on_cancel) -> ft.Container:
        step  = self.current_step[0]
        color = self._step_color(step)

        def _btn(label, icon, on_click, bgcolor, text_color, outline=False):
            return ft.Container(
                content=ft.Row([
                    ft.Icon(icon, size=14, color=text_color),
                    ft.Text(label, size=13, weight=ft.FontWeight.W_600, color=text_color),
                ], spacing=6, tight=True),
                on_click=on_click,
                bgcolor=bgcolor,
                border=ft.border.all(1, self._border()) if outline else None,
                border_radius=ft.border_radius.all(8),
                padding=ft.padding.symmetric(horizontal=18, vertical=10),
                ink=True,
            )

        cancel_btn = _btn("Cancel", ft.Icons.CLOSE_ROUNDED,
                          on_cancel,
                          ft.Colors.with_opacity(0.06,
                              ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK),
                          self._text_secondary(), outline=True)

        if step == 0:
            action_btn = _btn("Next Step", ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                              on_next, color, "#FFFFFF")
            right_btns = [action_btn]
        else:
            back_btn   = _btn("Back", ft.Icons.ARROW_BACK_IOS_ROUNDED,
                              on_back,
                              ft.Colors.with_opacity(0.06,
                                  ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK),
                              self._text_primary(), outline=True)
            submit_btn = _btn("Submit", ft.Icons.DONE_ALL_ROUNDED,
                              on_submit, "#16A34A", "#FFFFFF")
            right_btns = [back_btn, submit_btn]

        return ft.Container(
            content=ft.Row([
                cancel_btn,
                ft.Container(expand=True),
                *right_btns,
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(left=24, right=24, top=12, bottom=16),
            bgcolor=self._bg(),
            border=ft.border.only(top=ft.BorderSide(1, self._border())),
            border_radius=ft.border_radius.only(bottom_left=14, bottom_right=14),
        )

    # ── Dialog assembly ───────────────────────────────────────────────────────

    async def show_species_code_dialog(self):
        self.result_future = asyncio.Future()
        self.current_step  = [0]

        self.main_column = ft.Column(
            self._get_current_step_content(0),
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )

        async def on_next(e):
            self.current_step[0] = 1
            self._rebuild_dialog()

        async def on_back(e):
            self.current_step[0] = 0
            for code in self.missing_species_codes:
                if self.selected_types.get(code) == "Softwood":
                    self.selected_types[code] = None
            self._rebuild_dialog()

        async def on_submit(e):
            final = {c: t for c, t in self.selected_types.items() if t is not None}
            self.user_selections = final
            self.result_future.set_result(self.user_selections)
            self.submitted = True
            self.page.close(self.dialog)

        async def on_cancel(e):
            self.result_future.set_result(None)
            self.page.close(self.dialog)

        self._on_next   = on_next
        self._on_back   = on_back
        self._on_submit = on_submit
        self._on_cancel = on_cancel

        self.dialog = self._make_dialog()
        self.page.open(self.dialog)
        return await self.result_future

    def _make_dialog(self) -> ft.AlertDialog:
        body = ft.Container(
            content=ft.Column([
                self._build_header(),
                ft.Container(
                    content=self.main_column,
                    padding=ft.padding.symmetric(horizontal=20, vertical=14),
                    expand=True,
                    bgcolor=self._bg(),
                ),
                self._build_actions(
                    self._on_next, self._on_back,
                    self._on_submit, self._on_cancel,
                ),
            ], spacing=0, tight=False),
            width=520,
            height=520,
            bgcolor=self._bg(),
            border_radius=ft.border_radius.all(14),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            shadow=ft.BoxShadow(
                blur_radius=30, spread_radius=0,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            ),
        )

        return ft.AlertDialog(
            modal=True,
            content=body,
            content_padding=ft.padding.all(0),
            shape=ft.RoundedRectangleBorder(radius=14),
            bgcolor=ft.Colors.TRANSPARENT,
            inset_padding=ft.padding.symmetric(horizontal=20, vertical=20),
            alignment=ft.alignment.center,
        )

    def _rebuild_dialog(self):
        """Rebuild header + actions + content after step change."""
        self.main_column.controls = self._get_current_step_content(self.current_step[0])
        # Rebuild the whole inner column in the dialog body
        body_col = self.dialog.content.content
        body_col.controls[0] = self._build_header()
        body_col.controls[2] = self._build_actions(
            self._on_next, self._on_back,
            self._on_submit, self._on_cancel,
        )
        self.page.update()

    # ── Getters ───────────────────────────────────────────────────────────────

    def get_user_selections(self):
        return self.user_selections

    def was_submitted(self):
        return self.submitted