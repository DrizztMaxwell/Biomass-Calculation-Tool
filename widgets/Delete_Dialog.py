import flet as ft
from widgets.LogFileTxt import logger
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog


class Delete_Dialog:
    """Dialog for confirming species deletion."""
    
    # Constants
    DIALOG_WIDTH_MAX = 500
    DIALOG_WIDTH_RATIO = 0.8
    
    # Colors
    RED_400 = ft.Colors.RED_400
    RED_500 = ft.Colors.RED_500
    RED_600 = ft.Colors.RED_600
    WHITE = ft.Colors.WHITE
    PRIMARY = ft.Colors.PRIMARY
    SECONDARY_CONTAINER = ft.Colors.SECONDARY_CONTAINER
    SECONDARY = ft.Colors.SECONDARY
    GREY_100 = ft.Colors.GREY_100
    GREY_200 = ft.Colors.GREY_200
    BLACK = ft.Colors.BLACK
    TEXT_SECONDARY = ft.Colors.GREY_600
    
    def __init__(self, page):
        self.page = page
    
    def delete_species_confirmation(self, index, filtered_species, species_data, 
                                   controller, text_secondary=None, 
                                   refresh_callback=None, save_callback=None):
        """Show professional confirmation dialog for deletion."""
        
        self.text_secondary = text_secondary or self.TEXT_SECONDARY
        self.controller = controller
        self.refresh_callback = refresh_callback
        self.save_callback = save_callback
        
        # Find the species
        species, actual_index = self._find_species(index, filtered_species, species_data)
        if not species:
            self._show_error_dialog(f"Error: Species not found in master data.")
            return
        
        self.species = species
        self.display_value = self._get_display_value(species)
        self.actual_index = actual_index
        
        # Create and show dialog
        dialog = self._create_dialog()
        self._show_dialog(dialog)
    
    def _find_species(self, index, filtered_species, species_data):
        """Find species by index and locate it in the main data."""
        if index >= len(filtered_species):
            return None, None
        
        species = filtered_species[index]
        species_code = species.get("SpeciesCode", "Unknown")
        spec_common = species.get("SpecCommon", "Unknown")
        
        # Find actual index in species_data
        for i, sp in enumerate(species_data):
            sp_code = sp.get("SpeciesCode")
            sp_common = sp.get("SpecCommon")
            
            if species_code and sp_code and sp_code == species_code:
                return species, i
            elif spec_common and sp_common and sp_common == spec_common:
                return species, i
        
        return None, None
    
    def _get_display_value(self, species):
        """Get display value (common name or code)."""
        species_code = species.get("SpeciesCode", "Unknown")
        spec_common = species.get("SpecCommon", "Unknown")
        
        if spec_common and spec_common != "" and spec_common != "Unknown":
            return spec_common
        return species_code
    
    def _create_dialog(self):
        """Create the complete delete confirmation dialog."""
        dialog_width = self._calculate_dialog_width()
        
        def close_dialog(e):
            self._close_dialog(dialog)
        
        def confirm_delete_wrapper(e):
            self._confirm_delete(dialog)
        
        # Main container
        main_container = ft.Container(
            content=ft.Column([
                self._create_content_container(dialog_width),
                self._create_actions_container(close_dialog, confirm_delete_wrapper)
            ], spacing=0, tight=True),
            width=dialog_width,
            border_radius=16,
            shadow=self._create_main_shadow(),
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        # AlertDialog
        return ft.AlertDialog(
            modal=True,
            content=main_container,
            content_padding=0,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.TRANSPARENT,
            inset_padding=ft.padding.all(20)
        )
    
    def _calculate_dialog_width(self):
        """Calculate dialog width based on page size."""
        return min(self.DIALOG_WIDTH_MAX, self.page.width * self.DIALOG_WIDTH_RATIO)
    
    def _create_main_shadow(self):
        """Create main container shadow."""
        return ft.BoxShadow(
            spread_radius=2,
            blur_radius=40,
            color=ft.Colors.with_opacity(0.25, self.BLACK),
            offset=ft.Offset(0, 10)
        )
    
    def _create_content_container(self, width):
        """Create content container with header and warning."""
        return ft.Container(
            content=ft.Column([
                self._create_header(),
                self._create_warning_content()
            ], spacing=0),
            width=width,
            bgcolor=self.SECONDARY,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
    
    def _create_header(self):
        """Create dialog header with warning gradient."""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=36, color=self.WHITE),
                    bgcolor=ft.Colors.with_opacity(0.3, self.WHITE),
                    padding=14,
                    border_radius=14,
                    margin=ft.margin.only(right=15)
                ),
                ft.Column([
                    ft.Text(
                        "Confirm Delete", 
                        size=24, 
                        weight=ft.FontWeight.W_700, 
                        color=self.WHITE
                    ),
                    ft.Text(
                        f"Species: {self.display_value}", 
                        size=14, 
                        color=ft.Colors.with_opacity(0.9, self.WHITE)
                    ),
                ], spacing=4, alignment=ft.CrossAxisAlignment.START)
            ], alignment=ft.MainAxisAlignment.START),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[self.RED_600, self.RED_400]
            ),
            padding=ft.padding.symmetric(horizontal=30, vertical=24),
            border_radius=ft.border_radius.only(top_left=16, top_right=16),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.2, self.BLACK)
            )
        )
    
    def _create_warning_content(self):
        """Create warning content block."""
        return ft.Container(
            content=ft.Column([
                ft.Container(height=30),
                self._create_warning_icon(),
                self._create_warning_text(),
                ft.Container(height=30),
            ], spacing=0),
            padding=ft.padding.symmetric(horizontal=30),
        )
    
    def _create_warning_icon(self):
        """Create warning icon container."""
        return ft.Container(
            content=ft.Icon(ft.Icons.ERROR_OUTLINE, size=60, color=self.RED_400),
            padding=20,
            bgcolor=ft.Colors.with_opacity(0.1, self.RED_400),
            border_radius=50,
            margin=ft.margin.only(bottom=20)
        )
    
    def _create_warning_text(self):
        """Create warning text content."""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    f"Are you sure you want to delete species ", 
                    size=18, 
                    weight=ft.FontWeight.W_600, 
                    color=self.PRIMARY,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    f"{self.display_value}?", 
                    size=18, 
                    weight=ft.FontWeight.BOLD, 
                    color=self.PRIMARY,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=10),
                ft.Text(
                    "This action cannot be undone. All associated data will be permanently removed.", 
                    size=14, 
                    color=self.PRIMARY,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=5),
                ft.Text(
                    "⚠️ Warning: This is a destructive operation", 
                    size=13, 
                    color=self.RED_500,
                    weight=ft.FontWeight.W_500,
                    text_align=ft.TextAlign.CENTER
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            padding=ft.padding.all(30),
            bgcolor=self.SECONDARY_CONTAINER,
            border_radius=12,
            border=ft.border.all(1, self.GREY_100),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.08, self.BLACK)
            )
        )
    
    def _create_actions_container(self, close_handler, delete_handler):
        """Create action buttons container."""
        return ft.Container(
            content=ft.Row([
                self._create_cancel_button(close_handler),
                ft.Container(width=12),
                self._create_delete_button(delete_handler)
            ], alignment=ft.MainAxisAlignment.END),
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
            bgcolor=self.SECONDARY_CONTAINER,
            border=ft.border.only(top=ft.BorderSide(1, self.GREY_200)),
            border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16)
        )
    
    def _create_cancel_button(self, click_handler):
        """Create cancel button."""
        return ft.ElevatedButton(
            "Cancel",
            icon=ft.Icons.CLOSE,
            style=ft.ButtonStyle(
                bgcolor=self.GREY_100,
                color=self.text_secondary,
                padding=ft.padding.symmetric(horizontal=28, vertical=14),
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(1, self.GREY_200)
            ),
            on_click=click_handler
        )
    
    def _create_delete_button(self, click_handler):
        """Create delete button."""
        return ft.ElevatedButton(
            "Delete Species",
            icon=ft.Icons.DELETE,
            style=ft.ButtonStyle(
                bgcolor=self.RED_500,
                color=self.WHITE,
                padding=ft.padding.symmetric(horizontal=28, vertical=14),
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=2,
                shadow_color=ft.Colors.with_opacity(0.2, self.RED_500)
            ),
            on_click=click_handler
        )
    
    def _confirm_delete(self, dialog):
        """Handle delete confirmation."""
        logger.write(f"Confirming deletion of species: {self.species.get('SpeciesCode', '')}")
        self._close_dialog(dialog)
        
        try:
            # Re-confirm index before deletion
            current_actual_index = self._reconfirm_index()
            
            if current_actual_index is None:
                self._show_error_dialog(f"Species '{self.display_value}' not found just before deletion.")
                logger.write(f"Error: Species '{self.display_value}' not found just before deletion.")
                return
            
            # Perform deletion
            success = self._perform_deletion(current_actual_index)
            
            if success:
                self._show_success_message()
                if self.refresh_callback:
                    self.refresh_callback()
            else:
                self._show_error_dialog("Failed to save data after deleting species. Deletion canceled.")
                logger.write(f"Failed to save data after deleting species '{self.display_value}'. Deletion canceled.")
                
        except Exception as e:
            self._show_error_dialog(f"Error deleting species: {e}")
            logger.write(f"Exception while deleting species '{self.display_value}': {e}")
        
        self.page.update()
    
    def _reconfirm_index(self):
        """Re-confirm the species index before deletion."""
        species_code = self.species.get("SpeciesCode", "Unknown")
        spec_common = self.species.get("SpecCommon", "Unknown")
        
        for i, sp in enumerate(self.controller.get_species_data()):
            sp_code = sp.get("SpeciesCode")
            sp_common = sp.get("SpecCommon")
            
            if species_code and sp_code and sp_code == species_code:
                return i
            elif spec_common and sp_common and sp_common == spec_common:
                return i
        
        return None
    
    def _perform_deletion(self, index):
        """Perform the actual deletion."""
        deleted_species = self.controller.get_species_data().pop(index)
        
        # Try to save
        if self._save_species_data():
            return True
        else:
            # Rollback on failure
            self.controller.get_species_data().insert(index, deleted_species)
            return False
    
    def _save_species_data(self):
        """Save species data using callback or default."""
        if self.save_callback:
            return self.save_callback()
        return False
    
    def _show_success_message(self):
        """Show success message after deletion."""
        Custom_Alert_Dialog(
            page=self.page, 
            title_icon=ft.Icons.CHECK_CIRCLE, 
            title_color=self.BLACK, 
            title_icon_color=ft.Colors.GREEN,  
            title="Success", 
            message=f"Species '{self.display_value}' deleted successfully!", 
            button_text="OK"
        ).show()
        logger.write(f"Species '{self.display_value}' deleted successfully.")
    
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
                        bgcolor=self.RED_500,
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
    
    def _close_dialog(self, dialog):
        """Close the main dialog."""
        dialog.open = False
        self.page.update()
    
    def _show_dialog(self, dialog):
        """Show the dialog on the page."""
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)
        logger.write(f"Confirming deletion of species: {self.species.get('SpeciesCode', '')}")
        self.page.update()