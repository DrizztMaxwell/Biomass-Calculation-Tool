import flet as ft
from widgets.LogFileTxt import logger


class View_Dialog:
    """Base class for dialog views in the application."""
    
    # Constants for styling
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
    TERTIARY = ft.Colors.TERTIARY
    PURPLE_600 = ft.Colors.PURPLE_600
    BLACK = ft.Colors.BLACK
    BLUE_600 = ft.Colors.BLUE_600
    
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
    
    def __init__(self, page:ft.Page,):
        self.page = page
        
    
    def view_species_dialog(self, index, species_data, filtered_species=None, primary_color=None, secondary_color=None, accent_color=None):
        """Show species details in a beautiful professional dialog."""
        
        # Use provided colors or defaults
        self.primary_color = primary_color or self.PRIMARY_COLOR
        self.secondary_color = secondary_color or self.SECONDARY_COLOR
        self.accent_color = accent_color or self.ACCENT_COLOR
        self.text_primary = self.TEXT_PRIMARY
        self.text_secondary = self.TEXT_SECONDARY
        
        # Set colors for parameter categories
        self.PARAMETER_CATEGORIES["bh"]["color"] = self.secondary_color
        self.PARAMETER_CATEGORIES["b"]["color"] = self.accent_color
        
        if filtered_species and index >= len(filtered_species):
            return
        print("Filtere Species in View Dialog:", filtered_species)
        
        species = filtered_species[index] if filtered_species else species_data[index]
        
        # Calculate dialog dimensions
        dialog_width = min(self.DIALOG_WIDTH_MAX, self.page.width * self.DIALOG_WIDTH_RATIO)
        max_dialog_height = min(self.DIALOG_HEIGHT_MAX, self.page.height * self.DIALOG_HEIGHT_RATIO)
        
        # Create dialog content
        dialog_content = self._create_dialog_content(species, dialog_width, max_dialog_height)
        
        # Create and show dialog
        dialog = self._create_dialog(species, dialog_content, dialog_width)
        self._show_dialog(dialog, species)
    
    def _create_dialog_content(self, species, width, height):
        """Create the main dialog content."""
        return ft.Container(
            content=ft.Column([
                self._create_header(species),
                self._create_scrollable_content(species)
            ], spacing=0),
            width=width,
            height=height,
            bgcolor=self.SECONDARY,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
    
    def _create_header(self, species):
        """Create dialog header with gradient background."""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.REMOVE_RED_EYE_OUTLINED, size=32, color=self.WHITE),
                    bgcolor=ft.Colors.with_opacity(0.2, self.WHITE),
                    padding=12,
                    border_radius=12,
                    margin=ft.margin.only(right=15)
                ),
                ft.Column([
                    ft.Text(
                        "Species Details", 
                        size=24, 
                        weight=ft.FontWeight.W_700, 
                        color=self.WHITE
                    ),
                    ft.Text(
                        f"Species Code: {species.get('SpeciesCode', '')}", 
                        size=14, 
                        color=ft.Colors.with_opacity(0.9, self.WHITE)
                    ),
                ], spacing=4, alignment=ft.CrossAxisAlignment.START)
            ], alignment=ft.MainAxisAlignment.START),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[self.primary_color, self.BLUE_600]
            ),
            padding=ft.padding.symmetric(horizontal=30, vertical=24),
            border_radius=ft.border_radius.only(top_left=16, top_right=16),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, self.BLACK)
            )
        )
    
    def _create_scrollable_content(self, species):
        """Create scrollable content area with species details."""
        return ft.Container(
            content=ft.Column([
                ft.Container(height=24),
                self._create_basic_info_card(species),
                ft.Container(height=24),
                *self._create_parameter_cards(species),
                ft.Container(height=24),
            ], scroll=ft.ScrollMode.AUTO, spacing=0, tight=True),
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
            expand=True
        )
    
    def _create_basic_info_card(self, species):
        """Create basic information card."""
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
                
                ft.Container(height=20),
                self._create_detail_row("Species Code", str(species.get("SpeciesCode", "")), ft.Icons.TAG),
                ft.Container(height=12),
                self._create_detail_row("Common Name", species.get("SpecCommon", "N/A"), ft.Icons.TEXT_SNIPPET),
                ft.Container(height=12),
                self._create_detail_row("Origin", species.get("Origin", ""), ft.Icons.LOCATION_ON),
                ft.Container(height=12),
                self._create_detail_row("Equation Type", species.get("EquationType", "Height-based"), ft.Icons.FUNCTIONS),
                ft.Container(height=5),
            ], spacing=0),
            padding=ft.padding.all(24),
            bgcolor=self.SECONDARY_CONTAINER,
            border_radius=12,
            border=ft.border.all(1, self.GREY_100),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.08, self.BLACK)
            )
        )
    
    def _create_detail_row(self, title, value, icon):
        """Helper to create a detail row with icon."""
        return ft.Row([
            ft.Icon(icon, color=self.text_secondary, size=18),
            ft.Text(title + ":", size=14, weight=ft.FontWeight.W_500, color=self.text_secondary),
            ft.Container(expand=True),
            ft.Text(str(value), size=14, weight=ft.FontWeight.W_600, color=self.text_primary),
        ], alignment=ft.MainAxisAlignment.START)
    
    def _create_parameter_cards(self, species):
        """Create parameter cards for the species."""
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
                    "params": []
                }
            
            categorized[category_key]["params"].append((key, value))
        
        return categorized
    
    def _create_parameter_category_card(self, category_data):
        """Create a card for a parameter category."""
        param_rows = ft.Column(spacing=8)
        
        # Create rows for each parameter
        for param_key, param_value in category_data["params"]:
            param_rows.controls.append(self._create_parameter_row(param_key, param_value))
        
        # Create header row
        header = ft.Row([
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
        ], spacing=0)
        
        # Create parameter table header
        table_header = ft.Container(
            content=ft.Row([
                ft.Text(
                    "Parameter", 
                    size=13,
                    weight=ft.FontWeight.W_600,
                    color=self.PRIMARY,
                    width=180
                ),
                ft.Text(
                    "Value", 
                    size=13,
                    weight=ft.FontWeight.W_600,
                    color=self.PRIMARY
                ),
            ], spacing=0),
            padding=ft.padding.symmetric(horizontal=15, vertical=8),
            bgcolor=self.SECONDARY_CONTAINER,
            border_radius=6,
            border=ft.border.all(0.5, self.GREY_200)
        )
        
        return ft.Container(
            content=ft.Column([
                header,
                ft.Container(height=18),
                ft.Column([
                    table_header,
                    ft.Container(height=8),
                    param_rows
                ])
            ], spacing=0),
            padding=24,
            bgcolor=self.SECONDARY_CONTAINER,
            border_radius=12,
            border=ft.border.all(1, self.PRIMARY),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.08, self.BLACK)
            )
        )
    
    def _create_parameter_row(self, param_key, param_value):
        """Create a single parameter row."""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(
                        param_key, 
                        size=14, 
                        weight=ft.FontWeight.W_500,
                        color=self.PRIMARY
                    ),
                    width=180,
                    padding=ft.padding.symmetric(vertical=10, horizontal=15)
                ),
                ft.VerticalDivider(width=1, color=self.GREY_200),
                ft.Container(
                    content=ft.Text(
                        f"{float(param_value):.6f}", 
                        size=14, 
                        weight=ft.FontWeight.W_600,
                        color=self.PRIMARY
                    ),
                    expand=True,
                    padding=ft.padding.symmetric(vertical=10, horizontal=15),
                    bgcolor=self.SECONDARY_CONTAINER, 
                    border_radius=6
                )
            ], spacing=0),
            border=ft.border.all(0.5, self.GREY_200),
            border_radius=6,
            bgcolor=self.SECONDARY_CONTAINER
        )
    
    def _create_dialog(self, species, content, width):
        """Create the complete dialog."""
        def close_dialog(e):
            logger.write(f"Species details dialog closed for species: {species.get('SpeciesCode', '')}")
            self.page.dialog.open = False
            self.page.update()
        
        # Action buttons
        actions = ft.Container(
            content=ft.Row([
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Close",
                    icon=ft.Icons.CLOSE,
                    style=ft.ButtonStyle(
                        bgcolor=self.TERTIARY,
                        color=self.WHITE,
                        padding=ft.padding.symmetric(horizontal=28, vertical=14),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        side=ft.BorderSide(1, self.GREY_200)
                    ),
                    on_click=close_dialog
                ),
                ft.Container(width=12),
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
            inset_padding=ft.padding.symmetric(horizontal=20, vertical=40)
        )
    
    def _show_dialog(self, dialog, species):
        """Show the dialog on the page."""
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)
        logger.write(f"Viewing species: {species.get('SpeciesCode', '')}")
        self.page.update()