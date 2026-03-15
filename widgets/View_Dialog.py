import flet as ft
from widgets.LogFileTxt import logger


class View_Dialog:
    """Base class for dialog views in the application."""

    DIALOG_WIDTH_MAX  = 680
    DIALOG_WIDTH_MIN  = 320
    DIALOG_HEIGHT_MAX = 640
    DIALOG_HEIGHT_MIN = 400
    DIALOG_WIDTH_RATIO  = 0.9
    DIALOG_HEIGHT_RATIO = 0.85

    # Flet semantic colors (kept for compatibility)
    PRIMARY_COLOR       = ft.Colors.BLUE_700
    SECONDARY_COLOR     = ft.Colors.GREEN_600
    ACCENT_COLOR        = ft.Colors.ORANGE_500
    TEXT_PRIMARY        = ft.Colors.GREY_900
    TEXT_SECONDARY      = ft.Colors.GREY_600
    WHITE               = ft.Colors.WHITE
    GREY_100            = ft.Colors.GREY_100
    GREY_200            = ft.Colors.GREY_200
    PRIMARY             = ft.Colors.PRIMARY
    SECONDARY_CONTAINER = ft.Colors.SECONDARY_CONTAINER
    SECONDARY           = ft.Colors.SECONDARY
    TERTIARY            = ft.Colors.TERTIARY
    PURPLE_600          = ft.Colors.PURPLE_600
    BLACK               = ft.Colors.BLACK
    BLUE_600            = ft.Colors.BLUE_600

    PARAMETER_CATEGORIES = {
        "bh": {
            "name": "DBH + Height-based Parameters",
            "icon": ft.Icons.TRENDING_UP,
            "color": None,
        },
        "b": {
            "name": "DBH-based Parameters",
            "icon": ft.Icons.STRAIGHTEN,
            "color": None,
        },
        "default": {
            "name": "Other Parameters",
            "icon": ft.Icons.TUNE,
            "color": ft.Colors.PURPLE_600,
        },
    }

    def __init__(self, page: ft.Page):
        self.page = page

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self) -> bool:
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

    def _divider(self):
        return "#333333" if self._is_dark else "#F1F5F9"

    # ── Public entry point ────────────────────────────────────────────────────

    def view_species_dialog(
        self, index, species_data, filtered_species=None,
        primary_color=None, secondary_color=None, accent_color=None
    ):
        self.primary_color   = primary_color   or self.PRIMARY_COLOR
        self.secondary_color = secondary_color or self.SECONDARY_COLOR
        self.accent_color    = accent_color    or self.ACCENT_COLOR
        self.text_primary    = self.TEXT_PRIMARY
        self.text_secondary  = self.TEXT_SECONDARY

        self.PARAMETER_CATEGORIES["bh"]["color"] = self.secondary_color
        self.PARAMETER_CATEGORIES["b"]["color"]  = self.accent_color

        species = filtered_species[index] if filtered_species else species_data[index]

        dialog_width  = self._calc_width()
        dialog_height = self._calc_height()

        dialog = self._create_dialog(species, dialog_width, dialog_height)
        self._show_dialog(dialog, species)

    def _calc_width(self):
        w = (self.page.width or self.DIALOG_WIDTH_MAX) * self.DIALOG_WIDTH_RATIO
        return max(self.DIALOG_WIDTH_MIN, min(w, self.DIALOG_WIDTH_MAX))

    def _calc_height(self):
        h = (self.page.height or self.DIALOG_HEIGHT_MAX) * self.DIALOG_HEIGHT_RATIO
        return max(self.DIALOG_HEIGHT_MIN, min(h, self.DIALOG_HEIGHT_MAX))

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self, species) -> ft.Container:
        species_code = species.get("SpeciesCode", "")
        spec_common  = species.get("SpecCommon", "")
        subtitle     = spec_common if spec_common and spec_common != "None" else species_code

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, size=22, color="#FFFFFF"),
                    width=44, height=44,
                    bgcolor=ft.Colors.with_opacity(0.18, "#FFFFFF"),
                    border_radius=ft.border_radius.all(10),
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text(
                        "Species Details",
                        size=18,
                        weight=ft.FontWeight.W_700,
                        color="#FFFFFF",
                    ),
                    ft.Text(
                        subtitle,
                        size=12,
                        color=ft.Colors.with_opacity(0.75, "#FFFFFF"),
                    ),
                ], spacing=2, expand=True),

                # Close X
                ft.Container(
                    content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=16, color="#FFFFFF"),
                    on_click=lambda e: self.page.close(self._current_dialog),
                    bgcolor=ft.Colors.with_opacity(0.15, "#FFFFFF"),
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.all(6),
                    ink=True,
                    tooltip="Close",
                ),
            ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE_700,          # Blue — matches app primary action color
            padding=ft.padding.symmetric(horizontal=24, vertical=18),
            border_radius=ft.border_radius.only(top_left=14, top_right=14),
        )

    # ── Basic info card ───────────────────────────────────────────────────────

    def _info_row(self, icon, label, value) -> ft.Control | None:
        str_val = str(value) if value is not None else ""
        if not str_val.strip() or str_val == "None":
            return None

        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(icon, size=15, color=self._text_secondary()),
                    ft.Text(label, size=13, color=self._text_secondary(),
                            weight=ft.FontWeight.W_500),
                ], spacing=6),
                ft.Container(expand=True),
                ft.Text(str_val, size=13, weight=ft.FontWeight.W_600,
                        color=self._text_primary(),
                        overflow=ft.TextOverflow.ELLIPSIS, max_lines=1),
            ]),
            padding=ft.padding.symmetric(horizontal=16, vertical=11),
            border=ft.border.only(bottom=ft.BorderSide(1, self._divider())),
        )

    def _build_basic_info_card(self, species) -> ft.Container:
        rows = [
            self._info_row(ft.Icons.CODE,          "Species Code",  species.get("SpeciesCode")),
            self._info_row(ft.Icons.TEXT_SNIPPET,  "Common Name",   species.get("SpecCommon")),
            self._info_row(ft.Icons.LOCATION_ON,   "Origin",        species.get("Origin")),
            self._info_row(ft.Icons.FUNCTIONS,     "Equation Type", species.get("EquationType", "Height-based")),
        ]
        valid_rows = [r for r in rows if r is not None]

        # Remove bottom border from last row
        if valid_rows:
            last = valid_rows[-1]
            last.border = None

        return self._card(
            icon=ft.Icons.INFO_OUTLINE,
            icon_color="#2563EB",
            label="Basic Information",
            content=ft.Column(valid_rows, spacing=0),
        )

    # ── Parameter cards ───────────────────────────────────────────────────────

    def _build_parameter_cards(self, species) -> list:
        categorized = {}

        for key, value in species.items():
            if key in ["SpeciesCode", "Origin", "EquationType", "SpecCommon"]:
                continue
            category_key = "bh" if key.startswith("bh") else ("b" if key.startswith("b") else "default")
            cat = self.PARAMETER_CATEGORIES[category_key]
            if category_key not in categorized:
                categorized[category_key] = {
                    "name":    cat["name"],
                    "icon":    cat["icon"],
                    "color":   cat["color"],
                    "params":  [],
                }
            categorized[category_key]["params"].append((key, value))

        cards = []
        for cat_data in categorized.values():
            color = cat_data["color"]

            # Column header row
            col_header = ft.Container(
                content=ft.Row([
                    ft.Text("Parameter", size=11, weight=ft.FontWeight.W_700,
                            color=self._text_secondary()),
                    ft.Container(expand=True),
                    ft.Text("Value", size=11, weight=ft.FontWeight.W_700,
                            color=self._text_secondary()),
                ]),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                bgcolor=self._surface(),
                border_radius=ft.border_radius.all(6),
                margin=ft.margin.only(bottom=4),
            )

            param_rows = []
            for i, (k, v) in enumerate(cat_data["params"]):
                is_last = (i == len(cat_data["params"]) - 1)
                try:
                    display_val = f"{float(v):.6f}"
                except (ValueError, TypeError):
                    display_val = str(v)

                row = ft.Container(
                    content=ft.Row([
                        ft.Text(k, size=13, weight=ft.FontWeight.W_500,
                                color=self._text_primary(),
                                overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Container(expand=True),
                        ft.Text(display_val, size=13, weight=ft.FontWeight.W_600,
                                color=color or self._text_primary()),
                    ]),
                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                    border=ft.border.only(
                        bottom=ft.BorderSide(1, self._divider()) if not is_last else ft.BorderSide(0)
                    ),
                )
                param_rows.append(row)

            cards.append(self._card(
                icon=cat_data["icon"],
                icon_color=color or "#888888",
                label=cat_data["name"],
                content=ft.Column([col_header, *param_rows], spacing=0),
            ))

        return cards

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

    # ── Actions bar ───────────────────────────────────────────────────────────

    def _build_actions(self) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CLOSE_ROUNDED, size=15, color="#FFFFFF"),
                        ft.Text("Close", size=13, weight=ft.FontWeight.W_600, color="#FFFFFF"),
                    ], spacing=7),
                    on_click=lambda e: self.page.close(self._current_dialog),
                    bgcolor=ft.Colors.BLUE_700,
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    ink=True,
                ),
            ]),
            padding=ft.padding.only(left=24, right=24, top=14, bottom=18),
            bgcolor=self._bg(),
            border=ft.border.only(top=ft.BorderSide(1, self._border())),
        )

    # ── Dialog assembly ───────────────────────────────────────────────────────

    def _create_dialog(self, species, width, height) -> ft.AlertDialog:
        scrollable_body = ft.Container(
            content=ft.Column([
                ft.Container(height=16),
                self._build_basic_info_card(species),
                ft.Container(height=14),
                *self._build_parameter_cards(species),
                ft.Container(height=16),
            ], scroll=ft.ScrollMode.AUTO, spacing=0, tight=True, expand=True),
            padding=ft.padding.symmetric(horizontal=22),
            expand=True,
            bgcolor=self._bg(),
        )

        main = ft.Container(
            content=ft.Column([
                self._build_header(species),
                scrollable_body,
                self._build_actions(),
            ], spacing=0, tight=True),
            width=width,
            height=height,
            bgcolor=self._bg(),
            border_radius=ft.border_radius.all(14),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            shadow=ft.BoxShadow(
                blur_radius=30,
                spread_radius=0,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            ),
        )

        dialog = ft.AlertDialog(
            modal=True,
            content=main,
            content_padding=ft.padding.all(0),
            shape=ft.RoundedRectangleBorder(radius=14),
            bgcolor=ft.Colors.TRANSPARENT,
            inset_padding=ft.padding.symmetric(horizontal=20, vertical=20),
            alignment=ft.alignment.center,
        )

        self._current_dialog = dialog
        return dialog

    # ── Compat shims (kept so callers don't break) ────────────────────────────

    def _create_dialog_content(self, species, width, height):
        return self._create_dialog(species, width, height)

    def _show_dialog(self, dialog, species):
        self.page.open(dialog)
        logger.write(f"Viewing species: {species.get('SpeciesCode', '')}")