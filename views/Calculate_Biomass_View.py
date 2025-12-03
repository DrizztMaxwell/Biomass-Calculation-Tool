import flet as ft
import json
import datetime
import os
from widgets.Equation_Card_Description_Text import Equation_Card_Description_Text
from widgets.Equation_Card_Formula_Text import Equation_Card_Formula_Text
from widgets.Equation_Card_Title_Text import Equation_Card_Title_Text
from widgets.Hardwood_or_Softwood_Dialog import HardwoodOrSoftwoodDialog
from widgets.Loading_Spinner_Widget import Loading_Spinner_Widget
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
from widgets.Select_Components_Widget import Select_Components_Widget
from widgets.Equation_Type_Card import Equation_Type_Card
from data.components_data import COMPONENTS_DATA
from widgets.Calculate_Biomass_Button import Calculate_Biomass_Button
from widgets.Bar_Chart_Widget import Bar_Chart_Widget

class Calculate_Biomass_View:
    def __init__(self, controller, page: ft.Page, selected_file_path):
        self.data=None
        self.controller = controller
        self.page = page  # Initialize page reference
        self.is_button_disabled = False
        self.calculate_biomass_button =  Calculate_Biomass_Button(
                    on_click_callback=self.on_calculate_biomass_click,
                    is_disabled=self.is_button_disabled
                )
        print("Calculate_Biomass_View initialized")
        self.hardwood_softwood_dialog = None
        self.selected_components_text = ft.Text(
            value="",
            color=ft.Colors.BLACK,
            weight=ft.FontWeight.W_500
        )
        self.selected_file_path = selected_file_path
        # Results table container (initially empty)
        self.results_table_container = ft.Container(visible=False)

        self.component_cards_row = ft.Row(wrap=True)
        
        # File picker for export
        self.file_picker = ft.FilePicker(on_result=self._on_file_save_result)

        self.page.overlay.append(self.file_picker)
        
        self.page.update()
        

    def set_page(self, page: ft.Page):
        """Set the page reference for UI updates"""
        self.page = page
        print(f"Page reference set: {self.page}")

    def _create_equation_card(self, title: str, formula: str, description: str, radio_value: str) -> Equation_Type_Card:
        """Helper method to create equation type cards."""
        title_formula = ft.Column(
            controls=[
                Equation_Card_Title_Text(title),
                Equation_Card_Formula_Text(formula)
            ],
            spacing=2,
        )
        desc = Equation_Card_Description_Text(description)
       
        return Equation_Type_Card(title_formula, desc, radio_value)
    
    def on_equation_type_change(self, e):
        """Handle equation type selection change."""
        self.controller.set_equation_type(e.control.value)

    def _create_equation_section(self) -> ft.Container:
        """Create the equation type selection section."""
        equation_cards = [
            self._create_equation_card(
                title="DBH-based",
                formula="B = b₁ × DBHᵇ²",
                description="Uses only Diameter at Breast Height for calculation",
                radio_value="DBH-based"
            ),
            self._create_equation_card(
                title="DBH + Height-based Equation",
                formula="B = b₁ × DBHᵇ² × Heightᵇ³",
                description="Uses both DBH and tree height for more accurate estimation",
                radio_value="DBH + Height-based"
            )
        ]

        radio_group = ft.RadioGroup(
            content=ft.Column(equation_cards),
            on_change=self.on_equation_type_change,
            value="DBH-based"
        )
       
        return ft.Container(
            bgcolor="white",
            padding=20,
            margin=30,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
                offset=ft.Offset(0, 3),
            ),
            content=ft.Column([
                ft.Container(
                    margin=ft.margin.only(top=15, left=5, right=5, bottom=5),
                    content=ft.Column([
                        TitleTextWidget("Equation Type"),
                        DescriptionText("Choose the calculation method for biomass estimation"),
                    ]),
                ),
                radio_group
            ])
        )

    def _create_components_section(self) -> Select_Components_Widget:
        """Create the components selection section."""
        return Select_Components_Widget(
            title=TitleTextWidget("Select Tree Component"),
            description_text=DescriptionText("Select tree components for biomass calculation"),
            components_card_row=self.component_cards_row,
            selected_card_component=self.selected_components_text,
            components_data=COMPONENTS_DATA
        )
    async def show_species_code_dialog(self, missing_species_codes):
        """Show dialog to select hardwood or softwood for missing species codes."""
        self.hardwood_softwood_dialog = HardwoodOrSoftwoodDialog(self.page, missing_species_codes)
        
        # Show dialog and wait for result
        result = await self.hardwood_softwood_dialog.show_species_code_dialog()
        return result

    def _generate_filename(self):
        
        """Generate filename with date and time prefix."""
        now = datetime.datetime.now()
        date_prefix = now.strftime("%Y%m%d")
        time_prefix = now.strftime("%H%M%S")
        print(f"FILE PATH:{self.selected_file_path}")
        filename_without_ext = os.path.splitext(os.path.basename(self.selected_file_path))[0]
        print(filename_without_ext)  # Output: "data_set"
        return f"{filename_without_ext}_{date_prefix}_{time_prefix}.txt"
    
    def _export_to_txt(self, data, file_path: str):
        """Export data to a formatted text file."""
        try:
            with open(file_path, 'w') as f:
                # Write header
                f.write("BIOMASS CALCULATION RESULTS\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total records: {len(data)}\n\n")
                
                # Write column headers
                if data:
                    headers = list(data[0].keys())
                    # Write header row
                    header_line = "\t".join(headers)
                    f.write(header_line + "\n")
                    f.write("-" * len(header_line) + "\n")
                    
                    # Write data rows
                    for item in data:
                        row_values = []
                        for header in headers:
                            value = item.get(header, "")
                            # Format the value for display
                            if isinstance(value, (int, float)) and value is not None:
                                if header in ["Wood (KG)", "Bark (KG)", "Branch (KG)", "Foliage (KG)", 
                                            "Stem (KG)", "Crown (KG)", "Total (KG)"]:
                                    display_value = f"{value:.4f}" if value is not None else "N/A"
                                else:
                                    display_value = str(value)
                            else:
                                display_value = str(value) if value is not None else "N/A"
                            row_values.append(display_value)
                        
                        f.write("\t".join(row_values) + "\n")
                
                f.write(f"\nFile: {os.path.basename(file_path)}\n")
            
            return True
        except Exception as e:
            print(f"Export error: {str(e)}")
            return False
    
    def _on_file_save_result(self, e: ft.FilePickerResultEvent):
        """Handle file save dialog result."""
        if e.path:
            # Load the complete data from JSON
            try:
                with open('storage/biomass_results.json', 'r') as f:
                    data = json.load(f)
                
                # Export to the selected file path
                success = self._export_to_txt(data, e.path)
                
                if success:
                    print(f"Data exported successfully to {e.path}")
                else:
                    print(f"Failed to export data to {e.path}")
                    
            except Exception as ex:
                print(f"Error loading data: {str(ex)}")
        else:
            # User cancelled the save dialog
            print("Export cancelled by user")
        
    async def on_calculate_biomass_click(self, e):
        """Handle calculate biomass button click - delegate to controller."""
        print("Calculate biomass button clicked")
        loading_spinner = Loading_Spinner_Widget(self.page)
        loading_spinner.show_dialog()
               
        # Disable button and change appearance
        self.calculate_biomass_button.is_disabled = True
        e.control.bgcolor = "#CCCCCC"
        e.control.color = "#888888"
        e.control.disabled = True
        e.control.update()
        
        print(f"Button disabled: {self.is_button_disabled}")
       
        # Call controller method
        await loading_spinner.simulate_progressive_loading(0.0, 0.2, 0.1, "Beginning Calculation...")
        
        did_it_calculate = await self.controller.calculate_biomass()
        if not did_it_calculate:
            # Re-enable button
            self.calculate_biomass_button.is_disabled = False
            e.control.bgcolor = ft.Colors.GREEN_700
            e.control.color = ft.Colors.WHITE
            e.control.disabled = False
            e.control.update()
            loading_spinner.hide()
            return  # Exit if calculation did not complete successfully
        
        await loading_spinner.simulate_progressive_loading(1.0, 1.0, 0.1, "Completed...")
        loading_spinner.hide()
        
        
        # Show results table immediately
        self._show_results_table()
        
        # Re-enable button
        self.calculate_biomass_button.is_disabled = False
        e.control.bgcolor = ft.Colors.GREEN_700
        e.control.color = ft.Colors.WHITE
        e.control.disabled = False
        e.control.update()

    def _show_results_table(self):
      
        """Create and display the results table and auto-scroll to it."""
        results_table = self._create_results_table()
        self.results_table_container.content = results_table
        self.results_table_container.key = "results_table_container"
        self.results_table_container.visible = True
        self.page.scroll_to(
            key="results_table_container",  # Use the ID we set
            duration=259,
         
            curve=ft.AnimationCurve.EASE_OUT
        )
        print(self.selected_file_path)
        # Update UI first to ensure the table is rendered
        if self.page:
            self.page.update()
            print("updated")
            
       
    def get_selected_components(self):
        """Get currently selected components."""
        return [comp['title'] for comp in COMPONENTS_DATA if comp['is_selected']]

    def build(self) -> ft.Column:
        """Build the main view layout."""
        # Create the calculate button
        self.calculate_biomass_button = Calculate_Biomass_Button(
            on_click_callback=self.on_calculate_biomass_click,
            is_disabled=self.is_button_disabled
        ).create()
         # Add an ID to the results container for precise scrolling
        self.results_table_container.id = "results_table_container"
        return ft.Column(
            controls=[
                self._create_equation_section(),
                self._create_components_section(),
                self.calculate_biomass_button,
                self.results_table_container  # Initially hidden results table
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    async def _on_view_chart_click(self, e):
        """Handle View Chart button click - delegate to controller."""
        print("View Chart button clicked")
        loading_spinner = Loading_Spinner_Widget(self.page)
        loading_spinner.show_dialog()
        await loading_spinner.simulate_progressive_loading(0.0, 0.2, 0.1, "Preparing Chart...")
        species_data = self.controller._click_on_show_chart_button()
      
        
        self._show_biomass_chart(species_data)
        await loading_spinner.simulate_progressive_loading(1.0, 1.0, 0.1, "Completed...")
        loading_spinner.hide()
        
        
    def _show_biomass_chart(self, species_data):
        """Show biomass chart - delegate to controller."""
        chart = Bar_Chart_Widget(self.page, species_data=species_data).build()
        self.page.overlay.append(chart)
        self.page.update()
        
    
        
    def _create_results_table(self) -> ft.Container:
        """Create a table to display biomass results from JSON data."""
        # Load data from JSON file
        try:
            with open('storage/biomass_results.json', 'r') as f:
                data = json.load(f)
                self.data = data
        except FileNotFoundError:
            # Return empty container if file doesn't exist
            return ft.Container(
                content=ft.Text("No biomass results available", color=ft.Colors.GREY_600),
                padding=20
            )
        except Exception as e:
            return ft.Container(
                content=ft.Text(f"Error loading results: {str(e)}", color=ft.Colors.RED),
                padding=20
            )
        
        if not data:
            return ft.Container(
                content=ft.Text("No biomass results available", color=ft.Colors.GREY_600),
                padding=20
            )
        
        # Get first 10 rows only
        display_data = data[:10]
        
        # Extract column headers from the first item
        headers = list(display_data[0].keys())
        
        # Create data rows (first 10 only)
        data_rows = []
        for item in display_data:
            cells = []
            for header in headers:
                value = item.get(header, "")
                # Format the value for display
                if isinstance(value, (int, float)) and value is not None:
                    if header in ["Wood (KG)", "Bark (KG)", "Branch (KG)", "Foliage (KG)", 
                                "Stem (KG)", "Crown (KG)", "Total (KG)"]:
                        display_value = f"{value:.4f}" if value is not None else "N/A"
                    else:
                        display_value = str(value)
                else:
                    display_value = str(value) if value is not None else "N/A"
                
                cells.append(ft.DataCell(ft.Text(display_value)))
            
            data_rows.append(ft.DataRow(cells=cells))
        
        # Create the data table with horizontal scrolling
        data_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(header, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)) for header in headers],
            rows=data_rows,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            horizontal_margin=10,
            heading_row_color=ft.Colors.GREEN_700,
            heading_row_height=40,
            data_row_color={ft.ControlState.HOVERED: ft.Colors.GREY_100},
            data_text_style=ft.TextStyle(color=ft.Colors.BLACK),
            show_checkbox_column=False,
        )
        
        # Create View Chart button
        view_chart_button = ft.ElevatedButton(
            text="View Chart",
            icon=ft.Icons.BAR_CHART,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            on_click= lambda e: self.page.run_task(self._on_view_chart_click, e),  # You'll need to implement this method
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(10)),
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            )
        )
        
        # Create export button
        export_button = ft.ElevatedButton(
            text="Export to TXT",
            icon=ft.Icons.DOWNLOAD,
            bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE,
            on_click=self._on_export_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(10)),
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            )
        )
        
        # Create horizontally scrollable container for the table
        scrollable_table = ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[data_table],
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
                offset=ft.Offset(0, 3),
            ),
        )

        # Wrap in a container with title and info
        table_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    TitleTextWidget("Calculated Biomass Results Table"),
                    ft.Row([
                        view_chart_button,  # View Chart button on the left
                        export_button      # Export to TXT button on the right
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row([
                                DescriptionText(f"Showing first 10 of {len(data)} records"),
                                ft.Text("← Scroll horizontally →", 
                                    color=ft.Colors.GREEN_700,
                                    size=12,
                                    weight=ft.FontWeight.W_500)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                            scrollable_table
                        ]
                    ),
                )
            ]),
            margin=ft.margin.all(20),
            padding=ft.padding.all(30),
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
                offset=ft.Offset(0, 3),
            ),
            border_radius=10,
        )

        return table_container
    def _on_export_click(self, e):
        """Handle export button click - open file save dialog."""
        # Generate default filename with timestamp
        default_filename = self._generate_filename()
        
        # Open file save dialog
        self.file_picker.save_file(
            dialog_title="Save Biomass Results",
            file_name=default_filename,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"]
        )

# Initialize the file picker event handler
    def initialize_view(controller, page: ft.Page):
        view = Calculate_Biomass_View(controller, page)
        # Set up file picker event handler
        view.file_picker.on_result = view._on_file_save_result
        return view