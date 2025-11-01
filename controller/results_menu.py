# results_menu.py
import flet as ft
from views.results_menu_view import get_results_view
from data.output_generator import generate_csv_output

def show_results_page(container: ft.Column, page: ft.Page, results):
    print("✅ results_menu.show_results_page() called")
    print(f"📊 Received {len(results)} result entries")

    # Handlers
    def on_generate_plot_click(e):
        print("📈 Generate Plot clicked")
        # TODO: Implement plotting logic    

    def on_generate_outputfile_click(e):
        print("📦 Generate Output File clicked")
        generate_csv_output(page)  # or page if your Save As needs a page

    # Create the layout with handlers
    layout = get_results_view(results, on_generate_plot_click, on_generate_outputfile_click)

    # Replace container controls instead of page.add()
    container.controls.clear()
    container.controls.append(layout)
    container.update()  # Update the UI
    print("✅ Results page displayed successfully")
