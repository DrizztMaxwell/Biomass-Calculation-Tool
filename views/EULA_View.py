import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget

class EULA_View:
     # Define the custom color and constants for clarity
   
    """
    A class to display the EULA/disclaimer page with Agree/Disagree options.
    """
    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.controller = controller

    def get_eula_view(self):
        """
        Returns a Column layout showing the EULA/disclaimer
        and two buttons: Agree or Disagree.
        Buttons are styled for a modern, beautiful look.
        """
        # Header with icon
        header = ft.Container(
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=ft.Icons.SECURITY,
                        size=32,
                        color=ft.Colors.GREEN_700
                    ),
                    ft.Column(
                        controls=[
                            text_widget.TextWidget.create_description_text(
                                "End User License Agreement",
                                size=24,
                                color=ft.Colors.GREEN_700,
                                font_family="Arial"
                            ),
                            text_widget.TextWidget.create_description_text(
                                "Please read the following terms carefully",
                                size=14,
                                color=ft.Colors.PRIMARY,
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
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    name=icon_name,
                                    size=20,
                                    color=ft.Colors.GREEN_700
                                ),
                                text_widget.TextWidget.create_description_text(
                                    heading_text,
                                    size=16,
                                    color=ft.Colors.GREEN_700,
                                    font_family="Arial"
                                )
                            ],
                            spacing=10
                        ),
                        ft.Container(
                            content=text_widget.TextWidget.create_description_text(
                                content_text,
                                size=14,
                                color=ft.Colors.PRIMARY
                            ),
                            margin=ft.margin.only(left=30, top=10, bottom=10),
                            padding=ft.padding.all(15),
                            bgcolor=ft.Colors.SECONDARY_CONTAINER,
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
        
        disclaimer_section = create_section(
            "Important Disclaimers",
            """
    This tool is made available by MNR as a public service on an "as is, with all defects" and "as available" basis, without any warranties, representations or conditions of any kind, express or implied, arising by law or otherwise, including, without limitation, that the user's use of this tool will be uninterrupted, that the operation of this tool will be error free, or that this tool will be meet the user's requirements.\n\n MNR specifically disclaims any implied warranties or conditions of merchantable quality, fitness for a particular purpose, non-infringement of third-party rights, or those arising by law or by usage of trade or course of dealing.\n\n Use of this tool is at the user's sole risk and the entire risk as to the results from, and performance of, this tool is assumed by the user.\n\n Under no circumstances will His Majesty the King in Right of Ontario or the members of the Executive Council and their employees, agents and independent contractors have any responsibility or liability for any loss, damage or injury whatsoever, regardless of cause, arising from access to, use of, inability to use, failure of, any errors or omissions in, or reliance on this tool (including, without limitation, direct, indirect, special, incidental, consequential, punitive, exemplary or other damages, and including, without limitation, any loss of profit, costs, expenses, harm to business or reputation, business interruption, loss of information or programs or data, loss of savings, loss of revenue, loss of goodwill, loss of tangible or intangible property, legal fees or legal costs, wasted management or office time or damages of any kind whatsoever), whether based in contract, tort, negligence or on any other legal basis, arising out of or in connection with the use of this tool, even if the Government of Ontario has been specifically advised of the possibility of such loss, damage or injury or if such loss, damage or injury was foreseeable.
    """,
            ft.Icons.WARNING_AMBER
        )

        acceptance_section = create_section(
            "Acceptance of Terms",
            "By clicking 'Agree', you acknowledge that you have read, understood, and agree to be bound by all terms and conditions outlined in this agreement.",
            ft.Icons.CHECK_CIRCLE_OUTLINE
        )
        
        # --- ENHANCED BUTTONS FOR BETTER LOOK ---
        # Assuming create_button is flexible, we pass styling arguments for a FilledButton look
        agree_btn = button_widget.ButtonWidget.create_button(
            label="Agree", 
            on_click=self.controller.on_agree,
            # Modern filled/elevated style
        )
        
        disagree_btn = button_widget.ButtonWidget.create_button(
            label="Disagree", 
            on_click=self.controller.on_disagree,
            color=ft.Colors.RED_400,
            # Modern outlined style for contrast
        )

        btn_row = ft.Row(
            controls=[disagree_btn, agree_btn],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Scrollable content area
        scrollable_content = ft.Container(
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
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
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
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

        # CHANGED: Removed gradient, set to white background
        self.page.add(ft.Container(
            margin=30,
            content=layout,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,  # Changed from gradient to solid white
            expand=True
        ))

    def get_exit_view(self):
        """
        Returns a Column layout shown when the user disagrees with the EULA.
        Displays an exit message instructing them to close the application manually.
        """
        exit_content = ft.Container(
            padding=ft.padding.all(30),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
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
                            color=ft.Colors.PRIMARY
                        ),
                        padding=ft.padding.all(20),
                        margin=ft.margin.symmetric(vertical=10),
                        bgcolor=ft.Colors.SECONDARY_CONTAINER,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.GREY_300)
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
                
            ),
            # padding=ft.padding.all(40)
            height=400,
        )

        layout = container_widget.ContainerWidget.create_column(
            widgets=[exit_content],
            
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )

        # CHANGED: Card with shadow, no gradient, centered both horizontally and vertically
        return self.page.add(
            ft.Container(
                content=ft.Container(
                    content=layout,
                  
                    border_radius=12,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.Colors.BLACK38,
                        offset=ft.Offset(0, 4)
                    ),
             
                expand=True,
                height=400
          
                    # margin=ft.margin.all(20)
                ),
             
                # bgcolor=ft.Colors.SECONDARY,  # Solid white background
                expand=True,  # This allows the container to take full available space
                alignment=ft.alignment.center  # Centers the card both horizontally and vertically
            )
        )