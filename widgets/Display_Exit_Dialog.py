import flet as ft

class Display_Exit_Dialog:
    def __init__(self, page: ft.Page):
        self.page = page
        
        self.dialog = self._create_dialog()
    def yes_clicked(self, e):
        self.page.window.destroy()

    def no_clicked(self, e):
        self.page.close(self.get_dialog())
    def _create_dialog(self) -> ft.AlertDialog:
        return ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=24),
                    ft.Text("Confirm Exit", size=18, weight=ft.FontWeight.BOLD),
                ]
            ),
            content=ft.Container(
                content=ft.Text(
                    "You're about to close the application. Are you sure you want to exit the application?",
                    size=16,
                ),
            ),
            actions=[
                ft.OutlinedButton(
                    "Stay",
                    on_click=self.no_clicked,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                ft.FilledButton(
                    "Exit Anyway",
                    on_click=self.yes_clicked,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_700,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=16),
            content_padding=ft.padding.all(24),
        )
    
    def get_dialog(self) -> ft.AlertDialog:
        """Return the AlertDialog instance"""
        return self.dialog
    
    def open_dialog(self):
        """Open the dialog on the given page"""
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
    
    def close_dialog(self):
        """Close the dialog on the given page"""
        self.dialog.open = False
        self.page.update()