import flet as ft
from widgets.LogFileTxt import logger
from widgets.DescriptionText import DescriptionText
from widgets.Title_With_Icon import Title_With_Icon
from controller.Settings_Controller import Settings_Controller


class SettingsView:
    """View for application settings and preferences."""
    
    # Constants for styling
    _CONTENT_PADDING = 40
    _CONTAINER_MARGIN = 20
    _CARD_BORDER_RADIUS = 12
    _SHADOW_COLOR = ft.Colors.with_opacity(0.08, ft.Colors.BLACK)
    _SHADOW_OFFSET = ft.Offset(0, 2)
    
    def __init__(self, page: ft.Page, controller: Settings_Controller):
        self.page = page
        self.controller = controller

    def _build_header(self) -> ft.Container:
        """Build the header section with title and description."""
        return ft.Container(
            content=ft.Column([
                Title_With_Icon("Settings", ft.Icons.SETTINGS_OUTLINED),
                DescriptionText("Customize your experience and application preferences"),
                ft.Divider(color=ft.Colors.GREY_300, height=30),
            ]),
            margin=ft.margin.only(bottom=30)
        )

    def _build_theme_switch_row(self) -> ft.Row:
        """Build the theme toggle switch row."""
        return ft.Row(
            [
                ft.Icon(
                    ft.Icons.DARK_MODE_OUTLINED,
                    size=20,
                    color=ft.Colors.GREY_700,
                ),
                ft.Container(width=12),
                ft.Switch(
                    label="Dark Theme",
                    label_style=ft.TextStyle(color=ft.Colors.PRIMARY),
                    value=self.page.theme_mode == ft.ThemeMode.DARK,
                    on_change=self.controller.toggle_theme,
                    active_color=ft.Colors.TERTIARY,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

    def _build_appearance_card(self) -> ft.Container:
        """Build the appearance settings card."""
        return ft.Container(
            content=ft.Column([
                self._build_appearance_header(),
                ft.Divider(height=1, thickness=1, color=ft.Colors.GREY_300),
                self._build_appearance_content(),
            ], spacing=0),
            border_radius=self._CARD_BORDER_RADIUS,
            border=ft.border.all(1, ft.Colors.GREY_300),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            shadow=self._build_card_shadow(),
        )

    def _build_appearance_header(self) -> ft.ListTile:
        """Build the appearance card header."""
        return ft.ListTile(
            leading=ft.Icon(
                ft.Icons.PALETTE_OUTLINED,
                color=ft.Colors.BLUE_700,
                size=28
            ),
            title=ft.Text(
                "Appearance",
                color=ft.Colors.ON_PRIMARY_CONTAINER,
                size=18,
                weight=ft.FontWeight.W_600,
            ),
            subtitle=ft.Text(
                "Change the look and feel of the app",
                color=ft.Colors.ON_PRIMARY_CONTAINER,
                size=13,
            ),
            content_padding=ft.padding.all(16),
        )

    def _build_appearance_content(self) -> ft.Container:
        """Build the appearance card content section."""
        return ft.Container(
            content=ft.Column([
                self._build_theme_switch_row(),
                ft.Container(height=16),
            ], spacing=12),
            padding=ft.padding.all(20),
        )

    def _build_card_shadow(self) -> ft.BoxShadow:
        """Create consistent card shadow."""
        return ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=self._SHADOW_COLOR,
            offset=self._SHADOW_OFFSET,
        )

    def _build_main_content(self) -> ft.Container:
        """Build the main content area."""
        return ft.Container(
            bgcolor=ft.Colors.SECONDARY,
            content=ft.Column([
                self._build_header(),
                self._build_appearance_card(),
                ft.Container(height=20),
            ], spacing=0),
            padding=ft.padding.all(self._CONTENT_PADDING),
            expand=True,
        )

    def build(self) -> ft.Container:
        """Build the complete settings view."""
        main_content = self._build_main_content()
        
        return ft.Container(
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            margin=ft.margin.all(self._CONTAINER_MARGIN),
            content=ft.Column(
                [main_content],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            ),
            expand=True,
        )