import flet as ft
# Assuming data.components_data and the other imports are available
from data.components_data import COMPONENTS_DATA 
# Note: The original file did not include the import for the Controller used inside.
# We will define the ComponentCardController here, or assume it's imported if in a separate file.
from model.Create_Species_Model import Create_Species_Model
class ComponentCardController:
    """
    Manages the state and update logic for a single species component card.
    The visual control (ft.Container) is updated directly by this class's method.
    """
    def __init__(self, label: str, icon: str, initial_selected: bool, on_click_handler):
        self.label = label
        self.icon = icon
        self._is_selected = initial_selected
        self._on_click_handler = on_click_handler
    
    @property
    def is_selected(self) -> bool:
        return self._is_selected

    def handle_click(self, e: ft.ControlEvent):
        """Internal handler to proxy the click event to the main form controller."""
        # The main controller handles the state toggle and calls set_selected later.
        self._on_click_handler(e, self.label) 

    def set_selected(self, is_selected: bool, card_control: ft.Container):
        """Updates the card's visual state (the Flet control) based on the new selection status."""
        self._is_selected = is_selected
        
        # Manually set the properties of the raw Flet control based on new state
        card_control.bgcolor = ft.Colors.GREEN_100 if is_selected else ft.Colors.WHITE
        card_control.border = ft.border.all(2, ft.Colors.GREEN_400 if is_selected else ft.Colors.BLACK12)
        
        # Manually trigger update on the control to redraw
        card_control.update()


