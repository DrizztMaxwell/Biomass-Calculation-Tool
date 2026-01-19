import json
from sys import prefix
import flet as ft
import pandas as pd
from widgets.Create_Species_Preview_Modal import Create_Species_Preview_Modal
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
from widgets.Create_Label_With_Icon import Create_Label_With_Icon
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
from data.components_data_2 import COMPONENTS_DATA_2
from controller.Create_Species_Controller import Create_Species_Controller
from widgets.Select_Components_Widget import Select_Components_Widget
from widgets.Create_Title_And_Description_Widget import Create_Title_And_Description_Widget

class Create_Species_View:
    """The main application form, responsible for assembling the UI controls."""
    
    def __init__(self, page:ft.Page, controller: Create_Species_Controller):
        self.page = page
        self._controller = controller
        self.selected_components_text = ft.Text(
            value="",
            color=ft.Colors.PRIMARY,
            weight=ft.FontWeight.W_500
        )
        # Store parameter controls for dynamic visibility
        self.param_controls = {}
        self.parameters_section = None
        
        # Track current equation type
        self.current_equation_type = "DBH-based"
        
        # Store references for dialog
        self.page_ref = None
        self.dialog = None
        self.error_messages = []
        self.species_textfield = None
        self.origin_dropdown = None
        self.equation_type_dropdown = None
        self.create_species_preview_modal = Create_Species_Preview_Modal(page,{}, callback=self._handle_create_species_button_click)

    def _create_species_metadata_row(self) -> ft.Row:
        """Creates the Code, Origin, and Equation Type row and stores controls in the controller."""
        
        # Common width for all form elements to ensure equal sizing
        FORM_ELEMENT_WIDTH = 300
        
        # Species Code Control with expanded width for error text
        self.species_textfield = ft.TextField(
            hint_text="Alpine fir or 123",
            width=FORM_ELEMENT_WIDTH,  # Fixed width
             border_color=ft.Colors.PRIMARY,
        )
        
        species_container = ft.Container(
            content=ft.Column([
                Create_Label_With_Icon(label_text="Species (Code or Name)", icon_src="./assets/images/key.png"),
                self.species_textfield
            ], width=FORM_ELEMENT_WIDTH),
            padding=ft.padding.only(top=10),
            alignment=ft.alignment.center,
        )

        # Origin Dropdown Control
        self.origin_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("Natural Stand"),
                ft.dropdown.Option("Plantation"),
            ],
            value="Natural Stand",  # Default Value
            content_padding=ft.padding.only(left=8, right=8),
            border_radius=5,
            border_color=ft.Colors.PRIMARY,
            width=FORM_ELEMENT_WIDTH,  # Same width
         
        )
        
        origin_container = ft.Container(
            content=ft.Column([
                Create_Label_With_Icon(label_text="Select Origin", icon_src="./assets/images/origin.png"),
                self.origin_dropdown
            ], width=FORM_ELEMENT_WIDTH),
            padding=ft.padding.only(top=10),
        )

        # Equation Type Dropdown Control
        self.equation_type_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("DBH-based"),
                ft.dropdown.Option("DBH + Height-based"),
            ],
            value="DBH-based",
            content_padding=ft.padding.only(left=8, right=8),
            border_radius=5,
            on_change=self._on_equation_type_change,  # Add change handler
            width=FORM_ELEMENT_WIDTH,  # Same width
            border_color=ft.Colors.PRIMARY,
        )
        self._controller.equation_type_control = self.equation_type_dropdown  # Store in controller
        
        equation_container = ft.Container(
            content=ft.Column([
                Create_Label_With_Icon(label_text="Equation Type", icon_src="./assets/images/calculating.png"),
                self.equation_type_dropdown
            ], width=FORM_ELEMENT_WIDTH),
            padding=ft.padding.only(top=10),
        )

        return ft.Row(
            controls=[
                species_container,
                origin_container,
                equation_container,
            ],
            spacing=20,
           
        )
    
    def _on_equation_type_change(self, e):
        """Handle equation type change and update parameters visibility"""
        self.current_equation_type = e.control.value
        # Update parameters based on current selection
        selected_components = self._get_current_selected_components()
        self.selected_components = selected_components
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
            height=50,
            width=120,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=5,
            keyboard_type=ft.KeyboardType.NUMBER,
            error_text=None,
            max_lines=1,
            text_align=ft.TextAlign.CENTER,
            # Styling
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
           
            border_color=ft.Colors.PRIMARY,
            focused_border_color=ft.Colors.PRIMARY,
            focused_border_width=2,
            border_width=1,
       
            # Label styling
            label_style=ft.TextStyle(
                size=12,
                weight=ft.FontWeight.W_500,
                color=ft.Colors.PRIMARY,
            ),
            # Error styling
            error_style=ft.TextStyle(
                size=11,
                color=ft.Colors.RED_600
            ),
            # Hint text
            hint_text="0.00",
            hint_style=ft.TextStyle(
                size=13,
                color=ft.Colors.ON_PRIMARY_CONTAINER
            ),
        )
        
        # Store a reference to the Flet control in the Controller for state/validation access
        self.param_controls[label] = control
        return control

    def _create_parameters_section(self):
        """Creates the parameter input fields section with component labels."""
        self.no_parameters = ft.Text("No Components selected.")
        parameters_header = ft.Row([
            TitleTextWidget("Parameters"),
            ft.Icon(ft.Icons.SETTINGS)
        ], spacing=5)

        # Create all parameter controls for both equation types
        # DBH-based parameters (b1, b2)
        wood_b1 = self._param_input("b1")
        wood_b2 = self._param_input("b2")
        bark_b1 = self._param_input("b1")
        bark_b2 = self._param_input("b2")
        branch_b1 = self._param_input("b1")
        branch_b2 = self._param_input("b2")
        foliage_b1 = self._param_input("b1")
        foliage_b2 = self._param_input("b2")
        crown_b1 = self._param_input("b1")
        crown_b2 = self._param_input("b2")
        stem_b1 = self._param_input("b1")
        stem_b2 = self._param_input("b2")
        total_b1 = self._param_input("b1")
        total_b2 = self._param_input("b2")

        # DBH+Height-based parameters (b1, b2, b3)
        wood_b3 = self._param_input("b3")
        bark_b3 = self._param_input("b3")
        branch_b3 = self._param_input("b3")
        foliage_b3 = self._param_input("b3")
        crown_b3 = self._param_input("b3")
        stem_b3 = self._param_input("b3")
        total_b3 = self._param_input("b3")

        # Create component labels
        wood_label = ft.Text("Wood", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_PRIMARY_CONTAINER)
        bark_label = ft.Text("Bark", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_PRIMARY_CONTAINER)
        branch_label = ft.Text("Branch", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_PRIMARY_CONTAINER)
        foliage_label = ft.Text("Foliage", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_PRIMARY_CONTAINER)
        crown_label = ft.Text("Crown", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_PRIMARY_CONTAINER)
        stem_label = ft.Text("Stem", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_PRIMARY_CONTAINER)
        total_label = ft.Text("Total", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_PRIMARY_CONTAINER)

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
            "DBH + Height-based": {
                "Wood": [wood_b1, wood_b2, wood_b3],
                "Bark": [bark_b1, bark_b2, bark_b3],
                "Branch": [branch_b1, branch_b2, branch_b3],
                "Foliage": [foliage_b1, foliage_b2, foliage_b3],
                "Crown": [crown_b1, crown_b2, crown_b3],
                "Stem": [stem_b1, stem_b2, stem_b3],
                "Total": [total_b1, total_b2, total_b3]
            }
        }

        # Store label references for visibility control
        self.param_labels = {
            "Wood": wood_label,
            "Bark": bark_label,
            "Branch": branch_label,
            "Foliage": foliage_label,
            "Crown": crown_label,
            "Stem": stem_label,
            "Total": total_label
        }

        # Initially hide all parameters and labels
        for equation_type in self.param_controls.values():
            for component_params in equation_type.values():
                for param in component_params:
                    param.visible = False
        
        for label in self.param_labels.values():
            label.visible = False

        # Initially show "no parameters" message
        self.no_parameters.visible = True

        # Create parameter rows with component labels and parameters
        wood_section = ft.Column([
            wood_label,
            ft.Row([
                ft.Container(content=wood_b1, expand=True),
                ft.Container(content=wood_b2, expand=True),
                ft.Container(content=wood_b3, expand=True),
            ], spacing=20)
        ], spacing=10)
        
        bark_section = ft.Column([
            bark_label,
            ft.Row([
                ft.Container(content=bark_b1, expand=True),
                ft.Container(content=bark_b2, expand=True),
                ft.Container(content=bark_b3, expand=True),
            ], spacing=20)
        ], spacing=10)
        
        branch_section = ft.Column([
            branch_label,
            ft.Row([
                ft.Container(content=branch_b1, expand=True),
                ft.Container(content=branch_b2, expand=True),
                ft.Container(content=branch_b3, expand=True),
            ], spacing=20)
        ], spacing=10)
        
        foliage_section = ft.Column([
            foliage_label,
            ft.Row([
                ft.Container(content=foliage_b1, expand=True),
                ft.Container(content=foliage_b2, expand=True),
                ft.Container(content=foliage_b3, expand=True),
            ], spacing=20)
        ], spacing=10)
        
        crown_section = ft.Column([
            crown_label,
            ft.Row([
                ft.Container(content=crown_b1, expand=True),
                ft.Container(content=crown_b2, expand=True),
                ft.Container(content=crown_b3, expand=True),
            ], spacing=20)
        ], spacing=10)
        
        stem_section = ft.Column([
            stem_label,
            ft.Row([
                ft.Container(content=stem_b1, expand=True),
                ft.Container(content=stem_b2, expand=True),
                ft.Container(content=stem_b3, expand=True),
            ], spacing=20)
        ], spacing=10)
        
        total_section = ft.Column([
            total_label,
            ft.Row([
                ft.Container(content=total_b1, expand=True),
                ft.Container(content=total_b2, expand=True),
                ft.Container(content=total_b3, expand=True),
            ], spacing=20)
        ], spacing=10)
        
        return ft.Column(
            controls=[
                parameters_header,
                ft.Container(height=15),
                self.no_parameters,
                ft.Container(height=15),
                wood_section,
                ft.Container(height=15),
                bark_section,
                ft.Container(height=15),
                branch_section,
                ft.Container(height=15),
                foliage_section,
                ft.Container(height=15),
                crown_section,
                ft.Container(height=15),
                stem_section,
                ft.Container(height=15),
                total_section,
            ],
            spacing=5
        )

    def update_parameters_visibility(self, selected_components):
        """Update parameter visibility based on selected components and equation type."""
        print(f"Updating parameters for: {selected_components} with equation: {self.current_equation_type}")
        
        # Determine which equation type to use
        equation_key = "DBH-based" if "DBH-based" in self.current_equation_type else "DBH + Height-based"
        
        # Hide all parameters and labels first
        any_visible = False
        for equation_type in self.param_controls.values():
            for component_params in equation_type.values():
                for param in component_params:
                    param.visible = False
        
        for label in self.param_labels.values():
            label.visible = False
        
        # Show parameters and labels for selected components based on equation type
        for component in selected_components:
            if component in self.param_controls[equation_key]:
                # Show component label
                if component in self.param_labels:
                    self.param_labels[component].visible = True
                
                # Show parameters
                for param in self.param_controls[equation_key][component]:
                    param.visible = True
                    any_visible = True
        
        # Update "no parameters" text visibility
        self.no_parameters.visible = not any_visible
        
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



        if equation_type in self.param_controls:
            components = self.param_controls[equation_type]
            for component_name, controls_list in components.items():
                for control in controls_list:
                    if control.visible:
                        param_key = f"{equation_type}_{component_name}_{control.label}"
                        param_values[param_key] = control.value
                        print(f"Parameter {param_key}: {control.value}")
        
        if not self._controller._is_form_valid():
            print("Form is not valid, cannot show preview modal.")
            return
        ###
        self.create_species_preview_modal.species_data = {
             "species_code": self.species_textfield.value,
            "origin": self.origin_dropdown.value,
            "equation_type": equation_type,
            "selected_components": selected_components,
            "parameters": param_values
            } 
        self.create_species_preview_modal.show()
     
    def _handle_create_species_button_click(self, e):
        """Handle Create Species button click - show confirmation dialog."""
   
        does_species_code_exist_in_tree_parameters = self._does_species_code_exist_within_dataset((self.species_textfield.value), "data/treeparameters.json")
        if does_species_code_exist_in_tree_parameters:
            Custom_Alert_Dialog(self.page, title_icon=ft.Icons.ERROR_OUTLINE, title_color=ft.Colors.RED_700, title_icon_color=ft.Colors.RED, title="Error", message="Species Code already exists in the Lamberts et al. (2005) dataset.", solution="Please use a different code.").show()
            return
        
        does_species_code_exist_in_created_species = self._does_species_code_exist_within_dataset((self.species_textfield.value), "data/create_species.json")
        if does_species_code_exist_in_created_species:
            Custom_Alert_Dialog(self.page, title_icon=ft.Icons.ERROR_OUTLINE, title_color=ft.Colors.RED_700, title_icon_color=ft.Colors.RED, title="Error", message="User has already created a species with this code.", solution="Please use a different code.").show()
            return
        
        # If everything checks out then proceed
        self._proceed_with_creation(e)
       
    
    def _does_species_code_exist_within_dataset(self, species_name_or_code, json_file_path: str) -> bool:
        """Check if the species code already exists in the given JSON dataset."""
        try:
            data_set = pd.read_json(json_file_path)
            # try to convert species_code to int
            if species_name_or_code.isdigit():
                species_name_or_code = int(species_name_or_code)
                if 'SpeciesCode' in data_set.columns:
                    return species_name_or_code in data_set['SpeciesCode'].values
            else:
                species_name_or_code = str(species_name_or_code)
                if 'SpecCommon' in data_set.columns:
                    #lowercase comparison
                    return species_name_or_code.lower() in data_set['SpecCommon'].str.lower().values
            return False
          
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return False
   
    def _proceed_with_creation(self, e):
        """Proceed with species creation"""
        
        components = self._get_current_selected_components()
        
        if self.current_equation_type == "DBH-based":
            
            data_to_be_inserted_into_json = self._collect_parameter_data(components)
            print("Data to be inserted into JSON:")
            print(data_to_be_inserted_into_json)
        else:
            data_to_be_inserted_into_json = self._collect_parameter_data(components)
            print("Data to be inserted into JSON:")
            print(data_to_be_inserted_into_json)  
            
                # print(param.value)
        # insert the data into the json called storage/created_species.json
        # insert
        
        created_species_json = json.loads(open("data/create_species.json").read())
        if self.species_textfield.value.isdigit():
            created_species_json.append({"SpeciesCode": int(self.species_textfield.value),
            **data_to_be_inserted_into_json})
        else:
            created_species_json.append({"SpecCommon": self.species_textfield.value,
            **data_to_be_inserted_into_json})
            
        with open("data/create_species.json", "w") as f:
            json.dump(created_species_json, f, indent=4)
            print("Species data inserted into JSON file successfully.")
            display_alert = Custom_Alert_Dialog(self.page, title_icon=ft.Icons.CHECK_CIRCLE_OUTLINED, title_color=ft.Colors.GREEN_700, title_icon_color=ft.Colors.GREEN, title="Success",  message="Species created successfully!").show()

    def _get_equation_prefix(self, equation_type):
        return "bh" if equation_type == "DBH + Height-based" else "b"
    def _collect_parameter_data(self, components):
        # Select b for DBH + Height-based
        # Select bh for DBH-Based (Look at the tree_paramaters json for reference)
        data_to_be_inserted_into_json = {"Origin": self.origin_dropdown.value, 
                                         "EquationType": self.current_equation_type}
        
        
        
        prefix = self._get_equation_prefix(self.current_equation_type)

        param_label  = ["b1", "b2", "b3"]
        print(components)
        print("Collecting parameter data...")
        for component in components:
            for param in self.param_controls.get(self.current_equation_type).get(component):
                if prefix == "bh":
                    for _,index in param_label[0:len(param_label)]:    
                        if component.lower() == "branch":
                            data_to_be_inserted_into_json[f"{prefix}branches{index}"] = float(param.value)
                        else:
                            data_to_be_inserted_into_json[f"{prefix}{component.lower()}{index}"] = float(param.value)
                else:
                    for _,index in param_label[0:len(param_label)-1]:
                        if component.lower() == "branch":
                            data_to_be_inserted_into_json[f"{prefix}branches{index}"] = float(param.value)
                        else:
                            data_to_be_inserted_into_json[f"{prefix}{component.lower()}{index}"] = float(param.value)                    
           
        return data_to_be_inserted_into_json
    
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
                    bgcolor=ft.Colors.TERTIARY,
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

    def build(self)-> ft.Container:
        """Build the form and store page reference for dialogs"""
        
     
        self.parameters_section = self._create_parameters_section()
        
        return ft.Container(
            expand=True,  
            alignment=ft.alignment.center,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        Create_Title_And_Description_Widget("Create Species", "Create a new species to add it in the program"),
                        ft.Divider(color=ft.Colors.GREY_300, height=30),  # More space

                        self._create_species_metadata_row(),
                        ft.Divider(height=30, color=ft.Colors.GREY_300),  # More space
                        
                        Select_Components_Widget(
                            page=self.page,
                            title=TitleTextWidget("Select Tree Component"),
                            description_text=DescriptionText("Select tree components for biomass calculation"),
                            components_card_row=ft.Row(),
                            selected_card_component=self.selected_components_text,
                            components_data=COMPONENTS_DATA_2, # Pass the data,
                            displayButton=False,
                            displayShadow=False,
                            on_selection_change=self.on_component_selection_change,  # Add callback
                            is_alternate_card=True
                        ).get_widget(),
                        
                        ft.Divider(height=30, color=ft.Colors.GREY_300),  # More space
                        self.parameters_section,  # Use the stored reference
                        ft.Divider(height=30, color=ft.Colors.GREY_300),  # More space
                        self._create_submit_button(page=self.page),
                        ft.Container(height=20)  # Extra space at bottom
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                margin=30,
                padding=40,
                border_radius=15,
               
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.Colors.BLACK12,
                    offset=ft.Offset(0, 5),
                ),
            )
        )