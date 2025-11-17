import flet as ft

class Error_Alert_Import_Data_Dialog:
    """
    Simple error alert dialog for missing fields in import data.
    """
    def __init__(self, error_message, page: ft.Page = None):
        self.error_message = error_message
        self.page = page

    def show(self):
        """
        Display error alert dialog for missing fields.
        """
        self.error_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error: Fields not found.", color=ft.Colors.RED_700),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Fields not detected. Please make sure you have the following column names in text import file:",
                        size=14,
                    ),
                    ft.Text(
                        self.error_message,
                        size=14,
                        weight=ft.FontWeight.W_500,
                        selectable=True,
                        color=ft.Colors.BLUE_800
                    ),
                    ft.Text(
                        "The required column names can be case insensitive in text file.",
                        size=14,
                        italic=True
                    )
                ],
                tight=True,
                spacing=10
            ),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self._close_dialog(e)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return self.error_dialog
        
    def _close_dialog(self, e):
            self.page.close(self.error_dialog)
        
    
        