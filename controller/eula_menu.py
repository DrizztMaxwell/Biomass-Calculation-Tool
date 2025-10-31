import flet as ft
from views.eula_menu_view import get_eula_view, get_exit_view
from controller.main_menu import show_main_menu_page

def show_eula_page(page: ft.Page, show_main_menu_page):
    """
    Display the EULA/disclaimer page with Agree/Disagree options.
    """

    def on_agree(e):
        page.clean()
        show_main_menu_page(page)

    def on_disagree(e):
        page.clean()
        page.add(get_exit_view())
        page.update()
        print("❌ User disagreed with EULA. Showing exit screen instead of closing.")

    layout = get_eula_view(on_agree, on_disagree)

    page.clean()
    page.add(layout)
    page.update()
    print("📜 EULA page displayed")
