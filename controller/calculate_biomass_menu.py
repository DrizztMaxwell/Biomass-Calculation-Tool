# controller/calculate_biomass_menu.py
import flet as ft
from data.data_manager import DataManager
from data.calculate_biomass_helper import (
    calculate_wood,
    calculate_bark,
    calculate_foliage,
    calculate_branches,
    calculate_wood_height,
    calculate_bark_height,
    calculate_foliage_height,
    calculate_branches_height
)
from views.calculate_biomass_menu_view import get_calculate_biomass_menu_view
from controller import results_menu  # Keep this import!


def show_calculate_biomass_page(container: ft.Column, page: ft.Page):
    manager = DataManager()

    def on_run_click(e):
        if not equation_radio.value:
            ft.alert("Please select an equation type before running calculations.")
            return

        use_height_eq = equation_radio.value == "dbh_height"
        data = manager.get_all()
        results = []

        for i, entry in enumerate(data):
            updated_values = {}
            dbh = float(entry.get("DBH", 0))
            httot = float(entry.get("HtTot", 1))  # Only used for height-based equations

            # --- Wood ---
            if use_height_eq:
                val1 = float(entry.get("bhwood1", 1))
                val2 = float(entry.get("bhwood2", 1))
                val3 = float(entry.get("bhwood3", 1))
                updated_values["bio_wood"] = calculate_wood_height(val1, dbh, val2, httot, val3)
            else:
                val1 = float(entry.get("bwood1", 1))
                val2 = float(entry.get("bwood2", 1))
                updated_values["bio_wood"] = calculate_wood(val1, dbh, val2)

            # --- Bark ---
            if use_height_eq:
                val1 = float(entry.get("bhbark1", 1))
                val2 = float(entry.get("bhbark2", 1))
                val3 = float(entry.get("bhbark3", 1))
                updated_values["bio_bark"] = calculate_bark_height(val1, dbh, val2, httot, val3)
            else:
                val1 = float(entry.get("bbark1", 1))
                val2 = float(entry.get("bbark2", 1))
                updated_values["bio_bark"] = calculate_bark(val1, dbh, val2)

            # --- Foliage ---
            if use_height_eq:
                val1 = float(entry.get("bhfoliage1", 1))
                val2 = float(entry.get("bhfoliage2", 1))
                val3 = float(entry.get("bhfoliage3", 1))
                updated_values["bio_foliage"] = calculate_foliage_height(val1, dbh, val2, httot, val3)
            else:
                val1 = float(entry.get("bfoliage1", 1))
                val2 = float(entry.get("bfoliage2", 1))
                updated_values["bio_foliage"] = calculate_foliage(val1, dbh, val2)

            # --- Branches ---
            if use_height_eq:
                val1 = float(entry.get("bhbranches1", 1))
                val2 = float(entry.get("bhbranches2", 1))
                val3 = float(entry.get("bhbranches3", 1))
                updated_values["bio_branches"] = calculate_branches_height(val1, dbh, val2, httot, val3)
            else:
                val1 = float(entry.get("bbranches1", 1))
                val2 = float(entry.get("bbranches2", 1))
                updated_values["bio_branches"] = calculate_branches(val1, dbh, val2)

            # Merge results
            merged_entry = {**entry, **updated_values}
            results.append(merged_entry)

        # Save results
        for i, updated_entry in enumerate(results):
            manager.update_entry(i, updated_entry, save=False)
        manager.save()

        print(f"✅ Generated {len(results)} result entries")
        results_menu.show_results_page(container, page, results)

    # Create layout and single global radio group for equation selection
    layout, equation_radio = get_calculate_biomass_menu_view(on_run_click=on_run_click)

    container.controls.clear()
    container.controls.append(layout)
    page.update()
    print("📋 Biomass calculation menu loaded.")
