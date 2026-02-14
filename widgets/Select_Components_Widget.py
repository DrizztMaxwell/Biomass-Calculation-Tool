import flet as ft
from data.components_data import COMPONENTS_DATA
from helper_functions.Assets_Helper import asset_helper  # Import the asset helper

class Select_Components_Widget:
    def __init__(
        self,
        page: ft.Page,
        title: ft.Text,
        description_text: ft.Text,
        components_card_row,
        selected_card_component,
        components_data=None,
        display_button=True,
        display_shadow=True,
        on_selection_change=None,
        is_alternate_card=False,
        is_database_selected=False,
        is_in_create_species_page=False
    ):
        self.page = page
        self.title = title
        self.description_text = description_text
        self.components_card_row = components_card_row
        self.selected_card_component = selected_card_component
        self.components_data = components_data or self._prepare_component_data(COMPONENTS_DATA.copy())
        self.display_button = display_button
        self.display_shadow = display_shadow
        self.on_selection_change = on_selection_change
        self.is_alternate_card = is_alternate_card
        self.is_database_selected = is_database_selected
        self.is_in_create_species_page = is_in_create_species_page
        self.original_components_data = self._prepare_component_data(COMPONENTS_DATA.copy())
        
        self._initialize_widget()
    
    def _prepare_component_data(self, components):
        """Update image paths in component data for current environment"""
        for component in components:
            if "image_src" in component:
                component["image_src"] = asset_helper.get_asset_path(component["image_src"])
        return components
    
    def _initialize_widget(self):
        """Initialize the widget and its components"""
        if self.is_in_create_species_page == False:
            self._apply_database_mode()
        elif self.is_in_create_species_page:
            for component in self.components_data:
                component["is_selected"] = False
        else:
            self._apply_database_mode()
        self._create_select_all_button()
        self._build_component_cards()
        self._update_selected_text()
    
    def _apply_database_mode(self):
        """Apply database selection mode: select all and disable if database is selected"""
        for i, component in enumerate(self.components_data):
            if self.is_database_selected:
                component["is_selected"] = True
                component["is_disabled"] = True
            else:
                original_component = self.original_components_data[i]
                component["is_selected"] = original_component.get("is_selected", False)
                component["is_disabled"] = False
    
    def _create_select_all_button(self):
        """Create the select all button"""
        self.select_all_button = ft.TextButton(
            text=self._get_select_all_button_text(),
            icon=ft.Icons.CHECK_BOX_OUTLINED,
            style=ft.ButtonStyle(color=ft.Colors.TERTIARY),
            on_click=self._select_all_components,
            disabled=self.is_database_selected
        )
    
    def _get_select_all_button_text(self):
        """Get the appropriate text for the select all button"""
        if self.is_database_selected:
            return "All Required"
        return "Deselect All" if self._all_components_selected() else "Select All"
    
    def _all_components_selected(self):
        """Check if all components are selected"""
        return all(comp.get("is_selected", False) for comp in self.components_data)
    
    def _get_card_colors(self, is_selected, is_disabled):
        """Get colors for component card based on state"""
        is_light_mode = self.page.theme_mode == ft.ThemeMode.LIGHT
        
        if is_disabled:
            bgcolor = ft.Colors.GREEN_100 
            border_color = ft.Colors.GREEN if is_light_mode else ft.Colors.PRIMARY
        elif is_selected:
            bgcolor = ft.Colors.GREEN_50 if is_light_mode else ft.Colors.GREEN_300 
            border_color = ft.Colors.GREEN if is_light_mode else ft.Colors.PRIMARY
        else:
            bgcolor = ft.Colors.WHITE if is_light_mode else ft.Colors.GREY_300
            border_color = ft.Colors.GREY_300 if is_light_mode else ft.Colors.BLACK
        
        return bgcolor, border_color
    
    def _create_component_card(self, component):
        """Create individual component card"""
        is_disabled = component.get("is_disabled", False)
        is_selected = component["is_selected"]
        bgcolor, border_color = self._get_card_colors(is_selected, is_disabled)
        
        card_content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                self._create_image_container(component, is_disabled),
                self._create_title_text(component, is_disabled)
            ]
        )
        
        card = ft.Container(
            width=150,
            height=150,
            border_radius=10,
            bgcolor=bgcolor,
            border=ft.border.all(2, border_color),
            padding=10,
            alignment=ft.alignment.center,
            animate_scale=None if is_disabled else ft.Animation(300, "easeInOut"),
            scale=1.0,
            content=card_content,
            tooltip=self._get_card_tooltip(is_disabled)
        )
        
        if not is_disabled:
            card.on_click = lambda e, comp=component: self._toggle_component(e, comp)
            card.on_hover = lambda e: self._handle_hover(e, card)
        
        return card
    
    def _create_image_container(self, component, is_disabled):
        """Create image container for component card"""
        return ft.Container(
            width=50,
            height=50,
            alignment=ft.alignment.center,
            content=ft.Image(
                src=component["image_src"],
                fit=ft.ImageFit.CONTAIN,
                color=ft.Colors.GREY_400 if is_disabled else None,
                error_content=ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, size=30)  # Fallback if image fails to load
            )
        )
    
    def _create_title_text(self, component, is_disabled):
        """Create title text for component card"""
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Text(
                value=component["title"],
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.GREY_600 if is_disabled else ft.Colors.BLACK,
                size=18,
                text_align=ft.TextAlign.CENTER
            )
        )
    
    def _get_card_tooltip(self, is_disabled):
        """Get tooltip text for component card"""
        return "Required - cannot be deselected" if is_disabled else "Click to select/deselect"
    
    def _handle_hover(self, e, card):
        """Handle hover effects for enabled cards"""
        card.scale = 1.05 if e.data == "true" else 1.0
        card.update()
    
    def _toggle_component(self, e, component):
        """Handle component selection/deselection for enabled cards"""
        if component.get("is_disabled", False):
            return
        
        component["is_selected"] = not component["is_selected"]
        self._update_card_appearance(e.control, component)
        self._update_ui_state()
        
        if self.on_selection_change:
            self.on_selection_change(self.selected_components)
    
    def _update_card_appearance(self, card, component):
        """Update the visual appearance of a component card"""
        bgcolor, border_color = self._get_card_colors(component["is_selected"], False)
        card.bgcolor = bgcolor
        card.border = ft.border.all(2, border_color)
        card.update()
    
    def _update_ui_state(self):
        """Update all UI elements that depend on selection state"""
        self._update_selected_text()
        self.select_all_button.text = self._get_select_all_button_text()
        self._update_controls()
    
    def _update_selected_text(self):
        """Update selected components text display"""
        if self.is_database_selected:
            self.selected_card_component.value = "All components selected (database mode)"
        elif self.selected_components:
            self.selected_card_component.value = f"Selected: {', '.join(self.selected_components)}"
        else:
            self.selected_card_component.value = "No components selected"
        
        self.selected_card_component.color = ft.Colors.PRIMARY
    
    def _update_controls(self):
        """Update all control states"""
        if hasattr(self.select_all_button, '_Control__page') and self.select_all_button._Control__page is not None:
            self.select_all_button.update()
        self.selected_card_component.update()
    
    def _select_all_components(self, e=None):
        """Select or deselect all enabled components"""
        if self.is_database_selected:
            return
        
        all_selected = self._all_components_selected()
        
        for component in self.components_data:
            if not component.get("is_disabled", False):
                component["is_selected"] = not all_selected
        
        self._rebuild_component_cards()
        self._update_ui_state()
        
        if self.on_selection_change:
            self.on_selection_change(self.selected_components)
    
    def _build_component_cards(self):
        """Build all component cards and add them to the row"""
        self.components_card_row.controls.clear()
        for component in self.components_data:
            self.components_card_row.controls.append(self._create_component_card(component))
    
    def _rebuild_component_cards(self):
        """Rebuild all component cards with current state"""
        for i, component in enumerate(self.components_data):
            if i < len(self.components_card_row.controls):
                card = self.components_card_row.controls[i]
                if not component.get("is_disabled", False):
                    self._update_card_appearance(card, component)
    
    def get_widget(self):
        """Return the Flet widget container"""
        controls = [
            self.title,
            self.description_text,
            self._create_select_all_row(),
            ft.Container(height=10),
            self.components_card_row,
            self._create_selected_display()
        ]
        
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            padding=0 if self.is_alternate_card else 20,
            margin=0 if self.is_alternate_card else 30,
            border_radius=10,
            shadow=self._create_shadow() if self.display_shadow else None,
            alignment=ft.alignment.top_left,
            content=ft.Column(
                controls=controls,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            )
        )
    
    def _create_select_all_row(self):
        """Create the select all button row if display_button is True"""
        if self.display_button:
            return ft.Row(
                controls=[self.select_all_button],
                alignment=ft.MainAxisAlignment.START,
            )
        return ft.Container()
    
    def _create_selected_display(self):
        """Create the selected items display container"""
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_ACCENT_400),
            border_radius=10,
            margin=ft.margin.only(top=10, bottom=10),
            padding=10,
            alignment=ft.alignment.center_left,
            content=self.selected_card_component
        )
    
    def _create_shadow(self):
        """Create box shadow if display_shadow is True"""
        return ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
            offset=ft.Offset(0, 3),
        )
    
    @property
    def selected_components(self):
        """Get list of selected component titles"""
        return [comp["title"] for comp in self.components_data if comp["is_selected"]]
    
    def set_selected_components(self, component_titles):
        """Set specific components as selected (only if not disabled)"""
        if self.is_database_selected:
            return
        
        for component in self.components_data:
            if not component.get("is_disabled", False):
                component["is_selected"] = component["title"] in component_titles
        
        self._rebuild_component_cards()
        self._update_ui_state()
    
    def toggle_database_mode(self, is_database_selected: bool):
        """Toggle between database mode and normal mode"""
        self.is_database_selected = is_database_selected
        self._apply_database_mode()
        self.select_all_button.disabled = is_database_selected
        self.select_all_button.text = self._get_select_all_button_text()
        self._build_component_cards()
        self._update_selected_text()
        self._update_controls()

    def refresh_asset_paths(self):
        """Refresh all asset paths (useful if theme changes or after rebuild)"""
        for component in self.components_data:
            if "image_src" in component:
                component["image_src"] = asset_helper.get_asset_path(component["image_src"])
        self._build_component_cards()