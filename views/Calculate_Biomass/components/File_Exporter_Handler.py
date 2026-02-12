import datetime
import os
import flet as ft
from widgets.LogFileTxt import logger

class File_Exporter_Handler:
    """File export functionality."""
    
    def __init__(self, page: ft.Page, selected_file_path: str, controller):
        self.page = page
        self.selected_file_path = selected_file_path
        self.controller = controller
        self.file_picker = self._setup_file_picker()
    
    def _setup_file_picker(self) -> ft.FilePicker:
        """Setup file picker."""
        print("Setting up file picker for export")
        file_picker = ft.FilePicker(on_result=self._on_file_save_result)
        self.page.overlay.append(file_picker)
        # CRITICAL FIX: Update the page to register the file picker
        self.page.update()
        return file_picker
    
    def open_export_dialog(self):
        """Open file save dialog for export."""
        print("Opening export dialog")
        default_filename = self._generate_export_filename()
        
        # Make sure the page is updated before opening dialog
        self.page.update()
        
        self.file_picker.save_file(
            dialog_title="Save Biomass Results",
            file_name=default_filename,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"]
        )
        
        logger.write("Export file dialog opened")
    
    def _generate_export_filename(self) -> str:
        """Generate export filename with timestamp."""
        now = datetime.datetime.now()
        date_prefix = now.strftime("%Y%m%d")
        time_prefix = now.strftime("%H%M%S")
        
        if self.selected_file_path and os.path.isfile(self.selected_file_path):
            filename = os.path.splitext(
                os.path.basename(self.selected_file_path)
            )[0]
            result = f"Output_{filename}_{date_prefix}_{time_prefix}.txt"
            logger.write(f"Generated export filename: {result}")
            return result
        
        result = f"Output_Biomass_Results_{date_prefix}_{time_prefix}.txt"
        logger.write(f"Generated default export filename: {result}")
        return result
    
    def _on_file_save_result(self, event: ft.FilePickerResultEvent):
        """Handle file save result."""
        print(f"File save result received: {event.path}")
        if not event.path:
            logger.write("Export cancelled by user")
            print("Export cancelled by user")
            return
        
        try:
            print(f"Attempting to export data to: {event.path}")
            success = self.controller.export_results_to_text_file(event.path)
            print(f"Export success: {success}")
            if success:
                logger.write(f"Data exported successfully to {event.path}")
                print(f"Data exported successfully to {event.path}")
            else:
                logger.write(f"[Error] - Failed to export data to {event.path}")
                print(f"Failed to export data to {event.path}")
        except Exception as error:
            logger.write(f"[Error] - Failed to export data: {error}")
            print(f"Failed to export data: {error}")
        finally:
            self.page.update()