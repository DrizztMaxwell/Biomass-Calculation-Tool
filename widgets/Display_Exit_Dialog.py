import flet as ft

def Display_Exit_Dialog(yes_clicked: callable, no_clicked: callable) -> ft.AlertDialog:
    return ft.AlertDialog(
    modal=True,
    title=ft.Row(
        controls=[
            ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=24),
            ft.Text(" Confirm Exit", size=18, weight=ft.FontWeight.BOLD),
        ]
    ),
    content=ft.Container(
        content=ft.Text(
            "You're about to close the application. Are you sure you want to exit the application?",
            size=14,
        ),
        padding=ft.padding.only(top=10),
    ),
    actions=[
        ft.OutlinedButton(
            "Stay",
            on_click=no_clicked,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        ),
        ft.FilledButton(
            "Exit Anyway",
            on_click=yes_clicked,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED_700,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        ),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
    shape=ft.RoundedRectangleBorder(radius=16),
    content_padding=ft.padding.all(24),
)