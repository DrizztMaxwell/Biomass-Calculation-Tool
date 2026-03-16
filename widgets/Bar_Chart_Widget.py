import flet as ft
import datetime
import os
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─── Design tokens ────────────────────────────────────────────────────────────
_ACCENT        = "#2DD4BF"
_ACCENT_DARK   = "#0F766E"
_WOOD_COLOR    = "#F59E0B"
_BARK_COLOR    = "#92400E"
_BRANCH_COLOR  = "#FB923C"
_FOLIAGE_COLOR = "#22C55E"
_COMPONENT_COLORS = {
    "Wood":    _WOOD_COLOR,
    "Bark":    _BARK_COLOR,
    "Branch":  _BRANCH_COLOR,
    "Foliage": _FOLIAGE_COLOR,
}
_STACK_ORDER = ["Wood", "Bark", "Branch", "Foliage"]


class Bar_Chart_Widget(ft.BarChart):

    def __init__(self, page: ft.Page, on_save=None, species_data=None):
        super().__init__()
        self.page               = page
        self.on_save            = on_save
        self.species_data       = species_data or []
        self.card_ref           = ft.Ref[ft.Card]()
        self.confirmation_ref   = ft.Ref[ft.Container]()
        self.summary_table_ref  = ft.Ref[ft.Container]()
        self.file_path_of_saved_chart_image = ""
        self.has_saved          = False

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self) -> bool:
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _surface(self):      return "#1A1A1A" if self._is_dark else "#FFFFFF"
    def _surface_alt(self):  return "#222222" if self._is_dark else "#F8FAFC"
    def _border_color(self): return "#2E2E2E" if self._is_dark else "#E2E8F0"
    def _text_primary(self): return "#F5F5F5" if self._is_dark else "#0F172A"
    def _text_secondary(self): return "#888888" if self._is_dark else "#64748B"
    def _grid_color(self):   return "#2E2E2E" if self._is_dark else "#E2E8F0"
    def _chart_bg(self):     return "#111111" if self._is_dark else "#F8FAFC"

    # ── Data helpers ──────────────────────────────────────────────────────────

    def _calculate_max_y(self) -> float:
        if not self.species_data:
            return 1000
        max_val = max(sum(s.get(k, 0) for k in _STACK_ORDER) for s in self.species_data)
        return (((max_val * 1.15) + 99) // 100) * 100 if max_val > 0 else 1000

    # ── File dialogs ──────────────────────────────────────────────────────────

    def _show_confirmation(self, path: str, is_csv=False):
        if not self.confirmation_ref.current:
            return
        icon  = ft.Icons.TABLE_CHART_ROUNDED if is_csv else ft.Icons.IMAGE_ROUNDED
        color = "#16A34A" if is_csv else "#2563EB"
        label = "CSV saved to" if is_csv else "PNG saved to"
        c = self.confirmation_ref.current
        c.content = ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=color, size=16),
            ft.Text(label, size=12, color=self._text_secondary()),
            ft.Text(path, size=12, color=color,
                    weight=ft.FontWeight.W_600, selectable=True),
        ], spacing=6)
        c.bgcolor   = ft.Colors.with_opacity(0.10, color)
        c.border    = ft.border.all(1, ft.Colors.with_opacity(0.25, color))
        c.visible   = True
        c.opacity   = 1
        c.update()

    def _open_png_save_dialog(self, e):
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        def on_result(result: ft.FilePickerResultEvent):
            if not result.path:
                return
            path = result.path if result.path.endswith(".png") else result.path + ".png"
            try:
                self._render_chart_to_png(path)
                self.file_path_of_saved_chart_image = path
                self.has_saved = True
                self._show_confirmation(path, is_csv=False)
                self._snack(f"Chart exported to {os.path.basename(path)}", "#2563EB")
            except Exception as ex:
                self._snack(f"Export failed: {ex}", "#DC2626", is_error=True)

        picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(picker)
        self.page.update()
        picker.save_file(
            dialog_title="Save chart as PNG",
            file_name=f"biomass_chart_{stamp}.png",
            allowed_extensions=["png"],
        )

    def _open_csv_save_dialog(self, e):
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        def on_result(result: ft.FilePickerResultEvent):
            if not result.path:
                return
            path = result.path if result.path.endswith(".csv") else result.path + ".csv"
            try:
                self._export_csv(path)
                self._show_confirmation(path, is_csv=True)
                self._snack(f"Table exported to {os.path.basename(path)}", "#16A34A")
            except Exception as ex:
                self._snack(f"CSV export failed: {ex}", "#DC2626", is_error=True)

        picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(picker)
        self.page.update()
        picker.save_file(
            dialog_title="Save table as CSV",
            file_name=f"biomass_table_{stamp}.csv",
            allowed_extensions=["csv"],
        )

    def _snack(self, msg: str, color: str, is_error=False):
        icon = ft.Icons.ERROR_ROUNDED if is_error else ft.Icons.CHECK_CIRCLE_ROUNDED
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(icon, color="#FFFFFF"),
                ft.Text(msg, color="#FFFFFF", weight=ft.FontWeight.W_500),
            ]),
            bgcolor=color,
            duration=3500,
        )
        self.page.snack_bar.open = True
        self.page.update()

    # ── CSV export ────────────────────────────────────────────────────────────

    def _export_csv(self, filepath: str):
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Species", "Wood (kg)", "Bark (kg)", "Branch (kg)",
                              "Foliage (kg)", "Total (kg)",
                              "Wood %", "Bark %", "Branch %", "Foliage %"])
            for s in self.species_data:
                total = sum(s.get(k, 0) for k in _STACK_ORDER)
                def pct(v): return f"{v/total*100:.1f}" if total > 0 else "0.0"
                writer.writerow([
                    s["species_code"],
                    f"{s.get('Wood',    0):.4f}",
                    f"{s.get('Bark',    0):.4f}",
                    f"{s.get('Branch',  0):.4f}",
                    f"{s.get('Foliage', 0):.4f}",
                    f"{total:.4f}",
                    pct(s.get("Wood",    0)),
                    pct(s.get("Bark",    0)),
                    pct(s.get("Branch",  0)),
                    pct(s.get("Foliage", 0)),
                ])

    # ── PNG export ────────────────────────────────────────────────────────────

    def _render_chart_to_png(self, filepath: str):
        labels = [s["species_code"] for s in self.species_data]
        x      = np.arange(len(labels))
        is_dark = self._is_dark
        fig_bg = "#1A1A1A" if is_dark else "#FFFFFF"
        ax_bg  = "#111111" if is_dark else "#F8FAFC"
        txt    = "#F5F5F5" if is_dark else "#0F172A"
        grid_c = "#2E2E2E" if is_dark else "#E2E8F0"

        fig, ax = plt.subplots(figsize=(max(10, len(labels) * 0.85), 6))
        fig.patch.set_facecolor(fig_bg)
        ax.set_facecolor(ax_bg)

        bottoms = np.zeros(len(labels))
        for component in _STACK_ORDER:
            vals = np.array([s.get(component, 0) for s in self.species_data], dtype=float)
            ax.bar(x, vals, 0.52, bottom=bottoms, label=component,
                   color=_COMPONENT_COLORS[component], edgecolor=fig_bg, linewidth=0.8)
            bottoms += vals

        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9, color=txt)
        ax.set_ylabel("Biomass (KG)", fontsize=11, fontweight="bold", color=txt)
        ax.set_xlabel("Species",      fontsize=11, fontweight="bold", color=txt)
        ax.set_title("Biomass by Species Components",
                     fontsize=14, fontweight="bold", color=txt, pad=14)
        ax.set_ylim(0, self._calculate_max_y())
        ax.tick_params(colors=txt)
        for spine in ax.spines.values():
            spine.set_edgecolor(grid_c)
        ax.yaxis.grid(True, linestyle="--", linewidth=0.6, color=grid_c, alpha=0.8)
        ax.set_axisbelow(True)
        handles = [mpatches.Patch(color=_COMPONENT_COLORS[c], label=c) for c in _STACK_ORDER]
        legend  = ax.legend(handles=handles, title="Components", loc="upper right",
                            fontsize=9, title_fontsize=9,
                            facecolor=fig_bg, edgecolor=grid_c, labelcolor=txt)
        legend.get_title().set_color(txt)
        plt.tight_layout()
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        fig.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return filepath

    def _on_close(self, e):
        self.page.overlay.pop()
        self.page.update()

    # ── Sub-components ────────────────────────────────────────────────────────

    def _build_legend(self) -> ft.Control:
        items = [
            ft.Row([
                ft.Container(width=10, height=10, bgcolor=_COMPONENT_COLORS[c],
                             border_radius=ft.border_radius.all(2)),
                ft.Text(c, size=12, color=self._text_secondary(),
                        weight=ft.FontWeight.W_500),
            ], spacing=6)
            for c in _STACK_ORDER
        ]
        return ft.Container(
            content=ft.Column([
                ft.Text("COMPONENTS  ·  BOTTOM → TOP", size=10,
                        weight=ft.FontWeight.W_700, color=self._text_secondary()),
                ft.Row(items, spacing=20, wrap=True),
            ], spacing=8),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=self._surface_alt(),
            border=ft.border.all(1, self._border_color()),
            border_radius=ft.border_radius.all(10),
        )

    def _build_summary_table(self) -> ft.Control:
        def pct(val, total):
            return f"{val/total*100:.1f}%" if total > 0 else "—"

        def hcell(text, color):
            return ft.DataColumn(
                ft.Text(text, size=11, weight=ft.FontWeight.W_700, color=color)
            )

        table = ft.DataTable(
            columns=[
                hcell("SPECIES",  self._text_primary()),
                hcell("WOOD",     _WOOD_COLOR),
                hcell("BARK",     _BARK_COLOR),
                hcell("BRANCH",   _BRANCH_COLOR),
                hcell("FOLIAGE",  _FOLIAGE_COLOR),
                hcell("TOTAL kg", self._text_primary()),
            ],
            column_spacing=18,
            horizontal_margin=12,
            heading_row_height=38,
            divider_thickness=0,
            data_row_min_height=34,
            data_row_max_height=34,
            heading_row_color=self._surface_alt(),
        )

        for i, s in enumerate(self.species_data):
            total  = sum(s.get(k, 0) for k in _STACK_ORDER)
            row_bg = ft.Colors.with_opacity(
                0.04 if i % 2 == 0 else 0.0, ft.Colors.WHITE
            )
            table.rows.append(ft.DataRow(
                color=row_bg,
                cells=[
                    ft.DataCell(ft.Text(s["species_code"], size=12,
                                        weight=ft.FontWeight.W_600,
                                        color=self._text_primary())),
                    ft.DataCell(ft.Text(pct(s.get("Wood",    0), total), size=11, color=_WOOD_COLOR)),
                    ft.DataCell(ft.Text(pct(s.get("Bark",    0), total), size=11, color=_BARK_COLOR)),
                    ft.DataCell(ft.Text(pct(s.get("Branch",  0), total), size=11, color=_BRANCH_COLOR)),
                    ft.DataCell(ft.Text(pct(s.get("Foliage", 0), total), size=11, color=_FOLIAGE_COLOR)),
                    ft.DataCell(ft.Text(f"{total:.1f}", size=12,
                                        weight=ft.FontWeight.W_600,
                                        color=self._text_primary())),
                ],
            ))

       

        return ft.Container(
            ref=self.summary_table_ref,
            content=ft.Column([
                ft.Row([
                    ft.Text("COMPONENT BREAKDOWN", size=10,
                            weight=ft.FontWeight.W_700,
                            color=self._text_secondary()),
                    ft.Container(expand=True),
                 
                ]),
                ft.Container(
                    content=ft.Column(
                        [table], scroll=ft.ScrollMode.ADAPTIVE, height=160,
                    ),
                    border=ft.border.all(1, self._border_color()),
                    border_radius=ft.border_radius.all(8),
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
            ], spacing=10),
        )

    def _build_bar_chart(self):
        flet_colors = {
            "Wood":    "#F59E0B",
            "Bark":    "#92400E",
            "Branch":  "#FB923C",
            "Foliage": "#22C55E",
        }
        bar_groups = []
        for i, s in enumerate(self.species_data):
            stacked, cum = [], 0
            for comp in _STACK_ORDER:
                val = s.get(comp, 0)
                stacked.append(ft.BarChartRodStackItem(
                    from_y=cum, to_y=cum + val,
                    color=flet_colors[comp],
                    border_side=ft.BorderSide(
                        width=0.5,
                        color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE),
                    ),
                ))
                cum += val
            bar_groups.append(ft.BarChartGroup(
                x=i,
                bar_rods=[ft.BarChartRod(
                    from_y=0, to_y=cum, width=18,
                    border_radius=ft.border_radius.only(top_left=4, top_right=4),
                    rod_stack_items=stacked,
                )],
            ))

        chart_width = max(820, len(self.species_data) * 50)
        chart = ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(0, ft.Colors.TRANSPARENT),
            bgcolor=ft.Colors.TRANSPARENT,
            left_axis=ft.ChartAxis(
                title=ft.Text("Biomass (KG)", size=14, weight=ft.FontWeight.W_700,
                              color=self._text_primary()),
                labels_size=72, show_labels=True,
            ),
            bottom_axis=ft.ChartAxis(
                title=ft.Text("Species", size=14, weight=ft.FontWeight.W_700,
                              color=self._text_primary()),
                labels=[
                    ft.ChartAxisLabel(
                        value=i,
                        label=ft.Container(
                            content=ft.Text(
                                s["species_code"],
                                size=10,
                                weight=ft.FontWeight.W_500,
                                color=self._text_primary(),
                                text_align=ft.TextAlign.RIGHT,
                                max_lines=3,
                                overflow=ft.TextOverflow.VISIBLE,
                            ),
                            padding=ft.padding.only(top=4),
                            alignment=ft.alignment.top_right,
                            width=55,
                            rotate=ft.Rotate(
                                angle=-0.6,
                                alignment=ft.alignment.top_right,
                            ),
                        ),
                    )
                    for i, s in enumerate(self.species_data)
                ],
                labels_size=90, show_labels=True,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=self._grid_color(), width=1, dash_pattern=[4, 6],
            ),
            max_y=self._calculate_max_y(),
            min_y=0,
            interactive=True,
            expand=True,
            height=400,
            groups_space=36,
        )

        return ft.Container(
            bgcolor=self._chart_bg(),
            border=ft.border.all(1, self._border_color()),
            border_radius=ft.border_radius.all(10),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Column(
                [ft.Container(content=chart, padding=ft.padding.only(left=16, right=16, top=16, bottom=32), width=chart_width)],
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            width=1020,
            height=460,
        )

    def _make_close_btn(self):
        """Close button that turns red on hover."""
        btn = ft.Container(
            content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=16, color="#FFFFFF"),
            on_click=self._on_close,
            bgcolor=ft.Colors.with_opacity(
                0.15, ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK
            ),
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.all(8),
            ink=True,
            tooltip="Close",
            animate=ft.Animation(150, ft.AnimationCurve.LINEAR),
        )

        def on_hover(e):
            btn.bgcolor = "#DC2626" if e.data == "true" else ft.Colors.with_opacity(
                0.15, ft.Colors.WHITE if self._is_dark else ft.Colors.BLACK
            )
            btn.update()

        btn.on_hover = on_hover
        return btn

    # ── Main build ────────────────────────────────────────────────────────────

    def build(self):
        self._close_btn = self._make_close_btn()
        # Confirmation banner
        confirmation = ft.Container(
            ref=self.confirmation_ref,
            content=ft.Row(spacing=6),
            bgcolor=ft.Colors.with_opacity(0.10, "#16A34A"),
            border=ft.border.all(1, ft.Colors.with_opacity(0.25, "#16A34A")),
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            visible=False,
            opacity=0,
            animate_opacity=300,
        )

        # ── Header ──────────────────────────────────────────────────────────
        def _action_btn(label, icon, on_click, bgcolor, tooltip):
            return ft.Container(
                content=ft.Row([
                    ft.Icon(icon, size=14, color="#FFFFFF"),
                    ft.Text(label, size=12, color="#FFFFFF",
                            weight=ft.FontWeight.W_600),
                ], spacing=6, tight=True),
                on_click=on_click,
                bgcolor=bgcolor,
                border_radius=ft.border_radius.all(8),
                padding=ft.padding.symmetric(horizontal=14, vertical=8),
                ink=True,
                tooltip=tooltip,
            )

        header = ft.Row([
            ft.Column([
                ft.Text("Biomass Analysis", size=20, weight=ft.FontWeight.W_800,
                        color=self._text_primary()),
                ft.Text(
                    f"{len(self.species_data)} species · stacked by component",
                    size=12, color=self._text_secondary(),
                ),
            ], spacing=2, expand=True),

            # Export PNG
            _action_btn("Export PNG", ft.Icons.IMAGE_ROUNDED,
                        self._open_png_save_dialog, "#2563EB",
                        "Save chart as PNG"),
            ft.Container(width=6),
            # Export CSV (header shortcut — also available inside table section)
            _action_btn("Export CSV", ft.Icons.TABLE_CHART_ROUNDED,
                        self._open_csv_save_dialog, "#16A34A",
                        "Save table data as CSV"),
            ft.Container(width=6),
            # Close — turns red on hover
            self._close_btn,
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)

        divider = ft.Container(height=1, bgcolor=self._border_color(),
                               margin=ft.margin.symmetric(vertical=4))

        # Fixed header section (non-scrollable)
        fixed_header = ft.Container(
            content=ft.Column([
                header,
                divider,
            ], spacing=16),
            padding=ft.padding.only(left=28, right=28, top=28, bottom=0),
            bgcolor=self._surface(),
        )

        # Scrollable body below header
        scrollable_body = ft.Container(
            content=ft.Column([
                self._build_bar_chart(),
                confirmation,
                self._build_legend(),
                self._build_summary_table(),
                ft.Container(height=12),
            ], spacing=16, scroll=ft.ScrollMode.ADAPTIVE),
            padding=ft.padding.only(left=28, right=28, bottom=28, top=16),
            expand=True,
            bgcolor=self._surface(),
        )

        card = ft.Card(
            ref=self.card_ref,
            elevation=0,
            surface_tint_color=ft.Colors.TRANSPARENT,
            color=self._surface(),
            content=ft.Container(
                content=ft.Column([
                    fixed_header,
                    scrollable_body,
                ], spacing=0, expand=True),
                width=1080,
                border_radius=ft.border_radius.all(16),
                bgcolor=self._surface(),
                border=ft.border.all(1, self._border_color()),
            ),
        )

        return ft.Container(
            content=ft.Container(
                content=card,
                padding=ft.padding.all(24),
                alignment=ft.alignment.center,
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.65, ft.Colors.BLACK),
            expand=True,
        )