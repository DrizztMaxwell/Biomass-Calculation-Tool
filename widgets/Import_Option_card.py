import flet as ft

def Import_Option_Card(icon_name: ft.Icon, title: str, subtitle:str, color: ft.Colors, handle_on_click)-> ft.Container:
        return ft.Container(
            width=300,
            height=400,
            padding=ft.padding.all(30),
            border_radius=ft.border_radius.all(20),
            bgcolor=ft.Colors.WHITE,
            # Enhanced shadow for depth
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                offset=ft.Offset(0, 10),
            ),
            border=ft.border.all(1, ft.Colors.GREY_100),
            alignment=ft.alignment.center,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Column(
                [
                    # Large Icon Section with gradient background
                    ft.Container(
                        width=100,
                        height=100,
                        padding=ft.padding.all(20),
                        bgcolor=ft.Colors.with_opacity(0.08, color),
                        border_radius=ft.border_radius.all(20),
                        alignment=ft.alignment.center,
                        content=ft.Icon(
                            icon_name,
                            size=48,
                            color=color,
                        )
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                    # Title and Subtitle
                    ft.Column(
                        [
                            ft.Text(
                                title,
                                size=20,
                                weight=ft.FontWeight.W_800,
                                color=ft.Colors.BLACK87,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=10),
                            ft.Text(
                                subtitle,
                                size=14,
                                color=ft.Colors.BLACK54,
                                max_lines=3,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                text_align=ft.TextAlign.CENTER,
                                height=60
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                    # Action Button
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.UPLOAD_FILE, size=20),
                                ft.Text("Import", size=15, weight=ft.FontWeight.W_600),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        on_click=lambda e: handle_on_click(e),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=ft.padding.symmetric(horizontal=35, vertical=15),
                            bgcolor=color,
                            color=ft.Colors.WHITE,
                        ),
                        width=200,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0
            ),
        )