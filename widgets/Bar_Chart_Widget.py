import flet as ft
import base64
from io import BytesIO

import pyautogui
import datetime

class Bar_Chart_Widget(ft.BarChart):
    def __init__(self, page: ft.Page, on_save=None, species_data={}):
        super().__init__()
        self.page = page
        self.on_save = on_save
        self.card_ref = ft.Ref[ft.Card]()
        self.file_path_of_saved_chart_image = ""
        self.confirmation_container_ref = ft.Ref[ft.Container]()
        self.species_data = species_data
        self.summary_table_ref = ft.Ref[ft.Container]()
        print("Initializing Bar Chart Widget with species data:")
        # print(species_data)
        # Track if we've saved a screenshot
        self.has_saved = False
        
    def _calculate_max_y(self) -> float:
        if not self.species_data:
            return 1000
        max_val = 0
        for s in self.species_data:
            total = sum([s.get(k, 0) for k in ["Wood", "Bark", "Branch", "Foliage"]])
            max_val = max(max_val, total)
        # Pad by 15% and round to nearest 100
        return (( (max_val * 1.15) + 99) // 100) * 100 if max_val > 0 else 1000
        
    def _on_close(self, e):
        print("Closing Bar Chart Widget")
        self.page.overlay.pop()
        self.page.update()
        
    def _update_confirmation_display(self):
        """Update the confirmation text container."""
        if hasattr(self, 'confirmation_container_ref') and self.confirmation_container_ref.current:
            # Update existing container
            self.confirmation_container_ref.current.content = ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=20),
                    ft.Text(" Successfully saved to: ", size=14, color=ft.Colors.BLACK),
                    ft.Text(f"{self.file_path_of_saved_chart_image}", 
                           size=14, 
                           color=ft.Colors.BLUE, 
                           weight=ft.FontWeight.BOLD,
                           selectable=True)  # Added selectable so user can copy the path
                ]
            )
            self.confirmation_container_ref.current.bgcolor = ft.Colors.LIGHT_GREEN_100
            self.confirmation_container_ref.current.padding = 15
            self.confirmation_container_ref.current.border_radius = ft.border_radius.all(10)
            self.confirmation_container_ref.current.border = ft.border.all(2, ft.Colors.GREEN_300)
            self.confirmation_container_ref.current.visible = True
            self.confirmation_container_ref.current.opacity = 1
            
    def _on_save_result(self, e):
        print("Save button clicked")
        
        # Generate timestamp for filename
        date_and_time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.file_path_of_saved_chart_image = f"screenshots/screenshot_chart_{date_and_time_stamp}.png"
        
        # Take screenshot
        try:
            # Ensure screenshots directory exists
            import os
            os.makedirs("screenshots", exist_ok=True)
            
            pyautogui.screenshot(self.file_path_of_saved_chart_image)
            print(f"Screenshot saved to: {self.file_path_of_saved_chart_image}")
            
            # Mark as saved
            self.has_saved = True
            
            # Update the confirmation container
            self._update_confirmation_display()
            
            # Force UI update
            if hasattr(self, 'card_ref') and self.card_ref.current:
                self.card_ref.current.update()
            
            # Also update the page
            self.page.update()
            
            # Show success snackbar
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE),
                    ft.Text("Chart saved successfully!", color=ft.Colors.PRIMARY)
                ]),
                bgcolor=ft.Colors.GREEN,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()
            
        except Exception as ex:
            print(f"Error saving screenshot: {str(ex)}")
            # Show error message
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.WHITE),
                    ft.Text(f"Error saving screenshot: {str(ex)}", color=ft.Colors.WHITE)
                ]),
                bgcolor=ft.Colors.RED,
                duration=5000
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def _create_summary_table(self):
        """Create a summary table with component percentages for each species."""
        species_data = self.species_data
        
        # Create the DataTable
        summary_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Species", weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY, size=12)),
                ft.DataColumn(ft.Text("Wood %", weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER, size=12)),
                ft.DataColumn(ft.Text("Bark %", weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN, size=12)),
                ft.DataColumn(ft.Text("Branch %", weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE, size=12)),
                ft.DataColumn(ft.Text("Foliage %", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN, size=12)),
                ft.DataColumn(ft.Text("Total (kg)", weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY, size=12)),
            ],
            column_spacing=20,
            horizontal_margin=10,
            heading_row_color=ft.Colors.with_opacity(0.2, ft.Colors.PRIMARY),
            heading_row_height=40,
            divider_thickness=0.5,
            show_bottom_border=True,
        )
        
        # Create rows for each species and add to the table
        for i, species_info in enumerate(species_data):
            total = (species_info.get("Wood", 0) + 
                    species_info.get("Bark", 0) + 
                    species_info.get("Branch", 0) + 
                    species_info.get("Foliage", 0))
            
            # Calculate percentages (handle division by zero)
            if total > 0:
                wood_pct = (species_info.get("Wood", 0) / total) * 100
                bark_pct = (species_info.get("Bark", 0) / total) * 100
                branch_pct = (species_info.get("Branch", 0) / total) * 100
                foliage_pct = (species_info.get("Foliage", 0) / total) * 100
            else:
                wood_pct = bark_pct = branch_pct = foliage_pct = 0
            
            # Add alternating row colors
            row_color = ft.Colors.with_opacity(0.05, ft.Colors.PRIMARY) if i % 2 == 0 else ft.Colors.WHITE
            
            # Create data row
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(species_info["species_code"], size=11, weight=ft.FontWeight.W_500)),
                    ft.DataCell(ft.Text(f"{wood_pct:.1f}%", size=11)),
                    ft.DataCell(ft.Text(f"{bark_pct:.1f}%", size=11)),
                    ft.DataCell(ft.Text(f"{branch_pct:.1f}%", size=11)),
                    ft.DataCell(ft.Text(f"{foliage_pct:.1f}%", size=11)),
                    ft.DataCell(ft.Text(f"{total:.1f}", size=11, weight=ft.FontWeight.W_500)),
                ],
                color=row_color,
            )
            summary_table.rows.append(row)
        
        # Wrap in a scrollable container
        summary_container = ft.Container(
            ref=self.summary_table_ref,
            content=ft.Column([
               
                ft.Container(
                    content=ft.Column(
                        [summary_table],
                        scroll=ft.ScrollMode.ADAPTIVE,
                        height=180,
                    ),
                    padding=10,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.border_radius.all(8),
                    border=ft.border.all(1, ft.Colors.GREY_300),
                ),
            ], spacing=10),
            padding=10,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(1, ft.Colors.GREY_300),
        )
        
        return summary_container
        
    def build(self):
            # Stacked bar chart data for different species components
            species_data = self.species_data
            max_y = self._calculate_max_y()
            # Color scheme for different components
            component_colors = {
                "Bark": ft.Colors.BROWN,
                "Branch": ft.Colors.ORANGE,
                "Wood": ft.Colors.AMBER,
                "Foliage": ft.Colors.GREEN,
            }
            
            # Create bar groups for each species with proper stacking
            bar_groups = []
            for i, (species_info) in enumerate(species_data):
                # Stack order from bottom to top
                stack_order = ["Wood", "Bark", "Branch", "Foliage"]
                
                # Create stacked rod items
                stacked_items = []
                cumulative = 0
                
                for component in stack_order:
                    value = species_info[component]
                    stacked_items.append(
                        ft.BarChartRodStackItem(
                            from_y=cumulative,
                            to_y=cumulative + value,
                            color=component_colors[component],
                            border_side=ft.BorderSide(width=0.5, color=ft.Colors.WHITE70),
                        )
                    )
                    cumulative += value
                
                bar_groups.append(
                    ft.BarChartGroup(
                        x=i,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=cumulative,
                                width=15,
                                border_radius=0,
                                rod_stack_items=stacked_items,
                            )
                        ],
                    )
                )
            
            # Calculate chart width - increased multiplier for better spacing
            chart_width = max(800, len(species_data) * 45)
            
           # Update the bar chart creation with these adjustments:
            bar_chart = ft.BarChart(
                bar_groups=bar_groups,
                border=ft.border.all(1, ft.Colors.GREY_400),
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                
                left_axis=ft.ChartAxis(
                    title=ft.Text("Biomass (KG)", color=ft.Colors.PRIMARY, size=13, weight=ft.FontWeight.BOLD),
                    labels_size=80,  # Reduced from 70
                    show_labels=True,
                 
                ),
                
                bottom_axis=ft.ChartAxis(
                    title=ft.Text("Species", color=ft.Colors.PRIMARY, size=13, weight=ft.FontWeight.BOLD),
                    labels=[
                        ft.ChartAxisLabel(
                            value=i, 
                            label=ft.Container(
                                content=ft.Text(
                                    species_info["species_code"], 
                                    color=ft.Colors.PRIMARY, 
                                    size=14,
                                    weight=ft.FontWeight.W_600,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                padding=ft.padding.only(top=5, left=5, right=5),
                                alignment=ft.alignment.center,
                                width=80,
                            )
                        ) for i, species_info in enumerate(species_data)
                    ],
                    labels_size=80,
                    show_labels=True,
                    # labels_interval=1,
                ),
                
                horizontal_grid_lines=ft.ChartGridLines(
                    color=ft.Colors.GREY_300,
                    width=1,
                    dash_pattern=[5, 5],
                ),
                
                # Add these properties to improve layout
                max_y=self._calculate_max_y(),
                min_y=0,
                interactive=True,
                expand=True,
                height=450,
                groups_space=40,  # Slightly increased
               
                
                # Add margins to prevent label clipping
                # margin=ft.margin.all(10),  # Add margin around the chart
            )
            
            # Create scrollable container for the chart
            scrollable_chart_container = ft.Container(
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                content=ft.Column(
                    [
                        ft.Container(
                            padding=10,
                            content=bar_chart,
                            width=chart_width,
                        )
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                ),
                width=1000,  # Increased width
                height=500,  # Adjusted height
                border=ft.border.all(1, ft.Colors.GREY_300),
            )
            
            # Create summary table (scrollable)
            summary_table = self._create_summary_table()
            
            # Create scrollable container for the summary table
            scrollable_summary_container = ft.Container(
                content=ft.Column(
                    [
                        summary_table
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                    height=250,  # Fixed height for scrolling
                ),
                width=1000,
                height=270,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=ft.border_radius.all(8),
                padding=5,
            )
            
            # Saved screenshot confirmation text (with top margin)
            confirmation_container = ft.Container(
                ref=self.confirmation_container_ref,
                margin=ft.margin.only(top=20),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=18),
                        ft.Text("Chart image saved to:", size=13, color=ft.Colors.BLACK),
                        ft.Text("", size=13, color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD, selectable=True)
                    ]
                ),
                bgcolor=ft.Colors.LIGHT_GREEN_50,
                padding=10,
                border_radius=ft.border_radius.all(8),
                border=ft.border.all(1, ft.Colors.GREEN_300),
                visible=False,
                opacity=0,
                animate_opacity=300,
            )
            
            # Main card content
            card = ft.Card(
                ref=self.card_ref,
                elevation=20,
                
                content=ft.Container(
                    margin=ft.margin.all(20),
                    border_radius=ft.border_radius.all(15),
                    width=1000,  # Increased width slightly
                    height=650,  # Increased height
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    padding=25,
                    content=ft.Column([
                        # Header
                        ft.Row([
                            ft.Text(
                                "Biomass by Species Components",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.PRIMARY,
                                expand=True,
                            ),
                            # Save button
                            ft.IconButton(
                                icon=ft.Icons.SAVE_ALT,
                                icon_color=ft.Colors.BLUE_GREY_700,
                                tooltip="Save as PNG",
                                on_click=self._on_save_result,
                            ),
                            # Close button
                            ft.IconButton(
                                icon=ft.Icons.CANCEL,
                                icon_color=ft.Colors.RED_ACCENT_700,
                                tooltip="Close",
                                on_click=self._on_close
                            ),
                        ]),
                        
                        # Scrollable chart container
                        scrollable_chart_container,
                        
                        # Legend
                        ft.Container(
                            margin=ft.margin.only(top=10),
                            content=ft.Column([
                                ft.Text("Components Legend (Bottom to Top):", 
                                    size=14, 
                                    weight=ft.FontWeight.BOLD, 
                                    color=ft.Colors.PRIMARY),
                                ft.Row([
                                    ft.Row([
                                        ft.Container(width=15, height=15, bgcolor=ft.Colors.AMBER, border_radius=3),
                                        ft.Text("Wood", size=12, color=ft.Colors.PRIMARY),
                                    ], spacing=3),
                                    ft.Row([
                                        ft.Container(width=15, height=15, bgcolor=ft.Colors.BROWN, border_radius=3),
                                        ft.Text("Bark", size=12, color=ft.Colors.PRIMARY),
                                    ], spacing=3),
                                    ft.Row([
                                        ft.Container(width=15, height=15, bgcolor=ft.Colors.ORANGE, border_radius=3),
                                        ft.Text("Branch", size=12, color=ft.Colors.PRIMARY),
                                    ], spacing=3),
                                    ft.Row([
                                        ft.Container(width=15, height=15, bgcolor=ft.Colors.GREEN, border_radius=3),
                                        ft.Text("Foliage", size=12, color=ft.Colors.PRIMARY),
                                    ], spacing=3),
                                ], spacing=15, wrap=True),
                            ], spacing=8),
                        ),
                        
                        # Scrollable summary table
                        ft.Container(
                            margin=ft.margin.only(top=15),
                            content=ft.Column([
                                ft.Text("Summary Table - Component Percentages", 
                                       size=16, 
                                       weight=ft.FontWeight.BOLD, 
                                       color=ft.Colors.PRIMARY),
                                scrollable_summary_container,
                            ], spacing=5),
                        ),
                        
                        # Confirmation container
                        confirmation_container
                        
                    ], spacing=10, scroll=ft.ScrollMode.ADAPTIVE)  # Make entire card content scrollable if needed
                )
            )

            # Centered container with black semi-transparent background
            return ft.Container(
                
                content=card,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                expand=True,
            ) 