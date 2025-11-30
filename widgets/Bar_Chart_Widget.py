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
        
        self.pending_image_data = None
        
    def _calculate_max_y(self) -> float:
        """Calculate maximum Y value for the chart with some padding."""
        if not self.species_data:
            return 1000  # Default value
            
        max_value = 0
        for species in self.species_data:
            # Sum all components for this species
            total = species.get("Wood", 0) + species.get("Bark", 0) + species.get("Branch", 0) + species.get("Foliage", 0)
            max_value = max(max_value, total)
        
        # Add 10% padding and round up to nearest 100
        if max_value > 0:
            padded_max = max_value * 1.1
            # Round up to nearest 100 for clean axis labels
            return ((padded_max + 99) // 100) * 100
        return 1000   
        
    def _on_close(self, e):
        print("Closing Bar Chart Widget")
       
        self.page.overlay.pop()
        self.page.update()
    
    def _on_save_result(self, e: ft.FilePickerResultEvent):
        print(e)
        # save the bar chart as PNG
        #random name for file name 
        from datetime import datetime
        date_and_time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.file_path_of_saved_chart_image = f"screenshots/screenshot_chart_{date_and_time_stamp}.png"
        pyautogui.screenshot(self.file_path_of_saved_chart_image)
        self.page.update()
        
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
        print(species_data)
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
                        border_side=ft.BorderSide(width=0, color=ft.Colors.WHITE),
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
                            width=25,
                            border_radius=0,
                            rod_stack_items=stacked_items,
                        )
                    ],
                )
            )
        
        # Calculate chart width - reduce spacing between bars
        chart_width = max(600, len(species_data) * 40)  # Reduced from 60 to 40 pixels per species
        
        # Create the bar chart with proper spacing
        bar_chart = ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(1, ft.Colors.GREY_400),
            bgcolor=ft.Colors.WHITE,
            left_axis=ft.ChartAxis(
                title=ft.Text("Calculated Biomass (KG)", color=ft.Colors.BLACK),
                labels_size=40,
                labels_interval=max_y / 10 if max_y else 1,
                title_size=16,
            ),
            bottom_axis=ft.ChartAxis(
                title=ft.Text("Species", color=ft.Colors.BLACK),
                labels=[
                    ft.ChartAxisLabel(
                        value=i, 
                        label=ft.Text(
                            species_info["species_code"], 
                            color=ft.Colors.BLACK, 
                            size=12,  # Increased font size
                            weight=ft.FontWeight.NORMAL
                        )
                    ) for i, species_info in enumerate(species_data)
                ],
                labels_size=30,  # Reduced from 50 to reduce padding
                title_size=16,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.GREY_300,
                width=1,
                dash_pattern=[5, 5],
            ),
            max_y=max_y,
            min_y=0,
            interactive=True,
            width=chart_width,
            height=350,
            # Reduce spacing between groups
            groups_space=50,  # Reduced space between bar groups
        )
        
        # Create scrollable container for the chart
        scrollable_chart_container = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=bar_chart,
                        width=chart_width,
                    )
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            width=800,
            height=400,
            border=ft.border.all(1, ft.Colors.GREY_300),
        )
        
        # Main card content
        card = ft.Card(
            ref=self.card_ref,
            elevation=20,
            content=ft.Container(
                width=800,
                height=700,
                bgcolor=ft.Colors.WHITE,
                padding=30,
                content=ft.Column([
                    # Header with title and buttons
                    ft.Row([
                        ft.Text(
                            "Biomass Analysis by Species",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK,
                            expand=True,
                        ),
                        # Save button
                        ft.IconButton(
                            icon=ft.Icons.SAVE,
                            icon_color=ft.Colors.BLUE,
                            tooltip="Save as PNG",
                            on_click=self._on_save_result,
                        ),
                        # Close button
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=ft.Colors.RED,
                            tooltip="Close",
                            on_click=self._on_close
                        ),
                    ]),
                    
                    # Scrollable chart container
                    scrollable_chart_container,
                    
                    # Legend
                    ft.Container(
                        margin=ft.margin.only(top=20),
                        content=ft.Column([
                            ft.Text("Components Legend (Bottom to Top):", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                            ft.Row([  # Changed to Row for horizontal legend
                                ft.Row([
                                    ft.Container(width=20, height=20, bgcolor=ft.Colors.AMBER, border_radius=5),
                                    ft.Text("Wood", size=12),
                                ], spacing=5),
                                ft.Row([
                                    ft.Container(width=20, height=20, bgcolor=ft.Colors.BROWN, border_radius=5),
                                    ft.Text("Bark", size=12),
                                ], spacing=5),
                                ft.Row([
                                    ft.Container(width=20, height=20, bgcolor=ft.Colors.ORANGE, border_radius=5),
                                    ft.Text("Branch", size=12),
                                ], spacing=5),
                                ft.Row([
                                    ft.Container(width=20, height=20, bgcolor=ft.Colors.GREEN, border_radius=5),
                                    ft.Text("Foliage", size=12),
                                ], spacing=5),
                            ], spacing=20),  # Space between legend items
                        ]),
                    ),
                    
                    # Saved screenshot confirmation text
                    ft.Container(
                        ref=self.confirmation_container_ref,
                        bgcolor=ft.Colors.LIGHT_GREEN,
                        padding=10,
                        content=ft.Row(
                            controls=[
                                ft.Text("Chart saved as: ", size=12, color=ft.Colors.BLACK),
                                ft.Text(f"{self.file_path_of_saved_chart_image}", size=12, color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD)
                            ]
                        )
                    ) if self.file_path_of_saved_chart_image!="" else ft.Container()
                ])  # Close the main Column
            )  # Close the Container
        )  # Close the Card

        # Centered container with black semi-transparent background
        return ft.Container(
            content=card,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
            expand=True,
        )