import flet as ft
from widgets.TitleTextWidget import TitleTextWidget
from widgets.DescriptionText import DescriptionText
from widgets.Title_With_Icon import Title_With_Icon
from widgets.Select_Components_Widget import Select_Components_Widget
from .components.Species_Metadata_Row import Species_Metadata_Row
from .components.Parameter_Section import ParametersSection
from .components.Preview_Handler import Preview_Handler
from .components.Submit_Button import Submit_Button


class Create_Species_View:
    def __init__(self, page: ft.Page, controller):
        self.page = page
        self.__controller = controller
        self.metadata_row       = Species_Metadata_Row(page, controller)
        self.parameters_section = ParametersSection(controller)
        self.preview_handler    = Preview_Handler(page, controller)
        self.parameters_section_widget = None

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _text_primary(self):
        return "#F5F5F5" if self._is_dark else "#0F172A"

    def _text_secondary(self):
        return "#888888" if self._is_dark else "#64748B"

    def _border(self):
        return "#2E2E2E" if self._is_dark else "#E2E8F0"

    def _handle_create_button_click(self, e):
        try:
            if self.__controller.handle_create_species_button_click():
                self.preview_handler.show_preview()
        except Exception as ex:
            from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
            Custom_Alert_Dialog(
                self.page,
                title_icon=ft.Icons.ERROR_OUTLINE,
                title_color=ft.Colors.RED_700,
                title_icon_color=ft.Colors.RED,
                title="Error",
                message=f"An error occurred while creating the species: {ex}",
            ).show()

    def on_component_selection_change(self, selected_components):
        self.__controller.set_selected_components(selected_components)
        self.parameters_section.update_visibility(
            self.__controller.get_selected_components(),
            self.__controller.get_current_equation_type(),
        )
        if self.parameters_section_widget:
            self.parameters_section_widget.update()

    def on_equation_type_change(self, e):
        self.__controller.set_current_equation_type(e.control.value)
        self.parameters_section.update_visibility(
            self.__controller.get_selected_components(),
            e.control.value,
        )
        if self.parameters_section_widget:
            self.parameters_section_widget.update()

    def _section_header(self, number, title, subtitle):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(number, size=13, weight=ft.FontWeight.W_700, color="#FFFFFF"),
                    bgcolor="#16A34A",
                    border_radius=ft.border_radius.all(16),
                    width=30, height=30,
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text(title, size=16, weight=ft.FontWeight.W_700, color=self._text_primary()),
                    ft.Text(subtitle, size=12, color=self._text_secondary()),
                ], spacing=1, tight=True),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(bottom=16),
            border=ft.border.only(bottom=ft.BorderSide(1, self._border())),
            margin=ft.margin.only(bottom=18),
        )

    def _page_header(self) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ADD_BOX_OUTLINED, size=22, color="#FFFFFF"),
                        bgcolor="#16A34A",
                        border_radius=ft.border_radius.all(10),
                        width=44, height=44,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column([
                        ft.Text("Create Species", size=18,
                                weight=ft.FontWeight.W_700,
                                color=self._text_primary()),
                        ft.Text(
                            "Define a new tree species by specifying its parameters and components.",
                            size=12, color=self._text_secondary()),
                    ], spacing=2, expand=True),
                ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=1, bgcolor=self._border(),
                             margin=ft.margin.only(top=14)),
            ], spacing=0),
        )

    def build(self):
        self.parameters_section_widget = self.parameters_section.build()
        metadata_row_widget = self.metadata_row.build()
        self.metadata_row.equation_type_dropdown.on_change = self.on_equation_type_change

        select_components_widget = Select_Components_Widget(
            page=self.page,
            title=TitleTextWidget(""),
            description_text=DescriptionText(""),
            components_card_row=ft.Row(),
            selected_card_component=ft.Text(value=""),
            components_data=self.__controller.get_component_data(),
            display_button=False,
            display_shadow=False,
            on_selection_change=lambda e: self.on_component_selection_change(e),
            is_alternate_card=True,
            is_in_create_species_page=True,
        ).get_widget()

        submit_button = Submit_Button(self.page, self._handle_create_button_click).build()

        return ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self._page_header(),
                        ft.Container(height=24),
                        self._section_header("1", "Species Information",
                                             "Species code or name, origin and equation type"),
                        metadata_row_widget,
                        ft.Container(height=28),
                        self._section_header("2", "Tree Components",
                                             "Select which biomass components to include"),
                        select_components_widget,
                        ft.Container(height=28),
                        self._section_header("3", "Allometric Parameters",
                                             "Equation coefficients for each selected component"),
                        self.parameters_section_widget,
                        ft.Container(height=28),
                        submit_button,
                        ft.Container(height=24),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    spacing=0,
                ),
                margin=ft.margin.all(24),
                padding=ft.padding.all(32),
                border_radius=12,
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                shadow=ft.BoxShadow(
                    spread_radius=0, blur_radius=8,
                    color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
                    offset=ft.Offset(0, 2),
                ),
            ),
        )

    def get_species_textfield(self):    return self.metadata_row.get_species_textfield()
    def get_origin_dropdown(self):      return self.metadata_row.get_origin_dropdown()
    def get_equation_type_dropdown(self): return self.metadata_row.get_equation_type_dropdown()
    def get_parameter_controls(self):   return self.__controller.get_param_controls()
    def get_preview_modal(self):        return self.preview_handler.get_preview_modal()

    def update_parameters_visibility(self, selected_components, current_equation_type):
        self.parameters_section.update_visibility(selected_components, current_equation_type)
        if self.parameters_section_widget:
            self.parameters_section_widget.update()