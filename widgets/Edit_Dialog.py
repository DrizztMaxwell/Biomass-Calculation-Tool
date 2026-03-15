import flet as ft
from widgets.LogFileTxt import logger
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog


class Edit_Dialog:
    """Dialog for editing species data."""

    DIALOG_WIDTH_MAX    = 700
    DIALOG_WIDTH_MIN    = 320
    DIALOG_HEIGHT_MAX   = 650
    DIALOG_HEIGHT_MIN   = 400
    DIALOG_WIDTH_RATIO  = 0.9
    DIALOG_HEIGHT_RATIO = 0.85

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
    GREEN_500           = ft.Colors.GREEN_500
    RED_500             = ft.Colors.RED_500
    BLACK               = ft.Colors.BLACK
    PURPLE_600          = ft.Colors.PURPLE_600

    PARAMETER_CATEGORIES = {
        "bh": {"name": "DBH + Height-based Parameters", "icon": ft.Icons.TRENDING_UP,  "color": None},
        "b":  {"name": "DBH-based Parameters",          "icon": ft.Icons.STRAIGHTEN,   "color": None},
        "default": {"name": "Other Parameters",         "icon": ft.Icons.TUNE,         "color": ft.Colors.PURPLE_600},
    }

    MIN_VALUE = -5
    MAX_VALUE = 5

    def __init__(self, page):
        self.page = page
        self.current_species_index = None
        self.param_text_fields = {}
        self.origin_dropdown = None
        self._current_dialog = None

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

    def _input_bg(self):
        return "#2A2A2A" if self._is_dark else "#FFFFFF"

    # ── Public entry ──────────────────────────────────────────────────────────

    def edit_species_dialog(self, index, filtered_species, species_data,
                            controller, primary_color=None, secondary_color=None,
                            accent_color=None, refresh_callback=None, save_callback=None):
        self.primary_color   = primary_color   or self.PRIMARY_COLOR
        self.secondary_color = secondary_color or self.SECONDARY_COLOR
        self.accent_color    = accent_color    or self.ACCENT_COLOR
        self.text_secondary  = self.TEXT_SECONDARY
        self.refresh_callback = refresh_callback
        self.save_callback    = save_callback
        self.controller       = controller

        self.PARAMETER_CATEGORIES["bh"]["color"] = self.secondary_color
        self.PARAMETER_CATEGORIES["b"]["color"]  = self.accent_color

        species, actual_index = self._find_species(index, filtered_species, species_data)
        if not species:
            return

        self.current_species_index = actual_index
        display_value = self._get_display_value(species)
        width, height = self._calc_width(), self._calc_height()

        dialog = self._create_dialog(species, display_value, width, height)
        self._current_dialog = dialog
        self._show_dialog(dialog, species)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _find_species(self, index, filtered_species, species_data):
        if index >= len(filtered_species):
            return None, None
        item = filtered_species[index]
        code   = item.get("SpeciesCode")
        common = item.get("SpecCommon")
        for i, s in enumerate(species_data):
            if code   and s.get("SpeciesCode") == code:   return s, i
            if common and s.get("SpecCommon")  == common: return s, i
        return None, None

    def _get_display_value(self, species):
        c = species.get("SpecCommon")
        return c if c and c != "" else species.get("SpeciesCode")

    def _calc_width(self):
        w = (self.page.width or self.DIALOG_WIDTH_MAX) * self.DIALOG_WIDTH_RATIO
        return max(self.DIALOG_WIDTH_MIN, min(w, self.DIALOG_WIDTH_MAX))

    def _calc_height(self):
        h = (self.page.height or self.DIALOG_HEIGHT_MAX) * self.DIALOG_HEIGHT_RATIO
        return max(self.DIALOG_HEIGHT_MIN, min(h, self.DIALOG_HEIGHT_MAX))

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self, species, display_value) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.EDIT_OUTLINED, size=22, color="#FFFFFF"),
                    width=44, height=44,
                    bgcolor=ft.Colors.with_opacity(0.18, "#FFFFFF"),
                    border_radius=ft.border_radius.all(10),
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text("Edit Species", size=18, weight=ft.FontWeight.W_700,
                            color="#FFFFFF"),
                    ft.Text(display_value or "", size=12,
                            color=ft.Colors.with_opacity(0.75, "#FFFFFF")),
                ], spacing=2, expand=True),

                ft.Container(
                    content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=16, color="#FFFFFF"),
                    on_click=lambda e: self.page.close(self._current_dialog),
                    bgcolor=ft.Colors.with_opacity(0.15, "#FFFFFF"),
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.all(6),
                    ink=True,
                    tooltip="Cancel",
                ),
            ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#16A34A",
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

    # ── Basic info card ───────────────────────────────────────────────────────

    def _build_basic_info_card(self, species) -> ft.Container:
        self.origin_dropdown = ft.Dropdown(
            value=species.get("Origin", "Natural Stand"),
            options=[
                ft.dropdown.Option("Natural Stand"),
                ft.dropdown.Option("Plantation"),
            ],
            border_radius=ft.border_radius.all(8),
            filled=True,
            fill_color=self._input_bg(),
            border_color=self._border(),
            focused_border_color="#16A34A",
            text_size=13,
            content_padding=ft.padding.symmetric(horizontal=14, vertical=10),
            color=self._text_primary(),
            expand=True,
        )

        content = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=15,
                            color=self._text_secondary()),
                    ft.Text("Origin", size=13, weight=ft.FontWeight.W_500,
                            color=self._text_secondary()),
                ], spacing=6),
                ft.Container(expand=True),
                ft.Container(content=self.origin_dropdown, width=220),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=16, vertical=14),
        )

        return self._card(
            icon=ft.Icons.INFO_OUTLINE,
            icon_color="#2563EB",
            label="Basic Information",
            content=content,
        )

    # ── Parameter cards ───────────────────────────────────────────────────────

    def _categorize_parameters(self, species):
        categorized = {}
        for key, value in species.items():
            if key in ["SpeciesCode", "Origin", "EquationType", "SpecCommon"]:
                continue
            cat_key = "bh" if key.startswith("bh") else ("b" if key.startswith("b") else "default")
            cat = self.PARAMETER_CATEGORIES[cat_key]
            if cat_key not in categorized:
                categorized[cat_key] = {
                    "name": cat["name"], "icon": cat["icon"],
                    "color": cat["color"], "params": [],
                }
            categorized[cat_key]["params"].append((key, value))
        return categorized

    def _build_parameter_cards(self, species) -> list:
        self.param_text_fields = {}
        categorized = self._categorize_parameters(species)
        cards = []

        for cat_data in categorized.values():
            color = cat_data["color"] or "#888888"
            rows  = []

            for i, (k, v) in enumerate(cat_data["params"]):
                is_last = (i == len(cat_data["params"]) - 1)

                tf = ft.TextField(
                    value=str(v),
                    keyboard_type=ft.KeyboardType.NUMBER,
                    border_radius=ft.border_radius.all(8),
                    filled=True,
                    fill_color=self._input_bg(),
                    border_color=self._border(),
                    focused_border_color=color,
                    text_size=13,
                    color=self._text_primary(),
                    content_padding=ft.padding.symmetric(horizontal=12, vertical=10),
                    dense=True,
                    width=200,
                )
                self.param_text_fields[k] = tf

                row = ft.Container(
                    content=ft.Row([
                        ft.Text(k, size=13, weight=ft.FontWeight.W_500,
                                color=self._text_primary(),
                                expand=True,
                                overflow=ft.TextOverflow.ELLIPSIS),
                        tf,
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                    border=ft.border.only(
                        bottom=ft.BorderSide(1, self._divider()) if not is_last else ft.BorderSide(0)
                    ),
                )
                rows.append(row)

            cards.append(self._card(
                icon=cat_data["icon"],
                icon_color=color,
                label=cat_data["name"],
                content=ft.Column(rows, spacing=0),
            ))

        return cards

    # ── Actions bar ───────────────────────────────────────────────────────────

    def _build_actions(self, species) -> ft.Container:
        def save_wrapper(e):
            self._save_changes(e, self._current_dialog, species)

        return ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                # Cancel
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CLOSE_ROUNDED, size=14, color=self._text_secondary()),
                        ft.Text("Cancel", size=13, weight=ft.FontWeight.W_500,
                                color=self._text_secondary()),
                    ], spacing=6),
                    on_click=lambda e: self.page.close(self._current_dialog),
                    bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK),
                    border=ft.border.all(1, self._border()),
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                    ink=True,
                ),
                ft.Container(width=10),
                # Save
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_ROUNDED, size=15, color="#FFFFFF"),
                        ft.Text("Save Changes", size=13, weight=ft.FontWeight.W_600,
                                color="#FFFFFF"),
                    ], spacing=7),
                    on_click=save_wrapper,
                    bgcolor="#16A34A",
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    ink=True,
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(left=24, right=24, top=14, bottom=18),
            bgcolor=self._bg(),
            border=ft.border.only(top=ft.BorderSide(1, self._border())),
        )

    # ── Dialog assembly ───────────────────────────────────────────────────────

    def _create_dialog(self, species, display_value, width, height) -> ft.AlertDialog:
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
                self._build_header(species, display_value),
                scrollable_body,
                self._build_actions(species),
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
        return dialog

    # ── Save logic (unchanged) ────────────────────────────────────────────────

    def _save_changes(self, e, dialog, species):
        try:
            self.controller.get_species_data()[self.current_species_index]["Origin"] = self.origin_dropdown.value
            has_errors, error_messages = self._validate_parameters()
            if has_errors:
                self._show_validation_errors(error_messages)
                return
            if self._save_species_data():
                self._show_success_message(species)
                if self.refresh_callback:
                    self.refresh_callback()
            else:
                self._show_error_dialog("Failed to save changes.")
        except Exception as ex:
            self._show_error_dialog(f"Error saving species: {ex}")
            import traceback
            traceback.print_exc()

    def _validate_parameters(self):
        has_errors, error_messages = False, []
        for param_key, tf in self.param_text_fields.items():
            if not tf.value:
                has_errors = True
                self._mark_field_error(tf, "This field cannot be empty")
                error_messages.append(f"{param_key}: Field cannot be empty")
                continue
            try:
                value = float(tf.value)
                if value < self.MIN_VALUE or value > self.MAX_VALUE:
                    has_errors = True
                    self._mark_field_error(tf, f"Value must be between {self.MIN_VALUE} and {self.MAX_VALUE}")
                    error_messages.append(f"{param_key}: out of range")
                else:
                    self._clear_field_error(tf)
                    self.controller.get_species_data()[self.current_species_index][param_key] = value
            except ValueError:
                has_errors = True
                self._mark_field_error(tf, "Invalid number format")
                error_messages.append(f"{param_key}: Invalid number format")
        return has_errors, error_messages

    def _mark_field_error(self, tf, error_text):
        tf.error_text  = error_text
        tf.border_color = self.RED_500
        tf.update()

    def _clear_field_error(self, tf):
        tf.error_text   = None
        tf.border_color = self._border()
        tf.update()

    def _show_validation_errors(self, error_messages):
        self._show_error_dialog("Please fix the following errors:\n" +
                                "\n".join(f"• {m}" for m in error_messages))

    def _save_species_data(self):
        return self.save_callback() if self.save_callback else False

    def _show_error_dialog(self, message):
        d = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor=self._bg(),
            title=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.ERROR_OUTLINE, size=20, color="#FFFFFF"),
                    bgcolor="#DC2626",
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.all(6),
                ),
                ft.Text("Error", size=16, weight=ft.FontWeight.W_700,
                        color=self._text_primary()),
            ], spacing=10),
            content=ft.Text(message, size=13, color=self._text_secondary()),
            actions=[
                ft.Container(
                    content=ft.Container(
                        content=ft.Text("OK", size=13, weight=ft.FontWeight.W_600,
                                        color="#FFFFFF"),
                        on_click=lambda e: self.page.close(d),
                        bgcolor="#2563EB",
                        border_radius=ft.border_radius.all(8),
                        padding=ft.padding.symmetric(horizontal=20, vertical=9),
                        ink=True,
                    ),
                    padding=ft.padding.only(right=4, bottom=8),
                    alignment=ft.alignment.center_right,
                )
            ],
        )
        self.page.open(d)

    def _show_success_message(self, species):
        Custom_Alert_Dialog(
            page=self.page,
            title_icon=ft.Icons.CHECK_CIRCLE,
            title_color=self.BLACK,
            title_icon_color=ft.Colors.GREEN,
            title="Success",
            message="Species updated successfully!",
            button_text="OK",
        ).show()
        logger.write(f"Species '{species.get('SpeciesCode', '')}' updated successfully.")

    def _show_dialog(self, dialog, species):
        self.page.open(dialog)
        logger.write(f"Editing species: {species.get('SpeciesCode', '')}")