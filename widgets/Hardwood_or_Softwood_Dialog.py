import flet as ft
class HardwoodOrSoftwoodDialog:
    """
    A multi-step dialog for classifying missing species codes as Hardwood or Softwood,
    using a professional, checklist-style card layout.
    """
    def __init__(self, page: ft.Page, missing_species_codes: set):
        self.page = page
        self.missing_species_codes = missing_species_codes
        self.user_selections = {}
        # Track selected types for each species code globally within the dialog context
        self.selected_types = {code: None for code in missing_species_codes}
        self.submitted = False
        self.result_future = None
        
    async def show_species_code_dialog(self):
        """Show dialog to select hardwood or softwood for missing species codes."""
        
        # Create a future to await
        import asyncio
        self.result_future = asyncio.Future()
        
        # Current step (0 = hardwood selection, 1 = softwood selection)
        self.current_step = [0]
        
        # Main column that will hold the current step content
        self.main_column = ft.Column(
            self._get_current_step_content(self.current_step[0]),
            expand=True
        )

        async def on_next(e):
            """Move to softwood selection step."""
            self.current_step[0] = 1
            self.main_column.controls = self._get_current_step_content(self.current_step[0])
            update_dialog_actions()
            self.page.update()
        
        async def on_back(e):
            """Return to hardwood selection step."""
            self.current_step[0] = 0
            # Clear any softwood selections when going back
            for code in self.missing_species_codes:
                if self.selected_types.get(code) == "Softwood":
                    self.selected_types[code] = None
            self.main_column.controls = self._get_current_step_content(self.current_step[0])
            update_dialog_actions()
            self.page.update()
        
        async def on_submit(e):
            """Final submission and validation."""
            final_selections = {
                code: type_ for code, type_ in self.selected_types.items() if type_ is not None
            }
            print(f"User Selections before validation: {final_selections}")
            # Codes that were not selected as Hardwood OR Softwood
            missing_selections = [
                code for code in self.missing_species_codes 
                if final_selections.get(code) is None
            ]
            
            # if missing_selections:
            #     # Show error for missing selections
            #     self.page.show_snack_bar(
            #         ft.SnackBar(
            #             content=ft.Text(f"❌ Error: Please classify all codes. Missing: {', '.join(map(str, missing_selections))}", 
            #                             color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            #             bgcolor=ft.Colors.RED_600,
            #             duration=3000,
            #         )
            #     )
            #     self.page.update()
            #     return
            
            self.user_selections = final_selections
            # print(f"Final Selected types: {self.user_selections}")
            
            # Set the future result
            self.result_future.set_result(self.user_selections)
            self.submitted = True
            
            self.dialog.open = False
            self.page.update()
            
        
        async def on_cancel(e):
            """Cancel the dialog."""
            self.dialog.open = False
            self.page.update()
            print("Dialog cancelled")
            # Set the future to None to indicate cancellation
            self.result_future.set_result(None)
        
        def update_dialog_actions():
            """Dynamically update the action buttons based on the current step."""
            if self.current_step[0] == 0:
                self.dialog.actions = [
                    ft.ElevatedButton(text="Next Step", on_click=on_next, icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
                    ft.TextButton(text="Cancel", on_click=on_cancel)
                ]
            else:
                self.dialog.actions = [
                    ft.TextButton(text="Back", on_click=on_back, icon=ft.Icons.ARROW_BACK_IOS_ROUNDED),
                    ft.ElevatedButton(text="Submit Final", on_click=on_submit, icon=ft.Icons.DONE_ALL_ROUNDED, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
                    ft.TextButton(text="Cancel", on_click=on_cancel)
                ]
        
        # Initialize dialog with fixed width and height
        self.dialog = ft.AlertDialog(
            title=ft.Text("🌲 Species Type Checklist", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
            content=ft.Container(
                content=self.main_column,
                width=600,  # Fixed width
                height=500,  # Fixed height
                padding=10,
                expand=True,
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True,
            # Styling for a clean, professional look
            shape=ft.RoundedRectangleBorder(radius=15),
            bgcolor=ft.Colors.WHITE,
            content_padding=ft.padding.all(0),  # Remove content padding since we're using Container
        )
        
        # Set initial actions
        update_dialog_actions()

        # Show the dialog
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.open(self.dialog)
        self.page.update()
        
        # Wait for the dialog to be submitted or cancelled
        return await self.result_future

    def create_species_card(self, code, species_type: str):
        """
        Creates a professional, interactive Card component with a checklist appearance.
        The card's appearance changes based on whether it is selected.
        """
        
        # State variables for appearance and selection
        is_selected = self.selected_types.get(code) == species_type
        
        # Define the border color and thickness based on selection state
        # Use a Green color for a clear "checked" state
        border_color = ft.Colors.GREEN_600 if is_selected else ft.Colors.GREY_300
        border_width = 2.0 if is_selected else 1

        # The core interactive element: A Checkbox
        checkbox = ft.Checkbox(
            value=is_selected,
            fill_color=ft.Colors.WHITE,
            tooltip=f"Select {species_type}",
            disabled=True, # Disable standard checkbox interaction, use card tap instead
            check_color=ft.Colors.GREEN_700,
        )

        # Card content: List tile is now simpler, acting as the main touch area
        card_content = ft.ListTile(
            leading=checkbox,
            title=ft.Text(
                str(code),
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_GREY_900 if not is_selected else ft.Colors.BLACK87
            ),
            subtitle=ft.Text(
                f"Classify as {species_type}", 
                color=ft.Colors.BLUE_GREY_400
            ),
        )

        def on_tap(e):
            """Handles the tap event for the card (selection/deselection)."""
            
            # If currently selected, deselect it (set to None)
            if self.selected_types.get(code) == species_type:
                self.selected_types[code] = None
            # If not selected, select it (set to species_type)
            else:
                self.selected_types[code] = species_type
            
            # Re-render the dialog to reflect the change
            self.main_column.controls = self._get_current_step_content(self.current_step[0])
            self.page.update()

        # The interactive Card component
        card = ft.Card(
            content=ft.Container(
                content=card_content,
                padding=5,
                border=ft.border.all(border_width, border_color),
                border_radius=ft.border_radius.all(8),
                bgcolor=ft.Colors.WHITE if not is_selected else ft.Colors.GREEN_50, 
                on_click=on_tap,
                ink=True, 
            ),
            elevation=0,
        )
        
        return card

    def _get_current_step_content(self, step: int):
        """Generates the main content (cards) for the current step."""
        
        # Determine which codes are available for selection in this step
        if step == 0: # Hardwood Selection
            species_type = "Hardwood"
            available_codes = self.missing_species_codes
        else: # Softwood Selection (Step 1)
            species_type = "Softwood"
            # Only show codes that were NOT selected as Hardwood
            available_codes = [
                code for code in self.missing_species_codes 
                if self.selected_types.get(code) != "Hardwood"
            ]
        
        # Generate the list of cards
        card_list = []
        for code in available_codes:
            card_list.append(self.create_species_card(code, species_type))

        # Handle the case where all codes were already selected as Hardwood
        if step == 1 and not available_codes:
             info_message = ft.Column([
                ft.Text("✅ All remaining species codes were classified as Hardwood in the previous step.", 
                        weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
                ft.Text("Click 'Back' to review, or 'Submit Final' to complete the classification.", size=14)
            ])
             card_area = ft.Container(
                content=info_message,
                alignment=ft.alignment.center,
                height=300
            )
        else:
            card_area = ft.Container(
                content=ft.Column(
                    card_list,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=6,
                    expand=True  # Changed to expand to fill available space
                ),
                padding=10,
                border_radius=10,
                expand=True  # Make container expandable
            )

        # Assemble the full content for the step
        content = ft.Column([
            ft.Text(f"📋 Step {step + 1}: Select codes for {species_type}:", 
                    weight=ft.FontWeight.W_700, size=18, color=ft.Colors.BLUE_GREY_900),
            
            # Info for Softwood step
            *(
                [ft.Text("Codes selected as Hardwood are automatically removed from this list.", 
                         size=12, color=ft.Colors.BLUE_GREY_500)] 
                if step == 1 and available_codes else []
            ),

            card_area
        ], expand=True)  # Make column expand to fill space

        return [content]

    def get_user_selections(self):
        """Get the user selections after dialog submission."""
        return self.user_selections

    def was_submitted(self):
        """Check if the dialog was submitted."""
        return self.submitted