import flet as ft
from data.components_data import COMPONENTS_DATA
from helper_functions.Assets_Helper import asset_helper
import os
import sys


class Select_Components_Widget:
    def __init__(
        self,
        page: ft.Page,
        title: ft.Text,
        description_text: ft.Text,
        components_card_row,
        selected_card_component,
        components_data=None,
        display_button=True,
        display_shadow=True,
        on_selection_change=None,
        is_alternate_card=False,
        is_database_selected=False,
        is_in_create_species_page=False
    ):
        self.debug = False
        self.page = page
        self.title = title
        self.description_text = description_text
        self.components_card_row = components_card_row
        self.selected_card_component = selected_card_component

        if components_data:
            self.components_data = self._prepare_component_data(components_data)
        else:
            self.components_data = self._prepare_component_data(COMPONENTS_DATA.copy())

        self.display_button      = display_button
        self.display_shadow      = display_shadow
        self.on_selection_change = on_selection_change
        self.is_alternate_card   = is_alternate_card
        self.is_database_selected = is_database_selected
        self.is_in_create_species_page = is_in_create_species_page

        self.original_components_data = self._prepare_component_data(COMPONENTS_DATA.copy())
        self._initialize_widget()

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self):
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _card_bg(self, is_selected, is_disabled):
        if is_disabled or is_selected:
            return ft.Colors.with_opacity(0.10, "#16A34A")
        return "#2A2A2A" if self._is_dark else "#FFFFFF"

    def _card_border(self, is_selected, is_disabled):
        if is_disabled or is_selected:
            return "#16A34A"
        return "#3A3A3A" if self._is_dark else "#E2E8F0"

    def _card_border_width(self, is_selected, is_disabled):
        return 2 if (is_selected or is_disabled) else 1

    def _text_primary(self):
        return "#F5F5F5" if self._is_dark else "#0F172A"

    def _text_secondary(self):
        return "#888888" if self._is_dark else "#64748B"

    def _surface(self):
        return "#222222" if self._is_dark else "#F8FAFC"

    # ── Path helpers ──────────────────────────────────────────────────────────

    def _get_resource_path(self, relative_path):
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            clean_path = relative_path.replace('./', '').replace('\\', '/')
            return os.path.join(base_path, clean_path)
        except Exception:
            return relative_path

    def _prepare_component_data(self, components):
        for component in components:
            if "image_src" in component:
                component["image_src"] = self._get_resource_path(component["image_src"])
        return components

    # ── Init ──────────────────────────────────────────────────────────────────

    def _initialize_widget(self):
        if not self.is_in_create_species_page:
            self._apply_database_mode()
        elif self.is_in_create_species_page:
            for component in self.components_data:
                component["is_selected"] = False
        else:
            self._apply_database_mode()
        self._create_select_all_button()
        self._build_component_cards()
        self._update_selected_text()

    def _apply_database_mode(self):
        for i, component in enumerate(self.components_data):
            if self.is_database_selected:
                component["is_selected"] = True
                component["is_disabled"] = True
            else:
                if i < len(self.original_components_data):
                    component["is_selected"] = self.original_components_data[i].get("is_selected", False)
                else:
                    component["is_selected"] = False
                component["is_disabled"] = False

    # ── Select-all button ─────────────────────────────────────────────────────

    def _create_select_all_button(self):
        label = "All Required" if self.is_database_selected else (
            "Deselect All" if self._all_components_selected() else "Select All"
        )
        icon  = ft.Icons.CHECK_BOX_OUTLINED if not self._all_components_selected() else ft.Icons.CHECK_BOX_OUTLINE_BLANK

        self.select_all_button = ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=14,
                        color="#16A34A" if not self.is_database_selected else "#888888"),
                ft.Text(label, size=12, weight=ft.FontWeight.W_600,
                        color="#16A34A" if not self.is_database_selected else "#888888"),
            ], spacing=6, tight=True),
            on_click=None if self.is_database_selected else self._select_all_components,
            bgcolor=ft.Colors.with_opacity(0.07, "#16A34A" if not self.is_database_selected else "#888888"),
            border=ft.border.all(1, ft.Colors.with_opacity(
                0.25, "#16A34A" if not self.is_database_selected else "#888888"
            )),
            border_radius=ft.border_radius.all(20),
            padding=ft.padding.symmetric(horizontal=14, vertical=7),
            ink=not self.is_database_selected,
            tooltip="Select or deselect all components",
        )

    def _get_select_all_button_text(self):
        if self.is_database_selected:
            return "All Required"
        return "Deselect All" if self._all_components_selected() else "Select All"

    def _all_components_selected(self):
        return all(comp.get("is_selected", False) for comp in self.components_data)

    # ── Cards ─────────────────────────────────────────────────────────────────

    def _create_component_card(self, component):
        is_disabled = component.get("is_disabled", False)
        is_selected = component["is_selected"]

        # Checkmark badge (top-right) — only visible when selected
        check_badge = ft.Container(
            content=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, size=16, color="#16A34A"),
            visible=is_selected or is_disabled,
            alignment=ft.alignment.top_right,
        )

        image = ft.Image(
            src=component["image_src"],
            fit=ft.ImageFit.CONTAIN,
            color=ft.Colors.with_opacity(0.4, "#888888") if is_disabled else None,
            error_content=ft.Icon(ft.Icons.FOREST_OUTLINED, size=30,
                                   color="#16A34A" if is_selected else "#888888"),
        )

        card_content = ft.Stack([
            ft.Column([
                ft.Container(
                    content=image,
                    width=48, height=48,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=8),
                ft.Text(
                    component["title"],
                    size=13,
                    weight=ft.FontWeight.W_600,
                    color="#16A34A" if (is_selected or is_disabled) else self._text_primary(),
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
            ),
            ft.Container(
                content=check_badge,
                alignment=ft.alignment.top_right,
                padding=ft.padding.all(6),
            ),
        ])

        card = ft.Container(
            width=130,
            height=130,
            border_radius=ft.border_radius.all(10),
            bgcolor=self._card_bg(is_selected, is_disabled),
            border=ft.border.all(
                self._card_border_width(is_selected, is_disabled),
                self._card_border(is_selected, is_disabled),
            ),
            padding=10,
            alignment=ft.alignment.center,
            animate_scale=None if is_disabled else ft.Animation(200, "easeInOut"),
            scale=1.0,
            clip_behavior=ft.ClipBehavior.NONE,
            content=card_content,
            tooltip="Required" if is_disabled else "Click to select/deselect",
            shadow=ft.BoxShadow(
                blur_radius=6, spread_radius=0,
                color=ft.Colors.with_opacity(0.12 if is_selected else 0.04,
                                              "#16A34A" if is_selected else "#000000"),
                offset=ft.Offset(0, 2),
            ) if not is_disabled else None,
        )

        if not is_disabled:
            card.on_click = lambda e, comp=component: self._toggle_component(e, comp)
            card.on_hover = lambda e: self._handle_hover(e, card)

        return card

    def _handle_hover(self, e, card):
        card.scale = 1.05 if e.data == "true" else 1.0
        card.update()

    def _toggle_component(self, e, component):
        if component.get("is_disabled", False):
            return
        component["is_selected"] = not component["is_selected"]
        self._update_card_appearance(e.control, component)
        self._update_ui_state()
        if self.on_selection_change:
            self.on_selection_change(self.selected_components)

    def _update_card_appearance(self, card, component):
        is_selected = component["is_selected"]
        card.bgcolor = self._card_bg(is_selected, False)
        card.border  = ft.border.all(
            self._card_border_width(is_selected, False),
            self._card_border(is_selected, False),
        )
        card.shadow = ft.BoxShadow(
            blur_radius=6, spread_radius=0,
            color=ft.Colors.with_opacity(0.12 if is_selected else 0.04,
                                          "#16A34A" if is_selected else "#000000"),
            offset=ft.Offset(0, 2),
        )
        # Update check badge and title color inside the Stack
        try:
            stack   = card.content
            col     = stack.controls[0]
            badge_c = stack.controls[1]

            # Title text — last in column
            col.controls[-1].color = "#16A34A" if is_selected else self._text_primary()
            # Check badge visibility
            badge_c.content.visible = is_selected
        except Exception:
            pass
        card.update()

    def _update_ui_state(self):
        self._update_selected_text()
        self._refresh_select_all_button()
        self._update_controls()

    def _refresh_select_all_button(self):
        all_sel = self._all_components_selected()
        label = "Deselect All" if all_sel else "Select All"
        icon  = ft.Icons.CHECK_BOX_OUTLINE_BLANK if all_sel else ft.Icons.CHECK_BOX_OUTLINED
        try:
            row = self.select_all_button.content
            row.controls[0].name  = icon
            row.controls[1].value = label
            self.select_all_button.update()
        except Exception:
            pass

    def _update_selected_text(self):
        if self.is_database_selected:
            self.selected_card_component.value = "All components selected (database mode)"
        elif self.selected_components:
            self.selected_card_component.value = f"Selected: {', '.join(self.selected_components)}"
        else:
            self.selected_card_component.value = "No components selected"
        self.selected_card_component.color = self._text_secondary()

    def _update_controls(self):
        try:
            self.selected_card_component.update()
        except Exception:
            pass

    def _select_all_components(self, e=None):
        if self.is_database_selected:
            return
        all_selected = self._all_components_selected()
        for component in self.components_data:
            if not component.get("is_disabled", False):
                component["is_selected"] = not all_selected
        self._rebuild_component_cards()
        self._update_ui_state()
        if self.on_selection_change:
            self.on_selection_change(self.selected_components)

    def _build_component_cards(self):
        self.components_card_row.controls.clear()
        for component in self.components_data:
            self.components_card_row.controls.append(self._create_component_card(component))

    def _rebuild_component_cards(self):
        for i, component in enumerate(self.components_data):
            if i < len(self.components_card_row.controls):
                self._update_card_appearance(
                    self.components_card_row.controls[i], component
                )

    # ── Widget assembly ───────────────────────────────────────────────────────

    def get_widget(self):
        # Selected summary strip
        selected_strip = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE_ROUNDED if self.selected_components else ft.Icons.RADIO_BUTTON_UNCHECKED,
                    size=14,
                    color="#16A34A" if self.selected_components else self._text_secondary(),
                ),
                self.selected_card_component,
            ], spacing=8),
            bgcolor=ft.Colors.with_opacity(
                0.07 if self.selected_components else 0.03, "#16A34A"
            ),
            border=ft.border.all(
                1,
                ft.Colors.with_opacity(
                    0.20 if self.selected_components else 0.10, "#16A34A"
                ),
            ),
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            margin=ft.margin.only(top=12),
        )

        controls = []

        # Add title if it has visible content
        title_val = getattr(self.title, 'value', None)
        if title_val is None or title_val != "":
            # It's either a non-Text widget (ft.Row etc.) or a Text with content
            if not (hasattr(self.title, 'value') and self.title.value == ""):
                controls.append(self.title)
        # Add description if non-empty
        desc_val = getattr(self.description_text, 'value', None)
        if desc_val is None or desc_val != "":
            if not (hasattr(self.description_text, 'value') and self.description_text.value == ""):
                controls.append(ft.Container(content=self.description_text, margin=ft.margin.only(top=2)))

        if self.display_button:
            controls.append(
                ft.Container(
                    content=ft.Row([self.select_all_button],
                                   alignment=ft.MainAxisAlignment.START),
                    margin=ft.margin.only(top=10, bottom=10),
                )
            )

        controls += [
            ft.Container(
                content=ft.Row(
                    controls=self.components_card_row.controls,
                    spacing=12,
                    wrap=True,
                ),
                padding=ft.padding.all(8),  # breathing room so scaled cards aren't clipped
            ),
            selected_strip,
        ]

        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            padding=0 if self.is_alternate_card else 20,
            margin=0 if self.is_alternate_card else 30,
            border_radius=10,
            shadow=self._create_shadow() if self.display_shadow else None,
            alignment=ft.alignment.top_left,
            content=ft.Column(
                controls=controls,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=0,
                expand=True,
            ),
        )

    def _create_shadow(self):
        return ft.BoxShadow(
            spread_radius=0, blur_radius=6,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        )

    # ── Public API ────────────────────────────────────────────────────────────

    @property
    def selected_components(self):
        return [comp["title"] for comp in self.components_data if comp["is_selected"]]

    def set_selected_components(self, component_titles):
        if self.is_database_selected:
            return
        for component in self.components_data:
            if not component.get("is_disabled", False):
                component["is_selected"] = component["title"] in component_titles
        self._rebuild_component_cards()
        self._update_ui_state()

    def toggle_database_mode(self, is_database_selected: bool):
        self.is_database_selected = is_database_selected
        self._apply_database_mode()
        self._create_select_all_button()
        self._build_component_cards()
        self._update_selected_text()
        self._update_controls()

    def refresh_asset_paths(self):
        for component in self.components_data:
            if "image_src" in component:
                component["image_src"] = self._get_resource_path(component["image_src"])
        self._build_component_cards()

    def enable_debug(self, enabled=True):
        self.debug = enabled

    def _create_title_text(self, component, is_disabled):
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Text(
                value=component["title"],
                weight=ft.FontWeight.W_600,
                color=self._text_secondary() if is_disabled else self._text_primary(),
                size=13,
                text_align=ft.TextAlign.CENTER,
            ),
        )