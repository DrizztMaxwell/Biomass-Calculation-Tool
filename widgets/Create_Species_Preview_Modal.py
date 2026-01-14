import flet as ft

from widgets.DescriptionText import DescriptionText
from widgets.TitleTextWidget import TitleTextWidget

class Create_Species_Preview_Modal:
    """Modal to preview species data before creation."""
    
    def __init__(self, page: ft.Page, species_data: dict, callback=None):
        self.page = page
        self.species_data = species_data
        self.callback = callback
        print("Preview Modal Data:", species_data)
    
    def show(self):
        """Displays the preview modal."""
        dialog_content = ft.Column(
            controls=[
                DescriptionText("Preview the species data before proceeding."),
                ft.Divider(height=20),
                
                ft.Row([
                    ft.Text("Species Code:", weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                    ft.Text(self.species_data.get("species_code", "N/A"), color=ft.Colors.PRIMARY)
                ]),
                
                ft.Divider(height=15),
                
                ft.Row([
                    ft.Text("Origin:", weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                    ft.Text(self.species_data.get("origin", "N/A"), color=ft.Colors.PRIMARY)
                ]),
                
                ft.Divider(height=15),
                
                ft.Row([
                    ft.Text("Selected Components:", weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                    ft.Text(", ".join(self.species_data.get("selected_components", [])) if self.species_data.get("selected_components") else "No components selected", color=ft.Colors.PRIMARY)
                ]),
                
                ft.Divider(height=15),
                
                ft.Row([
                    ft.Text("Equation Type:", weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                    ft.Text(self.species_data.get("equation_type", ""), color=ft.Colors.PRIMARY)
                ]),
                
                ft.Divider(height=15),
                
                ft.Text("Parameters:", weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            height=400,  # Fixed height for scrollable content
        )
        
        # Add parameter values to dialog
        for param_name, value in self.species_data.get("parameters", {}).items():
            # Remove the equation type prefix (e.g., "DBH-based_" or "DBH + Height-based_")
            display_name = param_name.split('_', 1)[-1] if '_' in param_name else param_name
            
            dialog_content.controls.append(
                ft.Row([
                    ft.Text(f"{display_name}:", width=120, color=ft.Colors.PRIMARY),
                    ft.Text(value or "0.00", color=ft.Colors.PRIMARY)
                ])
            )
        # If no parameters, show message
        if not self.species_data.get("parameters"):
            dialog_content.controls.append(ft.Text("No parameters configured", color=ft.Colors.PRIMARY))
        
        # Wrap content in a Container with fixed dimensions
        content_container = ft.Container(
            content=dialog_content,
            width=600,  # Fixed width
            height=400,  # Fixed height
            padding=10,
        )
        
        # Create title with icon
        title_row = ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.VISIBILITY_ROUNDED,
                    color=ft.Colors.BLACK87,
                    size=28
                ),
                TitleTextWidget("Preview Species Data")
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START
        )
        
        # Create dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=title_row,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            content=content_container,
            actions=[
                ft.TextButton("Cancel", on_click = lambda e: self.close(e)),
                ft.ElevatedButton(
                    "Proceed", 
                    on_click=self.callback,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(self.dialog)
       
    def close(self, e):
        """Close the dialog"""
        self.page.close(self.dialog)