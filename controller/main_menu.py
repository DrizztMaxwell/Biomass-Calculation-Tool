# main_menu.py
import flet as ft
from views.navbar_view import get_navbar
from views.main_menu_view import get_main_menu_view
from controller import import_dataset_menu, view_species_menu, calculate_biomass_menu
from data.data_manager import DataManager

manager = DataManager()

def dataset_exists():
    return bool(manager.get_all())

def show_main_menu_page(page: ft.Page):

    # --- Container for dynamic content ---
    content_container = ft.Column(expand=True)

    # --- Dataset status text (dynamic) ---
    dataset_status_text = ft.Text(f"Dataset: {'Loaded' if dataset_exists() else 'Empty'}", size=14)

    # --- Function to update status ---
    def update_dataset_status():
        dataset_status_text.value = f"Dataset: {'Loaded' if dataset_exists() else 'Empty'}"
        page.update()

    # --- Warning dialog ---
    def warn_import_first(e=None):
        def close_dialog(e=None):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("⚠️ Action Blocked"),
            content=ft.Text("Please import dataset first!"),
            actions=[ft.TextButton("OK", on_click=close_dialog)],
            modal=True,
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # --- Navigation functions ---
    def go_home(e=None):
        if not dataset_exists():
            return warn_import_first()
        content_container.controls.clear()
        content_container.controls.append(get_main_menu_view())
        page.update()

    def go_import_dataset(e=None):
        content_container.controls.clear()
        import_dataset_menu.show_import_dataset_page(content_container, page, on_dataset_imported=update_dataset_status)
        page.update()

    def go_view_species(e=None):
        if not dataset_exists():
            return warn_import_first()
        content_container.controls.clear()
        view_species_menu.show_view_species_page(content_container, page)
        page.update()

    def go_calculate_biomass(e=None):
        if not dataset_exists():
            return warn_import_first()
        content_container.controls.clear()
        calculate_biomass_menu.show_calculate_biomass_page(content_container, page)
        page.update()

    # --- Navbar ---
    navbar = get_navbar(
        on_home_click=go_home,
        on_import_dataset_click=go_import_dataset,
        on_view_species_click=go_view_species,
        on_calculate_biomass_click=go_calculate_biomass,
        dataset_status_text=dataset_status_text  # <- pass the Text widget
    )

    # --- Page layout ---
    page.controls.clear()
    page.add(
        ft.Row(
            controls=[
                ft.Container(
                    content=navbar,
                    width=200,
                    expand=False,
                    padding=ft.padding.all(10),
                ),
                content_container,
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )

    # Load home content by default only if dataset exists
    if dataset_exists():
        go_home()
    else:
        go_import_dataset()
