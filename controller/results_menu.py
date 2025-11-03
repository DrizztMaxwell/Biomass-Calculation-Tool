import flet as ft
from views.results_menu_view import get_results_view
from data.output_generator import generate_csv_output

def show_results_page(container: ft.Column, page: ft.Page, results, selected_components):
    print("✅ results_menu.show_results_page() called")
    print(f"📊 Received {len(results)} result entries")

    # Handlers
    def on_generate_plot_click(e):
        print("📈 Generate Plot clicked")
        # TODO: Implement plotting logic    

    def on_generate_outputfile_click(e):
        print("📦 Generate Output File clicked")
        generate_csv_output(page)

    # --- Determine visible columns based on selected components ---
    all_headers = [
        "SpecCode", "SpecCommon", "DBH",
        "bio_wood", "bio_bark", "bio_foliage", "bio_branches"
    ]

    # Always show these core fields
    visible_headers = ["SpecCode", "SpecCommon", "DBH"]

    # Add biomass columns only if selected
    if selected_components.get("wood"): 
        visible_headers.append("bio_wood")
    if selected_components.get("bark"): 
        visible_headers.append("bio_bark")
    if selected_components.get("foliage"): 
        visible_headers.append("bio_foliage")
    if selected_components.get("branches"): 
        visible_headers.append("bio_branches")

    print(f"🧩 Visible columns: {visible_headers}")

    # Create the layout with filtered headers
    layout = get_results_view(
        data=results,
        headers=visible_headers,
        on_generate_plot_click=on_generate_plot_click,
        on_generate_outputfile_click=on_generate_outputfile_click
    )

    # Replace container controls instead of page.add()
    container.controls.clear()
    container.controls.append(layout)
    container.update()
    print("✅ Results page displayed successfully with component filters")
