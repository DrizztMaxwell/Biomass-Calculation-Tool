import flet as ft


# ── Equation_Card_Title_Text ──────────────────────────────────────────────────

def Equation_Card_Title_Text(text: str) -> ft.Text:
    return ft.Text(
        text,
        size=15,
        weight=ft.FontWeight.W_700,
        color=ft.Colors.ON_SURFACE,
    )


# ── Equation_Card_Formula_Text ────────────────────────────────────────────────

def Equation_Card_Formula_Text(
    text: str,
    color: str = "#16A34A",
    weight=ft.FontWeight.W_600,
    size: int = 13,
) -> ft.Text:
    return ft.Text(text, size=size, weight=weight, color=color)


# ── Equation_Card_Description_Text ───────────────────────────────────────────

def Equation_Card_Description_Text(text: str = "", size: int = 12) -> ft.Text:
    return ft.Text(
        text,
        size=size,
        color=ft.Colors.ON_SURFACE_VARIANT,
        weight=ft.FontWeight.W_400,
    )


# ── Equation_Type_Card ────────────────────────────────────────────────────────

def Equation_Type_Card(
    main_text_column: ft.Column,
    desc_widget: ft.Text,
    radio_value: str,
    is_selected: bool = False,
) -> ft.Container:
    """
    Single selectable equation card with radio button on the left.
    Hover → subtle grey tint. Selected → green tint + green border.
    Border is always soft (0.5px) — no harsh outline.
    """

    def _bg(selected, hovered):
        if selected:
            return ft.Colors.with_opacity(0.08, "#16A34A")
        if hovered:
            return ft.Colors.with_opacity(0.04, ft.Colors.ON_SURFACE)
        return ft.Colors.SECONDARY_CONTAINER

    def _border(selected):
        if selected:
            return ft.border.all(1.5, ft.Colors.with_opacity(0.5, "#16A34A"))
        return None  # No border at rest — only shown when selected

    radio = ft.Radio(value=radio_value, active_color="#16A34A")

    card = ft.Container(
        padding=ft.padding.symmetric(horizontal=16, vertical=14),
        margin=ft.margin.only(bottom=10),
        border_radius=ft.border_radius.all(10),
        border=_border(is_selected),
        bgcolor=_bg(is_selected, False),
        animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Row([
            radio,
            ft.Column([
                main_text_column,
                desc_widget,
            ], spacing=3, expand=True),
        ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
    )

    def on_hover(e):
        # Don't override selected state on hover
        if radio.value != getattr(radio, '_group_value', None):
            card.bgcolor = _bg(False, e.data == "true")
            card.update()

    def on_click(e):
        card.bgcolor = _bg(True, False)
        card.border  = _border(True)
        card.update()

    card.on_hover = on_hover
    card.on_click = on_click
    card.ink      = True

    return card


# ── Equation_Type_Card_Component (container for a group of cards) ─────────────

def Equation_Type_Card_Component(
    title_text: ft.Control,
    formula_message: str,
    description_message: str,
    radio_button_value: str,
) -> ft.Container:
    """
    Wrapper card for an equation type option.
    Matches the app's card pattern: surface bg, 1px border, 10px radius.
    """
    return ft.Container(
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        padding=ft.padding.all(20),
        border_radius=ft.border_radius.all(10),
        border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=6,
            color=ft.Colors.with_opacity(0.06, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
        content=ft.Column([
            title_text,
            ft.Container(height=4),
            Equation_Card_Formula_Text(formula_message),
            ft.Container(height=2),
            Equation_Card_Description_Text(description_message),
        ], spacing=0),
    )