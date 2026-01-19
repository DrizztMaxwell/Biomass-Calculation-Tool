import flet as ft
from data.components_data import COMPONENTS_DATA

class Select_Components_Widget:
    def __init__(
        
        self,
        page: ft.Page,
        title: ft.Text,
        description_text: ft.Text,
        components_card_row,
        selected_card_component,
        components_data=None,
        displayButton=True,
        displayShadow=True,
        on_selection_change=None,
        is_alternate_card=False,
        is_database_selected=False
    ):
        self.page = page
        self.title = title
        self.description_text = description_text
        self.components_card_row = components_card_row
        self.selected_card_component = selected_card_component
        self.components_data = components_data or COMPONENTS_DATA.copy()
        self.displayButton = displayButton
        self.displayShadow = displayShadow
        self.on_selection_change = on_selection_change
        self.is_alternate_card = is_alternate_card
        self.is_database_selected = is_database_selected
        
        # Store original components data to reset when needed
        self.original_components_data = COMPONENTS_DATA.copy()
        
        # Apply database selection mode if enabled
        self.apply_database_mode()
        
        # Create the select all button
        self.select_all_button = ft.TextButton(
            text=self.get_select_all_button_text(),
            icon=ft.Icons.CHECK_BOX_OUTLINED,
            style=ft.ButtonStyle(
                color=ft.Colors.TERTIARY,
            ),
            on_click=self.select_all_components,
            disabled=self.is_database_selected  # Disable button if database is selected
        )
        
        # Build the component cards
        self.build_component_cards()
        
        # Initialize selected components text
        self.update_selected_text()
    
    def apply_database_mode(self):
        """Apply database selection mode: select all and disable if database is selected"""
        if self.is_database_selected:
            # Select all components and mark them as disabled
            for component in self.components_data:
                component["is_selected"] = True
                component["is_disabled"] = True
        else:
            # Reset to normal mode - use original state
            for i, component in enumerate(self.components_data):
                original_component = self.original_components_data[i]
                component["is_selected"] = original_component.get("is_selected", False)
                component["is_disabled"] = False  # Ensure not disabled
    
    def get_select_all_button_text(self):
        """Get the appropriate text for the select all button"""
        if self.is_database_selected:
            return "All Required"
        
        all_selected = self.all_components_selected()
        if all_selected:
            return "Deselect All"
        else:
            return "Select All"
    
    def all_components_selected(self):
        """Check if all components are selected"""
        return all(comp.get("is_selected", False) for comp in self.components_data)
    
    def create_component_card(self, component):
        """Create individual component card"""
        is_disabled = component.get("is_disabled", False)
        is_selected = component["is_selected"]
        
        # Determine colors based on selection and disabled state
        if is_disabled:
            bgcolor = ft.Colors.GREEN_100 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.TERTIARY
            border_color = ft.Colors.GREEN if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.PRIMARY
        elif is_selected:
            bgcolor = ft.Colors.GREEN_50 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.TERTIARY
            border_color = ft.Colors.GREEN if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.PRIMARY
        else:
            # if in light mode
            bgcolor = ft.Colors.WHITE if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.GREY_500
            border_color = ft.Colors.GREY_300 if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.GREY_300
        
        # Determine if card should have hover animation
        animate_scale = None if is_disabled else ft.Animation(300, "easeInOut")
        scale = 1.0
        
        # Create the card
        card = ft.Container(
            width=150,
            height=150,
            border_radius=10,
            bgcolor=bgcolor,
            border=ft.border.all(2, border_color),
            padding=10,
            alignment=ft.alignment.center,
            animate_scale=animate_scale,
            scale=scale,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Container(
                        width=50,
                        height=50,
                        alignment=ft.alignment.center,
                        content=ft.Image(
                            src=component["image_src"],
                            fit=ft.ImageFit.CONTAIN,
                            color=ft.Colors.GREY_400 if is_disabled else None
                        )
                    ),
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Text(
                            value=component["title"],
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_600 if is_disabled else ft.Colors.PRIMARY,
                            size=18,
                            text_align=ft.TextAlign.CENTER
                        )
                    )
                ]
            ),
            tooltip="Required - cannot be deselected" if is_disabled else "Click to select/deselect"
        )
        
        # Set event handlers - only if not disabled
        if not is_disabled:
            card.on_click = lambda e, comp=component: self.toggle_component(e, comp)
            card.on_hover = lambda e: self.handle_hover(e, card)
        
        return card
    
    def handle_hover(self, e, card):
        """Handle hover effects (only for enabled cards)"""
        if e.data == "true":
            card.scale = 1.05
        else:
            card.scale = 1.0
        card.update()
    
    def toggle_component(self, e, component):
        """Handle component selection/deselection (only for enabled cards)"""
        if component.get("is_disabled", False):
            return  # Do nothing if component is disabled
        
        component["is_selected"] = not component["is_selected"]
        
        # Update the card appearance
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            
            e.control.bgcolor = ft.Colors.GREEN_100 if component["is_selected"] else ft.Colors.WHITE # see darkmode too
            e.control.border = ft.border.all(
                2, 
                ft.Colors.GREEN_400 if component["is_selected"] else ft.Colors.GREY_300
            )
        else:
            e.control.bgcolor = ft.Colors.TERTIARY if component["is_selected"] else ft.Colors.GREY_500
            e.control.border = ft.border.all(
                2, 
                ft.Colors.PRIMARY if component["is_selected"] else ft.Colors.GREY_300
            )
     
        
        # Update UI
        self.update_selected_text()
        
        # Update Select All button text
        all_selected = self.all_components_selected()
        self.select_all_button.text = "Deselect All" if all_selected else "Select All"
        
        # Call the callback if provided
        if self.on_selection_change:
            selected_items = [comp["title"] for comp in self.components_data if comp["is_selected"]]
            self.on_selection_change(selected_items)
        
        e.control.update()
        if hasattr(self.select_all_button, '_Control__page') and self.select_all_button._Control__page is not None:
            self.select_all_button.update()
    
        self.selected_card_component.update()
    
    def update_selected_text(self):
        """Update selected components text"""
        selected_items = [comp["title"] for comp in self.components_data if comp["is_selected"]]
        
        if self.is_database_selected:
            self.selected_card_component.value = "All components selected (database mode)"
            self.selected_card_component.color = ft.Colors.PRIMARY
        elif selected_items:
            self.selected_card_component.value = f"Selected: {', '.join(selected_items)}"
            self.selected_card_component.color = ft.Colors.PRIMARY
        else:
            self.selected_card_component.value = "No components selected"
            self.selected_card_component.color = ft.Colors.PRIMARY
    
    def select_all_components(self, e=None):
        """Select or deselect all components (only if not disabled)"""
        if self.is_database_selected:
            return  # Do nothing if database is selected
        
        all_selected = self.all_components_selected()
        
        # Toggle all components (only non-disabled ones)
        for component in self.components_data:
            if not component.get("is_disabled", False):
                component["is_selected"] = not all_selected
        
        # Update all cards
        for i, component in enumerate(self.components_data):
            if i < len(self.components_card_row.controls):
                card = self.components_card_row.controls[i]
                if not component.get("is_disabled", False):
                    # darkmode
                    if self.page.theme_mode == ft.ThemeMode.LIGHT:
                            card.bgcolor = ft.Colors.GREEN_100 if component["is_selected"] else ft.Colors.WHITE
                            card.border = ft.border.all(
                                2, 
                                ft.Colors.GREEN_400 if component["is_selected"] else ft.Colors.GREY_300
                            )
                    else:
                        card.bgcolor = ft.Colors.TERTIARY if component["is_selected"] else ft.Colors.GREY_500
                        card.border = ft.border.all(
                            2, 
                            ft.Colors.WHITE if component["is_selected"] else ft.Colors.GREY_300
                        )
                card.update()
        
        # Update UI
        self.update_selected_text()
        self.select_all_button.text = "Deselect All" if not all_selected else "Select All"
        
        # Call the callback if provided
        if self.on_selection_change:
            selected_items = [comp["title"] for comp in self.components_data if comp["is_selected"]]
            self.on_selection_change(selected_items)
        
        self.select_all_button.update()
        self.selected_card_component.update()
    
    def build_component_cards(self):
        """Build component cards and add them to the row"""
        self.components_card_row.controls.clear()
        for component in self.components_data:
            card = self.create_component_card(component)
            self.components_card_row.controls.append(card)
    
    def get_widget(self):
        """Return the Flet widget container"""
        # Create controls list
        controls = [
            self.title,
            self.description_text,
            
            # Select All button row
            ft.Row(
                controls=[self.select_all_button],
                alignment=ft.MainAxisAlignment.START,
            ) if self.displayButton else ft.Container(),
            
            ft.Container(height=10),  # Spacer
            
            self.components_card_row,

            # Selected Items Display
            ft.Container( 
                expand=True,
                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_ACCENT_400),
                border_radius=10,
                margin=ft.margin.only(top=10, bottom=10), 
                padding=10, 
                alignment=ft.alignment.center_left,
                content=self.selected_card_component
            )
        ]
        
        # Conditionally set shadow
        shadow = None
        if self.displayShadow:
            shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
                offset=ft.Offset(0, 3),
            )
        
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            padding=0 if self.is_alternate_card else 20,
            margin=0 if self.is_alternate_card else 30,
            border_radius=10,
            shadow=shadow,
            alignment=ft.alignment.top_left,
            content=ft.Column(
                controls=controls,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            )
        )
    
    # Property to get selected components
    @property
    def selected_components(self):
        """Get list of selected component titles"""
        return [comp["title"] for comp in self.components_data if comp["is_selected"]]
    
    # Method to set specific components
    def set_selected_components(self, component_titles):
        """Set specific components as selected (only if not disabled)"""
        if self.is_database_selected:
            return  # Do nothing if database is selected
        
        # First deselect all non-disabled components
        for component in self.components_data:
            if not component.get("is_disabled", False):
                component["is_selected"] = False
        
        # Select specified non-disabled components
        for component in self.components_data:
            if not component.get("is_disabled", False) and component["title"] in component_titles:
                component["is_selected"] = True
        
        # Update UI
        self.build_component_cards()
        self.update_selected_text()
        
        # Update button text
        all_selected = self.all_components_selected()
        self.select_all_button.text = "Deselect All" if all_selected else "Select All"
        self.select_all_button.update()
    
    def toggle_database_mode(self, is_database_selected: bool):
        """Toggle between database mode and normal mode"""
        self.is_database_selected = is_database_selected
        
        # Re-apply the mode
        self.apply_database_mode()
        
        # Update button state and text
        self.select_all_button.disabled = is_database_selected
        self.select_all_button.text = self.get_select_all_button_text()
        
        # Rebuild cards
        self.build_component_cards()
        
        # Update selected text
        self.update_selected_text()
        
        # Update UI
        self.select_all_button.update()
        self.selected_card_component.update()