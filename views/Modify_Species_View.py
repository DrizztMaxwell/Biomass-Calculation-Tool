import json
import flet as ft
from widgets.TitleTextWidget import TitleTextWidget
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
from widgets.DescriptionText import DescriptionText
from widgets.LogFileTxt import logger
from widgets.Title_With_Icon import Title_With_Icon
from constants.Modify_Species_Constants import Settings_Constants
from widgets.View_Dialog import View_Dialog
from widgets.Edit_Dialog import Edit_Dialog
from widgets.Delete_Dialog import Delete_Dialog


class Modify_Species_View:
    """CRUD interface for managing species in created_species.json"""

    def __init__(self, page: ft.Page, controller=None):
        self.page = page

        self.current_species_index = None
        self.__controller = controller
        self.__controller.load_species_data()
        self.CONSTANTS = Settings_Constants()
        # Pagination settings
        self.current_page = 1
        self.items_per_page = 10
        self.filtered_species = []

        self.primary_color = ft.Colors.BLUE_700
        self.secondary_color = ft.Colors.GREEN_600
        self.accent_color = ft.Colors.ORANGE_500
        self.bg_gradient_start = ft.Colors.WHITE
        self.bg_gradient_end = ft.Colors.BLUE_50
        self.card_bg = ft.Colors.WHITE
        self.text_primary = ft.Colors.GREY_900
        self.text_secondary = ft.Colors.GREY_600

        # Search Field with Uber Eats style
        self.search_field = ft.TextField(
            hint_text=self.CONSTANTS.SEARCH_FIELD_PLACEHOLDER,  # Updated hint
            hint_style=ft.TextStyle(size=14, color=ft.Colors.PRIMARY, italic=True),
            text_size=14,
            border_color=ft.Colors.PRIMARY,
            bgcolor=ft.Colors.SECONDARY,
            height=48,
            content_padding=ft.padding.only(left=20, right=20, top=15, bottom=15),
            border_radius=15,
            expand=True,
            filled=True,
            fill_color=ft.Colors.SECONDARY,
            focused_border_color=ft.Colors.PRIMARY,
            focused_bgcolor=ft.Colors.PRIMARY,
            on_change=self.filter_species,
            suffix_icon=ft.Icon(ft.Icons.SEARCH, color=self.primary_color, size=20),
        )

        # "No Data" Message with modern design
        self.no_data_display = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.AUTO_GRAPH_OUTLINED,
                            size=60,
                            color=ft.Colors.with_opacity(0.3, self.primary_color),
                        ),
                        padding=20,
                        bgcolor=ft.Colors.with_opacity(0.1, self.primary_color),
                        border_radius=50,
                        margin=ft.margin.only(bottom=20),
                    ),
                    ft.Text(
                        self.CONSTANTS.NO_SPECIES_MESSAGE,
                        size=18,
                        weight=ft.FontWeight.W_700,
                        color=self.text_primary,
                    ),
                    ft.Text(
                        self.CONSTANTS.NO_SPECIES_MESSAGE_SOLUTION,
                        size=14,
                        color=self.text_secondary,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=ft.alignment.center,
            padding=40,
            visible=False,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )

        # "No Search Results" Message
        self.no_search_results_display = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.SEARCH_OFF,
                            size=60,
                            color=ft.Colors.with_opacity(0.3, ft.Colors.RED_400),
                        ),
                        padding=20,
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED_400),
                        border_radius=50,
                        margin=ft.margin.only(bottom=20),
                    ),
                    ft.Text(
                        self.CONSTANTS.NO_SPECIES_FOUND_MESSAGE,
                        size=18,
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                    ),
                    ft.Text(
                        self.CONSTANTS.NO_SPECIES_FOUND_SOLUTION,
                        size=14,
                        color=ft.Colors.PRIMARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.TextButton(
                        "Clear Search",
                        icon=ft.Icons.CLEAR,
                        on_click=lambda e: setattr(self.search_field, "value", "")
                        or self.filter_species(e),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=ft.alignment.center,
            padding=40,
            visible=False,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            ),
        )

        # Data table with Uber Eats styling
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text(
                        "ROW",
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                        size=12,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "SPECIES",
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                        size=12,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "ORIGIN",
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                        size=12,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "EQUATION TYPE",
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                        size=12,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "ACTIONS",
                        weight=ft.FontWeight.W_700,
                        color=ft.Colors.PRIMARY,
                        size=12,
                    )
                ),
            ],
            rows=[],
            border=ft.border.all(0.5, ft.Colors.GREY_200),
            border_radius=10,
            vertical_lines=ft.BorderSide(0.5, ft.Colors.GREY_100),
            horizontal_lines=ft.BorderSide(0.5, ft.Colors.GREY_100),
            heading_row_color=ft.Colors.with_opacity(0.08, ft.Colors.GREEN_700),
            heading_row_height=55,
            data_row_min_height=60,
            data_row_max_height=70,
            column_spacing=30,
            width=9999,
            heading_text_style=ft.TextStyle(
                size=12, weight=ft.FontWeight.W_700, color=self.text_primary
            ),
        )

        # Pagination controls
        self.pagination_info = ft.Text(
            "", size=14, color=self.text_secondary, weight=ft.FontWeight.W_500
        )

        self.prev_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            icon_color=ft.Colors.GREY_400,
            icon_size=24,
            tooltip="Previous Page",
            disabled=True,
            on_click=self.previous_page,
        )

        self.next_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            icon_color=ft.Colors.GREY_400,
            icon_size=24,
            tooltip="Next Page",
            disabled=True,
            on_click=self.next_page,
        )

        # Page number display
        self.page_number_display = ft.Container(
            content=ft.Text(
                "1", size=14, weight=ft.FontWeight.W_600, color=self.text_primary
            ),
            padding=ft.padding.symmetric(horizontal=15, vertical=8),
            bgcolor=ft.Colors.with_opacity(0.1, self.primary_color),
            border_radius=8,
        )

        # Initialize filtered species
        self.filtered_species = self.__controller.get_species_data().copy()

    def filter_species(self, e):
        """Filter species based on search text and reset to first page"""
        self.current_page = 1
        self.refresh_data_table()

    def get_paginated_species(self):
        """Get species for current page"""
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        return self.filtered_species[start_index:end_index]

    def calculate_pagination_info(self):
        """Calculate pagination information without updating controls"""
        total_species = len(self.filtered_species)

        if total_species == 0:
            return {
                "info_text": "Showing 0 species",
                "current_page": 1,
                "total_pages": 1,
                "prev_disabled": True,
                "next_disabled": True,
                "prev_color": ft.Colors.GREY_400,
                "next_color": ft.Colors.GREY_400,
            }

        total_pages = max(
            1, (total_species + self.items_per_page - 1) // self.items_per_page
        )
        start_index = (self.current_page - 1) * self.items_per_page + 1
        end_index = min(self.current_page * self.items_per_page, total_species)

        return {
            "info_text": f"Showing {start_index}-{end_index} of {total_species} species",
            "current_page": self.current_page,
            "total_pages": total_pages,
            "prev_disabled": self.current_page <= 1,
            "next_disabled": self.current_page >= total_pages,
            "prev_color": (
                ft.Colors.GREY_400 if self.current_page <= 1 else self.primary_color
            ),
            "next_color": (
                ft.Colors.GREY_400
                if self.current_page >= total_pages
                else self.primary_color
            ),
        }

    def update_pagination_controls(self):
        """Update pagination controls with calculated values"""
        pagination_info = self.calculate_pagination_info()

        # Update controls directly
        self.pagination_info.value = pagination_info["info_text"]
        self.page_number_display.content.value = str(pagination_info["current_page"])
        self.prev_button.disabled = pagination_info["prev_disabled"]
        self.next_button.disabled = pagination_info["next_disabled"]
        self.prev_button.icon_color = pagination_info["prev_color"]
        self.next_button.icon_color = pagination_info["next_color"]

    def next_page(self, e):
        """Go to next page"""
        total_species = len(self.filtered_species)
        total_pages = max(
            1, (total_species + self.items_per_page - 1) // self.items_per_page
        )

        if self.current_page < total_pages:
            self.current_page += 1
            self.refresh_data_table()

    def previous_page(self, e):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_data_table()

    def refresh_data_table(self):
        """Refresh the data table with current species data"""
        # Clear existing rows
        self.data_table.rows.clear()

        # Apply search filter - search in SpeciesCode, SpecCommon, and Origin
        search_text = self.search_field.value.lower() if self.search_field.value else ""
        self.filtered_species = []

        for species in self.__controller.get_species_data():
            species_code = str(species.get("SpeciesCode", ""))
            spec_common = str(species.get("SpecCommon", ""))
            origin = species.get("Origin", "")

            # Check if search text matches any of these fields
            if search_text:
                matches_code = search_text in species_code.lower()
                matches_common = search_text in spec_common.lower()
                matches_origin = search_text in origin.lower()

                if not (matches_code or matches_common or matches_origin):
                    continue

            self.filtered_species.append(species)

        # Check if data exists
        if not self.filtered_species:
            self.data_table.visible = False
            self.no_data_display.visible = (
                len(self.__controller.get_species_data()) == 0
            )
            self.no_search_results_display.visible = (
                len(self.__controller.get_species_data()) > 0
            )
            self.pagination_info.value = "Showing 0 species"
            self.prev_button.visible = False
            self.next_button.visible = False
            self.page_number_display.visible = False
            # Update page once
            self.page.update()
            return

        # Show pagination controls
        self.prev_button.visible = True
        self.next_button.visible = True
        self.page_number_display.visible = True

        # Calculate pagination values
        pagination_info = self.calculate_pagination_info()
        self.pagination_info.value = pagination_info["info_text"]
        self.page_number_display.content.value = str(pagination_info["current_page"])
        self.prev_button.disabled = pagination_info["prev_disabled"]
        self.next_button.disabled = pagination_info["next_disabled"]
        self.prev_button.icon_color = pagination_info["prev_color"]
        self.next_button.icon_color = pagination_info["next_color"]

        # Get current page species
        current_page_species = self.get_paginated_species()

        # Populate table with current page species
        for index, species in enumerate(current_page_species):
            # Calculate actual index in filtered_species
            actual_index = (self.current_page - 1) * self.items_per_page + index

            species_code = str(species.get("SpeciesCode", ""))
            spec_common = str(species.get("SpecCommon", ""))
            origin = species.get("Origin", "")
            equation_type = species.get("EquationType", "Height-based")

            # Determine what to display in the SPECIES column
            # Show either SpecCommon OR SpeciesCode, not both
            if spec_common and spec_common != "" and spec_common != "None":
                species_display = spec_common  # Just show the common name
            else:
                species_display = species_code  # Show the code if no common name

            # Determine equation type color
            if equation_type == "DBH + Height-based":
                eq_color = ft.Colors.GREEN
                eq_icon = ft.Icons.TRENDING_UP
            elif equation_type == "DBH-based":
                eq_color = ft.Colors.AMBER_700
                eq_icon = ft.Icons.STRAIGHTEN
            else:
                eq_color = self.text_secondary
                eq_icon = ft.Icons.FUNCTIONS

            # Create row number with correct calculation
            row_number = (self.current_page - 1) * self.items_per_page + index + 1

            row = ft.DataRow(
                cells=[
                    # Row number cell
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                str(row_number),
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.PRIMARY,
                            ),
                            alignment=ft.alignment.center,
                            padding=10,
                        )
                    ),
                    # SPECIES cell - shows either common name OR code
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                species_display,
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.PRIMARY,
                            ),
                            padding=10,
                            tooltip=(
                                f"Code: {species_code}"
                                if spec_common
                                else f"Name: {spec_common}" if spec_common else None
                            ),
                        )
                    ),
                    # Origin cell
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.LOCATION_ON_OUTLINED,
                                    size=16,
                                    color=self.text_secondary,
                                ),
                                ft.Text(origin, size=14, color=ft.Colors.PRIMARY),
                            ],
                            spacing=8,
                        )
                    ),
                    # Equation Type cell
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.Icon(eq_icon, size=16, color=eq_color),
                                ft.Text(equation_type, size=14, color=eq_color),
                            ],
                            spacing=8,
                        )
                    ),
                    # Actions cell
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.IconButton(
                                        icon=ft.Icons.REMOVE_RED_EYE_OUTLINED,
                                        icon_color=ft.Colors.WHITE,
                                        icon_size=18,
                                        tooltip="View Details",
                                        on_click=lambda e, idx=actual_index: self.view_species_dialog(
                                            idx
                                        ),
                                    ),
                                    bgcolor=self.primary_color,
                                    border_radius=8,
                                    padding=ft.padding.all(2),
                                ),
                                ft.Container(
                                    content=ft.IconButton(
                                        icon=ft.Icons.EDIT_OUTLINED,
                                        icon_color=ft.Colors.WHITE,
                                        icon_size=18,
                                        tooltip="Edit",
                                        on_click=lambda e, idx=actual_index: self.display_edit_dialog(
                                            idx
                                        ),
                                    ),
                                    bgcolor=self.secondary_color,
                                    border_radius=8,
                                    padding=ft.padding.all(2),
                                ),
                                ft.Container(
                                    content=ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINED,
                                        icon_color=ft.Colors.WHITE,
                                        icon_size=18,
                                        tooltip="Delete",
                                        on_click=lambda e, idx=actual_index: self.delete_species_confirmation(
                                            idx
                                        ),
                                    ),
                                    bgcolor=ft.Colors.RED_400,
                                    border_radius=8,
                                    padding=ft.padding.all(2),
                                ),
                            ],
                            spacing=8,
                        )
                    ),
                ]
            )
            self.data_table.rows.append(row)

        # Show table
        self.data_table.visible = True
        self.no_data_display.visible = False
        self.no_search_results_display.visible = False
        self.page.update()

    def display_view_dialog(self, index):
        View_Dialog(self.page).view_species_dialog(
            index,
            self.__controller.get_species_data(),
            self.filtered_species,
            self.primary_color,
            self.secondary_color,
            self.accent_color,
        )

    def display_edit_dialog(self, index):
        Edit_Dialog(self.page).edit_species_dialog(
            index,
            self.__controller.get_species_data(),
            self.filtered_species,
            self.primary_color,
            self.secondary_color,
            self.accent_color,
        )

    def display_delete_dialog(self, index):
        Delete_Dialog(self.page).delete_species_confirmation(
            index,
            self.__controller.get_species_data(),
            self.filtered_species,
            self.primary_color,
            self.secondary_color,
            self.accent_color,
        )

    def show_success_dialog(self, title, message):
        """Show a professional success dialog"""
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.CHECK_CIRCLE, size=30, color=ft.Colors.WHITE
                        ),
                        bgcolor=ft.Colors.GREEN_500,
                        padding=10,
                        border_radius=50,
                    ),
                    ft.Text(title, size=20, weight=ft.FontWeight.W_700),
                ],
                spacing=15,
            ),
            content=ft.Text(message, size=14),
            actions=[
                ft.ElevatedButton(
                    "OK",
                    style=ft.ButtonStyle(
                        bgcolor=self.primary_color,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=30, vertical=12),
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                    on_click=lambda e: self.close_dialog(dialog),
                )
            ],
            actions_padding=ft.padding.all(20),
            shape=ft.RoundedRectangleBorder(radius=15),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)
        logger.write(f"Error dialog shown with message: {message}")

    def show_error_dialog(self, message):
        """Show a professional error dialog"""
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.ERROR_OUTLINE, size=30, color=ft.Colors.WHITE
                        ),
                        bgcolor=ft.Colors.RED_500,
                        padding=10,
                        border_radius=50,
                    ),
                    ft.Text("❌ Error", size=20, weight=ft.FontWeight.W_700),
                ],
                spacing=15,
            ),
            content=ft.Text(message, size=14),
            actions=[
                ft.ElevatedButton(
                    "OK",
                    style=ft.ButtonStyle(
                        bgcolor=self.primary_color,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=30, vertical=12),
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                    on_click=lambda e: self.close_dialog(dialog),
                )
            ],
            actions_padding=ft.padding.all(20),
            shape=ft.RoundedRectangleBorder(radius=15),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)

    def _create_detail_row(self, label, value, icon):
        """Helper to create a detail row with icon"""
        return ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(icon, size=18, color=ft.Colors.PRIMARY),
                        ft.Text(
                            label + ":",
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.PRIMARY,
                            width=120,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(
                    content=ft.Text(
                        value,
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.PRIMARY,
                    ),
                    expand=True,
                    padding=ft.padding.symmetric(vertical=8, horizontal=15),
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=8,
                ),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _create_form_field(self, label, value, keyboard_type, icon, icon_color):
        """Helper to create a styled form field"""
        return ft.TextField(
            value=value,
            keyboard_type=keyboard_type,
            border_radius=10,
            filled=True,
            fill_color=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_200,
            focused_border_color=self.primary_color,
            focused_bgcolor=ft.Colors.WHITE,
            text_size=14,
            content_padding=15,
            prefix_icon=ft.Icon(icon, color=icon_color, size=20),
            label=label,
            label_style=ft.TextStyle(size=13, color=self.text_secondary),
            dense=True,
        )

    def _create_professional_form_field(
        self, label, value, keyboard_type, icon_color, field_bg
    ):
        """Helper to create a professional styled form field"""
        return ft.Column(
            [
                ft.Text(
                    label,
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color=self.text_secondary,
                ),
                ft.Container(height=6),
                ft.Container(
                    content=ft.TextField(
                        value=value,
                        keyboard_type=keyboard_type,
                        border_radius=8,
                        filled=True,
                        border_color=ft.Colors.GREY_200,
                        focused_bgcolor=ft.Colors.WHITE,
                        text_size=14,
                        content_padding=ft.padding.symmetric(
                            horizontal=15, vertical=12
                        ),
                        dense=True,
                    ),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=5,
                        color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                        offset=ft.Offset(0, 2),
                    ),
                ),
            ],
            spacing=0,
        )

    def close_dialog(self, dialog):
        """Close dialog"""
        dialog.open = False
        logger.write("Dialog closed.")
        self.page.update()

    def show_dialog(self, title: str, message: str, color: ft.Colors = None):
        """Show a dialog message"""
        dialog = ft.AlertDialog(
            title=ft.Text(title, size=18, weight=ft.FontWeight.W_600),
            content=ft.Text(message, size=14),
            actions=[
                ft.ElevatedButton(
                    "OK",
                    style=ft.ButtonStyle(
                        bgcolor=self.primary_color,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=30, vertical=12),
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                    on_click=lambda e: self.close_dialog(dialog),
                )
            ],
            shape=ft.RoundedRectangleBorder(radius=15),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)

    def build(self):
        """Build the main view matching Uber Eats aesthetics"""
        # Initialize filtered species
        self.filtered_species = self.__controller.get_species_data().copy()

        # Calculate initial pagination values
        if self.filtered_species:
            total_species = len(self.filtered_species)
            start_index = min(
                (self.current_page - 1) * self.items_per_page + 1, total_species
            )
            end_index = min(self.current_page * self.items_per_page, total_species)
            self.pagination_info.value = (
                f"Showing {start_index}-{end_index} of {total_species} species"
            )
            self.pagination_info.color = ft.Colors.PRIMARY
            self.page_number_display.content.value = str(self.current_page)
            self.page_number_display.content.color = ft.Colors.PRIMARY

            # Calculate button states
            total_pages = max(
                1, (total_species + self.items_per_page - 1) // self.items_per_page
            )
            self.prev_button.disabled = self.current_page <= 1
            self.next_button.disabled = self.current_page >= total_pages
            self.prev_button.icon_color = (
                ft.Colors.GREY_400 if self.prev_button.disabled else self.primary_color
            )
            self.next_button.icon_color = (
                ft.Colors.GREY_400 if self.next_button.disabled else self.primary_color
            )
        else:
            self.pagination_info.value = "Showing 0 species"
            self.prev_button.disabled = True
            self.next_button.disabled = True
            self.prev_button.icon_color = ft.Colors.GREY_400
            self.next_button.icon_color = ft.Colors.GREY_400

        # Create the pagination row
        pagination_row = ft.Container(
            content=ft.Row(
                [
                    self.pagination_info,
                    ft.Container(expand=True),
                    ft.Row(
                        [
                            self.prev_button,
                            self.page_number_display,
                            self.next_button,
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=15, horizontal=20),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_200)),
            visible=len(self.filtered_species) > 0,
        )

        # Build the main content without calling refresh_data_table
        content = ft.Container(
            margin=ft.margin.all(20),
            padding=ft.padding.all(20),
            expand=True,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
            ),
            content=ft.Column(
                [
                    # Title Section
                    ft.Column(
                        [
                            Title_With_Icon("Modify Species", ft.Icons.EDIT_OUTLINED),
                            DescriptionText(
                                "Manage your created species. Edit or delete existing species as needed."
                            ),
                            ft.Divider(thickness=1, color=ft.Colors.GREY_200),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=25),
                    # Search Bar Row
                    ft.Row(
                        [
                            self.search_field,
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=25),
                    # Main content container
                    ft.Container(
                        content=ft.Column(
                            [
                                # Table container (scrollable)
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            self.data_table,
                                            self.no_data_display,
                                            self.no_search_results_display,
                                        ],
                                        scroll=ft.ScrollMode.ADAPTIVE,
                                    ),
                                    expand=True,
                                ),
                                # Pagination row (fixed at bottom)
                                pagination_row,
                            ],
                            spacing=0,
                        ),
                        expand=True,
                        border=ft.border.all(0.5, ft.Colors.PRIMARY),
                        border_radius=15,
                        bgcolor=ft.Colors.SECONDARY,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                        ),
                    ),
                ],
                height=min(700, self.page.window.height - 200),
                spacing=0,
            ),
        )

        # Now that the view is built, populate the table
        self.populate_initial_table()

        return content

    def populate_initial_table(self):
        """Populate the table with initial data"""
        # Apply search filter (if any)
        search_text = self.search_field.value.lower() if self.search_field.value else ""
        self.filtered_species = []

        for species in self.__controller.get_species_data():
            species_code = str(species.get("SpeciesCode", ""))
            spec_common = str(species.get("SpecCommon", ""))
            origin = species.get("Origin", "")

            if search_text:
                matches_code = search_text in species_code.lower()
                matches_common = search_text in spec_common.lower()
                matches_origin = search_text in origin.lower()

                if not (matches_code or matches_common or matches_origin):
                    continue

            self.filtered_species.append(species)

        # Check if data exists
        if not self.filtered_species:
            self.data_table.visible = False
            self.no_data_display.visible = (
                len(self.__controller.get_species_data()) == 0
            )
            self.no_search_results_display.visible = (
                len(self.__controller.get_species_data()) > 0
            )
            return

        # Get current page species
        current_page_species = self.get_paginated_species()

        # Populate table with current page species
        for index, species in enumerate(current_page_species):
            actual_index = (self.current_page - 1) * self.items_per_page + index

            species_code = str(species.get("SpeciesCode", ""))
            spec_common = str(species.get("SpecCommon", ""))
            origin = species.get("Origin", "")
            equation_type = species.get("EquationType", "Height-based")

            # Determine what to display in the SPECIES column
            # Show either SpecCommon OR SpeciesCode, not both
            if spec_common and spec_common != "" and spec_common != "None":
                species_display = spec_common  # Just show the common name
            else:
                species_display = species_code  # Show the code if no common name

            # Determine equation type color
            if equation_type == "DBH + Height-based":
                eq_color = ft.Colors.GREEN
                eq_icon = ft.Icons.TRENDING_UP
            else:
                eq_color = ft.Colors.AMBER_700
                eq_icon = ft.Icons.STRAIGHTEN

            # Create row number with correct calculation
            row_number = (self.current_page - 1) * self.items_per_page + index + 1

            row = ft.DataRow(
                cells=[
                    # Row number cell - centered
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                str(row_number),
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.PRIMARY,
                            ),
                            alignment=ft.alignment.center,
                            padding=10,
                        )
                    ),
                    # SPECIES cell - shows either common name OR code
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(
                                species_display,
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.PRIMARY,
                            ),
                            padding=10,
                        )
                    ),
                    # Origin cell
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.LOCATION_ON_OUTLINED,
                                    size=16,
                                    color=ft.Colors.PRIMARY,
                                ),
                                ft.Text(origin, size=14, color=ft.Colors.PRIMARY),
                            ],
                            spacing=8,
                        )
                    ),
                    # Equation Type cell
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.Icon(eq_icon, size=16, color=ft.Colors.PRIMARY),
                                ft.Text(
                                    equation_type, size=14, color=ft.Colors.PRIMARY
                                ),
                            ],
                            spacing=8,
                        )
                    ),
                    # Actions cell
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.IconButton(
                                        icon=ft.Icons.REMOVE_RED_EYE_OUTLINED,
                                        icon_color=ft.Colors.WHITE,
                                        icon_size=18,
                                        tooltip="View Details",
                                        on_click=lambda e, idx=actual_index: self.display_view_dialog(
                                            idx
                                        ),
                                    ),
                                    bgcolor=ft.Colors.BLUE_400,
                                    border_radius=8,
                                    padding=ft.padding.all(2),
                                ),
                                ft.Container(
                                    content=ft.IconButton(
                                        icon=ft.Icons.EDIT_OUTLINED,
                                        icon_color=ft.Colors.WHITE,
                                        icon_size=18,
                                        tooltip="Edit",
                                        on_click=lambda e, idx=actual_index: self.display_edit_dialog(
                                            idx
                                        ),
                                    ),
                                    bgcolor=self.secondary_color,
                                    border_radius=8,
                                    padding=ft.padding.all(2),
                                ),
                                ft.Container(
                                    content=ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINED,
                                        icon_color=ft.Colors.WHITE,
                                        icon_size=18,
                                        tooltip="Delete",
                                        on_click=lambda e, idx=actual_index: self.display_delete_dialog(
                                            idx
                                        ),
                                    ),
                                    bgcolor=ft.Colors.RED_400,
                                    border_radius=8,
                                    padding=ft.padding.all(2),
                                ),
                            ],
                            spacing=8,
                        )
                    ),
                ]
            )
            self.data_table.rows.append(row)

        # Show table
        self.data_table.visible = True
        self.no_data_display.visible = False
        self.no_search_results_display.visible = False
