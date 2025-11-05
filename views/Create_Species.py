import flet as ft
from widgets.Create_Label_With_Icon import Create_Label_With_Icon
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
from data.components_data_2 import COMPONENTS_DATA_2
from controller.Create_Species_Controller import Create_Species_Controller
from widgets.Select_Components_Widget import Select_Components_Widget

# 2. Main Form Control Class (No ft.UserControl inheritance)
class AddSpeciesForm:
    """The main application form, responsible for assembling the UI controls."""
    
    def __init__(self, controller: Create_Species_Controller):
        self._controller = controller
        self.selected_components_text = ft.Text(
            value="",
            color=ft.Colors.BLACK,
            weight=ft.FontWeight.W_500
        )
        self.component_cards_row = ft.Row(wrap=True)
        
        # Store parameter controls for dynamic visibility
        self.param_controls = {}
        self.parameters_section = None
        
        # Track current equation type
        self.current_equation_type = "DRH-based [Default]"
        
        # Store references for dialog
        self.page_ref = None
        self.dialog = None
    
    # --- UI Creation Helpers ---
    def _create_header(self):
        """Creates the header section."""
        return ft.Column(
            controls=[
                TitleTextWidget("Create Species"),
                DescriptionText("Create a new species to add it in the program"),
            ],
            spacing=5
    )

    def _create_species_row(self):
        """Creates the Code, Origin, and Equation Type row and stores controls in the controller."""
        
        # Species Code Control
        species_code_control = ft.TextField(hint_text="ABC123")
        self._controller.species_code_control = species_code_control # Store in controller
        species_code_form = ft.Column([
            Create_Label_With_Icon(label_text="Species Code", icon_src="./assets/images/key.png"),
            species_code_control
        ])

        # Origin Dropdown Control
        origin_control = ft.Dropdown(
            options=[
                ft.dropdown.Option("Natural Stand"),
                ft.dropdown.Option("Plantation"),
            ],
            value="Natural Stand", # Default Value
            content_padding=ft.padding.only(left=8, right=8),
            border_radius=5,
        )
        self._controller.origin_control = origin_control # Store in controller
        origin_form = ft.Column([
            Create_Label_With_Icon(label_text="Select Origin", icon_src="./assets/images/origin.png"),
            origin_control
        ])

        # Equation Type Dropdown Control
        equation_type_control = ft.Dropdown(
            options=[
                ft.dropdown.Option("DRH-based [Default]"),
                ft.dropdown.Option("Height-based"),
            ],
            value="DRH-based [Default]",
            content_padding=ft.padding.only(left=8, right=8),
            border_radius=5,
            on_change=self._on_equation_type_change  # Add change handler
        )
        self._controller.equation_type_control = equation_type_control # Store in controller
        equation_form = ft.Column([
            Create_Label_With_Icon(label_text="Equation Type", icon_src="./assets/images/calculating.png"),
            equation_type_control
        ])

        return ft.Row(
            controls=[
                ft.Container(content=species_code_form, padding=ft.padding.only(top=10), alignment=ft.alignment.center,),
                ft.Container(content=origin_form, padding=ft.padding.only(top=10)),
                ft.Container(content=equation_form, padding=ft.padding.only(top=10)),
            ],
            spacing=20,
        )
    
    def _on_equation_type_change(self, e):
        """Handle equation type change and update parameters visibility"""
        self.current_equation_type = e.control.value
        # Update parameters based on current selection
        selected_components = self._get_current_selected_components()
        self.update_parameters_visibility(selected_components)
    
    def _get_current_selected_components(self):
        """Get currently selected components from the widget"""
        selected_components = []
        for component in COMPONENTS_DATA_2:
            if component.get("is_selected", False):
                selected_components.append(component["title"])
        return selected_components
    
    def create_component_card_view(self, item: dict, on_hover_handler: callable, on_click_handler: callable) -> ft.Container:
        """
        Creates and returns the Flet Container control for a single component card.
        It links the visual component to the Controller's event handlers.
        """
        
        title = item.get("title", "Unknown")
        image_src = item.get("image_src", "./assets/images/default.png")
        is_selected = item.get("is_selected", False) # Get current state from Model data

        # Initial appearance based on state
        initial_bgcolor = "#A3FFDA" if is_selected else "white" 

        # Create and configure the ft.Container
        return ft.Container(
            # The data property is crucial for the controller to identify which card was clicked/hovered
            data=title,
            # Set initial visual state
            bgcolor=initial_bgcolor, 
            
            margin=10,
            padding=10,
            width=150,
            height=150,
            
            # Attach controller methods
            on_hover=on_hover_handler,
            on_click=on_click_handler, # <-- This is where the Controller's logic is attached
            
            # Styling and animation
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
                offset=ft.Offset(0, 3),
            ),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),

            # Card Content Layout
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Image(
                        src=image_src,
                        width=50,
                        height=50,
                        fit=ft.ImageFit.CONTAIN,
                        repeat=ft.ImageRepeat.NO_REPEAT,
                        border_radius=ft.border_radius.all(10),
                    ),
                    ft.Text(title, color="black", font_family="Arial", size=18, weight=ft.FontWeight.W_600)
                ]
            )
        )
    
    def _create_components_section(self):
        """Creates the component selection row using the functional component."""
        
        components_header = ft.Row([
            ft.Text("Tree Components", size=16, weight=ft.FontWeight.BOLD),
            ft.Icon(ft.Icons.APPS_OUTLINED)
        ], spacing=5)
        
        card_controls = []
        
        # Get the component data list (the Model state) from the controller
        component_data_list = self._controller.get_component_data() # Assuming this method exists
        
        # Iterate over the data dictionary, not a separate controller object
        for item in component_data_list: 
            
            # Use the imported function (renamed to create_component_card_view)
            card_view = self.create_component_card_view(
                item=item,
                # Attach the controller's event handlers directly
                on_click_handler=self._controller.handle_component_click, 
                on_hover_handler=self._controller.handle_component_hover
            )
            card_controls.append(card_view)
            
        components_row = ft.Row(
            controls=card_controls,
            spacing=10,
            wrap=True
        )
        
        return ft.Column(
            controls=[
                components_header,
                components_row
            ],
            spacing=10
        )
    
    def _create_components_section_alt(self):
        """Creates the component selection row using ComponentCardView."""
        
        components_header = ft.Row([
            ft.Text("Tree Components", size=16, weight=ft.FontWeight.BOLD),
            ft.Icon(ft.Icons.APPS_OUTLINED)
        ], spacing=5)
        
        card_controls = []
        for item in self._controller.get_initial_component_data():
            label = item["title"]
            icon = item["image_src"]
            initial_selected = label in self._controller.selected_components
            
            # 1. Create the ComponentCardController instance
            card_controller = self._controller.create_card_controller(
                label=label, 
                icon=icon, 
                initial_selected=initial_selected
            )
            
            # 2. Get the Flet control (View) and link it to the Controller
            card_view = self.create_component_card_view(
                item=item,
                # Attach the controller's event handlers directly
                on_click_handler=self._controller._handle_component_click, 
                on_hover_handler=self._controller._handle_component_click
            )
            card_controls.append(card_view)
            
        components_row = ft.Row(
            controls=card_controls,
            spacing=10,
            wrap=True
        )
        
        return ft.Column(
            controls=[
                components_header,
                components_row
            ],
            spacing=10
        )
    
    def _param_input(self, label: str):
        """Helper for parameter input fields with validation."""
        
        control = ft.TextField(
            label=label,
            value="0.00",
            height=40,
            content_padding=5,
            border_radius=5,
            keyboard_type=ft.KeyboardType.NUMBER,
            # Link on_change to the controller's validation method
            on_change=self._controller.param_input_validation, 
            error_text=None, 
            max_lines=1
        )
        # Store a reference to the Flet control in the Controller for state/validation access
        self._controller.param_controls[label] = control
        return control

    def _create_parameters_section(self):
        """Creates the parameter input fields section."""
        
        parameters_header = ft.Row([
            ft.Text("Parameters", size=16, weight=ft.FontWeight.BOLD),
            ft.Icon(ft.Icons.SETTINGS)
        ], spacing=5)

        # Create all parameter controls for both equation types
        # DBH-based parameters (b1, b2)
        wood_b1 = self._param_input("b1 (Wood)")
        wood_b2 = self._param_input("b2 (Wood)")
        bark_b1 = self._param_input("b1 (Bark)")
        bark_b2 = self._param_input("b2 (Bark)")
        branch_b1 = self._param_input("b1 (Branch)")
        branch_b2 = self._param_input("b2 (Branch)")
        foliage_b1 = self._param_input("b1 (Foliage)")
        foliage_b2 = self._param_input("b2 (Foliage)")
        crown_b1 = self._param_input("b1 (Crown)")
        crown_b2 = self._param_input("b2 (Crown)")
        stem_b1 = self._param_input("b1 (Stem)")
        stem_b2 = self._param_input("b2 (Stem)")
        total_b1 = self._param_input("b1 (Total)")
        total_b2 = self._param_input("b2 (Total)")

        # DBH+Height-based parameters (b1, b2, b3)
        wood_b3 = self._param_input("b3 (Wood)")
        bark_b3 = self._param_input("b3 (Bark)")
        branch_b3 = self._param_input("b3 (Branch)")
        foliage_b3 = self._param_input("b3 (Foliage)")
        crown_b3 = self._param_input("b3 (Crown)")
        stem_b3 = self._param_input("b3 (Stem)")
        total_b3 = self._param_input("b3 (Total)")

        # Store references for dynamic visibility
        self.param_controls = {
            "DBH-based": {
                "Wood": [wood_b1, wood_b2],
                "Bark": [bark_b1, bark_b2],
                "Branch": [branch_b1, branch_b2],
                "Foliage": [foliage_b1, foliage_b2],
                "Crown": [crown_b1, crown_b2],
                "Stem": [stem_b1, stem_b2],
                "Total": [total_b1, total_b2]
            },
            "Height-based": {
                "Wood": [wood_b1, wood_b2, wood_b3],
                "Bark": [bark_b1, bark_b2, bark_b3],
                "Branch": [branch_b1, branch_b2, branch_b3],
                "Foliage": [foliage_b1, foliage_b2, foliage_b3],
                "Crown": [crown_b1, crown_b2, crown_b3],
                "Stem": [stem_b1, stem_b2, stem_b3],
                "Total": [total_b1, total_b2, total_b3]
            }
        }

        # Initially hide all parameters
        for equation_type in self.param_controls.values():
            for component_params in equation_type.values():
                for param in component_params:
                    param.visible = False

        # Create parameter rows with more spacing
        parameters_row1 = ft.Row(
            controls=[
                ft.Container(content=wood_b1, expand=True),
                ft.Container(content=wood_b2, expand=True),
                ft.Container(content=wood_b3, expand=True),
            ],
            spacing=20
        )
        
        parameters_row2 = ft.Row(
            controls=[
                ft.Container(content=bark_b1, expand=True),
                ft.Container(content=bark_b2, expand=True),
                ft.Container(content=bark_b3, expand=True),
            ],
            spacing=20
        )
        
        parameters_row3 = ft.Row(
            controls=[
                ft.Container(content=branch_b1, expand=True),
                ft.Container(content=branch_b2, expand=True),
                ft.Container(content=branch_b3, expand=True),
            ],
            spacing=20
        )
        
        parameters_row4 = ft.Row(
            controls=[
                ft.Container(content=foliage_b1, expand=True),
                ft.Container(content=foliage_b2, expand=True),
                ft.Container(content=foliage_b3, expand=True),
            ],
            spacing=20
        )
        
        parameters_row5 = ft.Row(
            controls=[
                ft.Container(content=crown_b1, expand=True),
                ft.Container(content=crown_b2, expand=True),
                ft.Container(content=crown_b3, expand=True),
            ],
            spacing=20
        )
        
        parameters_row6 = ft.Row(
            controls=[
                ft.Container(content=stem_b1, expand=True),
                ft.Container(content=stem_b2, expand=True),
                ft.Container(content=stem_b3, expand=True),
            ],
            spacing=20
        )
        
        parameters_row7 = ft.Row(
            controls=[
                ft.Container(content=total_b1, expand=True),
                ft.Container(content=total_b2, expand=True),
                ft.Container(content=total_b3, expand=True),
            ],
            spacing=20
        )
        
        return ft.Column(
            controls=[
                parameters_header,
                ft.Container(height=15),  # Extra space
                parameters_row1,
                ft.Container(height=10),  # Extra space between rows
                parameters_row2,
                ft.Container(height=10),
                parameters_row3,
                ft.Container(height=10),
                parameters_row4,
                ft.Container(height=10),
                parameters_row5,
                ft.Container(height=10),
                parameters_row6,
                ft.Container(height=10),
                parameters_row7,
            ],
            spacing=5
        )

    def update_parameters_visibility(self, selected_components):
        """Update parameter visibility based on selected components and equation type."""
        print(f"Updating parameters for: {selected_components} with equation: {self.current_equation_type}")
        
        # Determine which equation type to use
        equation_key = "DBH-based" if "DRH-based" in self.current_equation_type else "Height-based"
        
        # Hide all parameters first
        for equation_type in self.param_controls.values():
            for component_params in equation_type.values():
                for param in component_params:
                    param.visible = False
        
        # Show parameters for selected components based on equation type
        for component in selected_components:
            if component in self.param_controls[equation_key]:
                for param in self.param_controls[equation_key][component]:
                    param.visible = True
        
        # Update the UI
        if self.parameters_section:
            self.parameters_section.update()

    def _show_confirmation_dialog(self, e, page:ft.Page):
        """Show confirmation dialog with preview of selected items"""
        print("Create Species button clicked!")
        
        
        # Get selected components
        selected_components = self._get_current_selected_components()
        
        # Get equation type
        equation_type = self.current_equation_type
        
        # Get parameter values
        param_values = {}
        for param_name, control in self._controller.param_controls.items():
            if hasattr(control, 'visible') and control.visible:
                param_values[param_name] = control.value
        
        # Create dialog content
        dialog_content = ft.Column(
            controls=[
                ft.Text("Confirm Species Creation", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                
                ft.Text("Selected Components:", weight=ft.FontWeight.BOLD),
                ft.Text(", ".join(selected_components) if selected_components else "No components selected"),
                
                ft.Divider(height=15),
                
                ft.Text("Equation Type:", weight=ft.FontWeight.BOLD),
                ft.Text(equation_type),
                
                ft.Divider(height=15),
                
                ft.Text("Parameters:", weight=ft.FontWeight.BOLD),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )
        
        # Add parameter values to dialog
        for param_name, value in param_values.items():
            dialog_content.controls.append(
                ft.Row([
                    ft.Text(f"{param_name}:", width=120),
                    ft.Text(value or "0.00")
                ])
            )
        
        # If no parameters, show message
        if not param_values:
            dialog_content.controls.append(ft.Text("No parameters configured"))
        
        # Create dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Species Creation"),
            content=dialog_content,
            actions=[
                ft.TextButton("Cancel", on_click=self._close_dialog),
                ft.ElevatedButton(
                    "Proceed", 
                    on_click=self._proceed_with_creation,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(self.dialog)
        # Open dialog - FIXED APPROACH
        if self.page_ref:
            self.page_ref.dialog = self.dialog
            self.dialog.open = True
            self.page_ref.update()
            print("Dialog opened successfully")
        else:
            print("ERROR: page_ref is None - trying alternative approach")
            # Alternative approach - get page from the event
            try:
                page = e.control.page
                page.dialog = self.dialog
                self.dialog.open = True
                page.update()
                print("Dialog opened via event approach")
            except Exception as ex:
                print(f"Failed to open dialog: {ex}")

    def _close_dialog(self, e):
        """Close the dialog"""
        if self.dialog:
            self.dialog.open = False
            if self.page_ref:
                self.page_ref.update()
            print("Dialog closed")

    def _proceed_with_creation(self, e):
        """Proceed with species creation"""
        print("Proceeding with species creation...")
        self._close_dialog(e)
        # Call the original controller submit method
        self._controller.handle_submit(None)

    def _create_submit_button(self, page: ft.Page):
        """Creates the submit button, linked to the confirmation dialog."""
        return ft.Row(
            [
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("Create Species", size=16, weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.ADD, size=20)
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                    # Link to confirmation dialog instead of direct submit
                    on_click=lambda e: self._show_confirmation_dialog(e, page), 
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE,
                    height=40,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def on_component_selection_change(self, selected_components):
        """Callback function when component selection changes"""
        self.update_parameters_visibility(selected_components)

    def build(self, page=None):
        """Build the form and store page reference for dialogs"""
        self.page_ref = page
        self.component_cards_row = ft.Row(wrap=True)
        
        # Create parameters section and store reference
        self.parameters_section = self._create_parameters_section()
        
        return ft.Container(
            expand=True,  # Expand to fill available space
            alignment=ft.alignment.center,  # Center the content inside the container
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self._create_header(),
                        ft.Divider(color=ft.Colors.GREY_300, height=30),  # More space

                        self._create_species_row(),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),  # More space
                        
                        Select_Components_Widget(
                            title=TitleTextWidget("Select Component"),
                            description_text=DescriptionText("Select tree components for biomass calculation"),
                            components_card_row=self.component_cards_row,
                            selected_card_component=self.selected_components_text,
                            components_data=COMPONENTS_DATA_2, # Pass the data,
                            displayButton=False,
                            displayShadow=False,
                            on_selection_change=self.on_component_selection_change  # Add callback
                        ),
                        
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),  # More space
                        self.parameters_section,  # Use the stored reference
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),  # More space
                        self._create_submit_button(page=page),
                        ft.Container(height=20)  # Extra space at bottom
                    ],
                    scroll=ft.ScrollMode.AUTO,  # Enable scrolling
                ),
                margin=30,
                padding=40,
                border_radius=15,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.Colors.BLACK12,
                    offset=ft.Offset(0, 5),
                ),
            )
        )