class Create_Species_Controller:
    """
    The main application controller, managing the overall form state, 
    validation, and submission flow.
    """
    def __init__(self):
        # Component Data Model
        self._components_data = [item.copy() for item in COMPONENTS_DATA]
       
        # Initial State (Model)
        self.selected_components = [item["title"] for item in self._components_data if item["title"]]
        
        # Storage for the ComponentCardController instances 
        self.card_instances: dict[str, ComponentCardController] = {} 
        # Storage for parameter input controls (set by the View)
        self.param_controls: dict[str, ft.TextField] = {}
        # Storage for main input controls (set by the View)
        self.species_code_control: ft.TextField = None
        self.origin_control: ft.Dropdown = None
        self.equation_type_control: ft.Dropdown = None

    # --- Core Logic ---
    def get_initial_component_data(self):
        """Exposes the raw data to the View for initial card creation."""
        return self._components_data
        
    def create_card_controller(self, label: str, icon: str, initial_selected: bool):
        """
        Creates and stores a controller for a single component card. 
        **Utilizes the ComponentCardController.**
        """
        card_controller = ComponentCardController(
            label=label, 
            icon=icon, 
            initial_selected=initial_selected, 
            # The main controller's method is passed as the handler
            on_click_handler=self._handle_component_click 
        )
        self.card_instances[label] = card_controller
        return card_controller

    # --- Event Handlers ---
    def _handle_component_click(self, e: ft.ControlEvent, label: str):
        """Toggles component selection and updates both state and visual representation."""
        
        is_currently_selected = label in self.selected_components
        
        if is_currently_selected:
            self.selected_components.remove(label)
            new_state = False
        else:
            self.selected_components.append(label)
            new_state = True
            
        # 1. Get the card's dedicated controller
        card_controller = self.card_instances[label]
        
        # 2. Instruct the card's controller to update its visual state.
        # The Flet control (e.control) is passed so the card controller can call .update() on it.
        card_controller.set_selected(new_state, card_control=e.control)

    def _run_validation_logic(self, control: ft.TextField, input_value: str):
        """Core logic to check parameter value range and format."""
        stripped_value = input_value.strip()
        
        if not stripped_value:
            control.error_text = None
        else:
            try:
                value = float(stripped_value)
                if -5.0 <= value <= 5.0:
                    control.error_text = None
                else:
                    control.error_text = "Value must be between -5.0 and 5.0"
            except ValueError:
                control.error_text = "Invalid number format"

    def param_input_validation(self, e: ft.ControlEvent):
        """Validates the input value on change (called from View)."""
        self._run_validation_logic(e.control, e.control.value)
        e.control.update()
        
    def _is_form_valid(self) -> bool:
        """Checks if all required fields are valid."""
        self.model = Create_Species_Model(self.species_code_control)
        self.model.set_species_code_control( self.species_code_control.value)

        is_species_code_control_value = self.model.is_species_control_valid()

        if is_species_code_control_value == False:
            print("FALSING")
            self.model.get_species_code_control().error_text = "Species Code is invalid."
            self.model.get_species_code_control().update()
        else:
            self.model.get_species_code_control().error_text = None
            self.model.get_species_code_control().update()

        # 2. Check all parameter inputs
        is_valid = True
        for name, control in self.param_controls.items():
            self._run_validation_logic(control, control.value)
            control.update() 
            if control.error_text:
                is_valid = False
        
        return is_valid

    # --- Modal Logic ---
    def create_modal(self) -> ft.AlertDialog:
        """Creates the confirmation modal with current form data."""
        
        def create_data_row(label, value):
            return ft.Row(
                [
                    ft.Text(label, weight=ft.FontWeight.BOLD, size=14, width=150),
                    ft.Text(value, size=14, color=ft.Colors.BLACK87, expand=True)
                ]
            )

        param_table_data = []
        for label in self.param_controls.keys():
            param_table_data.append(
                ft.Row([
                    ft.Text(label, size=14, color=ft.Colors.BLACK54, width=150),
                    ft.Text(self.param_controls[label].value, size=14, color=ft.Colors.BLACK, expand=True)
                ])
            )

        content = ft.Column(
            [
                ft.Text("Species Preview Information", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10),
                create_data_row("Species Code:", self.species_code_control.value if self.species_code_control else "N/A"),
                create_data_row("Select Origin:", self.origin_control.value if self.origin_control else "N/A"),
                create_data_row("Equation Type:", self.equation_type_control.value if self.equation_type_control else "N/A"),
                ft.Divider(height=10),
                create_data_row("Components Selected:", ", ".join(self.selected_components)),
                ft.Divider(height=10),
                ft.Text("Parameters:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                *param_table_data, 
                ft.Divider(height=20),
                ft.Text("Do you wish to proceed with adding this species?", size=14, weight=ft.FontWeight.W_500),

            ],
            tight=True,
            spacing=5
        )

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Species Details"),
            content=ft.Container(content, width=400),
            actions=[
                ft.TextButton("Cancel", on_click=self._close_modal),
                ft.ElevatedButton(
                    "Proceed & Add", 
                    bgcolor=ft.Colors.GREEN_700, 
                    color=ft.Colors.WHITE,
                    on_click=self._confirm_and_add
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return modal

    def _open_modal(self, e: ft.ControlEvent):
        """Opens the modal dialog."""
        page = ft.Page()
        modal = self.create_modal()
        page.dialog = modal
        page.dialog.open = True
        page.update()
        
    def _close_modal(self, e: ft.ControlEvent):
        """Closes the modal dialog."""
        e.page.dialog.open = False
        e.page.update()

    def _confirm_and_add(self, e: ft.ControlEvent):
        """Final submission logic after modal confirmation."""
        self._close_modal(e)
        print("Species Confirmed and Added to Database!")
        e.page.snack_bar = ft.SnackBar(
            ft.Text(f"Species {self.species_code_control.value} added successfully!", color=ft.Colors.WHITE), 
            bgcolor=ft.Colors.GREEN_600
        )
        e.page.snack_bar.open = True
        e.page.update()

    def handle_submit(self, e: ft.ControlEvent):
        """Main button click handler - validates form and opens modal."""
        try:
            if self._is_form_valid():
                self._open_modal(e)
            else:
                e.page.open (ft.SnackBar(
                    ft.Text("Please correct the errors in the form before submitting.", color=ft.Colors.BLACK),
                    bgcolor=ft.Colors.RED_600
                ))
                e.page.update()
        except:
            print("Error")