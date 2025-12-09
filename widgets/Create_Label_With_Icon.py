import flet as ft

def Create_Label_With_Icon( label_text:str ="", icon_src:str ="",  width=27, height = 27):
        return ft.Column([
            ft.Row([
                ft.Text(label_text, font_family="Poppins-Medium",  weight=ft.FontWeight.W_700, color=ft.Colors.BLACK, size=15),
                ft.Image(
                     src=icon_src,
        width=width,
        height=height,
        fit=ft.ImageFit.CONTAIN,
                )

            ]),
           
        ])