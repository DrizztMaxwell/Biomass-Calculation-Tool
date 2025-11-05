import flet as ft

from controller.import_dataset_menu import show_import_dataset_page

# Standalone function to handle the button click and page updates
def handle_import_click(e, title):
    """
    Handles the click event for the Import buttons, showing a SnackBar message.
    """
    print(f"Importing {title}...")

    # import from appropriate module (placeholder)

    show_import_dataset_page()

    
    # # Access the page object via the event (e.page) to update UI elements
    # e.page.snack_bar = ft.SnackBar(
    #     content=ft.Row([
    #         ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINED, color=ft.Colors.WHITE),
    #         ft.Text(f"Initializing {title} import...", weight=ft.FontWeight.BOLD),
    #     ]),
    #     bgcolor=ft.Colors.GREEN_600,
    #     duration=2000
    # )
    # e.page.snack_bar.open = True
    # e.page.update()

def handle_begin_click(e):
    """
    Handles the Begin button click event.
    """
    e.page.snack_bar = ft.SnackBar(
        content=ft.Row([
            ft.Icon(ft.Icons.ROCKET_LAUNCH, color=ft.Colors.BLACK),
            ft.Text("Starting your data journey...", weight=ft.FontWeight.BOLD),
        ]),
        bgcolor=ft.Colors.BLUE_600,
        duration=2000
    )
    e.page.snack_bar.open = True
    e.page.update()

class ImportDataComponents:
    """
    A class containing static methods to build the Flet UI components.
    It does NOT inherit from ft.UserControl.
    """
    @staticmethod
    def import_option_card(icon_name, title, subtitle, color):
        """
        Creates a beautifully styled, stateless card for an import option.
        """
        return ft.Container(
            width=300,
            height=400,
            padding=ft.padding.all(30),
            border_radius=ft.border_radius.all(20),
            bgcolor=ft.Colors.WHITE,
            # Enhanced shadow for depth
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                offset=ft.Offset(0, 10),
            ),
            border=ft.border.all(1, ft.Colors.GREY_100),
            alignment=ft.alignment.center,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Column(
                [
                    # Large Icon Section with gradient background
                    ft.Container(
                        width=100,
                        height=100,
                        padding=ft.padding.all(20),
                        bgcolor=ft.Colors.with_opacity(0.08, color),
                        border_radius=ft.border_radius.all(20),
                        alignment=ft.alignment.center,
                        content=ft.Icon(
                            icon_name,
                            size=48,
                            color=color,
                        )
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                    # Title and Subtitle
                    ft.Column(
                        [
                            ft.Text(
                                title,
                                size=20,
                                weight=ft.FontWeight.W_800,
                                color=ft.Colors.BLACK87,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=10),
                            ft.Text(
                                subtitle,
                                size=14,
                                color=ft.Colors.BLACK54,
                                max_lines=3,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                text_align=ft.TextAlign.CENTER,
                                height=60
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                    # Action Button
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.UPLOAD_FILE, size=20),
                                ft.Text("Import", size=15, weight=ft.FontWeight.W_600),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        on_click=lambda e: handle_import_click(e, title),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=ft.padding.symmetric(horizontal=35, vertical=15),
                            bgcolor=color,
                            color=ft.Colors.WHITE,
                        ),
                        width=200,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0
            ),
        )

    @staticmethod
    def create_main_layout():
        """
        Creates and returns the main layout container control.
        """
        # Enhanced Header with better typography
        header = ft.Column(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Data Import Hub",
                            size=36,
                            weight=ft.FontWeight.W_900,
                            color=ft.Colors.BLUE_GREY_900,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=10),
                        ft.Text(
                            "Select your preferred method to import datasets into the platform",
                            size=16,
                            color=ft.Colors.BLUE_GREY_600,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ]),
                    padding=ft.padding.only(bottom=40)
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        # Row holding the two import cards
        options_row = ft.Row(
            [
                ImportDataComponents.import_option_card(
                    icon_name=ft.Icons.FOLDER_OPEN,
                    title="Local File Import",
                    subtitle="Upload CSV, TXT, or Excel files from your local storage with advanced parsing options.",
                    color=ft.Colors.BLUE_600
                ),
                ImportDataComponents.import_option_card(
                    icon_name=ft.Icons.STORAGE,
                    title="Database Connection",
                    subtitle="Connect securely to SQL databases using JDBC/ODBC drivers with real-time data streaming.",
                    color=ft.Colors.INDIGO_600
                ),
            ],
            spacing=40,
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True
        )

        # Begin Button Section
        begin_section = ft.Column(
            [
                ft.Divider(height=50, color=ft.Colors.TRANSPARENT),
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.PLAY_ARROW, size=24),
                                ft.Text("Begin Data Journey", size=18, weight=ft.FontWeight.W_700),
                            ],
                            spacing=12,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        on_click=handle_begin_click,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=15),
                            padding=ft.padding.symmetric(horizontal=50, vertical=18),
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE,
                        ),
                        width=280,
                    ),
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.Text(
                        "Ready to start analyzing your data?",
                        size=14,
                        color=ft.Colors.BLUE_GREY_500,
                        text_align=ft.TextAlign.CENTER
                    ),
                    padding=ft.padding.only(top=15)
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )

        # Main content container
        main_content = ft.Column(
            [
                header,
                options_row,
                begin_section,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )

        # Enhanced outer container with gradient background - NOW CENTERED
        main_layout = ft.Container(
            content=main_content,
            padding=ft.padding.symmetric(vertical=50, horizontal=40),
            margin=ft.margin.all(30),
            border_radius=ft.border_radius.all(30),
            bgcolor=ft.Colors.WHITE,
            width=900,
            # Enhanced shadow and border
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=40,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 20),
            ),
            border=ft.border.all(1, ft.Colors.GREY_200),
            # Center the container both horizontally and vertically
            alignment=ft.alignment.center,
        )
    
        # Wrap in a container that centers both horizontally and vertically
        centered_layout = ft.Container(
            content=main_layout,
            expand=True,  # Take up all available space
            alignment=ft.alignment.center,  # Center the content
        )
    
        return centered_layout

def main(page: ft.Page):
    """
    The main function for the Flet application.
    Sets up the page configuration and adds the controls created by the helper class.
    """
    page.title = "Data Import Platform"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.padding = 0
    
    # Create a container with gradient background
    background_container = ft.Container(
        content=ImportDataComponents.create_main_layout(),
        alignment=ft.alignment.center,
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                ft.Colors.BLUE_GREY_50,
                ft.Colors.WHITE,
                ft.Colors.BLUE_GREY_100
            ]
        )
    )

    # Add the background container to the page
    page.add(background_container)


if __name__ == "__main__":
    ft.app(target=main)