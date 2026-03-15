import flet as ft
from .Parameter_Input import Parameter_Input


class ParametersSection:
    """Creates the parameter input fields section with component labels."""

    COMPONENT_COLORS = {
        "Wood":    "#F59E0B",
        "Bark":    "#92400E",
        "Branch":  "#FB923C",
        "Foliage": "#22C55E",
        "Crown":   "#2563EB",
        "Stem":    "#8B5CF6",
        "Total":   "#64748B",
    }

    COMPONENT_ICONS = {
        "Wood":    ft.Icons.CABIN_OUTLINED,
        "Bark":    ft.Icons.TEXTURE,
        "Branch":  ft.Icons.ACCOUNT_TREE_OUTLINED,
        "Foliage": ft.Icons.FOREST_OUTLINED,
        "Crown":   ft.Icons.CLOUD_OUTLINED,
        "Stem":    ft.Icons.STRAIGHTEN,
        "Total":   ft.Icons.FUNCTIONS,
    }

    def __init__(self, controller):
        self.controller = controller
        self.param_labels = {}
        self.no_parameters = None
        self.sections = {}

    def _create_component_section(self, component_name, b1, b2, b3=None):
        color = self.COMPONENT_COLORS.get(component_name, "#64748B")
        icon  = self.COMPONENT_ICONS.get(component_name, ft.Icons.TUNE)

        label = ft.Text(component_name, size=14, weight=ft.FontWeight.W_600, color=color)
        self.param_labels[component_name] = label

        param_items = [
            ft.Container(content=b1, expand=True),
            ft.Container(content=b2, expand=True),
        ]
        if b3:
            param_items.append(ft.Container(content=b3, expand=True))

        card_header = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=15, color=color),
                    bgcolor=ft.Colors.with_opacity(0.10, color),
                    border_radius=ft.border_radius.all(7),
                    width=30, height=30,
                    alignment=ft.alignment.center,
                ),
                label,
            ], spacing=10),
            padding=ft.padding.only(left=16, right=16, top=12, bottom=10),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
        )

        card_body = ft.Container(
            content=ft.Row(param_items, spacing=16),
            padding=ft.padding.symmetric(horizontal=16, vertical=14),
        )

        section = ft.Container(
            content=ft.Column([
                card_header,
                ft.Container(height=1, bgcolor=ft.Colors.OUTLINE_VARIANT),
                card_body,
            ], spacing=0),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=ft.border_radius.all(10),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        self.sections[component_name] = section
        return section

    def build(self):
        # DBH-based
        wood_b1    = Parameter_Input.create("b1", self.controller)
        wood_b2    = Parameter_Input.create("b2", self.controller)
        bark_b1    = Parameter_Input.create("b1", self.controller)
        bark_b2    = Parameter_Input.create("b2", self.controller)
        branch_b1  = Parameter_Input.create("b1", self.controller)
        branch_b2  = Parameter_Input.create("b2", self.controller)
        foliage_b1 = Parameter_Input.create("b1", self.controller)
        foliage_b2 = Parameter_Input.create("b2", self.controller)
        crown_b1   = Parameter_Input.create("b1", self.controller)
        crown_b2   = Parameter_Input.create("b2", self.controller)
        stem_b1    = Parameter_Input.create("b1", self.controller)
        stem_b2    = Parameter_Input.create("b2", self.controller)
        total_b1   = Parameter_Input.create("b1", self.controller)
        total_b2   = Parameter_Input.create("b2", self.controller)
        # b3
        wood_b3    = Parameter_Input.create("b3", self.controller)
        bark_b3    = Parameter_Input.create("b3", self.controller)
        branch_b3  = Parameter_Input.create("b3", self.controller)
        foliage_b3 = Parameter_Input.create("b3", self.controller)
        crown_b3   = Parameter_Input.create("b3", self.controller)
        stem_b3    = Parameter_Input.create("b3", self.controller)
        total_b3   = Parameter_Input.create("b3", self.controller)

        self.controller.set_param_controls({
            "DBH-based": {
                "Wood":    [wood_b1,    wood_b2],
                "Bark":    [bark_b1,    bark_b2],
                "Branch":  [branch_b1,  branch_b2],
                "Foliage": [foliage_b1, foliage_b2],
                "Crown":   [crown_b1,   crown_b2],
                "Stem":    [stem_b1,    stem_b2],
                "Total":   [total_b1,   total_b2],
            },
            "DBH + Height-based": {
                "Wood":    [wood_b1,    wood_b2,    wood_b3],
                "Bark":    [bark_b1,    bark_b2,    bark_b3],
                "Branch":  [branch_b1,  branch_b2,  branch_b3],
                "Foliage": [foliage_b1, foliage_b2, foliage_b3],
                "Crown":   [crown_b1,   crown_b2,   crown_b3],
                "Stem":    [stem_b1,    stem_b2,    stem_b3],
                "Total":   [total_b1,   total_b2,   total_b3],
            },
        })

        # Empty state
        self.no_parameters = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(ft.Icons.TOUCH_APP_OUTLINED, size=30,
                                    color=ft.Colors.with_opacity(0.4, ft.Colors.PRIMARY)),
                    bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.PRIMARY),
                    border_radius=ft.border_radius.all(28),
                    width=56, height=56,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=12),
                ft.Text("No components selected", size=15, weight=ft.FontWeight.W_600,
                        color=ft.Colors.ON_SURFACE, text_align=ft.TextAlign.CENTER),
                ft.Container(height=4),
                ft.Text("Select tree components above to configure their parameters.",
                        size=13, color=ft.Colors.ON_SURFACE_VARIANT,
                        text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, tight=True),
            padding=ft.padding.symmetric(vertical=16),
            alignment=ft.alignment.center,
            visible=True,
        )

        sections_list = [self.no_parameters]

        for component in ["Wood", "Bark", "Branch", "Foliage", "Crown", "Stem", "Total"]:
            section = self._create_component_section(
                component,
                locals()[f"{component.lower()}_b1"],
                locals()[f"{component.lower()}_b2"],
                locals().get(f"{component.lower()}_b3"),
            )
            sections_list.append(section)
            sections_list.append(ft.Container(height=10))

        self._hide_all_sections()
        return ft.Column(controls=sections_list, spacing=0)

    def _hide_all_parameters(self):
        param_controls = self.controller.get_param_controls()
        if param_controls:
            for eq in param_controls.values():
                for params in eq.values():
                    for p in params:
                        p.visible = False
        for lbl in self.param_labels.values():
            lbl.visible = False

    def _hide_all_sections(self):
        for s in self.sections.values():
            s.visible = False

    def update_visibility(self, selected_components, current_equation_type):
        eq_key = "DBH-based" if current_equation_type == "DBH-based" else "DBH + Height-based"
        self._hide_all_parameters()
        self._hide_all_sections()
        any_visible = False
        param_controls = self.controller.get_param_controls()
        for component in selected_components:
            if component in param_controls[eq_key]:
                if component in self.sections:
                    self.sections[component].visible = True
                if component in self.param_labels:
                    self.param_labels[component].visible = True
                for p in param_controls[eq_key][component]:
                    p.visible = True
                    any_visible = True
        if self.no_parameters:
            self.no_parameters.visible = not any_visible