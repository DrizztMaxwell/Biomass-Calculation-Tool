import flet as ft
from widgets.LogFileTxt import logger
from widgets.DescriptionText import DescriptionText
from widgets.Title_With_Icon import Title_With_Icon
from controller.Settings_Controller import Settings_Controller
from constants.Settings_Constants import SettingsConstants


class SettingsView:
    """View for application settings and preferences."""
    
    def __init__(self, page: ft.Page, controller: Settings_Controller):
        self.page = page
        self.controller = controller
        self.cnst = SettingsConstants()

    def _build_header(self) -> ft.Container:
        """Build the header section with title and description."""
        return ft.Container(
            content=ft.Column([
                Title_With_Icon(self.cnst.TITLE, self.cnst.SETTINGS_ICON),
                DescriptionText(self.cnst.DESCRIPTION),
                ft.Divider(color=self.cnst.GREY_300, height=self.cnst.DIVIDER_HEIGHT),
            ]),
            margin=ft.margin.only(bottom=self.cnst.HEADER_BOTTOM_MARGIN)
        )

    def _build_theme_switch_row(self) -> ft.Row:
        """Build the theme toggle switch row."""
        return ft.Row(
            [
                ft.Icon(
                    self.cnst.DARK_MODE_ICON,
                    size=self.cnst.DARK_MODE_ICON_SIZE,
                    color=self.cnst.GREY_700,
                ),
                ft.Container(width=self.cnst.ICON_CONTAINER_WIDTH),
                ft.Switch(
                    label=self.cnst.THEME_SWITCH_LABEL,
                    label_style=ft.TextStyle(color=self.cnst.PRIMARY),
                    value=self.page.theme_mode == ft.ThemeMode.DARK,
                    on_change=self.controller.toggle_theme,
                    active_color=self.cnst.TERTIARY,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

    def _build_appearance_card(self) -> ft.Container:
        """Build the appearance settings card."""
        return ft.Container(
            content=ft.Column([
                self._build_appearance_header(),
                ft.Divider(
                    height=1, 
                    thickness=self.cnst.DIVIDER_THICKNESS, 
                    color=self.cnst.BORDER_COLOR
                ),
                self._build_appearance_content(),
            ], spacing=self.cnst.CARD_SPACING),
            border_radius=self.cnst.CARD_BORDER_RADIUS,
            border=ft.border.all(self.cnst.BORDER_THICKNESS, self.cnst.BORDER_COLOR),
            bgcolor=self.cnst.SECONDARY_CONTAINER,
            shadow=self._build_card_shadow(),
        )

    def _build_appearance_header(self) -> ft.ListTile:
        """Build the appearance card header."""
        return ft.ListTile(
            leading=ft.Icon(
                self.cnst.PALETTE_ICON,
                color=self.cnst.BLUE_700,
                size=self.cnst.PALETTE_ICON_SIZE
            ),
            title=ft.Text(
                self.cnst.APPEARANCE_TITLE,
                color=self.cnst.ON_PRIMARY_CONTAINER,
                size=self.cnst.APPEARANCE_TITLE_SIZE,
                weight=self.cnst.APPEARANCE_TITLE_WEIGHT,
            ),
            subtitle=ft.Text(
                self.cnst.APPEARANCE_SUBTITLE,
                color=self.cnst.ON_PRIMARY_CONTAINER,
                size=self.cnst.APPEARANCE_SUBTITLE_SIZE,
            ),
            content_padding=self.cnst.HEADER_PADDING,
        )

    def _build_appearance_content(self) -> ft.Container:
        """Build the appearance card content section."""
        return ft.Container(
            content=ft.Column([
                self._build_theme_switch_row(),
                ft.Container(height=self.cnst.EXTRA_SPACING),
            ], spacing=self.cnst.CONTENT_SPACING),
            padding=self.cnst.CONTENT_PADDING_OBJ,
        )

    def _build_card_shadow(self) -> ft.BoxShadow:
        """Create consistent card shadow."""
        return ft.BoxShadow(
            spread_radius=self.cnst.SHADOW_SPREAD_RADIUS,
            blur_radius=self.cnst.SHADOW_BLUR_RADIUS,
            color=self.cnst.SHADOW_COLOR,
            offset=self.cnst.SHADOW_OFFSET,
        )

    def _build_main_content(self) -> ft.Container:
        """Build the main content area."""
        return ft.Container(
            bgcolor=self.cnst.SECONDARY,
            content=ft.Column([
                self._build_header(),
                self._build_appearance_card(),
                ft.Container(height=self.cnst.BOTTOM_SPACING),
            ], spacing=self.cnst.CARD_SPACING),
            padding=ft.padding.all(self.cnst.CONTENT_PADDING),
            expand=True,
        )

    def build(self) -> ft.Container:
        """Build the complete settings view."""
        main_content = self._build_main_content()
        
        return ft.Container(
            bgcolor=self.cnst.SECONDARY_CONTAINER,
            margin=ft.margin.all(self.cnst.CONTAINER_MARGIN),
            content=ft.Column(
                [main_content],
                scroll=self.cnst.SCROLL_MODE,
                expand=True
            ),
            expand=True,
        )