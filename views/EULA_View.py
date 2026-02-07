from widgets.LogFileTxt import logger
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget
from controller.SideNavbar_Controller import SideNavbar_Controller
from views.SideNavbar_View import SideNavbar_View
from constants.EULA_Constants import EULA_Constants

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
        """Create the main EULA layout."""
        return ft.Container(
            bgcolor=self.constants.PRIMARY_COLOR,
            content=ft.Column(
                controls=[
                    self._create_header(),
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
    
    def _create_header(self) -> ft.Container:
        """Create the EULA header with icon and title."""
        return ft.Container(
            bgcolor=self.constants.PRIMARY_COLOR,
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=self.constants.HEADER_ICON,
                        size=self.constants.HEADER_SIZE,
                        color=self.constants.HEADER_COLOR
                    ),
                    ft.Column(
                        controls=[
                            self._create_text(
                                self.constants.TITLE,
                                size=self.constants.TITLE_SIZE,
                                color=self.constants.HEADER_COLOR
                            ),
                            self._create_text(
                                self.constants.SUBTITLE,
                                size=self.constants.SUBTITLE_SIZE,
                                color=self.constants.TEXT_COLOR
                            )
                        ],
                        spacing=2
                    )
                ],
                spacing=15
            ),
            padding=ft.padding.only(bottom=20)
        )
    
    def _create_scrollable_content(self) -> ft.Container:
        """Create the scrollable content area with all EULA sections."""
        sections = [
            self._create_section(
                self.constants.TERMS_HEADING,
                self.constants.TERMS_CONTENT,
                self.constants.TERMS_ICON
            ),
            self._create_section(
                self.constants.ACCEPTANCE_HEADING,
                self.constants.ACCEPTANCE_CONTENT,
                self.constants.ACCEPTANCE_ICON
            ),
            self._create_section(
                self.constants.DISCLAIMER_HEADING,
                self.constants.DISCLAIMER_CONTENT,
                self.constants.DISCLAIMER_ICON
            )
        ]
        
        return ft.Container(
            bgcolor=self.constants.PRIMARY_COLOR,
            content=ft.ListView(
                controls=sections,
                spacing=self.constants.SECTION_SPACING,
            ),
            padding=ft.padding.symmetric(vertical=15),
            expand=True
        )
    
    def _create_section(self, heading: str, content: str, icon: str) -> ft.Container:
        """Create a consistent section with heading and content."""
        return ft.Container(
            bgcolor=self.constants.PRIMARY_COLOR,
            content=ft.Column(
                controls=[
                    self._create_section_heading(heading, icon),
                    self._create_section_content(content)
                ],
                spacing=self.constants.SECTION_SPACING,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            padding=ft.padding.symmetric(vertical=10)
        )
    
    def _create_section_heading(self, heading: str, icon: str) -> ft.Row:
        """Create section heading with icon."""
        return ft.Row(
            controls=[
                ft.Icon(
                    name=icon,
                    size=20,
                    color=self.constants.HEADER_COLOR
                ),
                self._create_text(
                    heading,
                    size=self.constants.SECTION_HEADING_SIZE,
                    color=self.constants.HEADER_COLOR
                )
            ],
            spacing=10
        )
    
    def _create_section_content(self, content: str) -> ft.Container:
        """Create styled section content container."""
        return ft.Container(
            content=self._create_text(
                content,
                size=self.constants.SECTION_TEXT_SIZE,
                color=self.constants.TEXT_COLOR
            ),
            margin=ft.margin.only(left=30, top=10, bottom=10),
            padding=ft.padding.all(15),
            bgcolor=self.constants.PRIMARY_COLOR,
            border_radius=self.constants.CONTENT_BORDER_RADIUS,
            border=ft.border.all(1, self.constants.BORDER_COLOR)
        )
    
    def _create_button_row(self) -> ft.Container:
        """Create row with agree/disagree buttons."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    self._create_disagree_button(),
                    self._create_agree_button()
                ],
                spacing=self.constants.BUTTON_SPACING,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=ft.padding.only(top=20)
        )
    
    def _create_agree_button(self) -> ft.ElevatedButton:
        """Create the 'Agree' button."""
        return button_widget.ButtonWidget.create_button(
            label=self.constants.AGREE_BUTTON,
            on_click=lambda e: self._handle_user_choice(e, agreed=True),
            color=ft.Colors.GREEN_400
        )
    
    def _create_disagree_button(self) -> ft.ElevatedButton:
        """Create the 'Disagree' button."""
        return button_widget.ButtonWidget.create_button(
            label=self.constants.DISAGREE_BUTTON,
            on_click=lambda e: self._handle_user_choice(e, agreed=False),
            color=ft.Colors.RED_400
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
             
                 
                        self._create_exit_content(),
                       
                 
             
                border_radius=self.constants.BORDER_RADIUS,
                border=ft.border.all(1, self.constants.BORDER_COLOR),

                height=400,
                expand=True
            ),
            expand=True,
            alignment=ft.alignment.center
        )
    
    def _create_exit_content(self) -> ft.Column:
        """Create exit view content."""
        return container_widget.ContainerWidget.create_column(
            widgets=[
                ft.Icon(
                    name=self.constants.EXIT_ICON,
                    size=64,
                    color=self.constants.ERROR_COLOR
                ),
                self._create_text(
                    self.constants.EXIT_TITLE,
                    size=self.constants.TITLE_SIZE,
                    color=self.constants.ERROR_COLOR
                ),
                ft.Container(
                    content=self._create_text(
                        self.constants.EXIT_MESSAGE,
                        size=self.constants.EXIT_MESSAGE_SIZE,
                        color=self.constants.TEXT_COLOR
                    ),
                    padding=ft.padding.all(20),
                    margin=ft.margin.symmetric(horizontal=20, vertical=10),
                    bgcolor=self.constants.PRIMARY_COLOR,
                    border_radius=self.constants.CONTENT_BORDER_RADIUS,
                    border=ft.border.all(1, self.constants.BORDER_COLOR)
                ),
                 ft.ElevatedButton(
                            text="Exit Application",
                            bgcolor=self.constants.ERROR_COLOR,
                            color="white",
                            
                            on_click=lambda e: self.page.window.close()
                        ),
                
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
            
        )
    
    def _display_on_page(self, layout: ft.Container) -> None:
        """Display the layout on the page."""
        self.page.add(
            ft.Container(
                margin=30,
                content=layout,
                bgcolor=self.constants.PRIMARY_COLOR,
                expand=True
            )
        )
    
    def _create_text(self, text: str, size: int = 14, color: str = None) -> ft.Text:
        """Helper method to create consistent text widgets."""
        return text_widget.TextWidget.create_description_text(
            text,
            size=size,
            color=color or self.constants.TEXT_COLOR,
        )
    
