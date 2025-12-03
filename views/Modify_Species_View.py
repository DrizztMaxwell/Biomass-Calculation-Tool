import json
import flet as ft
from widgets.TitleTextWidget import TitleTextWidget
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
from widgets.DescriptionText import DescriptionText

class Modify_Species_View:
    """CRUD interface for managing species in created_species.json"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.species_data = []
        self.current_species_index = None
        self.load_species_data()
        
        # Pagination settings
        self.current_page = 1
        self.items_per_page = 10
        self.filtered_species = []
        
        # Uber Eats inspired colors
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
            hint_text="🔍 Search species by code or origin...",
            hint_style=ft.TextStyle(size=14, color=ft.Colors.GREY_500, italic=True),
            text_size=14,
            border_color=ft.Colors.GREY_300,
            bgcolor=ft.Colors.WHITE,
            height=48,
            content_padding=ft.padding.only(left=20, right=20, top=15, bottom=15),
            border_radius=15,
            expand=True,
            filled=True,
            fill_color=ft.Colors.GREY_50,
            focused_border_color=ft.Colors.BLACK,
            focused_bgcolor=ft.Colors.WHITE,
            on_change=self.filter_species,
            suffix_icon=ft.Icon(ft.Icons.SEARCH, color=self.primary_color, size=20)
        )

        # "No Data" Message with modern design
        self.no_data_display = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(ft.Icons.AUTO_GRAPH_OUTLINED, size=60, 
                                   color=ft.Colors.with_opacity(0.3, self.primary_color)),
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.1, self.primary_color),
                    border_radius=50,
                    margin=ft.margin.only(bottom=20)
                ),
                ft.Text("No Species Created Yet", 
                       size=18, 
                       weight=ft.FontWeight.W_700, 
                       color=self.text_primary),
                ft.Text("Create your first species to get started", 
                       size=14, 
                       color=self.text_secondary,
                       text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            alignment=ft.alignment.center,
            padding=40,
            visible=False,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
            )
        )

        # "No Search Results" Message
        self.no_search_results_display = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(ft.Icons.SEARCH_OFF, size=60, 
                                   color=ft.Colors.with_opacity(0.3, ft.Colors.RED_400)),
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED_400),
                    border_radius=50,
                    margin=ft.margin.only(bottom=20)
                ),
                ft.Text("No Matching Species Found", 
                       size=18, 
                       weight=ft.FontWeight.W_700, 
                       color=self.text_primary),
                ft.Text("Try searching with a different species code or origin", 
                       size=14, 
                       color=self.text_secondary,
                       text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                ft.TextButton(
                    "Clear Search",
                    icon=ft.Icons.CLEAR,
                    on_click=lambda e: setattr(self.search_field, "value", "") or self.filter_species(e)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            alignment=ft.alignment.center,
            padding=40,
            visible=False,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
            )
        )

        # Data table with Uber Eats styling
        self.data_table = ft.DataTable(
            
            columns=[
                
                ft.DataColumn(ft.Text("ROW", 
                                     weight=ft.FontWeight.W_700, 
                                     color=self.text_primary,
                                     size=12)),
                ft.DataColumn(ft.Text("SPECIES CODE", 
                                     weight=ft.FontWeight.W_700, 
                                     color=self.text_primary,
                                     size=12)),
                ft.DataColumn(ft.Text("ORIGIN", 
                                     weight=ft.FontWeight.W_700, 
                                     color=self.text_primary,
                                     size=12)),
                ft.DataColumn(ft.Text("EQUATION TYPE", 
                                     weight=ft.FontWeight.W_700, 
                                     color=self.text_primary,
                                     size=12)),
                ft.DataColumn(ft.Text("ACTIONS", 
                                     weight=ft.FontWeight.W_700, 
                                     color=self.text_primary,
                                     size=12)),
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
            heading_text_style=ft.TextStyle(size=12, weight=ft.FontWeight.W_700, color=self.text_primary),
            
        )
        
        # Pagination controls
        self.pagination_info = ft.Text(
            "",
            size=14,
            color=self.text_secondary,
            weight=ft.FontWeight.W_500
        )
        
        self.prev_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            icon_color=ft.Colors.GREY_400,
            icon_size=24,
            tooltip="Previous Page",
            disabled=True,
            on_click=self.previous_page
        )
        
        self.next_button = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            icon_color=ft.Colors.GREY_400,
            icon_size=24,
            tooltip="Next Page",
            disabled=True,
            on_click=self.next_page
        )
        
        # Page number display
        self.page_number_display = ft.Container(
            content=ft.Text("1", 
                          size=14, 
                          weight=ft.FontWeight.W_600,
                          color=self.text_primary),
            padding=ft.padding.symmetric(horizontal=15, vertical=8),
            bgcolor=ft.Colors.with_opacity(0.1, self.primary_color),
            border_radius=8
        )
        
        # Initialize filtered species
        self.filtered_species = self.species_data.copy()

    def load_species_data(self):
        """Load species data from JSON file"""
        try:
            with open("data/create_species.json", "r") as f:
                self.species_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.species_data = []

    def save_species_data(self):
        """Save species data to JSON file"""
        try:
            with open("data/create_species.json", "w") as f:
                json.dump(self.species_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

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
                "next_color": ft.Colors.GREY_400
            }
        
        total_pages = max(1, (total_species + self.items_per_page - 1) // self.items_per_page)
        start_index = (self.current_page - 1) * self.items_per_page + 1
        end_index = min(self.current_page * self.items_per_page, total_species)
        
        return {
            "info_text": f"Showing {start_index}-{end_index} of {total_species} species",
            "current_page": self.current_page,
            "total_pages": total_pages,
            "prev_disabled": self.current_page <= 1,
            "next_disabled": self.current_page >= total_pages,
            "prev_color": ft.Colors.GREY_400 if self.current_page <= 1 else self.primary_color,
            "next_color": ft.Colors.GREY_400 if self.current_page >= total_pages else self.primary_color
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
        total_pages = max(1, (total_species + self.items_per_page - 1) // self.items_per_page)
        
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
        
        # Apply search filter
        search_text = self.search_field.value.lower() if self.search_field.value else ""
        self.filtered_species = []
        
        for species in self.species_data:
            species_code = str(species.get("SpeciesCode", ""))
            origin = species.get("Origin", "")
            
            if search_text and (search_text not in species_code.lower() and 
                               search_text not in origin.lower()):
                continue
            
            self.filtered_species.append(species)
        
        # Check if data exists
        if not self.filtered_species:
            self.data_table.visible = False
            self.no_data_display.visible = len(self.species_data) == 0
            self.no_search_results_display.visible = len(self.species_data) > 0
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
            origin = species.get("Origin", "")
            equation_type = species.get("EquationType", "Height-based")
            
            # Determine equation type color
            if equation_type == "DBH + Height-based":
                eq_color = ft.Colors.GREEN
                eq_icon = ft.Icons.TRENDING_UP
            elif equation_type == "DBH-based":
                eq_color = ft.Colors.AMBER_700
                eq_icon = ft.Icons.STRAIGHTEN
            else:
                eq_color = self.text_secondary  # Default for other types
                eq_icon = ft.Icons.FUNCTIONS
            
            # Create row number with correct calculation
            row_number = (self.current_page - 1) * self.items_per_page + index + 1
            
            row = ft.DataRow(
                cells=[
                    # Row number cell
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(str(row_number),
                                          size=14,
                                          weight=ft.FontWeight.W_600,
                                          color=self.text_primary),
                            alignment=ft.alignment.center,
                            padding=10,
                        )
                    ),
                    # Species Code cell
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(species_code, 
                                          size=14, 
                                          weight=ft.FontWeight.W_600,
                                          color=self.text_primary),
                            padding=10,
                        )
                    ),
                    # Origin cell
                    ft.DataCell(
                        ft.Row([
                            ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, 
                                   size=16, 
                                   color=self.text_secondary),
                            ft.Text(origin, size=14, color=self.text_secondary)
                        ], spacing=8)
                    ),
                    # Equation Type cell
                    ft.DataCell(
                        ft.Row([
                            ft.Icon(eq_icon, size=16, color=eq_color),
                            
                            ft.Text(equation_type, size=14, color=eq_color)
                        ], spacing=8)
                    ),
                    # Actions cell
                    ft.DataCell(
                        ft.Row([
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.REMOVE_RED_EYE_OUTLINED,
                                    icon_color=ft.Colors.WHITE,
                                    icon_size=18,
                                    tooltip="View Details",
                                    on_click=lambda e, idx=actual_index: self.view_species_dialog(idx)
                                ),
                                bgcolor=self.primary_color,
                                border_radius=8,
                                padding=ft.padding.all(2)
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    icon_color=ft.Colors.WHITE,
                                    icon_size=18,
                                    tooltip="Edit",
                                    on_click=lambda e, idx=actual_index: self.edit_species_dialog(idx)
                                ),
                                bgcolor=self.secondary_color,
                                border_radius=8,
                                padding=ft.padding.all(2)
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINED,
                                    icon_color=ft.Colors.WHITE,
                                    icon_size=18,
                                    tooltip="Delete",
                                    on_click=lambda e, idx=actual_index: self.delete_species_confirmation(idx)
                                ),
                                bgcolor=ft.Colors.RED_400,
                                border_radius=8,
                                padding=ft.padding.all(2)
                            ),
                        ], spacing=8)
                    ),
                ]
            )
            self.data_table.rows.append(row)
        
        # Show table
        self.data_table.visible = True
        self.no_data_display.visible = False
        self.no_search_results_display.visible = False

        # Update page once
        self.page.update()

    def view_species_dialog(self, index):
        """Show species details in a beautiful professional dialog"""
        
        # Placeholder for the missing utility method
        def _create_detail_row(title, value, icon):
            return ft.Row([
                ft.Icon(icon, color=self.text_secondary, size=18),
                ft.Text(title + ":", size=14, weight=ft.FontWeight.W_500, color=self.text_secondary),
                ft.Container(expand=True),
                ft.Text(str(value), size=14, weight=ft.FontWeight.W_600, color=self.text_primary),
            ], alignment=ft.MainAxisAlignment.START)
        
        # Assuming self._create_detail_row is available on the class instance.
        # If not, use the placeholder above or define it within the method if needed.
        if not hasattr(self, '_create_detail_row'):
            self._create_detail_row = _create_detail_row


        if index >= len(self.filtered_species):
            return
        
        species = self.filtered_species[index]
        
        # Calculate dialog width based on page width
        page_width = self.page.width
        dialog_width = min(700, page_width * 0.9)  # Max 700px or 90% of page width
        # Set a MAX height, but don't force it fixed on inner content
        max_dialog_height = min(650, self.page.height * 0.85)
        
        # Define a simple close function since you referenced self.close_dialog
        # If self.close_dialog exists, this is redundant but safe.
        def close_dialog(e):
            dialog.open = False
            self.page.update()

        # Header with professional gradient
        header = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, size=32, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                    padding=12,
                    border_radius=12,
                    margin=ft.margin.only(right=15)
                ),
                ft.Column([
                    ft.Text("Species Details", 
                            size=24, 
                            weight=ft.FontWeight.W_700, 
                            color=ft.Colors.WHITE),
                    ft.Text(f"Species Code: {species.get('SpeciesCode', '')}", 
                            size=14, 
                            color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE)),
                ], spacing=4, alignment=ft.CrossAxisAlignment.START)
            ], alignment=ft.MainAxisAlignment.START),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[self.primary_color, ft.Colors.BLUE_600]
            ),
            padding=ft.padding.symmetric(horizontal=30, vertical=24),
            border_radius=ft.border_radius.only(top_left=16, top_right=16),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)
            )
        )
        
        # Basic info card with better spacing
        basic_info_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, color=self.primary_color, size=20),
                    ft.Text("Basic Information", 
                            size=17, 
                            weight=ft.FontWeight.W_600, 
                            color=self.text_primary),
                ], spacing=12),
                ft.Divider(height=1, color=ft.Colors.GREY_200),
                ft.Container(height=20),
                self._create_detail_row("Species Code", str(species.get("SpeciesCode", "")), ft.Icons.TAG),
                ft.Container(height=12),
                self._create_detail_row("Origin", species.get("Origin", ""), ft.Icons.LOCATION_ON),
                ft.Container(height=12),
                self._create_detail_row("Equation Type", species.get("EquationType", "Height-based"), 
                                        ft.Icons.FUNCTIONS),
                ft.Container(height=5),
            ], spacing=0),
            padding=ft.padding.all(24),
            bgcolor=self.card_bg,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_100),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK)
            )
        )
        
        # --- Parameter Section Logic ---
        equation_params = {}
        for key, value in species.items():
            if key not in ["SpeciesCode", "Origin", "EquationType"]:
                if key.startswith("bh"):
                    category = "DBH + Height-based Parameters"
                    icon = ft.Icons.TRENDING_UP
                    color = self.secondary_color
                    icon_bg = ft.Colors.with_opacity(0.1, self.secondary_color)
                elif key.startswith("b"):
                    category = "DBH-based Parameters"
                    icon = ft.Icons.STRAIGHTEN
                    color = self.accent_color
                    icon_bg = ft.Colors.with_opacity(0.1, self.accent_color)
                else:
                    category = "Other Parameters"
                    icon = ft.Icons.TUNE
                    color = ft.Colors.PURPLE_600
                    icon_bg = ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_600)
                
                if category not in equation_params:
                    equation_params[category] = {
                        "params": [], 
                        "icon": icon, 
                        "color": color,
                        "icon_bg": icon_bg,
                    }
                equation_params[category]["params"].append((key, value))
        
        param_cards = []
        for category, data in equation_params.items():
            param_rows = ft.Column(spacing=8)
            for param_key, param_value in data["params"]:
                param_rows.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Text(param_key, 
                                                size=14, 
                                                weight=ft.FontWeight.W_500,
                                                color=self.text_secondary),
                                width=180,
                                padding=ft.padding.symmetric(vertical=10, horizontal=15)
                            ),
                            ft.VerticalDivider(width=1, color=ft.Colors.GREY_200),
                            ft.Container(
                                content=ft.Text(f"{float(param_value):.6f}", 
                                                size=14, 
                                                weight=ft.FontWeight.W_600,
                                                color=self.text_primary),
                                expand=True,
                                padding=ft.padding.symmetric(vertical=10, horizontal=15),
                                # *** FIX: Changed background to White ***
                                bgcolor=ft.Colors.GREY_50, 
                                border_radius=6
                            )
                        ], spacing=0),
                        border=ft.border.all(0.5, ft.Colors.GREY_100),
                        border_radius=6,
                        bgcolor=ft.Colors.WHITE
                    )
                )
            
            param_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Icon(data["icon"], color=data["color"], size=20),
                                bgcolor=data["icon_bg"],
                                padding=10,
                                border_radius=10,
                                margin=ft.margin.only(right=12)
                            ),
                            ft.Text(category, 
                                    size=16, 
                                    weight=ft.FontWeight.W_600, 
                                    color=data["color"]),
                        ], spacing=0),
                        ft.Container(height=18),
                        ft.Column([
                            ft.Container(
                                content=ft.Row([
                                    ft.Text("Parameter", 
                                            size=13,
                                            weight=ft.FontWeight.W_600,
                                            color=ft.Colors.GREY_600,
                                            width=180),
                                    ft.Text("Value", 
                                            size=13,
                                            weight=ft.FontWeight.W_600,
                                            color=ft.Colors.GREY_600),
                                ], spacing=0),
                                padding=ft.padding.symmetric(horizontal=15, vertical=8),
                                bgcolor=ft.Colors.GREY_50,
                                border_radius=6,
                                border=ft.border.all(0.5, ft.Colors.GREY_200)
                            ),
                            ft.Container(height=8),
                            param_rows
                        ])
                    ], spacing=0),
                    padding=24,
                    bgcolor=self.card_bg,
                    border_radius=12,
                    border=ft.border.all(1, ft.Colors.GREY_100),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=12,
                        color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK)
                    )
                )
            )
        
        # Build dialog content (The scrollable portion)
        content = ft.Container(
            content=ft.Column([
                header,
                # Scrollable Inner Content Area
                ft.Container(
                    content=ft.Column([
                        ft.Container(height=24),
                        basic_info_card,
                        ft.Container(height=24),
                        *param_cards,
                        ft.Container(height=24),
                    ], scroll=ft.ScrollMode.AUTO, spacing=0, tight=True), # Use tight=True
                    padding=ft.padding.symmetric(horizontal=30, vertical=20),
                    expand=True # Allows this inner container to take available vertical space
                )
            ], spacing=0),
            width=dialog_width,
            # *** FIX: Changed height to a max constraint, using expand=True on inner content ***
            height=max_dialog_height, 
            bgcolor=ft.Colors.WHITE,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        # Professional action buttons
        actions = ft.Container(
            content=ft.Row([
                ft.Container(expand=True),  # Spacer
                ft.ElevatedButton(
                    "Close",
                    icon=ft.Icons.CLOSE,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREY_100,
                        color=self.text_secondary,
                        padding=ft.padding.symmetric(horizontal=28, vertical=14),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        side=ft.BorderSide(1, ft.Colors.GREY_200)
                    ),
                    on_click=close_dialog # Use local close_dialog
                ),
                ft.Container(width=12),
            ], alignment=ft.MainAxisAlignment.END),
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
            bgcolor=ft.Colors.GREY_50,
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_200)),
            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)
        )
        
        # Main dialog container
        main_container = ft.Container(
            content=ft.Column([
                content,
                actions
            ], spacing=0),
            width=dialog_width,
            border_radius=16,
            # shadow=ft.BoxShadow(
            #     spread_radius=2,
            #     blur_radius=40,
            #     color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
            #     offset=ft.Offset(0, 10)
            # ),
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        # AlertDialog handles horizontal and vertical centering
        dialog = ft.AlertDialog(
            modal=True,
            content=main_container,
            content_padding=0,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.TRANSPARENT,
            # Keeping inset padding for screen safety
            inset_padding=ft.padding.symmetric(horizontal=20, vertical=40) 
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)
        self.page.update()

    def edit_species_dialog(self, index):
        """Show edit form in a beautiful professional dialog"""
        if index >= len(self.filtered_species):
            return
        
        # Find actual index in species_data
        filtered_species = self.filtered_species[index]
        actual_index = next((i for i, species in enumerate(self.species_data) 
                        if species.get("SpeciesCode") == filtered_species.get("SpeciesCode")), None)
        
        if actual_index is None:
            return
            
        species = self.species_data[actual_index]
        self.current_species_index = actual_index
        
        # Calculate dialog width based on page width
        page_width = self.page.width
        dialog_width = min(700, page_width * 0.9)
        dialog_height = min(650, self.page.height * 0.85)
        
        # Header with professional gradient
        header = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.EDIT_OUTLINED, size=32, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                    padding=12,
                    border_radius=12,
                    margin=ft.margin.only(right=15)
                ),
                ft.Column([
                    ft.Text("Edit Species", 
                        size=24, 
                        weight=ft.FontWeight.W_700, 
                        color=ft.Colors.WHITE),
                    ft.Text(f"Species Code: {species.get('SpeciesCode', '')}", 
                        size=14, 
                        color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE)),
                ], spacing=4, alignment=ft.CrossAxisAlignment.START)
            ], alignment=ft.MainAxisAlignment.START),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[self.secondary_color, ft.Colors.GREEN_500]
            ),
            padding=ft.padding.symmetric(horizontal=30, vertical=24),
            border_radius=ft.border_radius.only(top_left=16, top_right=16),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)
            )
        )
        
        # Basic info form card with professional styling
        origin_dropdown = ft.Dropdown(
            value=species.get("Origin", "Natural Stand"),
            options=[
                ft.dropdown.Option("Natural Stand"),
                ft.dropdown.Option("Plantation"),
            ],
            border_radius=10,
            filled=True,
            fill_color=ft.Colors.GREY_50,
            border_color=ft.Colors.GREY_200,
            focused_border_color=self.primary_color,
            focused_bgcolor=ft.Colors.WHITE,
            text_size=14,
            content_padding=15,
            prefix_icon=ft.Icon(ft.Icons.LOCATION_ON, color=self.text_secondary, size=20),
            hint_text="Select Origin"
        )
        
        basic_info_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, color=self.primary_color, size=20),
                    ft.Text("Basic Information", 
                        size=17, 
                        weight=ft.FontWeight.W_600, 
                        color=self.text_primary),
                ], spacing=12),
                ft.Divider(height=1, color=ft.Colors.GREY_200),
                ft.Container(height=15),
                ft.Text("Origin", size=14, weight=ft.FontWeight.W_500, color=self.text_secondary),
                origin_dropdown,
                ft.Container(height=15),
            ]),
            padding=ft.padding.all(24),
            bgcolor=self.card_bg,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_100),
        )
        
        # Parameters form with professional styling
        param_text_fields = {}  # Store TextField controls directly
        param_cards = []
        equation_params = {}
        
        for key, value in species.items():
            if key not in ["SpeciesCode", "Origin", "EquationType"]:
                if key.startswith("bh"):
                    category = "DBH + Height-based Parameters"
                    icon = ft.Icons.TRENDING_UP
                    color = self.secondary_color
                    icon_bg = ft.Colors.with_opacity(0.1, self.secondary_color)
                    field_bg = ft.Colors.with_opacity(0.05, self.secondary_color)
                elif key.startswith("b"):
                    category = "DBH-based Parameters"
                    icon = ft.Icons.STRAIGHTEN
                    color = self.accent_color
                    icon_bg = ft.Colors.with_opacity(0.1, self.accent_color)
                    field_bg = ft.Colors.with_opacity(0.05, self.accent_color)
                else:
                    category = "Other Parameters"
                    icon = ft.Icons.TUNE
                    color = ft.Colors.PURPLE_600
                    icon_bg = ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_600)
                    field_bg = ft.Colors.with_opacity(0.05, ft.Colors.PURPLE_600)
                
                if category not in equation_params:
                    equation_params[category] = {
                        "params": [], 
                        "icon": icon, 
                        "color": color,
                        "icon_bg": icon_bg,
                        "field_bg": field_bg
                    }
                equation_params[category]["params"].append((key, value))
        
        # Create param cards for EACH category in equation_params
        for category_name, category_data in equation_params.items():
            param_fields = ft.Column(spacing=12)
            
            # Process each parameter in this category
            for param_key, param_value in category_data["params"]:
                # Create TextField directly (instead of using helper method)
                text_field = ft.TextField(
                    value=str(param_value),
                    keyboard_type=ft.KeyboardType.NUMBER,
                    border_radius=8,
                    filled=True,
                    fill_color=ft.Colors.GREY_50,
                    border_color=ft.Colors.GREY_200,
                    focused_border_color=category_data["color"],
                    focused_bgcolor=ft.Colors.WHITE,
                    text_size=14,
                    content_padding=ft.padding.symmetric(horizontal=15, vertical=12),
                    dense=True
                )
                
                # Store reference to the TextField
                param_text_fields[param_key] = text_field
                
                # Create the field container
                field_container = ft.Column([
                    ft.Text(param_key, size=14, weight=ft.FontWeight.W_500, color=self.text_secondary),
                    ft.Container(height=6),
                    ft.Container(
                        content=text_field,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=5,
                            color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                            offset=ft.Offset(0, 2)
                        )
                    )
                ], spacing=0)
                
                param_fields.controls.append(field_container)
            
            # Create the category card
            param_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Icon(category_data["icon"], color=category_data["color"], size=20),
                                bgcolor=category_data["icon_bg"],
                                padding=10,
                                border_radius=10,
                                margin=ft.margin.only(right=12)
                            ),
                            ft.Text(category_name, 
                                size=16, 
                                weight=ft.FontWeight.W_600, 
                                color=category_data["color"]),
                        ], spacing=0),
                        ft.Container(height=20),
                        param_fields
                    ]),
                    padding=24,
                    bgcolor=self.card_bg,
                    border_radius=12,
                    border=ft.border.all(1, ft.Colors.GREY_100),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=12,
                        color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK)
                    )
                )
            )
        
        print(f"Total param_text_fields created: {len(param_text_fields)}")
        print(f"Keys in param_text_fields: {list(param_text_fields.keys())}")
        
        def save_changes(e):
            try:
                print("Saving changes...")
                print(f"Origin selected: {origin_dropdown.value}")
                print(f"Species_data before update: {self.species_data[self.current_species_index]}")
                print(f"Parameter text fields count: {len(param_text_fields)}")
                print(f"Parameter keys: {list(param_text_fields.keys())}")
                
                # Update basic info
                self.species_data[self.current_species_index]["Origin"] = origin_dropdown.value
                
                # Validate all parameter fields
                has_errors = False
                error_messages = []
                
                # Loop through each parameter text field
                for param_key, text_field in param_text_fields.items():
                    print(f"Processing {param_key}: {text_field.value}")
                    if text_field.value is not None and text_field.value != "":
                        try:
                            value = float(text_field.value)
                            print(f"Validating {param_key} with value {value}")
                            # Check if value is within range -5 to 5
                            if value < -5 or value > 5:
                                # Mark field with error
                                text_field.error_text = f"Value must be between -5 and 5"
                                text_field.border_color = ft.Colors.RED_500
                                text_field.update()
                                has_errors = True
                                error_messages.append(f"{param_key}: {value} is not between -5 and 5")
                                print(f"Error: {param_key} value {value} is out of range")
                            else:
                                # Clear any previous error
                                text_field.error_text = None
                                text_field.border_color = ft.Colors.GREY_200
                                text_field.update()
                                self.species_data[self.current_species_index][param_key] = value
                                print(f"Updated {param_key}: {value}")
                        except ValueError:
                            # Mark field with error
                            text_field.error_text = "Invalid number format"
                            text_field.border_color = ft.Colors.RED_500
                            text_field.update()
                            has_errors = True
                            error_messages.append(f"{param_key}: Invalid number format")
                            print(f"Warning: Invalid number for {param_key}: {text_field.value}")
                    else:
                        # Handle empty value - show error
                        text_field.error_text = "This field cannot be empty"
                        text_field.border_color = ft.Colors.RED_500
                        text_field.update()
                        has_errors = True
                        error_messages.append(f"{param_key}: Field cannot be empty")
                        print(f"Field {param_key} is empty")
                
                # If there are errors, show them and don't save
                if has_errors:
                    error_message = "Please fix the following errors:\n" + "\n".join(f"• {msg}" for msg in error_messages)
                    
                    return
                
                # All validations passed, save the data
                if self.save_species_data():
                    dialog.open = False
                    self.page.update()
                    Custom_Alert_Dialog(
                        page=self.page, 
                        title_icon=ft.Icons.CHECK_CIRCLE, 
                        title_color=ft.Colors.BLACK, 
                        title_icon_color=ft.Colors.GREEN,  
                        title="Success", 
                        message="Species updated successfully!", 
                        button_text="OK"
                    ).show()
                    self.refresh_data_table()
                else:
                    self.show_error_dialog("Failed to save changes.")
            except Exception as ex:
                self.show_error_dialog(f"Error saving species: {ex}")
                import traceback
                traceback.print_exc()
        
        # Professional action buttons
        actions = ft.Container(
            content=ft.Row([
                ft.Container(expand=True),  # Spacer
                ft.ElevatedButton(
                    "Cancel",
                    icon=ft.Icons.CLOSE,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREY_100,
                        color=self.text_secondary,
                        padding=ft.padding.symmetric(horizontal=28, vertical=14),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        side=ft.BorderSide(1, ft.Colors.GREY_200)
                    ),
                    on_click=lambda e: self.close_dialog(dialog)
                ),
                ft.Container(width=12),
                ft.ElevatedButton(
                    "Save Changes",
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    style=ft.ButtonStyle(
                        bgcolor=self.secondary_color,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=28, vertical=14),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=2,
                        shadow_color=ft.Colors.with_opacity(0.2, self.secondary_color)
                    ),
                    on_click=save_changes
                )
            ], alignment=ft.MainAxisAlignment.END),
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
            bgcolor=ft.Colors.GREY_50,
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_200)),
            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)
        )
        
        # Build dialog content
        content = ft.Container(
            content=ft.Column([
                header,
                ft.Container(
                    content=ft.Column([
                        ft.Container(height=24),
                        basic_info_card,
                        ft.Container(height=24),
                        *param_cards,
                        ft.Container(height=24),
                    ], scroll=ft.ScrollMode.AUTO, spacing=0),
                    padding=ft.padding.symmetric(horizontal=30),
                    expand=True
                )
            ], spacing=0),
            width=dialog_width,
            height=dialog_height,
            bgcolor=ft.Colors.WHITE,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        main_container = ft.Container(
            content=ft.Column([
                content,
                actions
            ], spacing=0),
            width=dialog_width,
            border_radius=16,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        dialog = ft.AlertDialog(
            modal=True,
            content=main_container,
            content_padding=0,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.TRANSPARENT,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)
        self.page.update()
    def delete_species_confirmation(self, index):
        """Show professional confirmation dialog for deletion, dynamically sized to content."""

        if index >= len(self.filtered_species):
            return
        
        species = self.filtered_species[index]
        species_code = species.get("SpeciesCode", "Unknown")
        
        # Find actual index in species_data
        # Use species_code for lookup, as 'species' object is from 'filtered_species'
        actual_index = next((i for i, sp in enumerate(self.species_data) 
                            if sp.get("SpeciesCode") == species_code), None)
        
        if actual_index is None:
            self.show_error_dialog(f"Error: Species Code {species_code} not found in master data.")
            return
        
        # Calculate dialog width
        page_width = self.page.width
        dialog_width = min(500, page_width * 0.8)
        
        def close_dialog(e):
            dialog.open = False
            self.page.update()

        def confirm_delete(e):
            close_dialog(e) # Close dialog immediately
            
            try:
                # Re-confirm index just before pop (robustness against concurrent edits)
                current_actual_index = next((i for i, sp in enumerate(self.species_data) 
                                            if sp.get("SpeciesCode") == species_code), None)

                if current_actual_index is None:
                    self.show_error_dialog(f"Species {species_code} not found just before deletion.")
                    return

                deleted_species = self.species_data.pop(current_actual_index)
                
                if self.save_species_data():
                    Custom_Alert_Dialog(page=self.page, title_icon=ft.Icons.CHECK_CIRCLE, title_color=ft.Colors.BLACK, title_icon_color=ft.Colors.GREEN,  title="Success", message=f"Species {species_code} deleted successfully!", button_text="OK").show()
                   
                    self.current_page = 1
                    self.refresh_data_table()
                else:
                    # Rollback: Re-insert species if save failed
                    self.species_data.insert(current_actual_index, deleted_species) 
                    self.show_error_dialog("Failed to save data after deleting species. Deletion canceled.")
            
            except Exception as e:
                self.show_error_dialog(f"Error deleting species: {e}")
            
            self.page.update() # Final update after operation and potentially showing success/error dialog

        # Header with warning gradient
        header = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=36, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.WHITE),
                    padding=14,
                    border_radius=14,
                    margin=ft.margin.only(right=15)
                ),
                ft.Column([
                    ft.Text("Confirm Delete", 
                            size=24, 
                            weight=ft.FontWeight.W_700, 
                            color=ft.Colors.WHITE),
                    ft.Text(f"Species Code: {species_code}", 
                            size=14, 
                            color=ft.Colors.with_opacity(0.9, ft.Colors.WHITE)),
                ], spacing=4, alignment=ft.CrossAxisAlignment.START)
            ], alignment=ft.MainAxisAlignment.START),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.Colors.RED_600, ft.Colors.RED_400]
            ),
            padding=ft.padding.symmetric(horizontal=30, vertical=24),
            border_radius=ft.border_radius.only(top_left=16, top_right=16),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)
            )
        )
        
        # Warning content block
        warning_content = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(ft.Icons.ERROR_OUTLINE, size=60, color=ft.Colors.RED_400),
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED_400),
                    border_radius=50,
                    margin=ft.margin.only(bottom=20)
                ),
                # make the **species code** bold in the text
                ft.Text(f"Are you sure you want to delete species ", 
                        size=18, 
                        weight=ft.FontWeight.W_600, 
                        color=self.text_primary,
                        text_align=ft.TextAlign.CENTER),
                 ft.Text(f"{species_code}?", 
                        size=18, 
                        weight=ft.FontWeight.BOLD, 
                        color=self.text_primary,
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                ft.Text("This action cannot be undone. All associated data will be permanently removed.", 
                        size=14, 
                        color=self.text_secondary,
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=5),
                ft.Text("⚠️ Warning: This is a destructive operation", 
                        size=13, 
                        color=ft.Colors.RED_500,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            padding=ft.padding.all(30),
            bgcolor=self.card_bg,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_100),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK)
            )
        )

        # Content container (WITHOUT fixed height)
        content_container = ft.Container(
            content=ft.Column([
                header,
                ft.Container(
                    content=ft.Column([
                        ft.Container(height=30),
                        warning_content,
                        ft.Container(height=30),
                    ], spacing=0),
                    padding=ft.padding.symmetric(horizontal=30),
                    # Removed expand=True and fixed height
                )
            ], spacing=0),
            width=dialog_width,
            bgcolor=ft.Colors.WHITE,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        # Professional action buttons
        actions = ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    "Cancel",
                    icon=ft.Icons.CLOSE,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREY_100,
                        color=self.text_secondary,
                        padding=ft.padding.symmetric(horizontal=28, vertical=14),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        side=ft.BorderSide(1, ft.Colors.GREY_200)
                    ),
                    on_click=close_dialog
                ),
                ft.Container(width=12),
                ft.ElevatedButton(
                    "Delete Species",
                    icon=ft.Icons.DELETE,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_500,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=28, vertical=14),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=2,
                        shadow_color=ft.Colors.with_opacity(0.2, ft.Colors.RED_500)
                    ),
                    on_click=confirm_delete
                )
            ], alignment=ft.MainAxisAlignment.END),
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
            bgcolor=ft.Colors.GREY_50,
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_200)),
            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)
        )
        
        # Main dialog container (WITHOUT fixed height, naturally sized by children)
        main_container = ft.Container(
            content=ft.Column([
                content_container,
                actions
            ], spacing=0, tight=True), # Use tight=True to prevent vertical expansion
            width=dialog_width,
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=40,
                color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                offset=ft.Offset(0, 10) # Keeping offset for a slight drop shadow effect
            ),
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        # AlertDialog is responsible for horizontal and vertical centering
        dialog = ft.AlertDialog(
            modal=True,
            content=main_container,
            content_padding=0,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.TRANSPARENT,
            # Using a small inset_padding prevents the dialog from hugging the edges on small screens
            inset_padding=ft.padding.all(20) 
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)
        self.page.update()

    def show_success_dialog(self, title, message):
        """Show a professional success dialog"""
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.CHECK_CIRCLE, size=30, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.GREEN_500,
                    padding=10,
                    border_radius=50
                ),
                ft.Text(title, size=20, weight=ft.FontWeight.W_700)
            ], spacing=15),
            content=ft.Text(message, size=14),
            actions=[
                ft.ElevatedButton(
                    "OK",
                    style=ft.ButtonStyle(
                        bgcolor=self.primary_color,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=30, vertical=12),
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=lambda e: self.close_dialog(dialog)
                )
            ],
            actions_padding=ft.padding.all(20),
            shape=ft.RoundedRectangleBorder(radius=15)
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)

    def show_error_dialog(self, message):
        """Show a professional error dialog"""
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.ERROR_OUTLINE, size=30, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_500,
                    padding=10,
                    border_radius=50
                ),
                ft.Text("❌ Error", size=20, weight=ft.FontWeight.W_700)
            ], spacing=15),
            content=ft.Text(message, size=14),
            actions=[
                ft.ElevatedButton(
                    "OK",
                    style=ft.ButtonStyle(
                        bgcolor=self.primary_color,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.symmetric(horizontal=30, vertical=12),
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=lambda e: self.close_dialog(dialog)
                )
            ],
            actions_padding=ft.padding.all(20),
            shape=ft.RoundedRectangleBorder(radius=15)
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)

    def _create_detail_row(self, label, value, icon):
        """Helper to create a detail row with icon"""
        return ft.Row([
            ft.Row([
                ft.Icon(icon, size=18, color=self.text_secondary),
                ft.Text(label + ":", 
                       size=14, 
                       weight=ft.FontWeight.W_500,
                       color=self.text_secondary,
                       width=120),
            ], spacing=10),
            ft.Container(
                content=ft.Text(value, 
                              size=14, 
                              weight=ft.FontWeight.W_600,
                              color=self.text_primary),
                expand=True,
                padding=ft.padding.symmetric(vertical=8, horizontal=15),
                bgcolor=ft.Colors.GREY_50,
                border_radius=8
            )
        ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)

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
            dense=True
        )

    def _create_professional_form_field(self, label, value, keyboard_type,  icon_color, field_bg):
        """Helper to create a professional styled form field"""
        return ft.Column([
            ft.Text(label, size=14, weight=ft.FontWeight.W_500, color=self.text_secondary),
            ft.Container(height=6),
            ft.Container(
                content=ft.TextField(
                    value=value,
                    keyboard_type=keyboard_type,
                    border_radius=8,
                    filled=True,
                    # fill_color=field_bg,
                    border_color=ft.Colors.GREY_200,
                    # focused_border_color=icon_color,
                    focused_bgcolor=ft.Colors.WHITE,
                    text_size=14,
                    content_padding=ft.padding.symmetric(horizontal=15, vertical=12),
                    # prefix_icon=ft.Icon(ft.Icons.CIRCLE, color=icon_color, size=16),
                    dense=True
                ),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=5,
                    color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                    offset=ft.Offset(0, 2)
                )
            )
        ], spacing=0)

    def close_dialog(self, dialog):
        """Close dialog"""
        dialog.open = False
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
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=lambda e: self.close_dialog(dialog)
                )
            ],
            shape=ft.RoundedRectangleBorder(radius=15)
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)

    def build(self):
        """Build the main view matching Uber Eats aesthetics"""
        # Initialize filtered species
        self.filtered_species = self.species_data.copy()
        
        # Calculate initial pagination values (don't call update_pagination_controls)
        if self.filtered_species:
            total_species = len(self.filtered_species)
            start_index = min((self.current_page - 1) * self.items_per_page + 1, total_species)
            end_index = min(self.current_page * self.items_per_page, total_species)
            self.pagination_info.value = f"Showing {start_index}-{end_index} of {total_species} species"
            self.page_number_display.content.value = str(self.current_page)
            
            # Calculate button states
            total_pages = max(1, (total_species + self.items_per_page - 1) // self.items_per_page)
            self.prev_button.disabled = self.current_page <= 1
            self.next_button.disabled = self.current_page >= total_pages
            self.prev_button.icon_color = ft.Colors.GREY_400 if self.prev_button.disabled else self.primary_color
            self.next_button.icon_color = ft.Colors.GREY_400 if self.next_button.disabled else self.primary_color
        else:
            self.pagination_info.value = "Showing 0 species"
            self.prev_button.disabled = True
            self.next_button.disabled = True
            self.prev_button.icon_color = ft.Colors.GREY_400
            self.next_button.icon_color = ft.Colors.GREY_400
        
        # Create the pagination row
        pagination_row = ft.Container(
            content=ft.Row([
                self.pagination_info,
                ft.Container(expand=True),  # Spacer
                ft.Row([
                    self.prev_button,
                    self.page_number_display,
                    self.next_button,
                ], spacing=10, alignment=ft.MainAxisAlignment.END)
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=15, horizontal=20),
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_200)),
            visible=len(self.filtered_species) > 0
        )
        
        # Build the main content without calling refresh_data_table
        content = ft.Container(
            margin=ft.margin.all(20),
            padding=ft.padding.all(20),
            expand=True,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)
            ),
            content=ft.Column([
                # Title Section
                ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.TUNE_OUTLINED, size=28, color=ft.Colors.BLACK),
                            TitleTextWidget("Modify Species")
                        ], spacing=15),
                        padding=ft.padding.only(bottom=10)
                    ),
                    DescriptionText("Manage your created species. Edit or delete existing species as needed."),
                    ft.Divider(thickness=1, color=ft.Colors.GREY_200)
                ], spacing=8),
                
                ft.Container(height=25),
                
                # Search Bar Row
                ft.Row([
                    self.search_field,
                ], spacing=10),
                
                ft.Container(height=25),
                
                # Main content container
                ft.Container(
                    content=ft.Column([
                        # Table container (scrollable)
                        ft.Container(
                            content=ft.Column([
                                self.data_table,
                                self.no_data_display,
                                self.no_search_results_display
                            ], scroll=ft.ScrollMode.ADAPTIVE),
                            expand=True,
                        ),
                        # Pagination row (fixed at bottom)
                        pagination_row
                    ], spacing=0),
                    expand=True,
                    border=ft.border.all(0.5, ft.Colors.GREY_200),
                    border_radius=15,
                    bgcolor=ft.Colors.WHITE,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)
                    ),
                )
            ], expand=True, spacing=0),
            
            # # Main container styling
            # bgcolor=ft.Colors.GREY_50,
            # padding=30,
            # border_radius=0,
            # expand=True
        )
        
        # Now that the view is built, populate the table
        # We'll use a small delay or call refresh_data_table after the page is loaded
        # For now, we'll populate the table directly
        self.populate_initial_table()
        
        return content
    
    def populate_initial_table(self):
        """Populate the table with initial data"""
        # Apply search filter (if any)
        search_text = self.search_field.value.lower() if self.search_field.value else ""
        self.filtered_species = []
        
        for species in self.species_data:
            species_code = str(species.get("SpeciesCode", ""))
            origin = species.get("Origin", "")
            
            if search_text and (search_text not in species_code.lower() and 
                               search_text not in origin.lower()):
                continue
            
            self.filtered_species.append(species)
        
        # Check if data exists
        if not self.filtered_species:
            self.data_table.visible = False
            self.no_data_display.visible = len(self.species_data) == 0
            self.no_search_results_display.visible = len(self.species_data) > 0
            return
        
        # Get current page species
        current_page_species = self.get_paginated_species()
        
        # Populate table with current page species
        for index, species in enumerate(current_page_species):
            # Calculate actual index in filtered_species
            actual_index = (self.current_page - 1) * self.items_per_page + index
            
            species_code = str(species.get("SpeciesCode", ""))
            origin = species.get("Origin", "")
            equation_type = species.get("EquationType", "Height-based")
            
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
                            content=ft.Text(str(row_number),
                                          size=14,
                                          weight=ft.FontWeight.W_600,
                                          color=self.text_primary),
                            alignment=ft.alignment.center,
                            padding=10,
                        )
                    ),
                    # Species Code cell
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(species_code, 
                                          size=14, 
                                          weight=ft.FontWeight.W_600,
                                          color=self.text_primary),
                            padding=10,
                        )
                    ),
                    # Origin cell
                    ft.DataCell(
                        ft.Row([
                            ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, 
                                   size=16, 
                                   color=self.text_secondary),
                            ft.Text(origin, size=14, color=self.text_secondary)
                        ], spacing=8)
                    ),
                    # Equation Type cell
                    ft.DataCell(
                        ft.Row([
                            ft.Icon(eq_icon, size=16, color=eq_color),
                            ft.Text(equation_type, size=14, color=eq_color)
                        ], spacing=8)
                    ),
                    # Actions cell
                    ft.DataCell(
                        ft.Row([
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.REMOVE_RED_EYE_OUTLINED,
                                    icon_color=ft.Colors.WHITE,
                                    icon_size=18,
                                    tooltip="View Details",
                                    on_click=lambda e, idx=actual_index: self.view_species_dialog(idx)
                                ),
                                bgcolor=self.primary_color,
                                border_radius=8,
                                padding=ft.padding.all(2)
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    icon_color=ft.Colors.WHITE,
                                    icon_size=18,
                                    tooltip="Edit",
                                    on_click=lambda e, idx=actual_index: self.edit_species_dialog(idx)
                                ),
                                bgcolor=self.secondary_color,
                                border_radius=8,
                                padding=ft.padding.all(2)
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINED,
                                    icon_color=ft.Colors.WHITE,
                                    icon_size=18,
                                    tooltip="Delete",
                                    on_click=lambda e, idx=actual_index: self.delete_species_confirmation(idx)
                                ),
                                bgcolor=ft.Colors.RED_400,
                                border_radius=8,
                                padding=ft.padding.all(2)
                            ),
                        ], spacing=8)
                    ),
                ]
            )
            self.data_table.rows.append(row)
        
        # Show table
        self.data_table.visible = True
        self.no_data_display.visible = False
        self.no_search_results_display.visible = False