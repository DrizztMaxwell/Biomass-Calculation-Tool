import flet as ft
from widgets.Create_Species_Preview_Modal import Create_Species_Preview_Modal
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
from widgets.Create_Label_With_Icon import Create_Label_With_Icon
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
from widgets.Select_Components_Widget import Select_Components_Widget
from widgets.Title_With_Icon import Title_With_Icon

class Create_Species_View:
    """The main application form, responsible for assembling the UI controls."""
    
    def __init__(self, page:ft.Page, controller):
        self.page = page
        self.__controller = controller
        
        # Store parameter controls for dynamic visibility
        # self.param_controls = {}
        self.parameters_section = None
        
        # Store references for dialog
        self.species_textfield = None
        self.origin_dropdown = None
        self.equation_type_dropdown = None
        
        # Initialize preview modal
        self.create_species_preview_modal = Create_Species_Preview_Modal(
            page, 
            {}, 
  callback=self._handle_preview_confirmation
        )

    def _handle_preview_confirmation(self, form_data):
        """Handle preview modal confirmation.
        
        Returns:
            bool: True if successful, False if failed
        """
        try:
            # Pass to controller and get result
            result = self.__controller.handle_create_species_button_click
            
            if result:
                print (result)
                # Success - close modal and show success message
                Custom_Alert_Dialog(
                    self.page, 
                    title_icon=ft.Icons.CHECK_CIRCLE_OUTLINED, 
                    title_color=ft.Colors.GREEN_700, 
                    title_icon_color=ft.Colors.GREEN, 
                    title="Success",  
                    message="Species created successfully!"
                ).show()
                return True
            else:
                # Failure - show error but keep modal open
                Custom_Alert_Dialog(
                    self.page, 
                    title_icon=ft.Icons.ERROR_OUTLINE, 
                    title_color=ft.Colors.RED_700, 
                    title_icon_color=ft.Colors.RED, 
                    title="Error", 
                    message="Failed to create species due to an unknown error."
                ).show()
                
                return False
                
        except Exception as e:
            print(f"Error: {e}")
            Custom_Alert_Dialog(
                self.page, 
                title_icon=ft.Icons.ERROR_OUTLINE, 
                title_color=ft.Colors.RED_700, 
                title_icon_color=ft.Colors.RED, 
                title="Error", 
                message=f"An error occurred while creating the species: {e}", 
            ).show()
            return False
    def show_preview_modal(self,):
        """Show the preview modal with the provided species data."""
         # def show_confirmation_dialog(self, e, page: ft.Page):
        """Show confirmation dialog with preview of selected items."""
        print("Create Species button clicked!")
        
        # Get selected components
        __selected_components = self.__controller.get_selected_components()
        print(f"Selected components: {__selected_components}")
        
        # Get equation type
        equation_type = self.__controller.get_current_equation_type()
        print(f"Current equation type: {equation_type}")
        
        # Get parameter values
        param_values = {}
        
        param_controls = self.__controller.get_param_controls()
        if equation_type in param_controls:
            components = param_controls[equation_type]
            for component_name, controls_list in components.items():
                for control in controls_list:
                    if control.visible:
                        param_key = f"{equation_type}_{component_name}_{control.label}"
                        param_values[param_key] = control.value
                        print(f"Parameter {param_key}: {control.value}")
       
       
            
        # Update preview modal with species data
        preview_modal = self.create_species_preview_modal
        preview_modal.species_data = {
            "species_code": self.__controller.get_species_code_or_name(),
            "origin": self.__controller.get_origin_type(),
            "equation_type": self.__controller.get_current_equation_type(),
            "__selected_components": self.__controller.get_selected_components(),
            "parameters": param_values
        }
        preview_modal.show()
    
    def _handle_create_create_button_click(self, e):
        """Handle the create button click event."""
        # Gather all input values
        try:
            
            self.show_preview_modal()
              
        except Exception as e:
            
            print(f"Error creating species: {e}")
          
            Custom_Alert_Dialog(
                self.page, 
                title_icon=ft.Icons.ERROR_OUTLINE, 
                title_color=ft.Colors.RED_700, 
                title_icon_color=ft.Colors.RED, 
                title="Error", 
                message=f"An error occurred while creating the species: {e}", 
               
            ).show()
        
    def _create_species_metadata_row(self) -> ft.Row:
        """Creates the Code, Origin, and Equation Type row."""
        
        FORM_ELEMENT_WIDTH = 300
        
        # Species Code Control
        self.species_textfield = ft.TextField(
            hint_text="Alpine fir or 123",
            width=FORM_ELEMENT_WIDTH,
            border_color=ft.Colors.PRIMARY,
            on_change=lambda e: self.__controller.set_species_code_or_name(e.control.value)
        )
        
        species_container = ft.Container(
            content=ft.Column([
                Create_Label_With_Icon(self.page, label_text="Species (Code or Name)", icon_src="./assets/images/key.png"),
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
            value="Natural Stand",
            content_padding=ft.padding.only(left=8, right=8),
            border_radius=5,
            border_color=ft.Colors.PRIMARY,
            on_change=lambda e: self.__controller.set_origin_type(e.control.value),  # Update controller with selected origin
            width=FORM_ELEMENT_WIDTH,
        )
        
        origin_container = ft.Container(
            content=ft.Column([
                Create_Label_With_Icon(self.page, label_text="Select Origin", icon_src="./assets/images/origin.png"),
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
            on_change=self.on_equation_type_change,
            width=FORM_ELEMENT_WIDTH,
            border_color=ft.Colors.PRIMARY,
        )
        
        equation_container = ft.Container(
            content=ft.Column([
                Create_Label_With_Icon(self.page, label_text="Equation Type", icon_src="./assets/images/calculating.png"),
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
        
    def on_equation_type_change(self, e):
        self.update_parameters_visibility(self.__controller.get_selected_components(), e.control.value)
    
    def _param_input(self, label: str):
        """Helper for parameter input fields."""
        
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
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_color=ft.Colors.PRIMARY,
            focused_border_color=ft.Colors.PRIMARY,
            focused_border_width=2,
            border_width=1,
            label_style=ft.TextStyle(
                size=12,
                weight=ft.FontWeight.W_500,
                color=ft.Colors.PRIMARY,
            ),
            error_style=ft.TextStyle(
                size=11,
                color=ft.Colors.RED_600
            ),
            hint_text="0.00",
            hint_style=ft.TextStyle(
                size=13,
                color=ft.Colors.ON_PRIMARY_CONTAINER
            ),
        )
        
        # Store a reference to the Flet control
        self.__controller.set_param_controls({ control})
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
        self.__controller.set_param_controls(   {
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
        )
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
        for equation_type in self.__controller.get_param_controls().values():
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

    def update_parameters_visibility(self, selected_components, current_equation_type):
        """Update parameter visibility based on selected components and equation type."""
        
        # Determine which equation type to use
        equation_key = "DBH-based" if current_equation_type == "DBH-based" else "DBH + Height-based"
        
        # Hide all parameters and labels first
        any_visible = False
        for equation_type in self.__controller.get_param_controls().values():
            for component_params in equation_type.values():
                for param in component_params:
                    param.visible = False
        
        for label in self.param_labels.values():
            label.visible = False
        
        # Show parameters and labels for selected components based on equation type
        for component in selected_components:
            if component in self.__controller.get_param_controls()[equation_key]:
                # Show component label
                if component in self.param_labels:
                    self.param_labels[component].visible = True
                
                # Show parameters
                for param in self.__controller.get_param_controls()[equation_key][component]:
                    param.visible = True
                    any_visible = True
        
        # Update "no parameters" text visibility
        self.no_parameters.visible = not any_visible
        
        # Update the UI
        if self.parameters_section:
            self.parameters_section.update()

    def _create_submit_button(self, page: ft.Page):
        """Creates the submit button."""
        return ft.Row(
            [
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("Create Species", size=16, weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.ADD, size=20)
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                    on_click=self._handle_create_create_button_click,
                    bgcolor=ft.Colors.TERTIARY,
                    color=ft.Colors.WHITE,
                    height=40,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def build(self) -> ft.Container:
        """Build the form."""
        
        self.parameters_section = self._create_parameters_section()
        
        return ft.Container(
            expand=True,  
            alignment=ft.alignment.center,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Column([
                            Title_With_Icon("Create Species", ft.Icons.ADD_BOX),
                            DescriptionText("Define a new tree species by specifying its parameters and components."),
                        ], spacing=8),
                        ft.Divider(color=ft.Colors.GREY_300, height=30),

                        self._create_species_metadata_row(),
                        ft.Divider(height=30, color=ft.Colors.GREY_300),
                        
                        Select_Components_Widget(
                            page=self.page,
                            title=TitleTextWidget("Select Tree Component"),
                            description_text=DescriptionText("Select tree components for biomass calculation"),
                            components_card_row=ft.Row(),
                            selected_card_component=ft.Text(value=""),
                            components_data=self.__controller.get_component_data(),
                            display_button=False,
                            display_shadow=False,
                            on_selection_change=self.__controller.on_component_selection_change,
                            is_alternate_card=True,
                            is_in_create_species_page=True
                        ).get_widget(),
                        
                        ft.Divider(height=30, color=ft.Colors.GREY_300),
                        self.parameters_section,
                        ft.Divider(height=30, color=ft.Colors.GREY_300),
                        self._create_submit_button(page=self.page),
                        ft.Container(height=20)
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

    
    # Getters for controller to access UI controls
    def get_species_textfield(self):
        return self.species_textfield
    
    def get_origin_dropdown(self):
        return self.origin_dropdown
    
    def get_equation_type_dropdown(self):
        return self.equation_type_dropdown
    
    def get_parameter_controls(self):
        return self.param_controls
    
    def get_preview_modal(self):
        return self.create_species_preview_modal