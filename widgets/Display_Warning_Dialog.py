import flet as ft
import numpy as np
import pandas as pd
from widgets.Warning_Dialog_Header import Warning_Dialog_Header

class Display_Warning_Dialog:
    """Utility class to build and return a complex warning Container that mimics a modal dialog."""

    def __init__(self, page: ft.Page, error_messages, error_message_for_out_of_bounds_dbh_or_height_value):
        self.error_messages = error_messages
        print("ERORR")
        print(error_messages)
        self.dialog = None 
        self.page = page
        self.error_message_for_out_of_bounds_dbh_or_height_value = error_message_for_out_of_bounds_dbh_or_height_value
        self.current_page_validation = 0
        self.current_page_measurement = 0
        self.rows_per_page = 20
        
        # Store references to the tab containers so we can update them
        self.validation_tab_container = None
        self.measurement_tab_container = None
        self.tabs_control = None
        
        
    def close_dialog(self, e):
        """Removes the custom container from the page to dismiss the 'modal' effect."""
        if self.dialog and self.dialog in self.page.overlay:
            self.page.overlay.remove(self.dialog)
            self.page.update()
        
    def _convert_row_data_to_lowercase(self, row_data):
        """Convert all keys in row_data to lowercase for case-insensitive access"""
        return {str(key).lower(): value for key, value in row_data.items()}
        
  
    
    def _create_table_row(self, error_data, is_tree_measurement_tab: bool):
        """Create a table row for an error entry with improved styling"""
        row_data_lower = self._convert_row_data_to_lowercase(error_data['row_data'])
        print(f"{error_data} ")
        nan_columns_lower = [col.lower() for col in error_data.get('nan_columns', [])]
        
        # Helper function to create styled text cells with better visual hierarchy
        def create_cell(value, is_error=False, column_name=None, row_data_lower=None, nan_columns_lower=None):
    
            # Determine if the value should be displayed as an error
            should_display_error = is_error
            
            if value is None or (isinstance(value, float) and np.isnan(value)):
                # Check for Python None or numpy.nan (float('nan'))
                display_value = "ERROR"  # Display 'ERROR' for None/NaN
                should_display_error = True  # Treat missing values as errors
            else:
                display_value = str(value)
                
                # Additional validation checks based on column type
                if column_name and row_data_lower is not None:
                    try:
                        if column_name == 'year':
                            # Year validation: should be integer and reasonable year
                            year_val = int(float(value))
                            if year_val < 1900 or year_val > 2100:
                                should_display_error = True
                                
                        elif column_name == 'tree number':
                            # Tree number validation: should be positive integer
                            tree_num = int(float(value))
                            if tree_num <= 0:
                                should_display_error = True
                                
                        elif column_name == 'speccode':
                            # SpecCode validation: should be integer
                            spec_val = float(value)
                            if spec_val != int(spec_val):  # Check if it's not a whole number
                                should_display_error = True
                                
                        elif column_name == 'dbh':
                            # DBH validation: should be numeric and within range
                            dbh_val = float(value)
                            if dbh_val < 2.5 or dbh_val > 100.0:
                                should_display_error = True
                                
                        elif column_name == 'height':
                            # Height validation: should be numeric and within range
                            height_val = float(value)
                            if height_val < 1.3 or height_val > 50.0:
                                should_display_error = True
                                
                    except (ValueError, TypeError):
                        # If conversion fails, it's a data type error
                        should_display_error = True
            
            return ft.DataCell(
                ft.Container(
                    content=ft.Text(
                        display_value,
                        size=12,
                        color=ft.Colors.RED_600 if should_display_error else ft.Colors.GREY_800,
                        weight=ft.FontWeight.W_500 if should_display_error else ft.FontWeight.NORMAL,
                    ),
                    padding=ft.padding.symmetric(horizontal=8, vertical=6),
                    # Optional: Add background color for errors to make them stand out more
                    bgcolor=ft.Colors.RED_50 if should_display_error else ft.Colors.TRANSPARENT,
                    border_radius=4 if should_display_error else 0,
                )
            )
        
        # Common cells for both tabs - Plot, Year, SpecCode, Tree Number, DBH, Height
        cells = [
    # Row Index
    create_cell(error_data['index'] + 1, is_error=False), 
    create_cell(row_data_lower.get('plot', None), 'plot' in nan_columns_lower, 'plot', row_data_lower, nan_columns_lower),
    create_cell(row_data_lower.get('year', None), 'year' in nan_columns_lower, 'year', row_data_lower, nan_columns_lower),
    create_cell(row_data_lower.get('species', None), 'species' in nan_columns_lower, 'species', row_data_lower, nan_columns_lower),
    create_cell(row_data_lower.get('tree number', None), 'tree number' in nan_columns_lower, 'tree number', row_data_lower, nan_columns_lower),
    create_cell(row_data_lower.get('dbh', None), 'dbh' in nan_columns_lower, 'dbh', row_data_lower, nan_columns_lower),
    create_cell(row_data_lower.get('height', None), 'height' in nan_columns_lower, 'height', row_data_lower, nan_columns_lower),
]
        if is_tree_measurement_tab:
            # For tree measurement errors, add Issue cell
            dbh_value = row_data_lower.get('dbh')
            height_value = row_data_lower.get('height')
            
            # Determine the issue
            issues = []
            
            # Check for missing values first
            if dbh_value is None or (isinstance(dbh_value, float) and np.isnan(dbh_value)):
                issues.append("Missing DBH")
            else:
                try:
                    dbh_float = float(dbh_value)
                    if dbh_float < 2.5 or dbh_float > 100.0:
                        issues.append("DBH out of bounds")
                except (ValueError, TypeError):
                    issues.append("Invalid DBH format")

            if height_value is None or (isinstance(height_value, float) and np.isnan(height_value)):
                issues.append("Missing Height")
            else:
                try:
                    height_float = float(height_value)
                    if height_float < 1.3 or height_float > 50.0:
                        issues.append("Height out of bounds")
                except (ValueError, TypeError):
                    issues.append("Invalid Height format")

            
            issue_text = ", ".join(issues) if issues else "Measurement error"
            cells.append(ft.DataCell(
                ft.Container(
                    content=ft.Text(issue_text, size=12, color=ft.Colors.RED_600, weight=ft.FontWeight.W_500),
                    padding=ft.padding.symmetric(horizontal=8, vertical=6),
                    bgcolor=ft.Colors.RED_50 if issues else ft.Colors.TRANSPARENT,
                    border_radius=4,
                )
            ))
        
        # Add alternating row colors for better readability
        row_color = ft.Colors.WHITE 
        return ft.DataRow(
            color=row_color,
            cells=cells
        )
    def _get_paginated_data(self, error_list, current_page):
        """Get the current page's data and pagination info"""
        total_rows = len(error_list)
        total_pages = max(1, (total_rows + self.rows_per_page - 1) // self.rows_per_page)  # Ceiling division
        
        start_idx = current_page * self.rows_per_page
        end_idx = min(start_idx + self.rows_per_page, total_rows)
        
        paginated_data = error_list[start_idx:end_idx]
        
        return paginated_data, total_rows, total_pages, current_page + 1
    
    def _create_pagination_controls(self, total_pages, current_page, on_previous, on_next):
        """Create pagination controls with page info and navigation buttons"""
        return ft.Container(
            margin=ft.margin.only(top=12),
            bgcolor=ft.Colors.SECONDARY,
            content=ft.Row(
                [
                    # Page info
                    ft.Text(
                        f"Page {current_page} of {total_pages}",
                        size=12,
                        color=ft.Colors.PRIMARY,
                        
                        weight=ft.FontWeight.W_500,
                    ),
                    
                    # Spacer
                    ft.Container(expand=True),
                    
                    # Navigation buttons
                    ft.OutlinedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.ARROW_BACK, size=16),
                                ft.Text("Previous", size=12),
                            ],
                            spacing=8,
                        ),
                        on_click=on_previous,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                        ),
                        disabled=current_page <= 1,
                    ),
                    
                    ft.OutlinedButton(
                        content=ft.Row(
                            [
                                ft.Text("Next", size=12),
                                ft.Icon(ft.Icons.ARROW_FORWARD, size=16),
                            ],
                            spacing=8,
                        ),
                        on_click=on_next,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(horizontal=16, vertical=8),
                        ),
                        disabled=current_page >= total_pages,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=12, horizontal=16),
            border_radius=8,
        )
        
    def _create_error_table(self, error_list, is_tree_measurement_tab: bool, page_type: str):
        """
        Create a table view for errors with pagination and horizontal/vertical scrolling.
        """
        if not error_list:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINED, size=48, color=ft.Colors.GREEN_400),
                        ft.Text("No errors found", size=18, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=16,
                ),
                padding=40,
                alignment=ft.alignment.center,
                expand=True,
            )
        
        # Get current page based on page_type
        if page_type == "validation":
            current_page = self.current_page_validation
        else:
            current_page = self.current_page_measurement
            
        # Get paginated data
        paginated_data, total_rows, total_pages, current_page_display = self._get_paginated_data(
            error_list, current_page
        )
        
        # Create callback functions for pagination
        def go_previous(e):
            if page_type == "validation":
                if self.current_page_validation > 0:
                    self.current_page_validation -= 1
            else:
                if self.current_page_measurement > 0:
                    self.current_page_measurement -= 1
            self._refresh_current_tab()
        
        def go_next(e):
            if page_type == "validation":
                if self.current_page_validation < total_pages - 1:
                    self.current_page_validation += 1
            else:
                if self.current_page_measurement < total_pages - 1:
                    self.current_page_measurement += 1
            self._refresh_current_tab()
        
        # ONLY populate data rows
        table_rows = [] 
        for error_data in paginated_data:
            table_rows.append(self._create_table_row(error_data, is_tree_measurement_tab))
        
        # Create table columns - same for both tabs except for Issue column
        columns = [
            ft.DataColumn(ft.Text("Row", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE)), # Added White color
            ft.DataColumn(ft.Text("Plot", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE)), # Added White color
            ft.DataColumn(ft.Text("Year", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE)), # Added White color
            ft.DataColumn(ft.Text("Species", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE)), # Added White color
            ft.DataColumn(ft.Text("Tree Number", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE)), # Added White color
            ft.DataColumn(ft.Text("DBH", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE)), # Added White color
            ft.DataColumn(ft.Text("Height", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE)), # Added White color
        ]
        
        if is_tree_measurement_tab:
            columns.append(ft.DataColumn(ft.Text("Issue", weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE))) # Added White color
        
        # Create a container for the DataTable with horizontal and vertical scrolling
        # Vertical Scrolling Fix: The outer Container needs a fixed height or max_height
        # to constrain the DataTable's vertical expansion and enable scrolling.
        # We'll use expand=True here, and rely on the main content panel's dimensions
        # to constrain it, then wrap the DataTable to handle scrolling.
        table_container = ft.Container(
            # 1. Outer Container sets the fixed height boundary
            # height=900, 
            
            margin=ft.margin.symmetric(horizontal=8),
            # expand=True,
           
            content=ft.Column(
                # 2. ft.Column handles Vertical Scrolling (to see more rows)
                controls=[
                    ft.Row( 
                        # 3. ft.Row handles Horizontal Scrolling (to see more columns)
                        controls=[
                            ft.DataTable(
                                columns=columns,
                                rows=table_rows,
                                vertical_lines=ft.BorderSide(1, ft.Colors.GREY_300),
                                horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_200),
                                heading_row_height=45,
                                data_row_min_height=42,
                                data_row_max_height=42,
                                column_spacing=12,
                                divider_thickness=1,
                                heading_row_color=ft.Colors.GREEN_700,
                                sort_column_index=0,
                                show_checkbox_column=False,
                                expand=True,  # Allows DataTable to stretch horizontally within the Row
                            )
                        ],
                        scroll=ft.ScrollMode.ADAPTIVE, # Horizontal Scrolling
                        expand=True,
                    ),
                ],
                scroll=ft.ScrollMode.ADAPTIVE, # Vertical Scrolling
                # The ft.Column does not need expand=True here, as its height is constrained by the parent Container's height.
                spacing=0, # Remove default spacing for cleaner table layout
            ),
        )
        
        return ft.Container(
           
            content=ft.Column(
                controls=[
                    # Results count - Bug Fix: Removed extraneous data that caused "Showing x of x 31 errors"
                    ft.Container(
                        content=ft.Text(
                            f"Showing {len(paginated_data)} of {total_rows} errors",
                            size=12,
                            color=ft.Colors.GREY_600,
                            weight=ft.FontWeight.W_500,
                        ),
                        # ADDED PADDING HERE:
                        padding=ft.padding.symmetric(horizontal=16, vertical=8),
                        alignment=ft.alignment.center_left,
                    ),
                    
                    # Table with horizontal/vertical scrolling - expanded
                    ft.Container(
                        content=table_container,
                        width=1000,
                        expand=True,  # Expand to fill available space
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                        alignment=ft.alignment.center,
                        # REMOVED scroll=ft.ScrollMode.ADAPTIVE here, it's inside table_container
                    ),
                    
                    # Pagination controls
                    self._create_pagination_controls(total_pages, current_page_display, go_previous, go_next),
                ],
                expand=True,  # Expand to fill available space
                spacing=8,                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            ),
            # ADDED PADDING HERE:
                        alignment=ft.alignment.center,
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
            padding=ft.padding.all(8),
        )

    def _refresh_current_tab(self):
        """Refresh only the currently visible tab"""
        if not self.tabs_control:
            return
            
        current_tab_index = self.tabs_control.selected_index
        
        # Ensure tabs list is accessible
        if not self.tabs_control.tabs:
            return

        if current_tab_index == 0:  # Validation Errors tab
            # Rebuild validation tab content
            new_validation_content = self._create_error_table(
                self.error_messages, 
                is_tree_measurement_tab=False,
                page_type="validation"
            )
            # Find the existing container for validation content and update its content
            if self.tabs_control.tabs[0].content:
                self.tabs_control.tabs[0].content.content = new_validation_content
            # NOTE: If the inner padding was removed from the validation tab content container in show_dialog, 
            # you need to ensure new_validation_content handles its own padding. (It does.)
            
        else:  # Tree Measurement Errors tab
            # Rebuild measurement tab content
            new_measurement_content = self._create_error_table(
                self.error_message_for_out_of_bounds_dbh_or_height_value, 
                is_tree_measurement_tab=True,
                page_type="measurement"
            )
            
            # Rebuild the entire measurement tab's Column content
            measurement_column = ft.Column(
                controls=[
                    # Informational banner
                    ft.Container(
                        padding=ft.padding.all(16),
                        # ADJUSTED MARGIN HERE:
                        margin=ft.margin.only(bottom=8, left=8, right=8),
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=12,
                        border=ft.border.all(1, ft.Colors.BLUE_200),
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.BLUE_600, size=20),
                                ft.Text(
                                    "Height must be (1.3 ≤ x ≤ 50.0), DBH must be (2.5 ≤ x ≤ 100.0)", 
                                    size=14, 
                                    weight=ft.FontWeight.W_500, 
                                    color=ft.Colors.BLUE_800
                                ),
                            ],
                            spacing=12,
                        ),
                    ),
                    # Table content
                    ft.Container(
                        content=new_measurement_content,
                        expand=True,  # Expand to fill available space
                        # REMOVED INNER PADDING/MARGIN HERE to let _create_error_table manage it
                    )
                ],
                expand=True,  # Expand to fill available space
                spacing=0,
            )
            
            self.tabs_control.tabs[1].content = measurement_column
        
        self.tabs_control.update() # Update the tabs control to reflect content changes
        self.page.update()

    def display_error_card_for_tree_measurements_information(self):
        """Displays errors for out-of-bounds DBH/Height values in table format."""
        return self._create_error_table(
            self.error_message_for_out_of_bounds_dbh_or_height_value, 
            is_tree_measurement_tab=True,
            page_type="measurement"
        )
        
    def display_error_card_for_validation_information(self):
        """Displays general validation errors in table format."""
        return self._create_error_table(
            self.error_messages, 
            is_tree_measurement_tab=False,
            page_type="validation"
        )
        
    def __del__(self):
        pass  
        
    def show_dialog(self):
        """
        Builds and returns a centered, blackened-out Container to mimic a modal dialog.
        The calling function must add this container to page.controls.
        """
        
        # Reset pagination when showing dialog
        self.current_page_validation = 0
        self.current_page_measurement = 0
        
        # Determine the initial tab index
        initial_tab_index = 0
        if len(self.error_message_for_out_of_bounds_dbh_or_height_value) > 0 and \
           (len(self.error_messages) == 0 or len(self.error_message_for_out_of_bounds_dbh_or_height_value) > len(self.error_messages)):
            initial_tab_index = 1
            
        header = Warning_Dialog_Header(self.error_messages, self.error_message_for_out_of_bounds_dbh_or_height_value) 
        
        # --- Content inside the central panel ---
        
        # 1. Validation Tab Content
        validation_tab_content = ft.Container(
            
            content=self.display_error_card_for_validation_information(),
            # ADDED PADDING around the validation table content:
            padding=ft.padding.all(16), 
            expand=True,
        )

        # 2. Measurement Tab Content (Complex Column)
        measurement_tab_content_column = ft.Column(
            controls=[
                # Informational banner
                ft.Container(
                    padding=ft.padding.all(16),
                    # ADDED MARGIN HERE to separate from tab edges:
                    margin=ft.margin.only(top=16, left=16, right=16, bottom=8),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=12,
                    border=ft.border.all(1, ft.Colors.BLUE_200),
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.BLUE_600, size=20),
                            ft.Text(
                                "Height must be (1.3 ≤ x ≤ 50.0), DBH must be (2.5 ≤ x ≤ 100.0)", 
                                size=14, 
                                weight=ft.FontWeight.W_500, 
                                color=ft.Colors.BLUE_800
                            ),
                        ],
                        spacing=12,
                    ),
                ),
                # Table content
                ft.Container(
                    content=self.display_error_card_for_tree_measurements_information(),
                    expand=True,
                    # ADDED PADDING AROUND TABLE HERE:
                    padding=ft.padding.only(left=8, right=8, bottom=8), 
                )
            ],
            expand=True,
            spacing=0,
        )
        
        self.tabs_control = ft.Tabs(
            selected_index=initial_tab_index,
            animation_duration=300,
            divider_color=ft.Colors.GREY_300,
            indicator_color=ft.Colors.GREEN_600,
            label_color=ft.Colors.GREEN_600,
            unselected_label_color=ft.Colors.GREY_600,
            tabs=[
                ft.Tab(
                    text="Validation Errors",
                    icon=ft.Icons.WARNING_AMBER_ROUNDED,
                    content=validation_tab_content,
                ),
                ft.Tab(
                    text="Tree Measurement Errors",
                    icon=ft.Icons.NATURE_PEOPLE_ROUNDED,
                    content=measurement_tab_content_column,
                ),
            ],
            expand=True,  # Make tabs expand
        )
        
        # Main content container (the white panel that holds the errors)
        main_content_panel = ft.Container(
            content=ft.Column(
                controls=[
                    header,
                    ft.Container(
                        content=self.tabs_control,
                        expand=True,  # Expand to fill available space
                        bgcolor=ft.Colors.SECONDARY_CONTAINER,
                        # REMOVED INNER PADDING HERE as it's added to the tab contents now
                        border_radius=ft.border_radius.only(top_left=12, top_right=12),
                    ),
                    # Action buttons with improved styling
                    ft.Container(
                        
                        content=ft.Row(
                            [
                                ft.OutlinedButton(
                                    
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.CLOSE_ROUNDED, size=20, color=ft.Colors.WHITE),
                                            ft.Text("Close", color=ft.Colors.WHITE, weight=ft.FontWeight.W_600),
                                        ],
                                        spacing=10,
                                    ),
                                    on_click=self.close_dialog, 
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(horizontal=28, vertical=16),
                                
                                bgcolor=ft.Colors.TERTIARY,
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        side=ft.BorderSide(2, ft.Colors.GREY_300),
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            
                        ),
                        # ADDED PADDING HERE:
                        padding=ft.padding.all(20),
                        bgcolor=ft.Colors.SECONDARY,
                        border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16), # Increased radius for consistency
                        border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_200))
                ,
                    )
                ],
                spacing=0,
                expand=True,
                
               
            ),
            # Vertical Scrolling Fix: Removed fixed height to allow inner column to expand
            # and push content correctly, relying on the overall dialog height.
           
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
                offset=ft.Offset(0, 4),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
        )

        # --- Full-page, blackened-out container with padding ---
        self.dialog = ft.Container(
            content=ft.Container(
                content=main_content_panel,
                # Margin already exists here:
                margin=ft.margin.all(40),
            ),
            # Blackened out background with subtle gradient
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                    ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
                ]
            ),
            # Center the content panel
            alignment=ft.alignment.center,
            # Ensure it covers the whole page/view
            expand=True,
            # Padding already exists here:
            padding=ft.padding.all(20),
        )
        
        return self.dialog