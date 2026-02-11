import flet as ft

class Content:
    def __init__(self, email_callback):
        self.email_callback = email_callback
        
    def create(self):
        return ft.Column([
            # Section 1: Intro (The "Lead")
            self._create_stack_item(
                "Overview",
                "This tool estimates aboveground biomass for Canadian tree species using national equations (Lambert et al. 2005). It converts standard forest inventory measurements into biomass estimates for carbon accounting and forest management. Biomass is calculated for individual tree components—wood, bark, branches, and foliage—with the sum equaling total aboveground biomass. Species-specific allometric models offer two precision levels: DBH-based equations (when height is unavailable) and more accurate DBH + height-based equations (when both measurements are provided).",
                ft.Icons.ANALYTICS_ROUNDED,
                ft.Colors.BLUE_50
            ),
            
            # Section 2: Precision & Features (Combined for height efficiency)
            self._create_stack_item(
                "Precision & Features",
                "Estimates aboveground biomass for 33 Canadian tree species using national equations (Lambert et al. 2005). Calculates biomass for wood, bark, branches, and foliage—summing to total biomass. Choose between DBH-based or more accurate DBH + height-based equations.",
                ft.Icons.SPEED_ROUNDED,
                ft.Colors.GREEN_50
            ),
           

            # Section 3: Target Audience
            self._create_stack_item(
                "Intended For",
                "Researchers, forest managers, and policy analysts requiring robust biomass estimates across Canada.",
                ft.Icons.GROUPS_ROUNDED,
                ft.Colors.GREY_50
            ),
            
            # Section 4: Contact (Streamlined)
            ft.Container(
                content=ft.Column([
                    ft.Text("Development & Contact", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                    ft.Row([
                        self._create_email_pill("Jamshid Eslamdoust", "Jamshid.Eslamdoust@ontario.ca", ft.Colors.ORANGE_800),
                        self._create_email_pill("Christopher Stratton", "Christopher.Stratton@ontario.ca", ft.Colors.BLUE_800),
                    ], spacing=10, alignment=ft.MainAxisAlignment.START),
                ], spacing=8),
                padding=12,
                bgcolor=ft.Colors.BLUE_GREY_50,
                border_radius=10,
            ),
        ], spacing=12, alignment=ft.MainAxisAlignment.START, expand=True)

    def _create_stack_item(self, title, text, icon, bgcolor):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=20, color=ft.Colors.BLUE_GREY_400),
                ft.Column([
                    ft.Text(title, size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                    ft.Text(text, size=11, color=ft.Colors.BLUE_GREY_800, width=700),
                ], spacing=2, expand=True)
            ], vertical_alignment=ft.CrossAxisAlignment.START),
            padding=12,
            bgcolor=bgcolor,
            border_radius=10,
        )

    def _create_info_chip(self, icon, label, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=14, color=color),
                ft.Text(label, size=10, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_GREY_900),
            ], spacing=5),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border=ft.border.all(1, ft.Colors.BLACK12),
            border_radius=20,
        )

    def _create_email_pill(self, name, email, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.MAIL_ROUNDED, size=14, color=color),
                ft.Text(f"{name} ({email})", size=10, weight=ft.FontWeight.W_500),
            ], spacing=8),
            on_click=lambda _: self.email_callback(email),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, color)),
            border_radius=8,
            ink=True,
        )