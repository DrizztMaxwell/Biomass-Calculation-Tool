from widgets.LogFileTxt import logger
import flet as ft
from .components.Header import Header
from .components.Content import Content

class About_Dialog_View:
    def __init__(self, page: ft.Page):
        self.page = page
        self.header_component = Header(self.close)
        self.content_component = Content(self._open_email)
        self.container = self._create_about_container()
        self.overlay = self._create_overlay()
        self.is_visible = False

    def show(self):
        """Show the about container with overlay"""
        self.page.overlay.append(self.overlay)
        self.page.overlay.append(self.container)
        self.is_visible = True
        self._update_container_size()
        logger.write("Displayed About Dialog")
        self.page.update()
        
    def close(self, e=None):
        """Close the about container and remove overlay"""
        self.page.overlay.remove(self.overlay)
        self.page.overlay.remove(self.container)
        self.is_visible = False
        logger.write("Closed About Dialog")
        self.page.update()
    
    def _update_container_size(self):
        """Update container size based on current page dimensions"""
        screen_width = self.page.width
        screen_height = self.page.height - 50
        
        dialog_width = min(max(screen_width * 0.90, 800), 1600)
        dialog_height = min(max(screen_height * 0.95, 600), 1200)
        
        self.container.width = dialog_width
        self.container.height = dialog_height
        
        self.container.left = (screen_width - dialog_width) / 2
        self.container.top = (screen_height - dialog_height) / 2
        
        self._update_content_font_sizes(dialog_height)

    def _update_content_font_sizes(self, dialog_height):
        """Dynamically adjust font sizes based on available height"""
        base_height = 800
        scale_factor = min(dialog_height / base_height, 1.2)
        # Font size updates would be handled by the components if needed
        pass

    def _create_overlay(self):
        """Create a dimmed overlay background"""
        return ft.Container(
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            expand=True,
            on_click=lambda e: self.close(),
        )

    def _open_email(self, email_address):
        """Open default email client with the specified email address"""
        self.page.launch_url(f"mailto:{email_address}")

    def _create_about_container(self):
        """Create the about section as a responsive container"""
        return ft.Container(
            content=ft.Column(
                [
                    self.header_component.create(),
                    ft.Container(
                        padding=ft.padding.all(15),
                        content=self.content_component.create(),
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            ),
            width=800,
            height=700,
            top=0,
            left=0,
        )

    def update_view(self):
        """Update the view if needed"""
        self.page.update()