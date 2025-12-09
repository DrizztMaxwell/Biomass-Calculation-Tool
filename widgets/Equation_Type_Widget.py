import flet as ft

def Equation_Type_Card_Component(title_text, formula_message:str, description_message: str, radio_button_value : str):
    return ft.Container(
            bgcolor="white",
            padding=20,
            margin=30,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_GREY_900),
                offset=ft.Offset(0, 3),
            ),
            content=ft.Column(
                [
                    ft.Container(
                        margin=ft.margin.only(top=15, left=5, right=5, bottom=5), 
                        content=ft.Column([
                           title_text,
                        description_message,
                            

                        ]),
                    ),
                    ft.RadioGroup(
            content=ft.Column([
                Equation_Type_Card,
                _equation_type_card(dbh_h_title_formula, dbh_h_desc, "DBH-Height-based"),
            ]),
            on_change=self._radio_group_changed,
           
            value="DBH-based"
        )
                ]
            )
        )

