import flet as ft
from widgets.DescriptionText import DescriptionText
from widgets.TitleTextWidget import TitleTextWidget

class Create_Species_Preview_Modal:
    """Refined Modal to preview species data with corrected color attributes."""
    
    def __init__(self, page: ft.Page, species_data: dict, callback=None):
        self.page = page
        self.species_data = species_data
        self.callback = callback
    
    def _create_info_row(self, label: str, value: str):
        """Creates a clean, professional key-value layout."""
        return ft.Container(
            content=ft.Row([
                ft.Text(label, weight=ft.FontWeight.W_500, color=ft.Colors.PRIMARY, size=13),
                ft.Text(value, weight=ft.FontWeight.W_700, color=ft.Colors.PRIMARY, size=14),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(vertical=2)
        )

    def show(self):
        """Displays the preview modal with a polished, compatible UI."""
        
        # --- Header Section ---
        header = ft.Column([
            DescriptionText("Review the finalized species configuration."),
            ft.Divider(height=10, thickness=1, color=ft.Colors.BLACK12),
        ])

        # --- Core Details Card (Summary) ---
        core_details = ft.Container(
            content=ft.Column([
                self._create_info_row("Species Code", self.species_data.get("species_code", "N/A")),
                self._create_info_row("Origin Type", self.species_data.get("origin", "N/A")),
                self._create_info_row("Equation Model", self.species_data.get("equation_type", "N/A")),
                ft.Divider(height=10, thickness=0.5),
                ft.Text("Active Components", weight=ft.FontWeight.W_500, color=ft.Colors.PRIMARY, size=12),
                ft.Text(
                    ", ".join(self.species_data.get("selected_components", [])) if self.species_data.get("selected_components") else "None",
                    color=ft.Colors.PRIMARY, weight=ft.FontWeight.BOLD, size=13
                ),
            ], spacing=5),
            padding=15,
            border=ft.border.all(1, ft.Colors.BLACK12),
            border_radius=8,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
        )

        # --- Parameters Section ---
        param_list = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)
        params = self.species_data.get("parameters", {})
        
        if params:
            for param_name, value in params.items():
                # Clean prefix logic
                display_name = param_name.split('_', 1)[-1] if '_' in param_name else param_name
                param_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ARROW_RIGHT_ALT_ROUNDED, size=18, color=ft.Colors.PRIMARY),
                            ft.Text(f"{display_name}:", width=140, color=ft.Colors.PRIMARY),
                            ft.Text(str(value) or "0.00", weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                        ]),
                        padding=ft.padding.only(left=5)
                    )
                )
        else:
            param_list.controls.append(ft.Text("No parameters provided", italic=True, color=ft.Colors.PRIMARY))

        # --- Content Assembly ---
        dialog_content = ft.Column(
            controls=[
                header,
                ft.Text("SYSTEM SUMMARY", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                core_details,
                ft.Text("COEFFICIENTS & PARAMETERS", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                ft.Container(content=param_list, padding=ft.padding.only(bottom=10)),
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        )

        # --- Title Bar ---
        title_row = ft.Row(
            controls=[
                ft.Icon(ft.Icons.FACT_CHECK_ROUNDED, color=ft.Colors.GREEN_700, size=24),
                TitleTextWidget("Data Validation")
            ],
            spacing=10,
        )

        self.dialog = ft.AlertDialog(
            modal=True,
            title=title_row,
            bgcolor=ft.Colors.SECONDARY, 
            content=ft.Container(dialog_content, width=500, height=450),
            actions=[
                ft.TextButton("Cancel", on_click=self.close,),
                ft.ElevatedButton(
                    "Finalize Creation", 
                    on_click=self.callback,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(self.dialog)

    def close(self, e):
        """Close the dialog"""
        self.page.close(self.dialog)