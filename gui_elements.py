import flet as ft

class WidgetFactory:
    """
    Factory for creating reusable Flet widgets:
    - Texts
    - Cards/Containers
    - Buttons
    - Input fields
    """

    # -------------------
    # Text Elements
    # -------------------
    @staticmethod
    def create_title_text(message: str, color="black", size=20, font_family="Arial"):
        return ft.Text(
            message,
            color=color,
            font_family=font_family,
            weight=ft.FontWeight.W_900,
            size=size
        )

    @staticmethod
    def create_description_text(message: str, color="#686868", size=18, font_family="Arial"):
        return ft.Text(
            message,
            color=color,
            font_family=font_family,
            size=size
        )

    @staticmethod
    def create_label_text(message: str, color="black", size=18):
        return ft.Text(
            message,
            color=color,
            size=size
        )

    # -------------------
    # Cards / Containers
    # -------------------
    @staticmethod
    def create_equation_card(title, formula, description, radio_value):
        """
        Creates a card with a radio button, title, formula, and description
        """
        return ft.Container(
            bgcolor="white",
            alignment=ft.alignment.center,
            content=ft.Row([
                ft.Radio(value=radio_value, fill_color="#049A5E"),  # Radio button
                ft.Column([
                    WidgetFactory.create_title_text(title),
                    WidgetFactory.create_description_text(formula),
                    WidgetFactory.create_description_text(description)
                ])
            ]),
            margin=ft.margin.only(top=15, left=20, right=20),
            padding=10,
            border_radius=10
        )

    @staticmethod
    def create_generic_card(content_widgets, bgcolor="white", padding=10, margin=None, border_radius=10):
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
            border_radius=border_radius
        )

    # -------------------
    # Buttons
    # -------------------
    @staticmethod
    def create_button(label: str, on_click=None, color="#049A5E", text_color="white", width=None):
        return ft.ElevatedButton(
            text=label,
            bgcolor=color,
            color=text_color,
            on_click=on_click,
            width=width
        )

    # -------------------
    # Input Fields
    # -------------------
    @staticmethod
    def create_text_field(label: str, value: str = "", keyboard_type=ft.KeyboardType.TEXT, width=None):
        return ft.TextField(
            label=label,
            value=value,
            keyboard_type=keyboard_type,
            width=width
        )

    # -------------------
    # Other reusable elements
    # -------------------
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
