# eula_menu_view.py
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget

def get_eula_view(on_agree, on_disagree):
    """
    Returns a Column layout showing the EULA/disclaimer
    and two buttons: Agree or Disagree.
    """
    # Bold headings
    terms_heading = text_widget.TextWidget.create_description_text(
        "Terms of Use:", size=18, color="black", font_family="Arial"
    )
    terms_heading.weight = ft.FontWeight.BOLD

    acceptance_heading = text_widget.TextWidget.create_description_text(
        "Acceptance", size=18, color="black", font_family="Arial"
    )
    acceptance_heading.weight = ft.FontWeight.BOLD

    disclaimers_heading = text_widget.TextWidget.create_description_text(
        "Disclaimers", size=18, color="black", font_family="Arial"
    )
    disclaimers_heading.weight = ft.FontWeight.BOLD

    # Disclaimer paragraphs
    paragraph1 = text_widget.TextWidget.create_description_text(
        "This tool was created by the Science and Research Branch of the Ontario Ministry of Natural Resources (MNR). "
        "Use of this tool is governed by the terms and conditions set out below and implies acceptance of these terms.\n"
    )

    paragraph2 = text_widget.TextWidget.create_description_text(
        "This tool is made available by MNR as a public service on an “as is, with all defects” and “as available” basis, "
        "without any warranties, representations or conditions of any kind, express or implied, arising by law or otherwise, "
        "including, without limitation, that the user’s use of this tool will be uninterrupted, that the operation of this tool "
        "will be error free, or that this tool will meet the user’s requirements.\n\n"
        "MNR specifically disclaims any implied warranties or conditions of merchantable quality, fitness for a particular purpose, "
        "non-infringement of third-party rights, or those arising by law or by usage of trade or course of dealing.\n\n"
        "Use of this tool is at the user's sole risk and the entire risk as to the results from, and performance of, this tool is assumed by the user.\n\n"
        "Under no circumstances will His Majesty the King in Right of Ontario or the members of the Executive Council and their "
        "employees, agents and independent contractors have any responsibility or liability for any loss, damage or injury whatsoever, "
        "regardless of cause, arising from access to, use of, inability to use, failure of, any errors or omissions in, or reliance on this tool "
        "(including, without limitation, direct, indirect, special, incidental, consequential, punitive, exemplary or other damages, and including, "
        "without limitation, any loss of profit, costs, expenses, harm to business or reputation, business interruption, loss of information or programs "
        "or data, loss of savings, loss of revenue, loss of goodwill, loss of tangible or intangible property, legal fees or legal costs, wasted management "
        "or office time or damages of any kind whatsoever), whether based in contract, tort, negligence or on any other legal basis, arising out of or "
        "in connection with the use of this tool, even if the Government of Ontario has been specifically advised of the possibility of such loss, "
        "damage or injury or if such loss, damage or injury was foreseeable."
    )

    # Buttons
    agree_btn = button_widget.ButtonWidget.create_button(
        "Agree", on_click=on_agree
    )
    disagree_btn = button_widget.ButtonWidget.create_button(
        "Disagree", on_click=on_disagree
    )
    btn_row = ft.Row(controls=[agree_btn, disagree_btn], spacing=20)

    # Full layout
    layout = container_widget.ContainerWidget.create_column(
        widgets=[
            terms_heading,
            acceptance_heading,
            paragraph1,
            disclaimers_heading,
            paragraph2,
            btn_row
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )

    return layout

def get_exit_view():
    """
    Returns a Column layout shown when the user disagrees with the EULA.
    Displays an exit message instructing them to close the application manually.
    """
    exit_message = text_widget.TextWidget.create_description_text(
        "You must agree to the EULA to continue.\nPlease close the application manually."
    )

    layout = container_widget.ContainerWidget.create_column(
        widgets=[exit_message],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    return layout
