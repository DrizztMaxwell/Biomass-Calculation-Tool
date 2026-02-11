import flet as ft
from .components.Header import Header
from .components.Content import Content

class About_Dialog_View:
    def __init__(self, page: ft.Page):
        self.page = page
        # Passing the restored email method and close method
        self.header_component = Header(self.close)
        self.content_component = Content(self._open_email)
        self.is_visible = False
        
        # Dimmed background overlay
        self.overlay = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
            expand=True,
            on_click=lambda e: self.close(),
        )
        
        # The main dialog container
        self.container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            shadow=ft.BoxShadow(
                blur_radius=40, 
                color=ft.Colors.BLACK45,
                offset=ft.Offset(0, 10)
            ),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
          
        )

    def _open_email(self, email_address):
        """Launches the default system email client."""
        self.page.launch_url(f"mailto:{email_address}")

    def show(self):
        """Calculates size, positions the container, and shows the dialog."""
        self._update_container_size()
        self.page.overlay.append(self.overlay)
        self.page.overlay.append(self.container)
        self.is_visible = True
        self.page.update()
        
    def close(self, e=None):
        """Removes the dialog and overlay from the page."""
        if self.overlay in self.page.overlay:
            self.page.overlay.remove(self.overlay)
        if self.container in self.page.overlay:
            self.page.overlay.remove(self.container)
        self.is_visible = False
        self.page.update()
    
    def _update_container_size(self):
        """
        Forces a professional column layout that fits any desktop window
        without requiring scrollbars.
        """
        screen_w = self.page.width
        screen_h = self.page.height
        
        # Max dimensions to keep the UI looking elegant and "app-like"
        # 500px height is the 'sweet spot' for fitting a 4-row column on most screens.
        target_w = min(screen_w * 0.9, 850)
        target_h = min(screen_h * 0.85, 500) 
        
        self.container.width = target_w
        self.container.height = target_h
        
        # Perfect centering calculation
        self.container.left = (screen_w - target_w) / 2
        self.container.top = (screen_h - target_h) / 2
        
        # Re-inject content into the container
        self.container.content = ft.Column([
            self.header_component.create(),
            ft.Container(
                content=self.content_component.create(),
                padding=ft.padding.only(left=30, right=30, top=20, bottom=30),
                expand=True # This forces the Content column to fill space efficiently
            )
        ], spacing=0)