import flet as ft
from .Equation_Section import Equation_Section
from .Components_Section import Components_Section
from widgets.Calculate_Biomass_Button import Calculate_Biomass_Button


class Layout:
    """Layout manager for Calculate Biomass view."""

    def __init__(self, controller, page: ft.Page):
        self.controller   = controller
        self.page         = page
        self.results_table_container = ft.Container(
            visible=False, key="results_table_container"
        )
        self.equation_section   = Equation_Section(controller)
        self.components_section = Components_Section(page, controller)

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _text_primary(self):   return "#F5F5F5" if self._is_dark else "#0F172A"
    def _text_secondary(self): return "#888888" if self._is_dark else "#64748B"
    def _border(self):         return "#2E2E2E" if self._is_dark else "#E2E8F0"

    # ── Build ─────────────────────────────────────────────────────────────────

    def build(self) -> ft.Column:
        page_header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.CALCULATE_OUTLINED,
                                        size=22, color="#FFFFFF"),
                        bgcolor="#16A34A",
                        border_radius=ft.border_radius.all(10),
                        width=44, height=44,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column([
                        ft.Text("Calculate Biomass", size=18,
                                weight=ft.FontWeight.W_700,
                                color=self._text_primary()),
                        ft.Text(
                            "Configure equation type and components, then run the calculation.",
                            size=12, color=self._text_secondary(),
                        ),
                    ], spacing=2, expand=True),
                ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(
                    height=1,
                    bgcolor=self._border(),
                    margin=ft.margin.only(top=14),
                ),
            ], spacing=0),
            padding=ft.padding.only(left=0, right=0, top=0, bottom=4),
        )

        card = ft.Container(
            content=ft.Column([
                page_header,
                self.equation_section.create(),
                self.components_section.create(),
                self._create_calculate_button(),
            ], spacing=0),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=ft.border_radius.all(12),
            border=ft.border.all(1, ft.Colors.GREY_200),
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=8,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            padding=ft.padding.all(24),
            margin=ft.margin.all(20),
        )

        return ft.Column(
            controls=[
                card,
                self.results_table_container,
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    def _create_calculate_button(self):
        return Calculate_Biomass_Button(
            on_click_callback=self.controller.on_calculate_biomass_click,
            is_disabled=False,
        ).create()

    def get_results_container(self):
        return self.results_table_container

    def show_results_table(self, content):
        self.results_table_container.content = content
        self.results_table_container.visible = True

    def scroll_to_results(self):
        self.page.scroll_to(
            key="results_table_container",
            duration=300,
            curve=ft.AnimationCurve.EASE_OUT,
        )