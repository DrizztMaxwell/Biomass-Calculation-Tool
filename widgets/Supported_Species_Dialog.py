import flet as ft
import json

class Supported_Species_Dialog:
    def __init__(self, page: ft.Page):
        self.page = page
        try:
            with open("data/treeparameters.json", "r") as f:
                self.species_data = json.load(f)
        except Exception:
            self.species_data = [{"SpeciesCode": "1", "SpecCommon": "alpine fir"}, {"SpeciesCode": "2", "SpecCommon": "lodgepole pine"}]

    def create_species_tile(self, code, name):
        """Creates a clean, modern tile for each species with Title Case formatting."""
        # .title() converts "alpine fir" to "Alpine Fir"
        formatted_name = str(name).title() 
        
        return ft.Container(
            content=ft.ListTile(
                leading=ft.Icon(ft.Icons.NATURE_PEOPLE_OUTLINED, color=ft.Colors.GREEN_400),
                title=ft.Text(
                    formatted_name, 
                    weight=ft.FontWeight.W_600, # Slightly heavier for better readability
                    size=16,
                    color=ft.Colors.BLUE_GREY_900
                ),
                subtitle=ft.Text(
                    f"Code: {code if code else 'N/A'}", 
                    size=12, 
                    color=ft.Colors.BLUE_GREY_400
                ),
                dense=True,
            ),
            margin=ft.margin.only(bottom=8),
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.ON_SURFACE_VARIANT),
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.OUTLINE)),
        )

    def show(self):
        # Container for the list items
        list_container = ft.Column(
            controls=[self.create_species_tile(s.get('SpeciesCode'), s.get('SpecCommon')) for s in self.species_data],
            spacing=0,
        )

        def on_search(e):
            search_term = e.control.value.lower()
            list_container.controls = []
            for s in self.species_data:
                common_name = str(s.get('SpecCommon', '')).lower()
                species_code = str(s.get('SpeciesCode', '')).lower()
                
                if search_term in common_name or search_term in species_code:
                    list_container.controls.append(
                        self.create_species_tile(s.get('SpeciesCode'), s.get('SpecCommon'))
                    )
            list_container.update()

        dialog = ft.AlertDialog(
            modal=True,
            title_padding=0,
            content_padding=0,
            shape=ft.RoundedRectangleBorder(radius=20),
            content=ft.Container(
                width=450,
                height=600,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Column(
                    spacing=0,
                    controls=[
                        # Header
                        ft.Container(
                            bgcolor=ft.Colors.GREEN,
                            padding=25,
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.NATURE_PEOPLE_OUTLINED, color=ft.Colors.WHITE, size=30),
                                    ft.Text("Tree Species", color=ft.Colors.WHITE, size=24, weight=ft.FontWeight.BOLD),
                                ], alignment=ft.MainAxisAlignment.START),
                                ft.Text("Official database for biomass calculation", color=ft.Colors.GREEN_100, size=12),
                            ])
                        ),
                        
                        # Search Bar
                        ft.Container(
                            padding=ft.padding.only(left=20, right=20, top=15, bottom=10),
                            content=ft.TextField(
                                hint_text="Search species or code...",
                                prefix_icon=ft.Icons.SEARCH,
                                border_radius=15,
                                text_size=14,
                                height=48,
                                content_padding=10,
                                on_change=on_search,
                                border_color=ft.Colors.OUTLINE_VARIANT,
                                focused_border_color=ft.Colors.GREEN,
                                bgcolor=ft.Colors.SURFACE,
                            )
                        ),
                        
                        # List Area
                        ft.Container(
                            expand=True,
                            padding=ft.padding.only(left=20, right=20, bottom=10),
                            content=ft.ListView(
                                controls=[list_container],
                                spacing=10,
                                padding=10,
                            )
                        )
                    ]
                )
            ),
            actions=[
                ft.TextButton(
                    "Dismiss", 
                    on_click=lambda e: self.page.close(dialog),
                    style=ft.ButtonStyle(color=ft.Colors.GREEN_700)
                )
            ],
            actions_padding=ft.padding.only(right=15, bottom=10)
        )

        self.page.open(dialog)
        return dialog