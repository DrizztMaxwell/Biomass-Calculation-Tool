import flet as ft
from widgets.LogFileTxt import logger
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog


class Edit_Dialog:
    """Dialog for editing species data."""
    
    # Constants
    DIALOG_WIDTH_MAX = 700
    DIALOG_HEIGHT_MAX = 650
    DIALOG_WIDTH_RATIO = 0.9
    DIALOG_HEIGHT_RATIO = 0.85
    
    # Colors
    PRIMARY_COLOR = ft.Colors.BLUE_700
    SECONDARY_COLOR = ft.Colors.GREEN_600
    ACCENT_COLOR = ft.Colors.ORANGE_500
    TEXT_PRIMARY = ft.Colors.GREY_900
    TEXT_SECONDARY = ft.Colors.GREY_600
    WHITE = ft.Colors.WHITE
    GREY_100 = ft.Colors.GREY_100
    GREY_200 = ft.Colors.GREY_200
    PRIMARY = ft.Colors.PRIMARY
    SECONDARY_CONTAINER = ft.Colors.SECONDARY_CONTAINER
    SECONDARY = ft.Colors.SECONDARY
    GREEN_500 = ft.Colors.GREEN_500
    RED_500 = ft.Colors.RED_500
    BLACK = ft.Colors.BLACK
    PURPLE_600 = ft.Colors.PURPLE_600
    
    # Parameter categories
    PARAMETER_CATEGORIES = {
        "bh": {
            "name": "DBH + Height-based Parameters",
            "icon": ft.Icons.TRENDING_UP,
            "color": None  # Will be set to secondary_color
        },
        "b": {
            "name": "DBH-based Parameters",
            "icon": ft.Icons.STRAIGHTEN,
            "color": None  # Will be set to accent_color
        },
        "default": {
            "name": "Other Parameters",
            "icon": ft.Icons.TUNE,
            "color": PURPLE_600
        }
    }
    
    # Validation
    MIN_VALUE = -5
    MAX_VALUE = 5
    
    def __init__(self, page):
        self.page = page
        self.current_species_index = None
        self.param_text_fields = {}
        self.origin_dropdown = None
        
    def edit_species_dialog(self, index, filtered_species, species_data, 
                           controller, primary_color=None, secondary_color=None, 
                           accent_color=None, refresh_callback=None, save_callback=None):
        """Show edit form in a beautiful professional dialog."""
        
        # Set colors
        self.primary_color = primary_color or self.PRIMARY_COLOR
        self.secondary_color = secondary_color or self.SECONDARY_COLOR
        self.accent_color = accent_color or self.ACCENT_COLOR
        self.text_secondary = self.TEXT_SECONDARY
        
        # Set colors for parameter categories
        self.PARAMETER_CATEGORIES["bh"]["color"] = self.secondary_color
        self.PARAMETER_CATEGORIES["b"]["color"] = self.accent_color
        
        # Store callbacks
        self.refresh_callback = refresh_callback
        self.save_callback = save_callback
        self.controller = controller
        
        # Find the species
        species, actual_index = self._find_species(index, filtered_species, species_data)
        if not species:
            return
        
        self.current_species_index = actual_index
        
        # Calculate dialog dimensions
        dialog_width, dialog_height = self._calculate_dialog_dimensions()
        
        # Determine display value for header
        display_value = self._get_display_value(species)
        
        # Create dialog content
        dialog_content = self._create_dialog_content(species, display_value, dialog_width, dialog_height)
        
        # Create and show dialog
        dialog = self._create_dialog(species, dialog_content, dialog_width)
        self._show_dialog(dialog, species)
    
    def _find_species(self, index, filtered_species, species_data):
        """Find species by index and locate it in the main data."""
        if index >= len(filtered_species):
            return None, None
        
        filtered_species_item = filtered_species[index]
        species_code = filtered_species_item.get("SpeciesCode")
        spec_common = filtered_species_item.get("SpecCommon")
        
        # Find actual index in species_data
        for i, species in enumerate(species_data):
            sp_code = species.get("SpeciesCode")
            sp_common = species.get("SpecCommon")
            
            if species_code is not None and sp_code is not None and sp_code == species_code:
                return species, i
            elif spec_common is not None and sp_common is not None and sp_common == spec_common:
                return species, i
        
        return None, None
    
    def _calculate_dialog_dimensions(self):
        """Calculate dialog dimensions based on page size."""
        dialog_width = min(self.DIALOG_WIDTH_MAX, self.page.width * self.DIALOG_WIDTH_RATIO)
        dialog_height = min(self.DIALOG_HEIGHT_MAX, self.page.height * self.DIALOG_HEIGHT_RATIO)
        return dialog_width, dialog_height
    
    def _get_display_value(self, species):
        """Get display value for header (common name or code)."""
        spec_common = species.get("SpecCommon")
        species_code = species.get("SpeciesCode")
        return spec_common if spec_common and spec_common != "" else species_code
    
    def _create_dialog_content(self, species, display_value, width, height):
        """Create the main dialog content."""
        return ft.Container(
            content=ft.Column([
                self._create_header(species, display_value),
                self._create_scrollable_content(species)
            ], spacing=0),
            width=width,
            height=height,
            bgcolor=self.SECONDARY,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
    
    def _create_header(self, species, display_value):
        """Create dialog header with gradient background."""
        return ft.Container(
            bgcolor=ft.Colors.GREEN_600,
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.EDIT_OUTLINED, size=32, color=self.WHITE),
                    bgcolor=ft.Colors.with_opacity(0.2, self.WHITE),
                    padding=12,
                    border_radius=12,
                    margin=ft.margin.only(right=15)
                ),
                ft.Column([
                    ft.Text(
                        "Edit Species", 
                        size=24, 
                        weight=ft.FontWeight.W_700, 
                        color=self.WHITE
                    ),
                    ft.Text(
                        f"Species: {display_value}", 
                        size=14, 
                        color=ft.Colors.with_opacity(0.9, self.WHITE)
                    ),
                ], spacing=4, alignment=ft.CrossAxisAlignment.START)
            ], alignment=ft.MainAxisAlignment.START),
           
            padding=ft.padding.symmetric(horizontal=30, vertical=24),
            border_radius=ft.border_radius.only(top_left=16, top_right=16),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, self.BLACK)
            )
        )
    
    def _create_scrollable_content(self, species):
        """Create scrollable content area with form."""
        return ft.Container(
            content=ft.Column([
                ft.Container(height=24),
                self._create_basic_info_card(species),
                ft.Container(height=24),
                *self._create_parameter_cards(species),
                ft.Container(height=24),
            ], scroll=ft.ScrollMode.AUTO, spacing=0),
            padding=ft.padding.symmetric(horizontal=30),
            expand=True
        )
    
    def _create_basic_info_card(self, species):
        """Create basic information form card."""
        # Create origin dropdown
        self.origin_dropdown = ft.Dropdown(
            value=species.get("Origin", "Natural Stand"),
            options=[
                ft.dropdown.Option("Natural Stand"),
                ft.dropdown.Option("Plantation"),
            ],
            border_radius=10,
            filled=True,
            fill_color=self.SECONDARY_CONTAINER,
            border_color=self.PRIMARY,
            focused_border_color=self.primary_color,
            focused_bgcolor=self.WHITE,
            text_size=14,
            content_padding=15,
            prefix_icon=ft.Icon(ft.Icons.LOCATION_ON, color=self.text_secondary, size=20),
            hint_text="Select Origin"
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, color=self.primary_color, size=20),
                    ft.Text(
                        "Basic Information", 
                        size=17, 
                        weight=ft.FontWeight.W_600, 
                        color=self.PRIMARY
                    ),
                ], spacing=12),
                ft.Divider(height=1, color=self.GREY_200),
                ft.Container(height=15),
                ft.Text("Origin", size=14, weight=ft.FontWeight.W_500, color=self.PRIMARY),
                self.origin_dropdown,
                ft.Container(height=15),
            ]),
            padding=ft.padding.all(24),
            bgcolor=self.SECONDARY_CONTAINER,
            border_radius=12,
            border=ft.border.all(1, self.PRIMARY),
        )
    
    def _create_parameter_cards(self, species):
        """Create parameter input cards."""
        # Reset parameter fields
        self.param_text_fields = {}
        
        # Organize parameters by category
        categorized_params = self._categorize_parameters(species)
        
        # Create a card for each category
        param_cards = []
        for category_key, category_data in categorized_params.items():
            param_cards.append(self._create_parameter_category_card(category_data))
        
        return param_cards
    
    def _categorize_parameters(self, species):
        """Categorize parameters based on their keys."""
        categorized = {}
        
        for key, value in species.items():
            if key in ["SpeciesCode", "Origin", "EquationType", "SpecCommon"]:
                continue
            
            # Determine category based on prefix
            if key.startswith("bh"):
                category_key = "bh"
            elif key.startswith("b"):
                category_key = "b"
            else:
                category_key = "default"
            
            category = self.PARAMETER_CATEGORIES[category_key]
            
            if category_key not in categorized:
                categorized[category_key] = {
                    "name": category["name"],
                    "icon": category["icon"],
                    "color": category["color"],
                    "icon_bg": ft.Colors.with_opacity(0.1, category["color"]),
                    "field_bg": ft.Colors.with_opacity(0.05, category["color"]),
                    "params": []
                }
            
            categorized[category_key]["params"].append((key, value))
        
        return categorized
    
    def _create_parameter_category_card(self, category_data):
        """Create a card for a parameter category."""
        param_fields = ft.Column(spacing=12)
        
        # Create fields for each parameter
        for param_key, param_value in category_data["params"]:
            field_container = self._create_parameter_field(param_key, param_value, category_data)
            param_fields.controls.append(field_container)
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(category_data["icon"], color=category_data["color"], size=20),
                        bgcolor=category_data["icon_bg"],
                        padding=10,
                        border_radius=10,
                        margin=ft.margin.only(right=12)
                    ),
                    ft.Text(
                        category_data["name"], 
                        size=16, 
                        weight=ft.FontWeight.W_600, 
                        color=category_data["color"]
                    ),
                ], spacing=0),
                ft.Container(height=20),
                param_fields
            ]),
            padding=24,
            bgcolor=self.SECONDARY_CONTAINER,
            border_radius=12,
            border=ft.border.all(1, self.GREY_100),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.08, self.BLACK)
            )
        )
    
    def _create_parameter_field(self, param_key, param_value, category_data):
        """Create a parameter input field."""
        # Create TextField
        text_field = ft.TextField(
            value=str(param_value),
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=8,
            filled=True,
            fill_color=self.SECONDARY_CONTAINER,
            border_color=self.PRIMARY,
            focused_border_color=category_data["color"],
            focused_bgcolor=self.WHITE,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=15, vertical=12),
            dense=True
        )
        
        # Store reference
        self.param_text_fields[param_key] = text_field
        text_field.color = self.PRIMARY
        
        # Create field container
        return ft.Column([
            ft.Text(param_key, size=14, weight=ft.FontWeight.W_500, color=self.PRIMARY),
            ft.Container(height=6),
            ft.Container(
                content=text_field,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=5,
                    color=ft.Colors.with_opacity(0.05, self.BLACK),
                    offset=ft.Offset(0, 2)
                )
            )
        ], spacing=0)
    
    def _save_changes(self, e, dialog, species):
        """Handle save changes button click."""
        try:
            # Update basic info
            self.controller.get_species_data()[self.current_species_index]["Origin"] = self.origin_dropdown.value
            
            # Validate all parameter fields
            has_errors, error_messages = self._validate_parameters()
            
            # If there are errors, show them
            if has_errors:
                self._show_validation_errors(error_messages)
                return
            
            # All validations passed, save the data
            if self._save_species_data():
                self._close_dialog()
                self._show_success_message(species)
                
                # Refresh data table if callback provided
                if self.refresh_callback:
                    self.refresh_callback()
            else:
                self._show_error_dialog("Failed to save changes.")
                logger.write(f"Failed to save changes for species '{species.get('SpeciesCode', '')}'.")
                
        except Exception as ex:
            self._show_error_dialog(f"Error saving species: {ex}")
            logger.write(f"Exception while saving species '{species.get('SpeciesCode', '')}': {ex}")
            import traceback
            traceback.print_exc()
    
    def _validate_parameters(self):
        """Validate all parameter fields."""
        has_errors = False
        error_messages = []
        
        for param_key, text_field in self.param_text_fields.items():
            if text_field.value is None or text_field.value == "":
                has_errors = True
                self._mark_field_error(text_field, "This field cannot be empty")
                error_messages.append(f"{param_key}: Field cannot be empty")
                continue
            
            try:
                value = float(text_field.value)
                if value < self.MIN_VALUE or value > self.MAX_VALUE:
                    has_errors = True
                    self._mark_field_error(text_field, f"Value must be between {self.MIN_VALUE} and {self.MAX_VALUE}")
                    error_messages.append(f"{param_key}: {value} is not between {self.MIN_VALUE} and {self.MAX_VALUE}")
                else:
                    self._clear_field_error(text_field)
                    self.controller.get_species_data()[self.current_species_index][param_key] = value
                    
            except ValueError:
                has_errors = True
                self._mark_field_error(text_field, "Invalid number format")
                error_messages.append(f"{param_key}: Invalid number format")
        
        return has_errors, error_messages
    
    def _mark_field_error(self, text_field, error_text):
        """Mark a field with error styling."""
        text_field.error_text = error_text
        text_field.border_color = self.RED_500
        text_field.update()
    
    def _clear_field_error(self, text_field):
        """Clear error styling from a field."""
        text_field.error_text = None
        text_field.border_color = self.GREY_200
        text_field.update()
    
    def _show_validation_errors(self, error_messages):
        """Show validation error dialog."""
        error_message = "Please fix the following errors:\n" + "\n".join(f"• {msg}" for msg in error_messages)
        self._show_error_dialog(error_message)
    
    def _save_species_data(self):
        """Save species data using controller callback or default."""
        if self.save_callback:
            return self.save_callback()
        return False
    
    def _show_error_dialog(self, message):
        """Show error dialog."""
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.ERROR_OUTLINE, size=30, color=self.WHITE),
                    bgcolor=self.RED_500,
                    padding=10,
                    border_radius=50
                ),
                ft.Text("❌ Error", size=20, weight=ft.FontWeight.W_700)
            ], spacing=15),
            content=ft.Text(message, size=14),
            actions=[
                ft.ElevatedButton(
                    "OK",
                    style=ft.ButtonStyle(
                        bgcolor=self.PRIMARY_COLOR,
                        color=self.WHITE,
                        padding=ft.padding.symmetric(horizontal=30, vertical=12),
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=lambda e: self._close_error_dialog(dialog)
                )
            ],
            actions_padding=ft.padding.all(20),
            shape=ft.RoundedRectangleBorder(radius=15)
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)
    
    def _close_error_dialog(self, dialog):
        """Close error dialog."""
        dialog.open = False
        self.page.update()
    
    def _show_success_message(self, species):
        """Show success message."""
        Custom_Alert_Dialog(
            page=self.page, 
            title_icon=ft.Icons.CHECK_CIRCLE, 
            title_color=self.BLACK, 
            title_icon_color=ft.Colors.GREEN,  
            title="Success", 
            message="Species updated successfully!", 
            button_text="OK"
        ).show()
        logger.write(f"Species '{species.get('SpeciesCode', '')}' updated successfully.")
    
    def _close_dialog(self):
        """Close the main dialog."""
        self.page.dialog.open = False
        
        self.page.update()
    
    def _create_dialog(self, species, content, width):
        """Create the complete dialog."""
        def close_dialog(e):
            
            self._close_dialog()
        
        def save_changes_wrapper(e):
            self._save_changes(e, e.control, species)
        
        # Action buttons
        actions = ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Cancel",
                    icon=ft.Icons.CLOSE,
                    style=ft.ButtonStyle(
                        bgcolor=self.GREY_100,
                        color=self.text_secondary,
                        padding=ft.padding.symmetric(horizontal=28, vertical=14),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        side=ft.BorderSide(1, self.GREY_200)
                    ),
                    on_click=close_dialog
                ),
                ft.Container(width=12),
                ft.ElevatedButton(
                    "Save Changes",
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_700,
                        color=self.WHITE,
                        padding=ft.padding.symmetric(horizontal=28, vertical=14),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=2,
                        shadow_color=ft.Colors.with_opacity(0.2, ft.Colors.GREEN_700)
                    ),
                    on_click=save_changes_wrapper
                )
            ], alignment=ft.MainAxisAlignment.END),
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
            bgcolor=self.SECONDARY_CONTAINER,
            border=ft.border.only(top=ft.BorderSide(1, self.GREY_200)),
            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)
        )
        
        # Main container
        main_container = ft.Container(
            content=ft.Column([
                content,
                actions
            ], spacing=0),
            width=width,
            border_radius=16,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        # AlertDialog
        return ft.AlertDialog(
            modal=True,
            content=main_container,
            content_padding=0,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.TRANSPARENT,
        )
    
    def _show_dialog(self, dialog, species):
        """Show the dialog on the page."""
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)
        logger.write(f"Editing species: {species.get('SpeciesCode', '')}")
        self.page.update()