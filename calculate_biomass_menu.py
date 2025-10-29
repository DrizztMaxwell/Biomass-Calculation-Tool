import flet as ft
from data_manager import DataManager
from calculate_biomass_helper import calculate_wood, calculate_bark, calculate_foilage, calculate_branches
from calculate_biomass_menu_view import get_calculate_biomass_menu_view
import results_menu  # Keep this import!

# Map checkbox keys to calculation functions and output fields
CALCULATION_MAP = {
    "wood":    ("bio_wood", calculate_wood, "wood1", "wood2"),
    "bark":    ("bio_bark", calculate_bark, "bark1", "bark2"),
    "foilage": ("bio_foilage", calculate_foilage, "foilage1", "foilage2"),
    "branches":("bio_branches", calculate_branches, "branches1", "branches2")
}

def show_calculate_biomass_page(page: ft.Page, main_menu_callback):
    manager = DataManager()

    def on_run_click(e):
        data = manager.get_all()
        if not checkboxes:
            return

        results = []

        for i, entry in enumerate(data):
            updated_values = {}
            dbh = float(entry.get("DBH", 0))

            # Loop dynamically over all checkboxes
            for key, (output_field, func, input1_field, input2_field) in CALCULATION_MAP.items():
                if checkboxes[key].value:
                    val1 = float(entry.get(input1_field, 1))
                    val2 = float(entry.get(input2_field, 1))
                    updated_values[output_field] = func(val1, dbh, val2)

            # Merge new results but don’t write yet
            merged_entry = {**entry, **updated_values}
            results.append(merged_entry)

        # ✅ Only write once, after loop is done
        for i, updated_entry in enumerate(results):
            manager.update_entry(i, updated_entry, save=False)

        # ✅ Now save everything once safely
        manager.save()

        print(f"✅ Generated {len(results)} result entries")

        # Pass results directly to results page
        results_menu.show_results_page(page, results, main_menu_callback)

    def on_back_click(e):
        page.clean()
        main_menu_callback(page)

    layout, checkboxes = get_calculate_biomass_menu_view(
        on_run_click=on_run_click,
        on_back_click=on_back_click
    )

    print("📋 Biomass calculation menu loaded.")
    page.clean()
    page.add(layout)
    page.update()
