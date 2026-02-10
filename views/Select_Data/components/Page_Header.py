import flet as ft
from widgets.DescriptionText import DescriptionText
from widgets.Title_With_Icon import Title_With_Icon

class Page_Header:
    """Component for the select data view header"""
    
    @staticmethod
    def create():
        """Create the header section with title and description"""
        return ft.Container(
            content=ft.Column(
                [
                    Title_With_Icon(
                        "Select Import Data", 
                        ft.Icons.FILE_PRESENT_OUTLINED
                    ),
                    DescriptionText(
                        "Select how you wish to import the dataset"
                    ),
                    ft.Divider(color=ft.Colors.GREY_300, height=30),
                ],
                spacing=8,
            ),
            padding=ft.padding.only(bottom=10),
        )   