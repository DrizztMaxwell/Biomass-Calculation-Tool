import flet as ft

class SettingsConstants:
    """Constants for Settings view styling and content."""
    
    # Layout constants
    CONTENT_PADDING = 40
    CONTAINER_MARGIN = 20
    CARD_BORDER_RADIUS = 12
    
    # Spacing constants
    HEADER_BOTTOM_MARGIN = 30
    DIVIDER_HEIGHT = 30
    ICON_CONTAINER_WIDTH = 12
    CONTENT_SPACING = 12
    EXTRA_SPACING = 16
    CARD_SPACING = 0
    BOTTOM_SPACING = 20
    
    # Shadow constants
    SHADOW_COLOR = ft.Colors.with_opacity(0.08, ft.Colors.BLACK)
    SHADOW_OFFSET = ft.Offset(0, 2)
    SHADOW_SPREAD_RADIUS = 0
    SHADOW_BLUR_RADIUS = 10
    
    # Color constants
    GREY_300 = ft.Colors.GREY_300
    GREY_700 = ft.Colors.GREY_700
    BLUE_700 = ft.Colors.BLUE_700
    PRIMARY = ft.Colors.PRIMARY
    TERTIARY = ft.Colors.TERTIARY
    SECONDARY = ft.Colors.SECONDARY
    SECONDARY_CONTAINER = ft.Colors.SECONDARY_CONTAINER
    ON_PRIMARY_CONTAINER = ft.Colors.ON_PRIMARY_CONTAINER
    
    # Icon constants
    SETTINGS_ICON = ft.Icons.SETTINGS_OUTLINED
    DARK_MODE_ICON = ft.Icons.DARK_MODE_OUTLINED
    PALETTE_ICON = ft.Icons.PALETTE_OUTLINED
    
    # Icon sizes
    SETTINGS_ICON_SIZE = None  # Default size from Title_With_Icon
    DARK_MODE_ICON_SIZE = 20
    PALETTE_ICON_SIZE = 28
    
    # Text constants
    TITLE = "Settings"
    DESCRIPTION = "Customize your experience and application preferences"
    APPEARANCE_TITLE = "Appearance"
    APPEARANCE_SUBTITLE = "Change the look and feel of the app"
    THEME_SWITCH_LABEL = "Dark Theme"
    
    # Text styling
    TITLE_FONT_SIZE = None  # Default from Title_With_Icon
    DESCRIPTION_FONT_SIZE = None  # Default from DescriptionText
    APPEARANCE_TITLE_SIZE = 18
    APPEARANCE_SUBTITLE_SIZE = 13
    
    # Font weights
    APPEARANCE_TITLE_WEIGHT = ft.FontWeight.W_600
    
    # Padding constants
    HEADER_PADDING = ft.padding.all(16)
    CONTENT_PADDING_OBJ = ft.padding.all(20)
    
    # Border constants
    BORDER_THICKNESS = 1
    BORDER_COLOR = ft.Colors.GREY_300
    DIVIDER_THICKNESS = 1
    
    # Scroll behavior
    SCROLL_MODE = ft.ScrollMode.ADAPTIVE