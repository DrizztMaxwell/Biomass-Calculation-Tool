import json
import flet as ft
import datetime
import os
from typing import List, Dict, Any, Optional

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
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
from widgets.LogFileTxt import logger


class Calculate_Biomass_View:
    """View for calculating and displaying biomass results."""
    
    # Constants
    _RESULTS_JSON_PATH = 'storage/biomass_results.json'
    _STORAGE_DIR = 'storage'
    _MAX_DISPLAY_ROWS = 10
    _BIOMASS_COLUMNS = {
        "Wood (KG)", "Bark (KG)", "Branch (KG)", "Foliage (KG)",
        "Stem (KG)", "Crown (KG)", "Total (KG)"
    }
    
    def __init__(
        self,
        controller,
        page: ft.Page,
        selected_file_path: Optional[str] = None
    ):
        self.controller = controller
        self.page = page
        self.selected_file_path = selected_file_path
        self.data = None
        self.is_button_disabled = False
        self.is_database_selected = False
        self.hardwood_softwood_dialog = None
        
        self._initialize_ui_components()
        self._setup_file_picker()
        
        print("Calculate_Biomass_View initialized")
    
    def _initialize_ui_components(self):
        """Initialize UI components."""
        self.selected_components_text = ft.Text(
            value="",
            color=ft.Colors.BLACK,
            weight=ft.FontWeight.W_500
        )
        
        self.component_cards_row = ft.Row(wrap=True)
        self.results_table_container = ft.Container(visible=False)
        
        
    
    def _setup_file_picker(self):
        """Setup file picker for export functionality."""
        self.file_picker = ft.FilePicker(on_result=self._on_file_save_result)
        self.page.overlay.append(self.file_picker)
    
    # -------------------------
    # MAIN LAYOUT
    # -------------------------
    
    def build(self) -> ft.Column:
        """Build the main view layout."""
        # Add ID to results container for scrolling
        self.results_table_container.id = "results_table_container"
        
        return ft.Column(
            controls=[
                self._create_equation_section(),
                self._create_components_section(),
                
                
                self._create_calculate_biomass_button(),
                
                self.results_table_container  # Initially hidden results table
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    
    def _create_calculate_biomass_button(self) -> Calculate_Biomass_Button:
        """Create the calculate biomass button."""
        return Calculate_Biomass_Button(
            on_click_callback=self.controller.on_calculate_biomass_click,   
            
            is_disabled=self.is_button_disabled
        ).create()
    # -------------------------
    # EQUATION SECTION
    # -------------------------
    
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
                title="DBH + Height-based",
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
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            padding=20,
            margin=30,
            border_radius=10,
            shadow=self._create_shadow(),
            content=ft.Column([
                self._create_section_header(
                    title="Equation Type",
                    description="Choose the calculation method for biomass estimation"
                ),
                radio_group
            ])
        )
    
    def _create_equation_card(
        self,
        title: str,
        formula: str,
        description: str,
        radio_value: str
    ) -> Equation_Type_Card:
        """Create an equation type card."""
        title_formula = ft.Column(
            controls=[
                Equation_Card_Title_Text(title),
                Equation_Card_Formula_Text(formula)
            ],
            spacing=2,
        )
        desc = Equation_Card_Description_Text(description)
        
        return Equation_Type_Card(title_formula, desc, radio_value)
    
    def on_equation_type_change(self, event):
        """Handle equation type selection change."""
        self.controller.set_equation_type(event.control.value)
    
    # -------------------------
    # COMPONENTS SECTION
    # -------------------------
    
    def _create_components_section(self) -> Select_Components_Widget:
        """Create the components selection section."""
        return Select_Components_Widget(
            page=self.page,
            title=TitleTextWidget("Select Tree Component"),
            description_text=DescriptionText("Select tree components for biomass calculation"),
            components_card_row=self.component_cards_row,
            selected_card_component=self.selected_components_text,
            components_data=COMPONENTS_DATA,
            is_database_selected=self.controller.get_database_selected_flag(),
        ).get_widget()
    
    def get_selected_components(self) -> List[str]:
        """Get currently selected components."""
        return [
            comp['title']
            for comp in COMPONENTS_DATA
            if comp['is_selected']
        ]
    
    # -------------------------
    # BIOMASS CALCULATE BUTTON STATES
    # -------------------------
   
    
    def _disable_calculation_button(self, button):
        """Disable the calculation button."""
        self.is_button_disabled = True
        button.bgcolor = "#CCCCCC"
        button.color = "#888888"
        button.disabled = True
        button.update()
    
    def _enable_calculation_button(self, button):
        """Enable the calculation button."""
        self.is_button_disabled = False
        button.bgcolor = ft.Colors.GREEN_700
        button.color = ft.Colors.WHITE
        button.disabled = False
        button.update()
    
    # -------------------------
    # SPECIES DIALOG
    # -------------------------
    
    async def show_species_code_dialog(self, missing_species_codes: List[str]):
        """Show dialog to select hardwood or softwood for missing species codes."""
        self.hardwood_softwood_dialog = HardwoodOrSoftwoodDialog(
            self.page,
            missing_species_codes
        )
        
        return await self.hardwood_softwood_dialog.show_species_code_dialog()
    
    # -------------------------
    # RESULTS TABLE
    # -------------------------
    
    def _show_results_table(self):
        """Create and display the results table."""
        results_table = self._create_results_table()
        self.results_table_container.content = results_table
        self.results_table_container.visible = True
        
        # Scroll to results
        self.page.scroll_to(
            key="results_table_container",
            duration=259,
            curve=ft.AnimationCurve.EASE_OUT
        )
        
        if self.page:
            self.page.update()
            print("Results table updated")
    
    def _create_results_table(self) -> ft.Container:
        """Create a table to display biomass results from JSON data."""
        # Load data
        data = self._load_results_data()
        if not data:
            return self._create_empty_results_message("No biomass results available")
        
        # Get first N rows
        display_data = data[:self._MAX_DISPLAY_ROWS]
        
        # Create table
        data_table = self._create_data_table(display_data)
        
        # Create buttons
        buttons_row = self._create_results_buttons()
        
        # Create scrollable table container
        scrollable_table = self._create_scrollable_table(data_table, len(data))
        
        # Wrap in final container
        return self._wrap_results_table(
            scrollable_table,
            buttons_row,
            len(data)
        )
    
    def _load_results_data(self) -> List[Dict]:
        """Load biomass results from JSON file."""
        try:
            if not os.path.exists(self._RESULTS_JSON_PATH):
                return []
            
            with open(self._RESULTS_JSON_PATH, 'r') as file:
                data = json.load(file)
                self.data = data
                return data
        
        except json.JSONDecodeError as error:
            logger.write(f"Error parsing results JSON: {error}")
            return []
        except Exception as error:
            logger.write(f"Error loading results: {error}")
            return []
    
    def _create_data_table(self, display_data: List[Dict]) -> ft.DataTable:
        """Create the data table with formatted rows."""
        if not display_data:
            return ft.DataTable()
        
        headers = list(display_data[0].keys())
        data_rows = []
        
        for item in display_data:
            cells = [
                ft.DataCell(self._format_table_cell(header, item.get(header)))
                for header in headers
            ]
            data_rows.append(ft.DataRow(cells=cells))
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text(header, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                )
                for header in headers
            ],
            rows=data_rows,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            horizontal_margin=10,
            heading_row_color=ft.Colors.GREEN_700,
            heading_row_height=40,
            data_row_color={ft.ControlState.HOVERED: ft.Colors.GREY_100},
            data_text_style=ft.TextStyle(color=ft.Colors.PRIMARY),
            show_checkbox_column=False,
        )
    
    def _format_table_cell(self, header: str, value: Any) -> ft.Text:
        """Format a table cell value for display."""
        if value is None:
            return ft.Text("N/A", color=ft.Colors.PRIMARY)
        
        if isinstance(value, (int, float)):
            if header in self._BIOMASS_COLUMNS:
                formatted_value = f"{value:.4f}"
            else:
                formatted_value = str(value)
        else:
            formatted_value = str(value)
        
        return ft.Text(formatted_value, color=ft.Colors.PRIMARY)
    
    def _create_results_buttons(self) -> ft.Row:
        """Create action buttons for results."""
        buttons = [
            self._create_view_chart_button(),
            self._create_export_button(),
        ]
        
        if self.controller.get_database_selected_flag():
            buttons.append(self._create_write_database_button())
        
        return ft.Row(buttons)
    
    def _create_view_chart_button(self) -> ft.ElevatedButton:
        """Create the View Chart button."""
        return ft.ElevatedButton(
            text="View Chart",
            icon=ft.Icons.BAR_CHART,
            bgcolor=ft.Colors.TERTIARY,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.page.run_task(self._on_view_chart_click, e),
            style=self._create_button_style()
        )
    
    def _create_export_button(self) -> ft.ElevatedButton:
        """Create the Export button."""
        return ft.ElevatedButton(
            text="Export to TXT",
            icon=ft.Icons.DOWNLOAD,
            bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE,
            on_click=self._on_export_click,
            style=self._create_button_style()
        )
    
    def _create_write_database_button(self) -> ft.ElevatedButton:
        """Create the Write to Database button."""
        return ft.ElevatedButton(
            text="Write to Database",
            icon=ft.Icons.STORAGE,
            bgcolor=ft.Colors.ORANGE_700,
            color=ft.Colors.WHITE,
            on_click=lambda e: self.page.run_task(
                
                self.controller._on_write_database_click, e
                                                  ),
            style=self._create_button_style()
        )
    
    def _create_button_style(self) -> ft.ButtonStyle:
        """Create a consistent button style."""
        return ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(10)),
            padding=ft.padding.symmetric(horizontal=20, vertical=10)
        )
    
    def _create_scrollable_table(
        self,
        data_table: ft.DataTable,
        total_records: int
    ) -> ft.Container:
        """Create a scrollable container for the data table."""
        return ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[data_table],
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            shadow=self._create_shadow(),
        )
    
    def _wrap_results_table(
        self,
        scrollable_table: ft.Container,
        buttons_row: ft.Row,
        total_records: int
    ) -> ft.Container:
        """Wrap the results table in a final container."""
        return ft.Container(
            border_radius=10,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            content=ft.Column([
                ft.Row([
                    TitleTextWidget("Calculated Biomass Results Table"),
                    buttons_row
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(
                    content=ft.Column([
                        self._create_results_info_row(total_records),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        scrollable_table
                    ])
                )
            ]),
            margin=ft.margin.all(20),
            padding=ft.padding.all(30),
            shadow=self._create_shadow(),
        )
    
    def _create_results_info_row(self, total_records: int) -> ft.Row:
        """Create information row for results table."""
        return ft.Row([
            DescriptionText(f"Showing first {self._MAX_DISPLAY_ROWS} of {total_records} records"),
            ft.Text(
                "← Scroll horizontally →",
                color=ft.Colors.GREEN_700,
                size=12,
                weight=ft.FontWeight.W_500
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def _create_empty_results_message(self, message: str) -> ft.Container:
        """Create a message container when no results are available."""
        return ft.Container(
            content=ft.Text(message, color=ft.Colors.GREY_600),
            padding=20
        )
    
    # -------------------------
    # CHART VIEWING
    # -------------------------
    
    async def _on_view_chart_click(self, event):
        """Handle View Chart button click."""
        print("View Chart button clicked")
        
        loading_spinner = Loading_Spinner_Widget(self.page)
        loading_spinner.show_dialog()
        
        await loading_spinner.simulate_progressive_loading(
            0.0, 0.2, 0.1, "Preparing Chart..."
        )
        
        species_data = self.controller._click_on_show_chart_button()
        self._show_biomass_chart(species_data)
        
        logger.write("Biomass chart displayed")
        await loading_spinner.simulate_progressive_loading(
            1.0, 1.0, 0.1, "Completed..."
        )
        loading_spinner.hide()
    
    def _show_biomass_chart(self, species_data):
        """Show biomass chart."""
        chart = Bar_Chart_Widget(self.page, species_data=species_data).build()
        logger.write("Biomass chart displayed")
        self.page.overlay.append(chart)
        self.page.update()
    
    
    # -------------------------
    # EXPORT FUNCTIONALITY
    # -------------------------
    
    def _on_export_click(self, event):
        """Handle export button click - open file save dialog."""
        default_filename = self._generate_export_filename()
        
        self.file_picker.save_file(
            dialog_title="Save Biomass Results",
            file_name=default_filename,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"]
        )
        
        logger.write("Export file dialog opened")
    
    def _generate_export_filename(self) -> str:
        """Generate filename with date and time prefix."""
        
        now = datetime.datetime.now()
        date_prefix = now.strftime("%Y%m%d")
        time_prefix = now.strftime("%H%M%S")
        
        if self.selected_file_path and os.path.isfile(self.selected_file_path):
            filename = os.path.splitext(
                os.path.basename(self.selected_file_path)
            )[0]
            result = f"Output_{filename}_{date_prefix}_{time_prefix}.txt"
            logger.write(f"Generated export filename: {result}")
            return result
        
        result = f"Output_Biomass_Results_{date_prefix}_{time_prefix}.txt"
        logger.write(f"Generated default export filename: {result}")
        return result
    
    def _on_file_save_result(self, event: ft.FilePickerResultEvent):
        """Handle file save dialog result."""
        if not event.path:
            logger.write("Export cancelled by user")
            return
        
        try:
            data = self._load_results_data()
            success = self.controller._export_to_text(data, event.path)
            
            if success:
                logger.write(f"Data exported successfully to {event.path}")
            else:
                logger.write(f"[Error] - Failed to export data to {event.path}")
        
        except Exception as error:
            logger.write(f"[Error] - Failed to export data: {error}")
    
   
    
    # -------------------------
    # HELPER METHODS
    # -------------------------
    
    def _create_section_header(self, title: str, description: str) -> ft.Container:
        """Create a consistent section header."""
        return ft.Container(
            margin=ft.margin.only(top=15, left=5, right=5, bottom=5),
            content=ft.Column([
                TitleTextWidget(title),
                DescriptionText(description),
            ]),
        )
    
    def _create_shadow(self) -> ft.BoxShadow:
        """Create consistent shadow for containers."""
        return ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
            offset=ft.Offset(0, 3),
        )
    
    def show_success_dialog(self, title: str, message: str):
        """Show success dialog."""
        Custom_Alert_Dialog(
            self.page,
            title_icon=ft.Icons.CHECK_CIRCLE,
            title_icon_color=ft.Colors.GREEN,
            title_color=ft.Colors.GREEN,
            title=title,
            message=message,
            button_text="OK",
        ).show()
        self.page.update()
    
    def show_error_dialog(self, title: str, message: str):
        """Show error dialog."""
        Custom_Alert_Dialog(
            self.page,
            title_icon=ft.Icons.ERROR,
            title_icon_color=ft.Colors.RED,
            title_color=ft.Colors.RED,
            title=title,
            message=message,
            button_text="OK",
        ).show()
        self.page.update()