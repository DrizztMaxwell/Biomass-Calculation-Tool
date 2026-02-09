from widgets.LogFileTxt import logger
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget
from controller.SideNavbar_Controller import SideNavbar_Controller
from views.SideNavbar_View import SideNavbar_View
from constants.EULA_Constants import EULA_Constants
from .components.Create_Header import Create_Header
from .components.Create_Section import Create_Section
from .components.Create_Exit_Content import Create_Exit_Content
from .components.Create_Button import Create_Button
class EULA_View:
    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller
        self.constants = EULA_Constants()
    
    def get_eula_view(self) -> None:
        """Display the EULA view with terms and acceptance buttons."""
        layout = self._create_eula_layout()
        self._display_on_page(layout)
    
    def _create_eula_layout(self) -> ft.Container:
        """Create the main EULA layout that fits screen without scrolling."""
        return ft.Container(
            bgcolor=self.constants.PRIMARY_COLOR,
            content=ft.Column(
                controls=[
                    Create_Header(),
                    ft.Divider(height=1, color=self.constants.BORDER_COLOR),
                    self._create_scrollable_content(),
                    ft.Divider(height=1, color=self.constants.BORDER_COLOR),
                    self._create_button_row(),
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.all(self.constants.CONTENT_PADDING),
            margin=ft.margin.all(self.constants.MARGIN),
            border_radius=self.constants.BORDER_RADIUS,
            border=ft.border.all(1, self.constants.BORDER_COLOR),
            expand=True
        )
    
    def _create_scrollable_content(self) -> ft.Container:
        """Create scrollable content area that prevents overlapping."""
        return ft.Container(
            content=ft.ListView(
                controls=[
                    Create_Section(
                        self.constants.TERMS_HEADING,
                        self.constants.TERMS_CONTENT,
                        self.constants.TERMS_ICON
                    ),
                    Create_Section(
                        self.constants.ACCEPTANCE_HEADING,
                        self.constants.ACCEPTANCE_CONTENT,
                        self.constants.ACCEPTANCE_ICON
                    ),
                    Create_Section(
                        self.constants.DISCLAIMER_HEADING,
                        self.constants.DISCLAIMER_CONTENT,
                        self.constants.DISCLAIMER_ICON
                    )
                ],
                spacing=self.constants.SECTION_SPACING,
                # Auto-scroll when content is too long
                auto_scroll=False,
            ),
            expand=True,  # Take all available space between header and buttons
        )
    
    
    def _create_button_row(self) -> ft.Container:
        """Create row with agree/disagree buttons - fixed at bottom."""
        agree_button = Create_Button(self.constants.AGREE_BUTTON, "white", ft.Colors.GREEN_400, lambda e: self._handle_user_choice(e, agreed=True), )
        disagree_button = Create_Button(self.constants.DISAGREE_BUTTON, "white", ft.Colors.RED_400, lambda e: self._handle_user_choice(e, agreed=False), )    
        return ft.Container(
            content=ft.Row(
                controls=[
           
                    disagree_button,
                            agree_button,
                ],
                spacing=self.constants.BUTTON_SPACING,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=ft.padding.only(top=20),
            height=70,  # Fixed height to prevent resizing
        )
    
    
    def _handle_user_choice(self, event: ft.ControlEvent, agreed: bool) -> None:
        """Handle user's EULA choice (agree or disagree)."""
        button_text = self.constants.AGREE_BUTTON if agreed else self.constants.DISAGREE_BUTTON
        print(f"Button clicked: {button_text}")
        
        if agreed:
            logger.write("User agreed to EULA - proceeding with application")
            self._proceed_to_application()
        else:
            logger.write("User rejected EULA - application cannot proceed")
            self._show_exit_view()
    
    def _proceed_to_application(self) -> None:
        """Proceed to the main application."""
        self.page.clean()
        SideNavbar_Controller(SideNavbar_View(self.page)).build()
        self.page.update()
    
    def _show_exit_view(self) -> None:
        """Show exit view when user disagrees."""
        self.page.clean()
        self._display_exit_view()
        self.page.update()
    
    def _display_exit_view(self) -> None:
        """Display the exit view."""
        self.page.add(self._create_exit_layout())
    
    def _create_exit_layout(self) -> ft.Container:
        """Create exit view layout."""
        return ft.Container(
            content=ft.Container(
                content=Create_Exit_Content(self),
                border_radius=self.constants.BORDER_RADIUS,
                border=ft.border.all(1, self.constants.BORDER_COLOR),
                height=400,
                expand=True
            ),
            expand=True,
            alignment=ft.alignment.center
        )
    
    
    
    def _display_on_page(self, layout: ft.Container) -> None:
        """Display the layout on the page - centered and without scrolling."""
        self.page.add(
            ft.Container(
                margin=30,
                content=layout,
                bgcolor=self.constants.PRIMARY_COLOR,
                expand=True
            )
        )
    
   