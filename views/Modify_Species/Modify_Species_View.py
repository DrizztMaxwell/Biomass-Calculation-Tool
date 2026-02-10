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

# Import the new components
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
        
        # Pagination settings
        self.current_page = 1
        self.items_per_page = 10
        self.filtered_species = []

        # Color scheme
        self.primary_color = ft.Colors.BLUE_700
        self.secondary_color = ft.Colors.GREEN_600
        self.accent_color = ft.Colors.ORANGE_500
        self.bg_gradient_start = ft.Colors.WHITE
        self.bg_gradient_end = ft.Colors.BLUE_50
        self.card_bg = ft.Colors.WHITE
        self.text_primary = ft.Colors.GREY_900
        self.text_secondary = ft.Colors.GREY_600

        # Initialize components
        self.search_field = Search_Field(
            self.CONSTANTS.SEARCH_FIELD_PLACEHOLDER,
            self.filter_species
        )
        
        self.no_data_display = No_Data_Display(
            self.primary_color,
            self.text_primary,
            self.text_secondary
        )
        
        self.no_search_results_display = No_Search_Results_Display(
            self.clear_search
        )
        
        self.data_table = Species_Data_Table()
        
        self.pagination_controls = Pagination_Controls(
            self.primary_color,
            self.text_primary,
            self.text_secondary
        )
        
        # Set up pagination button callbacks
        self.pagination_controls.prev_button.on_click = self.previous_page
        self.pagination_controls.next_button.on_click = self.next_page

        # Initialize filtered species
        self.filtered_species = self.__controller.get_species_data().copy()

    def clear_search(self, e):
        """Clear search field and refresh data"""
        self.search_field.value = ""
        self.filter_species(e)

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
        """Calculate pagination information"""
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
        self.pagination_controls.update_pagination(
            pagination_info["info_text"],
            pagination_info["current_page"],
            pagination_info["prev_disabled"],
            pagination_info["next_disabled"],
            pagination_info["prev_color"],
            pagination_info["next_color"]
        )
        self.pagination_controls.visible = len(self.filtered_species) > 0

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

    def create_table_row(self, species, index, actual_index):
        """Create a single table row for the species"""
        species_code = str(species.get("SpeciesCode", ""))
        spec_common = str(species.get("SpecCommon", ""))
        origin = species.get("Origin", "")
        equation_type = species.get("EquationType", "Height-based")

        # Determine what to display in the SPECIES column
        if spec_common and spec_common != "" and spec_common != "None":
            species_display = spec_common
        else:
            species_display = species_code

        # Determine equation type color and icon
        if equation_type == "DBH + Height-based":
            eq_color = ft.Colors.GREEN
            eq_icon = ft.Icons.TRENDING_UP
        elif equation_type == "DBH-based":
            eq_color = ft.Colors.AMBER_700
            eq_icon = ft.Icons.STRAIGHTEN
        else:
            eq_color = self.text_secondary
            eq_icon = ft.Icons.FUNCTIONS

        # Create action buttons
        action_buttons = Action_Buttons(
            actual_index,
            self.display_view_dialog,
            self.display_edit_dialog,
            self.display_delete_dialog,
            self.primary_color,
            self.secondary_color
        )

        # Calculate row number
        row_number = (self.current_page - 1) * self.items_per_page + index + 1

        return ft.DataRow(
            cells=[
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
                ft.DataCell(
                    ft.Row(
                        [
                            ft.Icon(eq_icon, size=16, color=eq_color),
                            ft.Text(equation_type, size=14, color=eq_color),
                        ],
                        spacing=8,
                    )
                ),
                ft.DataCell(action_buttons),
            ]
        )

    def refresh_data_table(self):
        """Refresh the data table with current species data"""
        # Clear existing rows
        self.data_table.rows.clear()

        # Apply search filter
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
            self.pagination_controls.visible = False
            self.page.update()
            return

        # Show pagination controls
        self.pagination_controls.visible = True
        self.update_pagination_controls()

        # Get current page species
        current_page_species = self.get_paginated_species()

        # Populate table with current page species
        for index, species in enumerate(current_page_species):
            actual_index = (self.current_page - 1) * self.items_per_page + index
            row = self.create_table_row(species, index, actual_index)
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
            index=index,
            filtered_species=self.filtered_species, # The list being viewed
            species_data=self.__controller.get_species_data(), # The master list
            controller=self.__controller, # THIS WAS MISSING/MISPLACED
            primary_color=self.primary_color,
            secondary_color=self.secondary_color,
            accent_color=self.accent_color,
            refresh_callback=self.refresh_data_table, # Highly recommended to pass this
            save_callback=self.__controller.save_species_data # Or whatever your save method is
        )

    def display_delete_dialog(self, index):
        # Inside Modify_Species_View class

    # 1. Get the current data from the controller
        master_data = self.__controller.get_species_data()
        
        # 2. Initialize the Dialog with page and controller
        delete_utility = Delete_Dialog(self.page, self.__controller)
        
        # 3. Call the confirmation with the correct parameter order
        delete_utility.delete_species_confirmation(
            index=index,
            filtered_species=self.filtered_species,
            species_data=master_data,
            controller=self.__controller,
            text_secondary=self.text_secondary,
            refresh_callback=self.refresh_data_table, # Refresh table after delete
            save_callback=self.__controller.save_species_data # Pass the actual save function
        )

    # ... (keep the dialog methods and helper methods as they are)

    def build(self):
        """Build the main view matching Uber Eats aesthetics"""
        # Initialize filtered species
        self.filtered_species = self.__controller.get_species_data().copy()

        # Build the main content
        content = ft.Container(
            margin=ft.margin.all(20),
            padding=ft.padding.all(30),
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
                    ft.Row([self.search_field], spacing=10),
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
                                    alignment=ft.alignment.center,
                                    padding=ft.padding.all(10),
                                    
                                    expand=True,
                                ),
                                # Pagination controls
                                self.pagination_controls,
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

        # Populate the table with initial data
        self.populate_initial_table()

        return content

    def populate_initial_table(self):
        """Populate the table with initial data"""
        self.refresh_data_table()