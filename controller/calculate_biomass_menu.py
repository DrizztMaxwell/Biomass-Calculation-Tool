#calculate_biomass_Menu
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

        # Gather user-selected components
        selected_components = {
            "wood": wood_checkbox.value,
            "bark": bark_checkbox.value,
            "foliage": foliage_checkbox.value,
            "branches": branches_checkbox.value,
        }

        if not any(selected_components.values()):
            ft.alert("Please select at least one biomass component to calculate.")
            return

        use_height_eq = equation_radio.value == "dbh_height"
        data = manager.get_all()
        results = []

        for i, entry in enumerate(data):
            updated_values = {}
            dbh = entry.get("DBH", 0)      # do NOT wrap in float()
            httot = entry.get("HtTot", 1)  # do NOT wrap in float()

            # --- Wood ---
            if selected_components["wood"]:
                if use_height_eq:
                    val1 = entry.get("bhwood1", 1)
                    val2 = entry.get("bhwood2", 1)
                    val3 = entry.get("bhwood3", 1)
                    updated_values["bio_wood"] = calculate_wood_height(val1, dbh, val2, httot, val3)
                else:
                    val1 = entry.get("bwood1", 1)
                    val2 = entry.get("bwood2", 1)
                    updated_values["bio_wood"] = calculate_wood(val1, dbh, val2)

            # --- Bark ---
            if selected_components["bark"]:
                if use_height_eq:
                    val1 = entry.get("bhbark1", 1)
                    val2 = entry.get("bhbark2", 1)
                    val3 = entry.get("bhbark3", 1)
                    updated_values["bio_bark"] = calculate_bark_height(val1, dbh, val2, httot, val3)
                else:
                    val1 = entry.get("bbark1", 1)
                    val2 = entry.get("bbark2", 1)
                    updated_values["bio_bark"] = calculate_bark(val1, dbh, val2)

            # --- Foliage ---
            if selected_components["foliage"]:
                if use_height_eq:
                    val1 = entry.get("bhfoliage1", 1)
                    val2 = entry.get("bhfoliage2", 1)
                    val3 = entry.get("bhfoliage3", 1)
                    updated_values["bio_foliage"] = calculate_foliage_height(val1, dbh, val2, httot, val3)
                else:
                    val1 = entry.get("bfoliage1", 1)
                    val2 = entry.get("bfoliage2", 1)
                    updated_values["bio_foliage"] = calculate_foliage(val1, dbh, val2)

            # --- Branches ---
            if selected_components["branches"]:
                if use_height_eq:
                    val1 = entry.get("bhbranches1", 1)
                    val2 = entry.get("bhbranches2", 1)
                    val3 = entry.get("bhbranches3", 1)
                    updated_values["bio_branches"] = calculate_branches_height(val1, dbh, val2, httot, val3)
                else:
                    val1 = entry.get("bbranches1", 1)
                    val2 = entry.get("bbranches2", 1)
                    updated_values["bio_branches"] = calculate_branches(val1, dbh, val2)

            # Merge results
            merged_entry = {**entry, **updated_values}
            results.append(merged_entry)

        # Save results
        for i, updated_entry in enumerate(results):
            manager.update_entry(i, updated_entry, save=False)
        manager.save()

        print(f"✅ Generated {len(results)} result entries")
        results_menu.show_results_page(container, page, results, selected_components)

    # --- Get UI layout and controls from view ---
    layout, equation_radio, wood_checkbox, bark_checkbox, foliage_checkbox, branches_checkbox = \
        get_calculate_biomass_menu_view(on_run_click=on_run_click)

    # --- Display the layout ---
    container.controls.clear()
    container.controls.append(layout)
    page.update()
    print("📋 Biomass calculation menu loaded with component selection.")
