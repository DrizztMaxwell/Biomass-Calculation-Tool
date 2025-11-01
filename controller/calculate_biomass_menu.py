#calculate_biomass_menu
import flet as ft
from data.data_manager import DataManager
from data.calculate_biomass_helper import calculate_wood, calculate_bark, calculate_foilage, calculate_branches
from views.calculate_biomass_menu_view import get_calculate_biomass_menu_view
from controller import results_menu  # Keep this import!

# Map checkbox keys to calculation functions and output fields
CALCULATION_MAP = {
    "wood":    ("bio_wood", calculate_wood, "bwood1", "bwood2"),
    "bark":    ("bio_bark", calculate_bark, "bbark1", "bbark2"),
    "foilage": ("bio_foilage", calculate_foilage, "bfoilage1", "bfoilage2"),
    "branches":("bio_branches", calculate_branches, "bbranches1", "bbranches2")
}

def show_calculate_biomass_page(container: ft.Column, page: ft.Page):
    manager = DataManager()

    def on_run_click(e):
        data = manager.get_all()
        if not checkboxes:
            return

        results = []

        for i, entry in enumerate(data):
            updated_values = {}
            dbh = float(entry.get("DBH", 0))

            for key, (output_field, func, input1_field, input2_field) in CALCULATION_MAP.items():
                if checkboxes[key].value:
                    val1 = float(entry.get(input1_field, 1))
                    val2 = float(entry.get(input2_field, 1))
                    updated_values[output_field] = func(val1, dbh, val2)

            merged_entry = {**entry, **updated_values}
            results.append(merged_entry)

        for i, updated_entry in enumerate(results):
            manager.update_entry(i, updated_entry, save=False)
        manager.save()

        print(f"✅ Generated {len(results)} result entries")
        results_menu.show_results_page(container, page, results)  # Pass container instead of page

    layout, checkboxes = get_calculate_biomass_menu_view(
        on_run_click=on_run_click,
    )

    container.controls.clear()
    container.controls.append(layout)
    page.update()
    print("📋 Biomass calculation menu loaded.")
