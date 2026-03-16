import flet as ft
from widgets.Select_Components_Widget import Select_Components_Widget
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
from data.components_data import COMPONENTS_DATA


class Components_Section:
    """Tree components selection section."""

    def __init__(self, page: ft.Page, controller):
        self.page       = page
        self.controller = controller
        self.component_cards_row        = ft.Row(wrap=True)
        self.selected_components_text   = ft.Text(value="",
                                                   color=ft.Colors.ON_SURFACE_VARIANT,
                                                   weight=ft.FontWeight.W_500,
                                                   size=13)

    def create(self) -> ft.Container:
        widget = Select_Components_Widget(
            display_shadow=False,
            page=self.page,
            title=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.FOREST_OUTLINED, size=22,
                                            color="#FFFFFF"),
                            bgcolor="#16A34A",
                            border_radius=ft.border_radius.all(10),
                            width=44, height=44,
                            alignment=ft.alignment.center,
                        ),
                        ft.Column([
                            ft.Text("Select Tree Component", size=18,
                                    weight=ft.FontWeight.W_700,
                                    color=ft.Colors.ON_SURFACE),
                            ft.Text("Select which biomass components to include",
                                    size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                        ], spacing=2, expand=True),
                    ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),

                ], spacing=0),
                margin=ft.margin.only(bottom=16),
            ),
            description_text=ft.Text(""),
            components_card_row=self.component_cards_row,
            selected_card_component=self.selected_components_text,
            components_data=COMPONENTS_DATA,
            is_database_selected=self.controller.get_database_selected_flag(),
            is_alternate_card=True,
        ).get_widget()

        return ft.Container(
            content=widget,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            padding=20,
            margin=30,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
                offset=ft.Offset(0, 3),
            ),
        )

    def get_selected_components(self):
        return [c['title'] for c in COMPONENTS_DATA if c['is_selected']]