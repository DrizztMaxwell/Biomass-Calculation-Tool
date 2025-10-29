# results_menu.py
import flet as ft
from results_menu_view import get_results_view
from output_generator import generate_csv_output

def show_results_page(page: ft.Page, results, main_menu_callback):
    print("✅ results_menu.show_results_page() called")
    print(f"📊 Received {len(results)} result entries")

    # Handlers
    def on_back_click(e):
        page.clean()
        main_menu_callback(page)

    def on_generate_plot_click(e):
        print("📈 Generate Plot clicked")
        # TODO: Implement plotting logic    
    
    def on_generate_outputfile_click(e):
        print("📦 Generate Output File clicked")
        generate_csv_output()

    # Create the layout with handlers
    layout = get_results_view(results, on_back_click, on_generate_plot_click, on_generate_outputfile_click)

    page.clean()
    page.add(layout)
    page.update()

    print("✅ Results page displayed successfully")

