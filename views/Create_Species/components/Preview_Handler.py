from widgets.Create_Species_Preview_Modal import Create_Species_Preview_Modal
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
import flet as ft

class Preview_Handler:
    """Handles preview modal operations with a professional UI/UX flow."""
    
    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller
        # Initialize the modal once; data is injected later via species_data property
        self.preview_modal = Create_Species_Preview_Modal(
            page, 
            {}, 
            callback=self._handle_preview_confirmation
        )
    
    def _handle_preview_confirmation(self, form_data):
        """Handle preview modal confirmation with polished feedback."""
        try:
            result = self.controller._proceed_with_creation()
            
            if result:
                # Success Dialog: Using soft green and professional icons
                Custom_Alert_Dialog(
                    self.page, 
                    title_icon=ft.Icons.CHECK_CIRCLE_ROUNDED, 
                    title_color=ft.Colors.GREEN_800, 
                    title_icon_color=ft.Colors.GREEN_400, 
                    title="Process Complete",  
                    message="The new species has been successfully registered in the database."
                ).show()
                return True
            else:
                # Failure Dialog: Using deep orange/red for clarity
                Custom_Alert_Dialog(
                    self.page, 
                    title_icon=ft.Icons.GPP_BAD_ROUNDED, 
                    title_color=ft.Colors.RED_800, 
                    title_icon_color=ft.Colors.RED_400, 
                    title="Creation Failed", 
                    message="The system encountered an issue. Please verify your inputs and try again."
                ).show()
                return False
                
        except Exception as e:
            # Critical Error Dialog
            Custom_Alert_Dialog(
                self.page, 
                title_icon=ft.Icons.REPORT_GMAILERRORRED_ROUNDED, 
                title_color=ft.Colors.RED_900, 
                title_icon_color=ft.Colors.RED_accent, 
                title="System Error", 
                message=f"An unexpected error occurred: {str(e)}", 
            ).show()
            return False
    
    def show_preview(self):
        """Orchestrates the data collection and triggers the modal."""
        # Visual feedback for the terminal/logs
        print("--- Initiating Species Preview ---")
        
        # Aggregate data from controller
        selected_components = self.controller.get_selected_components()
        equation_type = self.controller.get_current_equation_type()
        param_values = self._get_parameter_values(equation_type)
        
        # Construct a clean data object for the UI Modal
        self.preview_modal.species_data = {
            "species_code": self.controller.get_species_code_or_name(),
            "origin": self.controller.get_origin_type(),
            "equation_type": equation_type,
            "selected_components": selected_components,
            "parameters": param_values
        }
        
        self.preview_modal.show()
    
    def _get_parameter_values(self, equation_type):
        """Extracts and cleans parameter values for display."""
        param_values = {}
        param_controls = self.controller.get_param_controls()
        
        if equation_type in param_controls:
            components = param_controls[equation_type]
            for component_name, controls_list in components.items():
                for control in controls_list:
                    # Only collect data from active/visible inputs to keep UI clean
                    if control.visible:
                        # Professional key naming: 'Component: Label'
                        param_key = f"{component_name}: {control.label}"
                        param_values[param_key] = control.value if control.value else "N/A"
        
        return param_values

    def get_preview_modal(self):
        return self.preview_modal