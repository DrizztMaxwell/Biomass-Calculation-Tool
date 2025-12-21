#text_widget
import flet as ft

class TextWidget:
    """Reusable text element factory"""

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
