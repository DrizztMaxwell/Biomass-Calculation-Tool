# eula_menu_view.py
import flet as ft
import widgets.text_widget as text_widget
import widgets.container_widget as container_widget
import widgets.button_widget as button_widget

def get_eula_view(on_agree, on_disagree):
    """
    Returns a Column layout showing a placeholder EULA/disclaimer
    and two buttons: Agree or Disagree.
    """
    # Placeholder disclaimer text
    disclaimer = text_widget.TextWidget.create_description_text(
        "DISCLAIMER: This is placeholder EULA text. Please read carefully before proceeding."
    )

    # Buttons
    agree_btn = button_widget.ButtonWidget.create_button(
        "Agree", on_click=on_agree
    )
    disagree_btn = button_widget.ButtonWidget.create_button(
        "Disagree", on_click=on_disagree
    )

    # Button row
    btn_row = ft.Row(
        controls=[agree_btn, disagree_btn],
        spacing=20
    )

    # Full layout
    layout = container_widget.ContainerWidget.create_column(
        widgets=[disclaimer, btn_row],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    return layout

def get_exit_view():
    """
    Returns a Column layout shown when the user disagrees with the EULA.
    Displays an exit message instructing them to close the application manually.
    """
    # Exit message text
    exit_message = text_widget.TextWidget.create_description_text(
        "You must agree to the EULA to continue.\n"
        "Please close the application manually.",
    )

    # Full layout (centered vertically)
    layout = container_widget.ContainerWidget.create_column(
        widgets=[exit_message],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    return layout


