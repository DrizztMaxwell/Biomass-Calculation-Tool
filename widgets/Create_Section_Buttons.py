import flet as ft

def Create_Section_Buttons(button_1_text:str, button_2_text:str, switch_view_all, switch_view_tree_management ,current_view:str="all"):
        """Create toggle buttons for different error sections"""
        return ft.Row(
            controls=[
                # All Errors Button
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.LIST_ALT_ROUNDED, 
                                    size=18, 
                                    color=ft.Colors.WHITE if current_view == "all" else ft.Colors.BLUE_600
                                ),
                                ft.Text(
                                   button_1_text, 
                                    color=ft.Colors.WHITE if current_view == "all" else ft.Colors.BLUE_600,
                                    weight=ft.FontWeight.BOLD,
                                    size=13,
                                ),
                            ],
                            spacing=8,
                        ),
                        #_switch_view("all")
                        on_click=lambda e: switch_view_all(),
                        bgcolor=ft.Colors.BLUE_600 if current_view == "all" else ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(horizontal=20, vertical=12),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            shadow_color=ft.Colors.with_opacity(0.2, ft.Colors.BLUE_600) if current_view == "all" else None,
                            elevation=3 if current_view == "all" else 0,
                        ),
                    ),
                ),
                # Tree Measurements Button
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.NATURE_PEOPLE_ROUNDED, 
                                    size=18, 
                                    color=ft.Colors.WHITE if current_view == "tree_measurements" else ft.Colors.GREEN_600
                                ),
                                ft.Text(
                                    button_2_text, 
                                    color=ft.Colors.WHITE if current_view == "tree_measurements" else ft.Colors.GREEN_600,
                                    weight=ft.FontWeight.BOLD,
                                    size=13,
                                ),
                            ],
                            spacing=8,
                        ),
                        on_click=lambda e: switch_view_tree_management(),
                        bgcolor=ft.Colors.GREEN_600 if current_view == "tree_measurements" else ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(horizontal=20, vertical=12),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            shadow_color=ft.Colors.with_opacity(0.2, ft.Colors.GREEN_600) if current_view == "tree_measurements" else None,
                            elevation=3 if current_view == "tree_measurements" else 0,
                        ),
                    ),
                ),
            ],
            spacing=15,
        )