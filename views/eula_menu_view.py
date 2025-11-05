# eula_menu_view.py
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget

# Define the custom color and constants for clarity
CUSTOM_GREEN = "#077213"
# Use ft.Colors.BLACK for consistency
CUSTOM_BLACK = ft.Colors.BLACK

def get_eula_view(on_agree, on_disagree):
    """
    Returns a Column layout showing the EULA/disclaimer
    and two buttons: Agree or Disagree.
    Buttons are styled for a modern, beautiful look.
    """
    # Header with icon
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    name=ft.Icons.SECURITY,
                    size=32,
                    color=CUSTOM_GREEN
                ),
                ft.Column(
                    controls=[
                        text_widget.TextWidget.create_description_text(
                            "End User License Agreement",
                            size=24,
                            color=CUSTOM_GREEN,
                            font_family="Arial"
                        ),
                        text_widget.TextWidget.create_description_text(
                            "Please read the following terms carefully",
                            size=14,
                            color=ft.Colors.BLUE_700,
                            font_family="Arial"
                        )
                    ],
                    spacing=2
                )
            ],
            spacing=15
        ),
        padding=ft.padding.only(bottom=20)
    )

    # Section containers (no significant change needed here)
    def create_section(heading_text, content_text, icon_name):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name=icon_name,
                                size=20,
                                color=CUSTOM_GREEN
                            ),
                            text_widget.TextWidget.create_description_text(
                                heading_text,
                                size=16,
                                color=CUSTOM_GREEN,
                                font_family="Arial"
                            )
                        ],
                        spacing=10
                    ),
                    ft.Container(
                        content=text_widget.TextWidget.create_description_text(
                            content_text,
                            size=14,
                            color=ft.Colors.GREY_800
                        ),
                        margin=ft.margin.only(left=30, top=10, bottom=10),
                        padding=ft.padding.all(15),
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.GREY_300)
                    )
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            padding=ft.padding.symmetric(vertical=10)
        )

    # Content sections (unchanged)
    terms_section = create_section(
        "Terms of Use",
        "This tool was created by the Science and Research Branch of the Ontario Ministry of Natural Resources (MNR). "
        "Use of this tool is governed by the terms and conditions set out below and implies acceptance of these terms.",
        ft.Icons.DESCRIPTION
    )
    acceptance_section = create_section(
        "Acceptance of Terms",
        "By clicking 'Agree', you acknowledge that you have read, understood, and agree to be bound by all terms and conditions outlined in this agreement.",
        ft.Icons.CHECK_CIRCLE_OUTLINE
    )
    disclaimer_section = create_section(
        "Important Disclaimers",
        "This tool is made available by MNR as a public service on an \"as is, with all defects\" and \"as available\" basis, "
        "without any warranties, representations or conditions of any kind, express or implied, arising by law or otherwise.\n\n"
        "MNR specifically disclaims any implied warranties or conditions of merchantable quality, fitness for a particular purpose, "
        "non-infringement of third-party rights, or those arising by law or by usage of trade or course of dealing.\n\n"
        "Use of this tool is at the user's sole risk and the entire risk as to the results from, and performance of, this tool is assumed by the user.\n\n"
        "Under no circumstances will His Majesty the King in Right of Ontario or the members of the Executive Council and their "
        "employees, agents and independent contractors have any responsibility or liability for any loss, damage or injury whatsoever...",
        ft.Icons.WARNING_AMBER
    )

    # --- ENHANCED BUTTONS FOR BETTER LOOK ---
    # Assuming create_button is flexible, we pass styling arguments for a FilledButton look
    agree_btn = button_widget.ButtonWidget.create_button(
        label="I Agree", 
        on_click=on_agree,

        # Modern filled/elevated style
    )
    
    disagree_btn = button_widget.ButtonWidget.create_button(
        label="I Disagree", 
        on_click=on_disagree,
        color=CUSTOM_BLACK,
        # Modern outlined style for contrast

    )

    btn_row = ft.Row(
        controls=[disagree_btn, agree_btn],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Scrollable content area
    scrollable_content = ft.Container(
        content=ft.ListView( # Changed to ListView for built-in scrolling
            controls=[
                terms_section,
                acceptance_section,
                disclaimer_section
            ],
            spacing=5,
        ),
        expand=True
    )

    # --- FIX: Main layout alignment ---
    layout = ft.Container(
        content=ft.Column(
            controls=[
                header,
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Container(
                    content=scrollable_content,
                    padding=ft.padding.symmetric(vertical=15),
                    expand=True # This container takes all remaining vertical space
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Container(
                    content=btn_row,
                    padding=ft.padding.only(top=20)
                )
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            # IMPORTANT: Set main_axis_alignment to center the column's children
            # within the whole page height when maximized (if the outer container expands).
            # This is key for the spacing fix.
            alignment=ft.MainAxisAlignment.START 
        ),
        padding=ft.padding.all(30),
        margin=ft.margin.all(20),
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        border=ft.border.all(1, ft.Colors.GREY_300),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK38,
            offset=ft.Offset(0, 4)
        ),
        expand=True # Ensures the card takes up available space
    )

    # Wrap in a gradient background container
    return ft.Container(
        content=layout,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.with_opacity(0.1, CUSTOM_GREEN), ft.Colors.GREY_100] 
        ),
        padding=ft.padding.all(10),
        expand=True
    )

def get_exit_view():
    """
    Returns a Column layout shown when the user disagrees with the EULA.
    Displays an exit message instructing them to close the application manually.
    """
    exit_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(
                    name=ft.Icons.EXIT_TO_APP,
                    size=64,
                    color=ft.Colors.RED_600
                ),
                text_widget.TextWidget.create_description_text(
                    "EULA Not Accepted",
                    size=24,
                    color=ft.Colors.RED_700,
                    font_family="Arial"
                ),
                ft.Container(
                    content=text_widget.TextWidget.create_description_text(
                        "You must agree to the EULA to use this application.\n\n"
                        "Please close the application manually.",
                        size=16,
                        color=ft.Colors.GREY_700
                    ),
                    padding=ft.padding.all(20),
                    margin=ft.margin.symmetric(vertical=10),
                    bgcolor=ft.Colors.GREY_50,
                    border_radius=8,
                    border=ft.border.all(1, ft.Colors.GREY_300)
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=ft.padding.all(40)
    )

    layout = container_widget.ContainerWidget.create_column(
        widgets=[exit_content],
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    # Add background styling
    return ft.Container(
        content=layout,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.RED_50, ft.Colors.GREY_100] 
        ),
        expand=True
    )