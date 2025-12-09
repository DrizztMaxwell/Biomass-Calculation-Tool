import flet as ft
def Equation_Type_Card(main_text_column, desc_widget, radio_value):
        """
        Replicates Equation_Type_Component functionality.
        The radio button is now on the left.
        main_text_column is a ft.Column containing the title and the formula.
        """
        return ft.Container(
            padding=15,
            margin=ft.margin.only(bottom=10),
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
            bgcolor=ft.Colors.WHITE,
            content=ft.Row([
                ft.Radio(value=radio_value,  active_color="#047648", ), # Radio on the left
                ft.Column([
                    main_text_column, # Stacked Title and Formula
                    desc_widget
                ], alignment=ft.MainAxisAlignment.START, spacing=5, expand=True),
            ], alignment=ft.MainAxisAlignment.START)
        )
