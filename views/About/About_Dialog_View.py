import flet as ft
from .components.Header import Header
from .components.Content import Content

class About_Dialog_View:
    def __init__(self, page: ft.Page):
        self.page = page
        # Passing page reference to components
        self.header_component = Header(self.close, page)
        self.content_component = Content(self._open_email, page)
        self.is_visible = False
        
        self._init_colors()
        
        # Dimmed background overlay
        self.overlay = ft.Container(
            bgcolor=self.overlay_color,
            expand=True,
            on_click=lambda e: self.close(),
        )
        
        # The main dialog container
        self.container = ft.Container(
            bgcolor=self.bg_color,
            border_radius=16,
            shadow=ft.BoxShadow(
                blur_radius=40, 
                color=self.shadow_color,
                offset=ft.Offset(0, 10)
            ),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            # animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )
        
        # Constants for height calculation
        self.HEADER_HEIGHT = 70  # Approximate header height
        self.SECTION_HEIGHT = 120  # Approximate height per content section
        self.CONTACT_HEIGHT = 80  # Height of contact section
        self.PADDING_TOTAL = 80  # Total vertical padding (top + bottom)

    def _init_colors(self):
        """Initialize colors based on current theme mode"""
        self.shadow_color = ft.Colors.BLACK45
        
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.bg_color = ft.Colors.WHITE
            self.shadow_color = ft.Colors.BLACK45
            self.overlay_color = ft.Colors.with_opacity(0.7, ft.Colors.BLACK)
        else:
            self.bg_color = ft.Colors.GREY_900
            self.overlay_color = ft.Colors.with_opacity(0.8, ft.Colors.BLACK)

    def _update_theme_colors(self):
        """Update colors when theme changes"""
        self._init_colors()
        
        # Update overlay
        self.overlay.bgcolor = self.overlay_color
        
        # Update container
        self.container.bgcolor = self.bg_color
        self.container.shadow.color = self.shadow_color
        
        # Update components
        self.header_component.update_colors()
        self.content_component.update_colors()

    def _open_email(self, email_address):
        """Launches the default system email client."""
        self.page.launch_url(f"mailto:{email_address}")

    def _calculate_optimal_height(self):
        """Calculate the optimal height based on content, with max limit"""
        # Count number of content sections (3 main sections + contact)
        num_sections = 3  # Overview, Precision & Features, Intended For
        contact_present = 1  # Contact section is always present
        
        # Calculate total content height
        sections_height = num_sections * self.SECTION_HEIGHT
        contact_height = contact_present * self.CONTACT_HEIGHT
        
        # Total needed height including header and padding
        total_needed = (self.HEADER_HEIGHT + 
                       sections_height + 
                       contact_height + 
                       self.PADDING_TOTAL)
        
        # Maximum height (90% of screen height)
        max_height = self.page.height * 0.9 if self.page.height else 800
        
        # Return the smaller of needed height or max height
        return min(total_needed, max_height)

    def show(self):
        """Calculates size, positions the container, and shows the dialog."""
        self._update_theme_colors()
        self._update_container_size()
        #print window dimensions and calculated optimal height for debugging
        print(f"Window dimensions: {self.page.width}x{self.page.height}")
        
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
        """Updates container size and position based on content"""
        screen_w = self.page.width
        screen_h = self.page.height
        
        # Calculate optimal height based on content
        optimal_h = self._calculate_optimal_height()
        
        # Width calculation (fixed logic)
        target_w = min(screen_w * 0.9, 850)
        target_h = optimal_h
        
        self.container.width = target_w
        self.container.height = target_h
        
        self.container.left = (screen_w - target_w) / 2
        self.container.top = (screen_h - target_h) / 2
        
        # Create content without scrolling
        self.container.content = ft.Column([
            self.header_component.create(),
            ft.Container(
                content=self.content_component.create(),
                padding=ft.padding.only(left=30, right=30, top=20, bottom=20),
                expand=False  # Don't expand - use fixed height based on content
            )
        ], spacing=0, )  # No scrolling needed

    def handle_theme_change(self):
        """Public method to handle theme changes while dialog is visible"""
        if self.is_visible:
            self._update_theme_colors()
            self._update_container_size()
            self.page.update()