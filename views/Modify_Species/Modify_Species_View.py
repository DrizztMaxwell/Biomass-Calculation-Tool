#modify species view

import flet as ft
from matplotlib.pyplot import title
from widgets.TitleTextWidget import TitleTextWidget
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
from widgets.DescriptionText import DescriptionText
from widgets.LogFileTxt import logger
from widgets.Title_With_Icon import Title_With_Icon
from constants.Modify_Species_Constants import Settings_Constants
from widgets.View_Dialog import View_Dialog
from widgets.Edit_Dialog import Edit_Dialog
from widgets.Delete_Dialog import Delete_Dialog

from .components.Search_Field import Search_Field
from .components.Action_Buttons import Action_Buttons
from .components.No_Data_Display import No_Data_Display
from .components.No_Search_Results_Display import No_Search_Results_Display
from .components.Pagination_Controls import Pagination_Controls
from .components.Species_Data_Table import Species_Data_Table


class Modify_Species_View:
    """CRUD interface for managing species in created_species.json"""

    def __init__(self, page: ft.Page, controller=None):
        self.page = page
        self.current_species_index = None
        self.__controller = controller
        self.__controller.load_species_data()
        self.CONSTANTS = Settings_Constants()

        self.current_page    = 1
        self.items_per_page  = 10
        self.filtered_species = []

        self.primary_color   = ft.Colors.BLUE_700
        self.secondary_color = ft.Colors.GREEN_600
        self.accent_color    = ft.Colors.ORANGE_500
        self.text_secondary  = ft.Colors.GREY_600

        self.search_field = Search_Field(
            self.CONSTANTS.SEARCH_FIELD_PLACEHOLDER,
            self.filter_species,
        )
        self.no_data_display = No_Data_Display(
            self.primary_color, ft.Colors.GREY_900, self.text_secondary
        )
        self.no_search_results_display = No_Search_Results_Display(self.clear_search)
        self.data_table = Species_Data_Table(page=page)
        self.pagination_controls = Pagination_Controls(
            self.primary_color, ft.Colors.GREY_900, self.text_secondary
        )
        self.pagination_controls.prev_button.on_click = self.previous_page
        self.pagination_controls.next_button.on_click = self.next_page

        self.filtered_species = self.__controller.get_species_data().copy()

        # File Pickers
        self.save_file_picker = ft.FilePicker(on_result=self.on_save_file_result)
        self.load_file_picker = ft.FilePicker(on_result=self.on_load_file_result)

        self.page.overlay.append(self.save_file_picker)
        self.page.overlay.append(self.load_file_picker)

    # ─────────────────────────────────────────────────────────────
    # Save species button handler
    # ─────────────────────────────────────────────────────────────
    def save_species_to_file(self, e):
        self.save_file_picker.save_file(
            dialog_title="Save Species File",
            file_name="species.species",
            allowed_extensions=["species"]
        )

    def on_save_file_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            success = self.__controller.export_species_file(e.path)
            if success:
                Custom_Alert_Dialog(
                    page=self.page,
                    title_icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    title_color=ft.Colors.GREEN,
                    title_icon_color=ft.Colors.GREEN,
                    title="Save Successful",
                    message="Species saved successfully.",
                    solution="",
                    button_text="I Understand",
                ).show()

            else:
                Custom_Alert_Dialog(
                    page=self.page,
                    title_icon=ft.Icons.ERROR,
                    title_color=ft.Colors.RED,
                    title_icon_color=ft.Colors.RED,
                    title="Save Failed",
                    message="Error saving species.",
                    solution="",
                    button_text="I Understand",
                ).show()
            self.page.update()

    # ─────────────────────────────────────────────────────────────
    # Load species button handler
    # ─────────────────────────────────────────────────────────────
    def load_species_from_file(self, e):
        self.load_file_picker.pick_files(
            dialog_title="Load Species File",
            allowed_extensions=["species"]
        )

    def on_load_file_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            success, appended_count, duplicate_count = self.__controller.import_species_file(file_path)

            if success:
                self.refresh_data_table()
                
                # Show appropriate message based on what was imported
                if appended_count > 0:
                    message = f"Successfully imported {appended_count} new species.\n"
                    if duplicate_count > 0:
                        message += f"Skipped {duplicate_count} duplicate species."
                    else:
                        message += "All species were new."
                    
                    dialog = Custom_Alert_Dialog(
                        page=self.page,
                        title_icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                        title_color=ft.Colors.GREEN,
                        title_icon_color=ft.Colors.GREEN,
                        title="Import Successful",
                        message=message,
                        solution="",
                        button_text="I Understand",
                    )
                else:
                    dialog = Custom_Alert_Dialog(
                        page=self.page,
                        title_icon=ft.Icons.INFO_OUTLINE,
                        title_color=ft.Colors.ORANGE,
                        title_icon_color=ft.Colors.ORANGE,
                        title="No New Species",
                        message=f"No new species were imported. All {duplicate_count} species already exist in the database.",
                        solution="Try importing a different file with new species.",
                        button_text="I Understand",
                    )
                dialog.show()
            else:
                dialog = Custom_Alert_Dialog(
                    page=self.page,
                    title_icon=ft.Icons.ERROR,
                    title_color=ft.Colors.RED,
                    title_icon_color=ft.Colors.RED,
                    title="Import Failed",
                    message="Error importing species.",
                    solution="Please check the file format and try again.",
                    button_text="I Understand",
                )
                dialog.show()
        
            self.page.update()

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):           return "#1A1A1A" if self._is_dark else "#FFFFFF"
    def _surface(self):      return "#222222" if self._is_dark else "#F8FAFC"
    def _surface_card(self): return "#2A2A2A" if self._is_dark else "#FFFFFF"
    def _border(self):       return "#2E2E2E" if self._is_dark else "#E2E8F0"
    def _text_primary(self): return "#F5F5F5" if self._is_dark else "#0F172A"
    def _text_sec(self):     return "#888888" if self._is_dark else "#64748B"

    def _row_even_bg(self):
        return ft.Colors.with_opacity(0.0, ft.Colors.WHITE)

    def _row_odd_bg(self):
        return (ft.Colors.with_opacity(0.04, ft.Colors.WHITE)
                if self._is_dark
                else ft.Colors.with_opacity(0.5, ft.Colors.BLUE_50))

    # ── Search bar ────────────────────────────────────────────────────────────

    def _build_search_bar(self) -> ft.Container:
        def on_clear(e):
            self._search_input.value = ""
            self._search_input.update()
            self._clear_btn.visible = False
            self._clear_btn.update()
            self.filter_species(e)

        def on_change(e):
            self._clear_btn.visible = bool(self._search_input.value)
            self._clear_btn.update()
            self.filter_species(e)

        self._search_input = ft.TextField(
            hint_text=self.CONSTANTS.SEARCH_FIELD_PLACEHOLDER,
            on_change=on_change,
            border=ft.InputBorder.NONE,
            filled=False,
            color=self._text_primary(),
            hint_style=ft.TextStyle(color=self._text_sec(), size=13),
            text_style=ft.TextStyle(size=13),
            cursor_color=self._text_primary(),
            expand=True,
            content_padding=ft.padding.symmetric(vertical=10),
        )
        self._clear_btn = ft.Container(
            content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=16, color=self._text_sec()),
            on_click=on_clear,
            visible=False,
            padding=ft.padding.all(4),
            border_radius=ft.border_radius.all(20),
            ink=True,
            tooltip="Clear search",
        )
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SEARCH_ROUNDED, size=18, color=self._text_sec()),
                ft.Container(width=8),
                self._search_input,
                self._clear_btn,
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            bgcolor=self._surface_card(),
            border=ft.border.all(1, self._border()),
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.symmetric(horizontal=14, vertical=2),
            expand=True,
        )

    # ── Pagination helpers ────────────────────────────────────────────────────

    def get_paginated_species(self):
        start = (self.current_page - 1) * self.items_per_page
        return self.filtered_species[start: start + self.items_per_page]

    def calculate_pagination_info(self):
        total = len(self.filtered_species)
        if total == 0:
            return {"info_text": "Showing 0 species", "current_page": 1,
                    "total_pages": 1, "prev_disabled": True, "next_disabled": True,
                    "prev_color": ft.Colors.GREY_400, "next_color": ft.Colors.GREY_400}
        total_pages = max(1, (total + self.items_per_page - 1) // self.items_per_page)
        start = (self.current_page - 1) * self.items_per_page + 1
        end   = min(self.current_page * self.items_per_page, total)
        return {
            "info_text":      f"Showing {start}–{end} of {total} species",
            "current_page":   self.current_page,
            "total_pages":    total_pages,
            "prev_disabled":  self.current_page <= 1,
            "next_disabled":  self.current_page >= total_pages,
            "prev_color": ft.Colors.GREY_400 if self.current_page <= 1 else self.primary_color,
            "next_color": ft.Colors.GREY_400 if self.current_page >= total_pages else self.primary_color,
        }

    def update_pagination_controls(self):
        info = self.calculate_pagination_info()
        self.pagination_controls.update_pagination(
            info["info_text"], info["current_page"],
            info["prev_disabled"], info["next_disabled"],
            info["prev_color"],   info["next_color"],
        )
        self.pagination_controls.visible = len(self.filtered_species) > 0

    def next_page(self, e):
        total_pages = max(1, (len(self.filtered_species) + self.items_per_page - 1)
                         // self.items_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.refresh_data_table()

    def previous_page(self, e):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_data_table()

    def clear_search(self, e):
        if hasattr(self, "_search_input"):
            self._search_input.value = ""
            self._search_input.update()
        if hasattr(self, "_clear_btn"):
            self._clear_btn.visible = False
            self._clear_btn.update()
        self.filter_species(e)

    def filter_species(self, e):
        self.current_page = 1
        self.refresh_data_table()

    # ── Table row ─────────────────────────────────────────────────────────────

    def create_table_row(self, species, index, actual_index):
        species_code  = str(species.get("SpeciesCode", ""))
        spec_common   = str(species.get("SpecCommon", ""))
        origin        = species.get("Origin", "")
        equation_type = species.get("EquationType", "Height-based")

        species_display = (spec_common if spec_common and spec_common not in ("", "None")
                           else species_code)

        if equation_type == "DBH + Height-based":
            eq_color, eq_icon = ft.Colors.GREEN, ft.Icons.TRENDING_UP
        elif equation_type == "DBH-based":
            eq_color, eq_icon = ft.Colors.AMBER_700, ft.Icons.STRAIGHTEN
        else:
            eq_color, eq_icon = self.text_secondary, ft.Icons.FUNCTIONS

        row_number = (self.current_page - 1) * self.items_per_page + index + 1
        row_bg     = self._row_odd_bg() if index % 2 != 0 else self._row_even_bg()

        action_buttons = Action_Buttons(
            actual_index,
            self.display_view_dialog, self.display_edit_dialog,
            self.display_delete_dialog,
            self.primary_color, self.secondary_color,
        )

        return ft.DataRow(
            color=row_bg,
            cells=[
                ft.DataCell(ft.Container(
                    content=ft.Text(str(row_number), size=13,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.PRIMARY),
                    alignment=ft.alignment.center, padding=10,
                )),
                ft.DataCell(ft.Container(
                    content=ft.Text(species_display, size=13,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.PRIMARY),
                    padding=10,
                    tooltip=f"Code: {species_code}" if spec_common else None,
                )),
                ft.DataCell(ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=15,
                            color=self.text_secondary),
                    ft.Text(origin, size=13, color=ft.Colors.PRIMARY),
                ], spacing=6)),
                ft.DataCell(ft.Row([
                    ft.Icon(eq_icon, size=15, color=eq_color),
                    ft.Text(equation_type, size=13, color=eq_color),
                ], spacing=6)),
                ft.DataCell(action_buttons),
            ],
        )

    # ── Refresh ───────────────────────────────────────────────────────────────

    def refresh_data_table(self):
        self.data_table.rows.clear()

        search_text = ""
        if hasattr(self, "_search_input"):
            search_text = (self._search_input.value or "").lower()
        elif self.search_field.value:
            search_text = self.search_field.value.lower()

        self.filtered_species = []
        for species in self.__controller.get_species_data():
            if search_text:
                fields = [str(species.get(k, ""))
                          for k in ("SpeciesCode", "SpecCommon", "Origin")]
                if not any(search_text in f.lower() for f in fields):
                    continue
            self.filtered_species.append(species)

        no_data   = len(self.__controller.get_species_data()) == 0
        no_result = not self.filtered_species and not no_data

        self.data_table.visible               = bool(self.filtered_species)
        self.no_data_display.visible          = no_data
        self.no_search_results_display.visible = no_result
        self.pagination_controls.visible      = bool(self.filtered_species)

        if self.filtered_species:
            self.update_pagination_controls()
            for i, species in enumerate(self.get_paginated_species()):
                actual = (self.current_page - 1) * self.items_per_page + i
                self.data_table.rows.append(self.create_table_row(species, i, actual))

        self.page.update()

    # ── Dialogs ───────────────────────────────────────────────────────────────

    def display_view_dialog(self, index):
        View_Dialog(self.page).view_species_dialog(
            index, self.__controller.get_species_data(),
            self.filtered_species,
            self.primary_color, self.secondary_color, self.accent_color,
        )

    def display_edit_dialog(self, index):
        Edit_Dialog(self.page).edit_species_dialog(
            index=index, filtered_species=self.filtered_species,
            species_data=self.__controller.get_species_data(),
            controller=self.__controller,
            primary_color=self.primary_color,
            secondary_color=self.secondary_color,
            accent_color=self.accent_color,
            refresh_callback=self.refresh_data_table,
            save_callback=self.__controller.save_species_data,
        )

    def display_delete_dialog(self, index):
        Delete_Dialog(self.page, self.__controller).delete_species_confirmation(
            index=index, filtered_species=self.filtered_species,
            species_data=self.__controller.get_species_data(),
            controller=self.__controller,
            text_secondary=self.text_secondary,
            refresh_callback=self.refresh_data_table,
            save_callback=self.__controller.save_species_data,
        )

    # ── Build ─────────────────────────────────────────────────────────────────

    def build(self):
        self.filtered_species = self.__controller.get_species_data().copy()

        # ── Page header ───────────────────────────────────────────────────────
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.EDIT_OUTLINED, size=22,
                                        color="#FFFFFF"),
                        bgcolor="#16A34A",
                        border_radius=ft.border_radius.all(10),
                        width=44, height=44,
                        alignment=ft.alignment.center,
                    ),

                    ft.Column([
                        ft.Text("Modify Species", size=18,
                                weight=ft.FontWeight.W_700,
                                color=self._text_primary()),
                        ft.Text("Manage your created species — edit, delete, import or export.",
                                size=12, color=self._text_sec()),
                    ], spacing=2, expand=True),

                    # NEW BUTTONS
                    ft.Row([
                         ft.ElevatedButton(
                        "Clear Data",
                        bgcolor=ft.Colors.RED_700,
                        color=ft.Colors.WHITE,
                        icon=ft.Icons.DELETE_SWEEP,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(horizontal=14, vertical=6),
                            shape=ft.RoundedRectangleBorder(radius=5)
                        ),
                        on_click=self.clear_all_species_data,
                    ),
                        ft.ElevatedButton(
                            "Load Species",
                            bgcolor=ft.Colors.PURPLE_800 if self._is_dark else ft.Colors.ORANGE_600,
                            color=ft.Colors.WHITE,
                            
                             style=ft.ButtonStyle(
                                 padding=ft.padding.symmetric(horizontal=14, vertical=6),
                                 
                shape=ft.RoundedRectangleBorder(radius=5)  # Set radius here
            ),
                            icon=ft.Icons.UPLOAD_FILE,
                            on_click=self.load_species_from_file,
                            
                        ),
                        ft.ElevatedButton(
                            "Save Species",
                            bgcolor=ft.Colors.GREEN_700 if self._is_dark else ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE,
                            icon=ft.Icons.DOWNLOAD,
                            on_click=self.save_species_to_file,
                               style=ft.ButtonStyle(
                                 padding=ft.padding.symmetric(horizontal=14, vertical=6),
                                 
                shape=ft.RoundedRectangleBorder(radius=5)  # Set radius here
            ),
                        ),
                    ], spacing=10),
                ],
                
                spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=1, bgcolor=self._border(),
                             margin=ft.margin.only(top=14)),
            ], spacing=0),
            margin=ft.margin.only(bottom=16),
        )

        # ── Search row ────────────────────────────────────────────────────────
        search_row = ft.Row([self._build_search_bar()], spacing=0)

        # ── Table area ────────────────────────────────────────────────────────
        # expand=True lets this fill all remaining vertical space so the
        # view grows/shrinks with the window — no fixed height
        table_area = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        self.data_table.scroll_container,
                        self.no_data_display,
                        self.no_search_results_display,
                    ], spacing=0),
                    expand=True,
                    padding=ft.padding.all(8),
                ),
                self.pagination_controls,
            ], spacing=0, expand=True),
            expand=True,
            border=ft.border.all(1, self._border()),
            border_radius=ft.border_radius.all(10),
            bgcolor=self._surface_card(),
            clip_behavior=ft.ClipBehavior.NONE,
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=8,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

        # ── Outer card ────────────────────────────────────────────────────────
        # expand=True + no fixed height = fully responsive
        content = ft.Container(
            content=ft.Column([
                header,
                search_row,
                ft.Container(height=14),
                table_area,
            ], spacing=0, expand=True),
            margin=ft.margin.all(20),
            padding=ft.padding.all(24),
            expand=True,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=ft.border_radius.all(12),
            border=ft.border.all(1, self._border()),
            clip_behavior=ft.ClipBehavior.NONE,
            shadow=ft.BoxShadow(
                spread_radius=0, blur_radius=10,
                color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
            ),
        )

        self.populate_initial_table()
        return content
    
    def populate_initial_table(self):
        self.refresh_data_table()

    def clear_all_species_data(self, e):
        """Clear all species data from the database"""

        def show_confirmation():
            is_dark = self.page.theme_mode == ft.ThemeMode.DARK
            bg       = "#1A1A1A" if is_dark else "#FFFFFF"
            surface  = "#222222" if is_dark else "#F8FAFC"
            border   = "#2E2E2E" if is_dark else "#E2E8F0"
            text_pri = "#F5F5F5" if is_dark else "#0F172A"
            text_sec = "#888888" if is_dark else "#64748B"
            icon_color = ft.Colors.RED_700

            # ── Icon badge ────────────────────────────────────────────
            icon_badge = ft.Container(
                content=ft.Icon(ft.Icons.DELETE_SWEEP, size=22, color=icon_color),
                bgcolor=ft.Colors.with_opacity(0.12, icon_color),
                border_radius=ft.border_radius.all(10),
                width=44, height=44,
                alignment=ft.alignment.center,
            )

            # ── Header ────────────────────────────────────────────────
            header = ft.Container(
                content=ft.Row([
                    icon_badge,
                    ft.Column([
                        ft.Text("Clear All Data", size=16,
                                weight=ft.FontWeight.W_700, color=text_pri),
                    ], spacing=0, tight=True, expand=True),
                    ft.Container(
                        content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=15, color=text_sec),
                        on_click=lambda e: close_dialog(),
                        bgcolor=ft.Colors.with_opacity(
                            0.06, ft.Colors.WHITE if is_dark else ft.Colors.BLACK
                        ),
                        border_radius=ft.border_radius.all(7),
                        padding=ft.padding.all(5),
                        ink=True,
                        tooltip="Close",
                    ),
                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.only(left=20, right=20, top=18, bottom=14),
                bgcolor=surface,
                border_radius=ft.border_radius.only(top_left=12, top_right=12),
            )

            # ── Body ──────────────────────────────────────────────────
            body = ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Are you sure you want to clear ALL species data?",
                        size=13, color=text_sec,
                    ),
                    ft.Container(height=8),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=13,
                                    color=icon_color),
                            ft.Text(
                                "This action cannot be undone and will permanently delete all species.",
                                size=12, weight=ft.FontWeight.W_500,
                                color=text_sec, expand=True,
                            ),
                        ], spacing=8),
                        bgcolor=ft.Colors.with_opacity(0.07, icon_color),
                        border=ft.border.all(1, ft.Colors.with_opacity(0.15, icon_color)),
                        border_radius=ft.border_radius.all(8),
                        padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    ),
                ], spacing=0, tight=True),
                padding=ft.padding.symmetric(horizontal=20, vertical=14),
                bgcolor=bg,
            )

            # ── Actions ───────────────────────────────────────────────
            actions = ft.Container(
                content=ft.Row([
                    ft.Container(expand=True),
                    # Cancel button
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CLOSE_ROUNDED, size=14,
                                    color=text_sec),
                            ft.Text("Cancel", size=13,
                                    weight=ft.FontWeight.W_600, color=text_sec),
                        ], spacing=6, tight=True),
                        on_click=lambda e: close_dialog(),
                        bgcolor=ft.Colors.with_opacity(
                            0.06, ft.Colors.WHITE if is_dark else ft.Colors.BLACK
                        ),
                        border_radius=ft.border_radius.all(8),
                        padding=ft.padding.symmetric(horizontal=16, vertical=9),
                        ink=True,
                    ),
                    ft.Container(width=8),
                    # Confirm button
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.DELETE_ROUNDED, size=14, color="#FFFFFF"),
                            ft.Text("Clear Data", size=13,
                                    weight=ft.FontWeight.W_600, color="#FFFFFF"),
                        ], spacing=6, tight=True),
                        on_click=lambda e: confirm_clear(),
                        bgcolor=icon_color,
                        border_radius=ft.border_radius.all(8),
                        padding=ft.padding.symmetric(horizontal=18, vertical=9),
                        ink=True,
                    ),
                ]),
                padding=ft.padding.only(left=20, right=20, top=12, bottom=16),
                bgcolor=bg,
                border=ft.border.only(top=ft.BorderSide(1, border)),
            )

            # ── Assemble ──────────────────────────────────────────────
            main = ft.Container(
                content=ft.Column([
                    header,
                    ft.Container(height=1, bgcolor=border),
                    body,
                    actions,
                ], spacing=0, tight=True),
                width=420,
                bgcolor=bg,
                border_radius=ft.border_radius.all(12),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                shadow=ft.BoxShadow(
                    blur_radius=24, spread_radius=0,
                    color=ft.Colors.with_opacity(0.18, ft.Colors.BLACK),
                    offset=ft.Offset(0, 6),
                ),
            )

            confirm_dialog = ft.AlertDialog(
                modal=True,
                content=main,
                content_padding=ft.padding.all(0),
                shape=ft.RoundedRectangleBorder(radius=12),
                bgcolor=ft.Colors.TRANSPARENT,
                inset_padding=ft.padding.symmetric(horizontal=40, vertical=20),
                alignment=ft.alignment.center,
            )

            def close_dialog():
                self.page.close(confirm_dialog)
                self.page.update()

            def confirm_clear():
                self.__controller.clear_species_data()
                self.refresh_data_table()
                self.page.close(confirm_dialog)
                Custom_Alert_Dialog(
                    page=self.page,
                    title_icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    title_color=ft.Colors.GREEN,
                    title_icon_color=ft.Colors.GREEN,
                    title="Data Cleared",
                    message="All species data has been successfully cleared.",
                    solution="",
                    button_text="I Understand",
                ).show()
                self.page.update()

            self.page.open(confirm_dialog)

        show_confirmation()