import flet as ft

class Submit_Button:
    """Creates the submit button."""
    
    def __init__(self, page: ft.Page, on_click_handler):
        self.page = page
        self.on_click_handler = on_click_handler
        
    def build(self):
        """Build the submit button."""
        return ft.Row(
            [
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("Create Species", size=16, weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.ADD, size=20)
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                    on_click=self.on_click_handler,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE,
                    height=40,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )