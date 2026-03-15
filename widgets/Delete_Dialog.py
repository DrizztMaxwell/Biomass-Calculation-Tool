import flet as ft
from widgets.LogFileTxt import logger
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog


class Delete_Dialog:
    """Dialog for confirming species deletion."""

    DIALOG_WIDTH_MAX    = 500
    DIALOG_WIDTH_MIN    = 320
    DIALOG_HEIGHT_MAX   = 400
    DIALOG_HEIGHT_MIN   = 400
    DIALOG_WIDTH_RATIO  = 0.8
    DIALOG_HEIGHT_RATIO = 0.5

    RED_400             = ft.Colors.RED_400
    RED_500             = ft.Colors.RED_500
    RED_600             = ft.Colors.RED_600
    WHITE               = ft.Colors.WHITE
    PRIMARY             = ft.Colors.PRIMARY
    SECONDARY_CONTAINER = ft.Colors.SECONDARY_CONTAINER
    SECONDARY           = ft.Colors.SECONDARY
    GREY_100            = ft.Colors.GREY_100
    GREY_200            = ft.Colors.GREY_200
    BLACK               = ft.Colors.BLACK
    TEXT_SECONDARY      = ft.Colors.GREY_600

    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
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

    # ── Public entry ──────────────────────────────────────────────────────────

    def delete_species_confirmation(self, index, filtered_species, species_data,
                                    controller, text_secondary=None,
                                    refresh_callback=None, save_callback=None):
        self.text_secondary   = text_secondary or self.TEXT_SECONDARY
        self.controller       = controller
        self.refresh_callback = refresh_callback
        self.save_callback    = save_callback

        species, actual_index = self._find_species(index, filtered_species, species_data)
        if not species:
            self._show_error_dialog("Error: Species not found in master data.")
            return

        self.species       = species
        self.display_value = self._get_display_value(species)
        self.actual_index  = actual_index

        width, height = self._calc_width(), self._calc_height()
        dialog = self._create_dialog(width, height)
        self._current_dialog = dialog
        self._show_dialog(dialog)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _find_species(self, index, filtered_species, species_data):
        if index >= len(filtered_species):
            return None, None
        sp    = filtered_species[index]
        code  = sp.get("SpeciesCode", "Unknown")
        common = sp.get("SpecCommon", "Unknown")
        for i, s in enumerate(species_data):
            if code   and s.get("SpeciesCode") == code:   return sp, i
            if common and s.get("SpecCommon")  == common: return sp, i
        return None, None

    def _get_display_value(self, species):
        c = species.get("SpecCommon", "")
        return c if c and c not in ("", "Unknown") else species.get("SpeciesCode", "Unknown")

    def _calc_width(self):
        w = (self.page.width or self.DIALOG_WIDTH_MAX) * self.DIALOG_WIDTH_RATIO
        return max(self.DIALOG_WIDTH_MIN, min(w, self.DIALOG_WIDTH_MAX))

    def _calc_height(self):
        h = (self.page.height or self.DIALOG_HEIGHT_MAX) * self.DIALOG_HEIGHT_RATIO
        return max(self.DIALOG_HEIGHT_MIN, min(h, self.DIALOG_HEIGHT_MAX))

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED, size=22, color="#FFFFFF"),
                    width=44, height=44,
                    bgcolor=ft.Colors.with_opacity(0.18, "#FFFFFF"),
                    border_radius=ft.border_radius.all(10),
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text("Delete Species", size=18, weight=ft.FontWeight.W_700,
                            color="#FFFFFF"),
                    ft.Text(self.display_value, size=12,
                            color=ft.Colors.with_opacity(0.75, "#FFFFFF"),
                            overflow=ft.TextOverflow.ELLIPSIS),
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
            bgcolor="#DC2626",          # Red — destructive action
            padding=ft.padding.symmetric(horizontal=24, vertical=18),
            border_radius=ft.border_radius.only(top_left=14, top_right=14),
        )

    # ── Warning body ──────────────────────────────────────────────────────────

    def _build_body(self) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=28,
                                    color="#DC2626"),
                    width=56, height=56,
                    bgcolor=ft.Colors.with_opacity(0.08, "#DC2626"),
                    border_radius=ft.border_radius.all(28),
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=12),
                ft.Text(
                    f'Delete "{self.display_value}"?',
                    size=15,
                    weight=ft.FontWeight.W_700,
                    color=self._text_primary(),
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=6),
                ft.Text(
                    "This action cannot be undone.\nAll associated data will be permanently removed.",
                    size=13,
                    color=self._text_secondary(),
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=14),
                # Pill in Row to prevent full-width stretch
                ft.Row([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ERROR_OUTLINE_ROUNDED, size=13,
                                    color="#DC2626"),
                            ft.Text("Destructive — cannot be reversed", size=12,
                                    weight=ft.FontWeight.W_500, color="#DC2626"),
                        ], spacing=6, tight=True),
                        bgcolor=ft.Colors.with_opacity(0.07, "#DC2626"),
                        border=ft.border.all(1, ft.Colors.with_opacity(0.2, "#DC2626")),
                        border_radius=ft.border_radius.all(20),
                        padding=ft.padding.symmetric(horizontal=14, vertical=7),
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            tight=True),
            padding=ft.padding.symmetric(horizontal=28, vertical=22),
            bgcolor=self._bg(),
            alignment=ft.alignment.center,
        )

    # ── Actions bar ───────────────────────────────────────────────────────────

    def _build_actions(self) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                # Cancel
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CLOSE_ROUNDED, size=14,
                                color=self._text_secondary()),
                        ft.Text("Cancel", size=13, weight=ft.FontWeight.W_500,
                                color=self._text_secondary()),
                    ], spacing=6),
                    on_click=lambda e: self.page.close(self._current_dialog),
                    bgcolor=ft.Colors.with_opacity(
                        0.06, ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK
                    ),
                    border=ft.border.all(1, self._border()),
                    border_radius=ft.border_radius.all(8),
                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                    ink=True,
                ),
                ft.Container(width=10),
                # Delete
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.DELETE_ROUNDED, size=15, color="#FFFFFF"),
                        ft.Text("Delete", size=13, weight=ft.FontWeight.W_600,
                                color="#FFFFFF"),
                    ], spacing=7),
                    on_click=lambda e: self._confirm_delete(self._current_dialog),
                    bgcolor="#DC2626",
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

    def _create_dialog(self, width, height) -> ft.AlertDialog:
        main = ft.Container(
            content=ft.Column([
                self._build_header(),
                # Body scrollable + expands to fill available space
                ft.Container(
                    content=ft.Column(
                        [self._build_body()],
                        scroll=ft.ScrollMode.AUTO,
                        spacing=0,
                        tight=True,
                    ),
                    expand=True,
                    bgcolor=self._bg(),
                ),
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
        return dialog

    # ── Delete logic (unchanged) ──────────────────────────────────────────────

    def _confirm_delete(self, dialog):
        logger.write(f"Confirming deletion: {self.species.get('SpeciesCode', '')}")
        self.page.close(dialog)
        try:
            current_index = self._reconfirm_index()
            if current_index is None:
                self._show_error_dialog(f"Species '{self.display_value}' not found before deletion.")
                return
            if self._perform_deletion(current_index):
                self._show_success_message()
                if self.refresh_callback:
                    self.refresh_callback()
            else:
                self._show_error_dialog("Failed to save data after deleting species.")
        except Exception as ex:
            self._show_error_dialog(f"Error deleting species: {ex}")
            logger.write(f"Exception: {ex}")
        self.page.update()

    def _reconfirm_index(self):
        code   = self.species.get("SpeciesCode", "Unknown")
        common = self.species.get("SpecCommon",  "Unknown")
        for i, sp in enumerate(self.controller.get_species_data()):
            if code   and sp.get("SpeciesCode") == code:   return i
            if common and sp.get("SpecCommon")  == common: return i
        return None

    def _perform_deletion(self, index):
        deleted = self.controller.get_species_data().pop(index)
        if self._save_species_data():
            return True
        self.controller.get_species_data().insert(index, deleted)
        return False

    def _save_species_data(self):
        return self.save_callback() if self.save_callback else False

    def _show_success_message(self):
        Custom_Alert_Dialog(
            page=self.page,
            title_icon=ft.Icons.CHECK_CIRCLE,
            title_color=self.BLACK,
            title_icon_color=ft.Colors.GREEN,
            title="Success",
            message=f"Species '{self.display_value}' deleted successfully!",
            button_text="OK",
        ).show()
        logger.write(f"Species '{self.display_value}' deleted successfully.")

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
                        bgcolor="#DC2626",
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

    def _close_dialog(self, dialog):
        if dialog:
            dialog.open = False
            self.page.update()

    def _show_dialog(self, dialog):
        self.page.open(dialog)
        logger.write(f"Confirming deletion: {self.species.get('SpeciesCode', '')}")