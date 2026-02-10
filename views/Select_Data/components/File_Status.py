# components/FileStatus.py

import flet as ft

class File_Status:
    def __init__(self, controller):
        self.controller = controller
        self.text = ft.Text(
            "File selected: No file selected",
            size=13,
            color=ft.Colors.GREY_700,
            weight=ft.FontWeight.W_500,
        )

    def create(self):
        return ft.Container(
            content=self.text,
            padding=ft.padding.all(16),
            bgcolor=ft.Colors.CYAN_50,
            border_radius=ft.border_radius.all(8),
            border=ft.border.all(1, ft.Colors.CYAN_200),
        )
    def _get_file_status_text(self, file_path):
        """Generate status text based on the file path"""
        
        self.controller._get_file_status().value
        
    def set_file_status(self, status_text):
        """Update the file status text"""
        self.text.value = status_text
        self.text.update()
    def update(self):
        self.text.value = ""
        