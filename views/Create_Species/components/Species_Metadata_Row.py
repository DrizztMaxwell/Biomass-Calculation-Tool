import flet as ft


class Species_Metadata_Row:
    """Creates the Code, Origin, and Equation Type row — responsive wrap layout."""

    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.species_textfield      = None
        self.origin_dropdown        = None
        self.equation_type_dropdown = None

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _input_bg(self):  return "#2A2A2A" if self._is_dark else "#FFFFFF"
    def _border(self):    return "#3A3A3A" if self._is_dark else "#E2E8F0"
    def _text(self):      return "#F5F5F5" if self._is_dark else "#0F172A"
    def _hint(self):      return "#555555" if self._is_dark else "#94A3B8"

    def _label(self, icon, text) -> ft.Row:
        return ft.Row([
            ft.Icon(icon, size=14, color=ft.Colors.PRIMARY),
            ft.Text(text, size=13, weight=ft.FontWeight.W_600,
                    color=ft.Colors.ON_SURFACE),
        ], spacing=6)

    def _field_col(self, icon, label, control) -> ft.Column:
        """Label + input stacked vertically, fixed width so wrap works correctly."""
        return ft.Column([
            self._label(icon, label),
            ft.Container(height=6),
            control,
        ], spacing=0, width=260)   # fixed width — wrap=True needs concrete widths

    def build(self) -> ft.Row:
        # ── Species text field ────────────────────────────────────────────
        self.species_textfield = ft.TextField(
            width=260,
            hint_text="e.g. Alpine fir or 123",
            border_radius=ft.border_radius.all(8),
            filled=True,
            fill_color=self._input_bg(),
            border_color=self._border(),
            focused_border_color="#16A34A",
            color=self._text(),
            hint_style=ft.TextStyle(size=13, color=self._hint()),
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=14, vertical=12),
            on_change=lambda e: self.controller.set_species_code_or_name(e.control.value),
        )

        # ── Origin dropdown ───────────────────────────────────────────────
        self.origin_dropdown = ft.Dropdown(
            width=260,
            options=[
                ft.dropdown.Option("Natural Stand"),
                ft.dropdown.Option("Plantation"),
            ],
            value="Natural Stand",
            border_radius=ft.border_radius.all(8),
            filled=True,
            fill_color=self._input_bg(),
            border_color=self._border(),
            focused_border_color="#16A34A",
            color=self._text(),
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=14, vertical=10),
            on_change=lambda e: self.controller.set_origin_type(e.control.value),
        )

        # ── Equation type dropdown ────────────────────────────────────────
        self.equation_type_dropdown = ft.Dropdown(
            width=260,
            options=[
                ft.dropdown.Option("DBH-based"),
                ft.dropdown.Option("DBH + Height-based"),
            ],
            value="DBH-based",
            border_radius=ft.border_radius.all(8),
            filled=True,
            fill_color=self._input_bg(),
            border_color=self._border(),
            focused_border_color="#16A34A",
            color=self._text(),
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=14, vertical=10),
            on_change=self._on_equation_type_change,
        )

        return ft.Row(
            controls=[
                self._field_col(ft.Icons.KEY_OUTLINED,
                                "Species (Code or Name)",
                                self.species_textfield),
                self._field_col(ft.Icons.LOCATION_ON_OUTLINED,
                                "Origin",
                                self.origin_dropdown),
                self._field_col(ft.Icons.FUNCTIONS,
                                "Equation Type",
                                self.equation_type_dropdown),
            ],
            spacing=20,
            run_spacing=16,   # gap between lines when wrapped
            wrap=True,        # fields drop to next line on narrow screens
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _on_equation_type_change(self, e):
        self.controller.set_current_equation_type(e.control.value)

    def get_species_textfield(self):      return self.species_textfield
    def get_origin_dropdown(self):        return self.origin_dropdown
    def get_equation_type_dropdown(self): return self.equation_type_dropdown