import flet as ft
from widgets.text_widget import TextWidget

class ContainerWidget:
    """Reusable container/card components"""

    @staticmethod
    def create_equation_card(title, formula, description, radio_value):
        """
        Creates a card with a radio button, title, formula, and description
        """
        return ft.Container(
            bgcolor="white",
            alignment=ft.alignment.center,
            content=ft.Row([
                ft.Radio(value=radio_value, fill_color="#049A5E"),
                ft.Column([
                    TextWidget.create_title_text(title),
                    TextWidget.create_description_text(formula),
                    TextWidget.create_description_text(description)
                ])
            ]),
            margin=ft.margin.only(top=15, left=20, right=20),
            padding=10,
            border_radius=10
        )

    @staticmethod
    def create_generic_card(content_widgets, bgcolor="white", padding=10, margin=None, border_radius=10, expand=False):
        """
        Creates a generic container card with any widgets inside
        """
        if margin is None:
            margin = ft.margin.all(5)
        return ft.Container(
            content=ft.Column(content_widgets),
            bgcolor=bgcolor,
            padding=padding,
            margin=margin,
            border_radius=border_radius,
            expand=expand
        )

    @staticmethod
    def create_radio_group(cards, value=None, on_change=None):
        """
        Wrap multiple cards containing radios into a RadioGroup
        """
        return ft.RadioGroup(
            content=ft.Column(cards),
            value=value,
            on_change=on_change
        )

    @staticmethod
    def create_column(widgets, alignment=None, spacing=10):
        return ft.Column(
            controls=widgets,
            alignment=alignment,
            spacing=spacing
        )

    @staticmethod
    def create_row(widgets, alignment=None, spacing=10):
        return ft.Row(
            controls=widgets,
            alignment=alignment,
            spacing=spacing
        )
