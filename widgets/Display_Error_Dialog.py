import flet as ft

class Display_Error_Dialog:
    def __init__(self, page: ft.Page, title="Error", description="An error occurred"):
        self.page = page
        self.title = title
        self.description = description
    
    def show(self):
        """Display the error dialog"""
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED_400, size=24),
                ft.Text(self.title, size=18, weight=ft.FontWeight.BOLD),
            ]),
            content=ft.Column([
                ft.Text(self.description, size=14, color=ft.Colors.GREY_700),
            ], tight=True, spacing=10),
            actions=[
                ft.TextButton(
                    "OK",
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED_400,
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    ),
                    on_click=lambda e: self._close_dialog( dialog)
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=10),
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        return dialog
    
    def _close_dialog(self,  dialog: ft.AlertDialog):
        dialog.open = False
        self.page.update()