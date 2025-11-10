import flet as ft
import pandas as pd
from widgets.Create_Section_Buttons import Create_Section_Buttons
from widgets.Warning_Dialog_Display_Errors_Header import Warning_Dialog_Display_Errors_Header
from widgets.Warning_Dialog_Header import Warning_Dialog_Header

class Display_Warning_Dialog:
    def __init__(self, page: ft.Page, error_messages, error_message_for_out_of_bounds_dbh_or_height_value):
        self.error_messages = error_messages
        self.dialog = None
        self.page = page
        self.current_view = "all"  # "all" or "tree_measurements"
        self.error_message_for_out_of_bounds_dbh_or_height_value = error_message_for_out_of_bounds_dbh_or_height_value
        print(self.error_message_for_out_of_bounds_dbh_or_height_value)
        
    def display_error_card_for_tree_measurements_information(self):
        issue_counter = 0
        error_cards = []
        
        # Helper function to create a bold label + value row
        def create_detail_row(label, value, value_color=ft.Colors.GREY_800):
            return ft.Row(
                spacing=4,
                controls=[
                    # Bold Label
                    ft.Text(f"{label}:", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                    # Regular Value (with optional conditional color)
                    ft.Text(f"{value}", size=12, color=value_color),
                ]
            )

        # Loop through all error messages
        for error_data in self.error_message_for_out_of_bounds_dbh_or_height_value:
            print(f"Index: {error_data['index']}")
            print(f"Row data: {error_data['row_data']}")
            print(f"NaN columns: {error_data['nan_columns']}")
            
            # Determine the colors for DBH and Height based on nan_columns (same as before)
            dbh_color = ft.Colors.RED_600 if 'DBH' in error_data['nan_columns'] else ft.Colors.GREY_800
            height_color = ft.Colors.RED_600 if 'Height' in error_data['nan_columns'] else ft.Colors.GREY_800
            species_color = ft.Colors.RED_600 if 'SpecCode' in error_data['nan_columns'] else ft.Colors.GREY_800
            plot_color = ft.Colors.RED_600 if 'Plot' in error_data['nan_columns'] else ft.Colors.GREY_800
            tree_color = ft.Colors.RED_600 if 'Tree Number' in error_data['nan_columns'] else ft.Colors.GREY_800
            year_color = ft.Colors.RED_600 if 'Year' in error_data['nan_columns'] else ft.Colors.GREY_800
            origin_color = ft.Colors.RED_600 if 'Origin' in error_data['nan_columns'] else ft.Colors.GREY_800
            tree_status_color = ft.Colors.RED_600 if 'Tree Status' in error_data['nan_columns'] else ft.Colors.GREY_800
            

            # Create a card for each error
            error_card = ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=20,
                margin=ft.margin.only(bottom=15),
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=12,
                content=ft.Column(
                    spacing=8,
                    controls=[
                        # Issue header
                        ft.Text(f"Issue #{issue_counter + 1}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        ft.Text("The following tree measurement values are out of bounds:", size=12, color=ft.Colors.GREY_600),
                        
                        # Row information (using the helper function)
                        create_detail_row("Row Index", error_data['index'] + 1),
                        
                     
                        
                        # Additional row data
                        create_detail_row("Plot", error_data['row_data']['Plot'], plot_color),
                        create_detail_row("Year", error_data['row_data']['Year'], year_color),
                        create_detail_row("Origin", error_data['row_data']['Origin'], origin_color),
                        create_detail_row("Tree Status", error_data['row_data']['Tree Status'], tree_status_color),
                        create_detail_row("SpecCode", error_data['row_data']['SpecCode'], species_color),
                        create_detail_row("Tree Number", error_data['row_data']['Tree Number'], tree_color),
                        create_detail_row("DBH", error_data['row_data']['DBH'], dbh_color),
                        create_detail_row("Height", error_data['row_data']['Height'], height_color),
                        
                    ]
                )
            )
            
            error_cards.append(error_card)
            issue_counter += 1
        
        # Return a scrollable container with all error cards
        return ft.Container(
            expand=True,
            content=ft.ListView(
                controls=error_cards,
                spacing=10,
                padding=20,
                auto_scroll=False,
            )
        )
        
        
    def display_error_card_for_validation_information(self):
        issue_counter = 0
        error_cards = []
        
        # Helper function to create a bold label + value row
        def create_detail_row(label, value, value_color=ft.Colors.GREY_800):
            return ft.Row(
                spacing=4,
                controls=[
                    # Bold Label
                    ft.Text(f"{label}:", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                    # Regular Value (with optional conditional color)
                    ft.Text(f"{value}", size=12, color=value_color),
                ]
            )

        # Loop through all error messages
        for error_data in self.error_messages:
            print(f"Index: {error_data['index']}")
            print(f"Row data: {error_data['row_data']}")
            print(f"NaN columns: {error_data['nan_columns']}")
            
            # Determine the colors for DBH and Height based on nan_columns (same as before)
            dbh_color = ft.Colors.RED_600 if 'DBH' in error_data['nan_columns'] else ft.Colors.GREY_800
            height_color = ft.Colors.RED_600 if 'Height' in error_data['nan_columns'] else ft.Colors.GREY_800
            plot_color = ft.Colors.RED_600 if 'Plot' in error_data['nan_columns'] else ft.Colors.GREY_800
            species_color = ft.Colors.RED_600 if 'SpecCode' in error_data['nan_columns'] else ft.Colors.GREY_800
            year_color = ft.Colors.RED_600 if 'Year' in error_data['nan_columns'] else ft.Colors.GREY_800
            tree_status_color = ft.Colors.RED_600 if 'Tree Status' in error_data['nan_columns'] else ft.Colors.GREY_800
            origin_color = ft.Colors.RED_600 if 'Origin' in error_data['nan_columns'] else ft.Colors.GREY_800
            tree_color = ft.Colors.RED_600 if 'Tree Number' in error_data['nan_columns'] else ft.Colors.GREY_800

            # Create a card for each error
            error_card = ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=20,
                margin=ft.margin.only(bottom=15),
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=12,
                content=ft.Column(
                    spacing=8,
                    controls=[
                        # Issue header
                        ft.Text(f"Issue #{issue_counter + 1}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        ft.Text("The following tree measurement values are out of bounds:", size=12, color=ft.Colors.GREY_600),
                        
                        # Row information (using the helper function)
                        create_detail_row("Row Index", error_data['index'] + 1),
                        
                        #Plot Subplot Year Origin TreeStatus Species Tree DBH Height
                        create_detail_row("Plot", error_data['row_data']['Plot'], plot_color),
                        create_detail_row("Year", error_data['row_data']['Year'], year_color),
                        create_detail_row("Origin", error_data['row_data']['Origin'], origin_color),
                        create_detail_row("Tree Status", error_data['row_data']['Tree Status'], tree_status_color),
                        create_detail_row("SpecCode", error_data['row_data']['SpecCode'], species_color),
                        create_detail_row("Tree Number", error_data['row_data']['Tree Number'], tree_color ),
                        create_detail_row("DBH", error_data['row_data']['DBH'], dbh_color),
                        create_detail_row("Height", error_data['row_data']['Height'], height_color),
                        

                    
                    ]
                )
            )
            
            error_cards.append(error_card)
            issue_counter += 1
        
        # Return a scrollable container with all error cards
        return ft.Container(
            expand=True,
            content=ft.ListView(
                controls=error_cards,
                spacing=10,
                padding=20,
                auto_scroll=False,
            )
        )
            
        
        
        
    def build(self):
        """Build a stunning warning dialog with modern aesthetics and toggle buttons"""
        
        # Create section buttons
        # section_buttons = Create_Section_Buttons("Validation Errors", "Tree Measurements Error", lambda: self._switch_view("all"), lambda: self._switch_view("tree_measurements"))
    
        header = Warning_Dialog_Header( self.error_messages, self.error_message_for_out_of_bounds_dbh_or_height_value)        
        # Section header for errors
        # errors_header = Warning_Dialog_Display_Errors_Header()
        
        # Create scrollable content for error messages
        self.error_content = ft.ListView(
            expand=True,
            spacing=12,
            padding=20,
            auto_scroll=False,
        )
        
        # Populate with current view
        self._update_error_display()
        
        tabs_section = ft.Tabs(
            selected_index = 0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Validation Errors",
                    icon=ft.Icons.WARNING,
                    content=self.display_error_card_for_validation_information(),
                ),
                ft.Tab(
                    text="Tree Measurement Errors",
                    icon=ft.Icons.NATURE_PEOPLE_ROUNDED,
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                #STYLING
                                padding=ft.padding.all(10),
                                margin=10,
                                bgcolor=ft.Colors.YELLOW_50,
                                border_radius=12,
                                border=ft.border.all(1, ft.Colors.YELLOW_200),
                                content=ft.Row(
                                    controls=[
                                        ft.Text("Height must be (1.3 <= x <= 50.0), DBH must be (2.5 <= x <= 100.0)", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                                    ]
                                ),
                            ),
                            self.display_error_card_for_tree_measurements_information()
                        ],
                    ),
                ),
               
            ],
            expand=1,
        )
        
        # Main content container with tabs
        main_content = ft.Column(
            controls=[
                header,
              
                # ft.Container(
                #     content=self.error_content,
                #     expand=2,  # Give error content more space
                #     bgcolor=ft.Colors.GREY_50,
                #     border_radius=12,
                # ),
                ft.Container(
                    content=tabs_section,
                    expand=1,  # Give tabs less space
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    padding=10,
                ),
            ],
            spacing=3,
            expand=True,
        ) 
        
        # Modern action buttons
        self.dialog = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=15),
            content=ft.Container(
                content=main_content,
                width=900,
                height=950,
            ),
            actions=[
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.DOWNLOAD_ROUNDED, size=20, color=ft.Colors.WHITE),
                                ft.Text("Export Report", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=10,
                            tight=True,
                        ),
                        # on_click=self.export_report,
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        elevation=3,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(horizontal=24, vertical=16),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            shadow_color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_600),
                        ),
                    ),
                ),
                ft.Container(
                    content=ft.OutlinedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.CLOSE_ROUNDED, size=20, color=ft.Colors.GREY_700),
                                ft.Text("Close", color=ft.Colors.GREY_700, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=10,
                            tight=True,
                        ),
                        on_click=self.close_dialog,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(horizontal=24, vertical=16),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            side=ft.BorderSide(2, ft.Colors.GREY_300),
                        ),
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            actions_padding=ft.padding.all(20),
            bgcolor=ft.Colors.WHITE,
        )
        
        return self.dialog
   
    
    
    
    
    def _switch_view(self,view_type):
        """Switch between different error views"""
        self.current_view = view_type
        print("OPOPOPO")
        
        # Update button states by rebuilding the dialog
        if self.dialog:
            # self.dialog.open = False
            print("OPENING")
            
            self.page.open(self.build())
            # self.dialog.open = True
            self.page.update()
    
    def _update_error_display(self):
        """Update the error display based on current view"""
        self.error_content.controls.clear()
        
        # Filter errors based on current view
        if self.current_view == "tree_measurements":
            filtered_errors = self._filter_tree_measurement_errors()
        else:
            filtered_errors = self.error_messages
        
        # Color palette for different error cards
        error_colors = [
            (ft.Colors.RED_50, ft.Colors.RED_500, ft.Colors.RED_700),
            (ft.Colors.ORANGE_50, ft.Colors.ORANGE_500, ft.Colors.ORANGE_700),
            (ft.Colors.DEEP_ORANGE_50, ft.Colors.DEEP_ORANGE_500, ft.Colors.DEEP_ORANGE_700),
        ]
        
        # Add filtered error messages as stunning cards
        for i, error_msg in enumerate(filtered_errors):
            color_set = error_colors[i % len(error_colors)]
            bg_color, accent_color, text_color = color_set
            
            # Parse the error message to extract structured data
            parsed_error = self._parse_error_message(error_msg)
            
            error_card = ft.Container(
                content=ft.Column(
                    controls=[
                        # Error header with modern badge
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(
                                                ft.Icons.CIRCLE,
                                                color=ft.Colors.WHITE,
                                                size=8,
                                            ),
                                            ft.Text(
                                                f"Issue #{i+1}", 
                                                color=ft.Colors.WHITE,
                                                weight=ft.FontWeight.BOLD,
                                                size=13,
                                            ),
                                        ],
                                        spacing=6,
                                    ),
                                    bgcolor=accent_color,
                                    border_radius=20,
                                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                    shadow=ft.BoxShadow(
                                        spread_radius=0,
                                        blur_radius=8,
                                        color=ft.Colors.with_opacity(0.3, accent_color),
                                        offset=ft.Offset(0, 2),
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.ERROR_ROUNDED, 
                                        color=accent_color, 
                                        size=20
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        # Error message content with modern styling
                        ft.Container(
                            content=parsed_error,
                            padding=ft.padding.all(16),
                            bgcolor=ft.Colors.with_opacity(0.5, bg_color),
                            border_radius=12,
                            border=ft.border.all(1, ft.Colors.with_opacity(0.3, accent_color)),
                        ),
                    ],
                    spacing=12,
                ),
                padding=ft.padding.all(16),
                bgcolor=ft.Colors.WHITE,
                border_radius=16,
                border=ft.border.all(1, ft.Colors.GREY_200),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=20,
                    color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4),
                ),
            )
            self.error_content.controls.append(error_card)
    
    def _filter_tree_measurement_errors(self):
        """Filter errors to show only DBH and Height validation errors"""
        tree_measurement_errors = []
        
        for error_msg in self.error_messages:
            nan_columns = error_msg["nan_columns"]
            row_data = error_msg["row_data"]
            
            # Check if this is a tree measurement error (DBH or Height related)
            is_tree_measurement_error = (
                any(col in ['DBH', 'Height'] for col in nan_columns) or  # Missing DBH/Height
                self._is_invalid_tree_measurement(row_data)  # Invalid DBH/Height values
            )
            
            if is_tree_measurement_error:
                tree_measurement_errors.append(error_msg)
        
        return tree_measurement_errors
    
    def _is_invalid_tree_measurement(self, row_data):
        """Check if DBH or Height values are outside valid ranges"""
        try:
            dbh = row_data.get('DBH')
            height = row_data.get('Height')
            
            # Check if values are outside typical tree measurement ranges
            if dbh is not None and not pd.isna(dbh):
                if dbh < 0 or dbh > 500:  # DBH typically 0-500 cm
                    return True
            
            if height is not None and not pd.isna(height):
                if height < 0 or height > 100:  # Height typically 0-100 meters
                    return True
            
            return False
        except (TypeError, ValueError):
            return False
    
    def _parse_error_message(self, error_msg):
        """Parse error message and create a beautifully formatted display"""
        index = error_msg["index"]
        row_data = error_msg["row_data"]
        nan_columns = error_msg["nan_columns"]
        
        # Handle NaN values by converting to "MISSING" display
        def format_value(key, value):
            if pd.isna(value) or value is None:
                return ft.Text("MISSING", color=ft.Colors.RED_600, weight=ft.FontWeight.BOLD, size=12)
            else:
                return ft.Text(str(value), color=ft.Colors.GREY_800, size=12)
            
        
        return self._create_full_display(index, row_data, nan_columns, format_value)

    def _parse_error_message_for_out_of_bounds_dbh_or_height_value(self):
        print(self.error_message_for_out_of_bounds_dbh_or_height_value[0]["index"])
        print(self.error_message_for_out_of_bounds_dbh_or_height_value[0]["row_data"])
        print(self.error_message_for_out_of_bounds_dbh_or_height_value[0]["nan_columns"])
        
        
    
    def _create_full_display(self, index, row_data, nan_columns, format_value):
        """Create full error display with all columns"""
        return ft.Column(
            controls=[
                # Header with row index
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(ft.Icons.TAG, size=16, color=ft.Colors.BLUE_600),
                                padding=ft.padding.all(6),
                                bgcolor=ft.Colors.BLUE_50,
                                border_radius=8,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Row Index", size=11, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                                    ft.Text(str(index + 1), size=16, color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.all(12),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.BLUE_200),
                ),
                
                # Data display
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    padding=ft.padding.all(12),
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text("Plot:", color=ft.Colors.GREY_600, size=12),
                                            ft.Text("Year:", color=ft.Colors.GREY_600, size=12),
                                            ft.Text("Origin:", color=ft.Colors.GREY_600, size=12),
                                            ft.Text("Tree Status:", color=ft.Colors.GREY_600, size=12),
                                            ft.Text("SpecCode:", color=ft.Colors.GREY_600, size=12),
                                            ft.Text("Tree Number:", color=ft.Colors.GREY_600, size=12),
                                            ft.Text("DBH:", color=ft.Colors.GREY_600, size=12),
                                            ft.Text("Height:", color=ft.Colors.GREY_600, size=12),
                                        ],
                                        spacing=8,
                                    ),
                                    ft.Column(
                                        controls=[
                                            format_value("Plot", row_data["Plot"]),
                                            format_value("Year", row_data["Year"]),
                                            format_value("Origin", row_data["Origin"]),
                                            format_value("Tree Status", row_data["Tree Status"]),
                                            format_value("SpecCode", row_data["SpecCode"]),
                                            format_value("Tree Number", row_data["Tree Number"]),
                                            format_value("DBH", row_data["DBH"]),
                                            format_value("Height", row_data["Height"]),
                                        ],
                                        spacing=8,
                                    ),
                                ],
                                spacing=20,
                            ),
                            # FIX: nan_columns is already a list, don't index it
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.WARNING, color=ft.Colors.AMBER, size=16),
                                        ft.Text(f"Missing data in: {', '.join(nan_columns)}", 
                                            color=ft.Colors.AMBER_700,
                                            weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=8,
                                ),
                                padding=ft.padding.all(10),
                                bgcolor=ft.Colors.AMBER_50,
                                border_radius=8,
                                margin=ft.margin.only(top=10),
                            ),
                        ],
                    ),
                )              
            ]
        )
    def _create_tree_measurement_display(self, index, row_data, nan_columns, format_value):
        """Create focused display for tree measurement errors"""
        return ft.Column(
            controls=[
                # Header with tree measurement focus
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(ft.Icons.NATURE, size=16, color=ft.Colors.GREEN_600),
                                padding=ft.padding.all(6),
                                bgcolor=ft.Colors.GREEN_50,
                                border_radius=8,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text("Tree Measurement Error", size=11, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                                    ft.Text(f"Row { 1}", size=16, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.all(12),
                    bgcolor=ft.Colors.GREEN_50,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREEN_200),
                ),
                
                # Focused tree measurement data
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    padding=ft.padding.all(12),
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text("SpecCode:", color=ft.Colors.GREY_600, size=12),
                                            ft.Text("Tree Number:", color=ft.Colors.GREY_600, size=12),
                                            ft.Text("DBH:", color=ft.Colors.GREY_600, size=12),
                                            ft.Text("Height:", color=ft.Colors.GREY_600, size=12),
                                        ],
                                        spacing=8,
                                    ),
                                    ft.Column(
                                        controls=[
                                            format_value("SpecCode", row_data["SpecCode"]),
                                            format_value("Tree Number", row_data["Tree Number"]),
                                            format_value("DBH", row_data["DBH"]),
                                            format_value("Height", row_data["Height"]),
                                        ],
                                        spacing=8,
                                    ),
                                ],
                                spacing=20,
                            ),
                            # Enhanced warning for tree measurements
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.HEIGHT, color=ft.Colors.RED, size=16),
                                        ft.Text(f"Tree measurement issue: {', '.join(nan_columns)}", 
                                            color=ft.Colors.RED_700,
                                            weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=8,
                                ),
                                padding=ft.padding.all(10),
                                bgcolor=ft.Colors.RED_50,
                                border_radius=8,
                                margin=ft.margin.only(top=10),
                            ),
                        ],
                    ),
                )              
            ]
        )
    
    def show_dialog(self):
        """Display the dialog on the given page"""
        if self.dialog is None:
            self.build()
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
    
    def close_dialog(self, e):
        """Close the dialog"""
        self.dialog.open = False
        self.page.update()

# Quick usage function
def show_warning_dialog(page: ft.Page, error_messages: list):
    """Helper function to quickly display stunning warning dialog"""
    if error_messages:
        dialog = Display_Warning_Dialog(page, error_messages)
        dialog.show_dialog()
    else:
        # Show modern success message
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=ft.Colors.WHITE, size=24),
                        ft.Text(
                            "✨ All data validation checks passed!",
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    spacing=12,
                ),
                bgcolor=ft.Colors.GREEN_600,
                behavior=ft.SnackBarBehavior.FLOATING,
                margin=ft.margin.all(20),
                padding=ft.padding.symmetric(horizontal=20, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation=6,
            )
        )