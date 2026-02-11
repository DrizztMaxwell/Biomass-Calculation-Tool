import flet as ft
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
from widgets.Title_With_Icon import Title_With_Icon
from widgets.Select_Components_Widget import Select_Components_Widget
from .components.Species_Metadata_Row import Species_Metadata_Row
from .components.Parameter_Section import ParametersSection
from .components.Preview_Handler import Preview_Handler
from .components.Submit_Button import Submit_Button

class Create_Species_View:
    """The main application form, responsible for assembling the UI controls."""
    
    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.__controller = controller
        
        # Initialize components
        self.metadata_row = Species_Metadata_Row(page, controller)
        self.parameters_section = ParametersSection(controller)  # Keep the instance
        self.preview_handler = Preview_Handler(page, controller)
        
        # Store references
        self.parameters_section_widget = None  # This will store the ft.Column
        
    def _handle_create_button_click(self, e):
        """Handle the create button click event."""
        try:
            if self.__controller.handle_create_species_button_click():
                self.preview_handler.show_preview()
        except Exception as e:
            print(f"Error creating species: {e}")
            from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
            Custom_Alert_Dialog(
                self.page, 
                title_icon=ft.Icons.ERROR_OUTLINE, 
                title_color=ft.Colors.RED_700, 
                title_icon_color=ft.Colors.RED, 
                title="Error", 
                message=f"An error occurred while creating the species: {e}", 
            ).show()
    
    def on_component_selection_change(self, selected_components):
        """Callback function when component selection changes."""
        self.__controller.set_selected_components(selected_components)
        print(f"Component selection changed: {self.__controller.get_selected_components()}")
        
        # Call update_visibility on the ParametersSection instance, not the widget
        self.parameters_section.update_visibility(
            self.__controller.get_selected_components(),
            self.__controller.get_current_equation_type()
        )
        
        # Update the UI
        if self.parameters_section_widget:
            self.parameters_section_widget.update()
    
    def on_equation_type_change(self, e):
        """Handle equation type change."""
        self.__controller.set_current_equation_type(e.control.value)
        
        # Call update_visibility on the ParametersSection instance, not the widget
        self.parameters_section.update_visibility(
            self.__controller.get_selected_components(),
            e.control.value
        )
        
        # Update the UI
        if self.parameters_section_widget:
            self.parameters_section_widget.update()
    
    def build(self) -> ft.Container:
        """Build the form."""
        
        # Build parameters section widget and store both the widget and the instance
        self.parameters_section_widget = self.parameters_section.build()
        
        # Build metadata row and attach equation type change handler
        metadata_row_widget = self.metadata_row.build()
        self.metadata_row.equation_type_dropdown.on_change = self.on_equation_type_change
        
        # Build select components widget
        select_components_widget = Select_Components_Widget(
            page=self.page,
            title=TitleTextWidget("Select Tree Component"),
            description_text=DescriptionText("Select tree components for biomass calculation"),
            components_card_row=ft.Row(),
            selected_card_component=ft.Text(value=""),
            components_data=self.__controller.get_component_data(),
            display_button=False,
            display_shadow=False,
            on_selection_change=lambda e: self.on_component_selection_change(e),
            is_alternate_card=True,
            is_in_create_species_page=True
        ).get_widget()
        
        # Build submit button
        submit_button = Submit_Button(
            self.page, 
            self._handle_create_button_click
        ).build()
        
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
                        
                        metadata_row_widget,
                        ft.Divider(height=30, color=ft.Colors.GREY_300),
                        
                        select_components_widget,
                        
                        ft.Divider(height=30, color=ft.Colors.GREY_300),
                        self.parameters_section_widget,
                        ft.Divider(height=30, color=ft.Colors.GREY_300),
                        submit_button,
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
    
    # Getters for controller
    def get_species_textfield(self):
        return self.metadata_row.get_species_textfield()
    
    def get_origin_dropdown(self):
        return self.metadata_row.get_origin_dropdown()
    
    def get_equation_type_dropdown(self):
        return self.metadata_row.get_equation_type_dropdown()
    
    def get_parameter_controls(self):
        return self.__controller.get_param_controls()
    
    def get_preview_modal(self):
        return self.preview_handler.get_preview_modal()
    
    def update_parameters_visibility(self, selected_components, current_equation_type):
        """Public method to update parameter visibility."""
        # Call update_visibility on the ParametersSection instance, not the widget
        self.parameters_section.update_visibility(
            selected_components, 
            current_equation_type
        )
        
        # Update the UI
        if self.parameters_section_widget:
            self.parameters_section_widget.update()