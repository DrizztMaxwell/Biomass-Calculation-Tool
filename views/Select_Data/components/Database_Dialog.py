import os
import flet as ft
from data.database_config import get_mssql_data_path
from widgets.Display_Error_Dialog import Display_Error_Dialog
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog


class Database_Dialog:
    """Component for database connection dialog — styled to match app look & feel."""

    def __init__(self, page: ft.Page, history_manager, on_connect_callback):
        self.page = page
        self.history_manager = history_manager
        self.on_connect_callback = on_connect_callback

    # ── Theme helpers ─────────────────────────────────────────────────────────

    @property
    def _is_dark(self) -> bool:
        return self.page.theme_mode == ft.ThemeMode.DARK

    def _bg(self):
        return "#1A1A1A" if self._is_dark else "#FFFFFF"

    def _surface(self):
        return "#222222" if self._is_dark else "#F8FAFC"

    def _border(self):
        return "#2E2E2E" if self._is_dark else "#E2E8F0"

    def _text_primary(self):
        return "#F5F5F5" if self._is_dark else "#0F172A"

    def _text_secondary(self):
        return "#888888" if self._is_dark else "#64748B"

    def _input_bg(self):
        return "#2A2A2A" if self._is_dark else "#FFFFFF"

    # ── Public ────────────────────────────────────────────────────────────────

    def open(self):
        detected_servers = self._detect_sql_servers()
        server_input     = self._create_server_input(detected_servers)
        db_input         = self._create_database_input()
        history_dropdown = self._create_history_dropdown(server_input, db_input)
        dialog           = self._create_dialog(server_input, db_input, history_dropdown)

        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)
        self.page.update()

    # ── Detection ─────────────────────────────────────────────────────────────

    def _detect_sql_servers(self):
        detected_path    = get_mssql_data_path()
        detected_servers = []
        if detected_path:
            folder_name = os.path.basename(os.path.dirname(os.path.dirname(detected_path)))
            if "SQLEXPRESS" in folder_name.upper():
                computer_name = os.environ.get("COMPUTERNAME", "LOCALHOST")
                detected_servers.append(f"{computer_name}\\SQLEXPRESS")
        return detected_servers

    # ── Input fields ──────────────────────────────────────────────────────────

    def _create_server_input(self, detected_servers):
        return ft.TextField(
            label="Server Name",
            value=detected_servers[0] if len(detected_servers) == 1 else "",
            hint_text="e.g., COMPUTER\\SQLEXPRESS",
            prefix_icon=ft.Icons.COMPUTER,
            bgcolor=self._input_bg(),
            filled=True,
            color=self._text_primary(),
            label_style=ft.TextStyle(color=self._text_secondary(), size=13),
            hint_style=ft.TextStyle(color=self._text_secondary()),
            border_color=self._border(),
            focused_border_color="#2563EB",
            cursor_color=self._text_primary(),
            capitalization=ft.TextCapitalization.CHARACTERS,
            border_radius=ft.border_radius.all(8),
        )

    def _create_database_input(self):
        return ft.TextField(
            label="Database Name",
            value="",
            prefix_icon=ft.Icons.TABLE_CHART,
            filled=True,
            bgcolor=self._input_bg(),
            color=self._text_primary(),
            label_style=ft.TextStyle(color=self._text_secondary(), size=13),
            border_color=self._border(),
            focused_border_color="#2563EB",
            cursor_color=self._text_primary(),
            border_radius=ft.border_radius.all(8),
        )

    def _create_history_dropdown(self, server_input, db_input):
        history = self.history_manager.get_history()
        options = (
            [
                ft.dropdown.Option(
                    key=str(i),
                    text=f"{c['server']}  ·  {c['database']}  ({c['last_used']})",
                )
                for i, c in enumerate(history)
            ]
            if history
            else [ft.dropdown.Option("empty", "No saved connections", disabled=True)]
        )
        return ft.Dropdown(
            label="Recent Connections",
            prefix_icon=ft.Icons.HISTORY,
            options=options,
            on_change=lambda e: self._on_history_selected(e, server_input, db_input),
            bgcolor=self._input_bg(),
            color=self._text_primary(),
            label_style=ft.TextStyle(color=self._text_secondary(), size=13),
            border_color=self._border(),
            focused_border_color="#2563EB",
            border_radius=ft.border_radius.all(8),
            expand=True,
        )

    def _on_history_selected(self, e, server_input, db_input):
        if e.control.value != "empty":
            history = self.history_manager.get_history()
            conn = history[int(e.control.value)]
            server_input.value = conn["server"]
            db_input.value     = conn["database"]
            server_input.update()
            db_input.update()

    # ── Dialog assembly ───────────────────────────────────────────────────────

    def _create_dialog(self, server_input, db_input, history_dropdown):
        dialog = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=self._bg(),
            shadow_color=ft.Colors.with_opacity(0.18, ft.Colors.BLACK),
            elevation=12,
            title=self._build_title(),
            content=self._build_content(server_input, db_input, history_dropdown),
            actions=[self._build_actions(server_input, db_input, history_dropdown)],
            actions_padding=ft.padding.all(0),
            title_padding=ft.padding.all(0),
            content_padding=ft.padding.all(0),
        )
        self.current_dialog = dialog
        return dialog

    # ── Title ─────────────────────────────────────────────────────────────────

    def _build_title(self) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.STORAGE_ROUNDED, color="#FFFFFF", size=20),
                        width=42, height=42,
                        bgcolor="#2563EB",
                        border_radius=ft.border_radius.all(10),
                        alignment=ft.alignment.center,
                    ),
                    ft.Column([
                        ft.Text(
                            "Database Connection",
                            weight=ft.FontWeight.W_700,
                            size=18,
                            color=self._text_primary(),
                        ),
                        ft.Text(
                            "Connect to a SQL Server instance",
                            size=12,
                            color=self._text_secondary(),
                        ),
                    ], spacing=2, expand=True),
                ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),

                ft.Container(
                    height=1,
                    bgcolor=self._border(),
                    margin=ft.margin.only(top=18),
                ),
            ]),
            padding=ft.padding.only(left=24, right=24, top=22, bottom=0),
        )

    # ── Section card ──────────────────────────────────────────────────────────

    def _section_card(self, icon, icon_color, icon_bg, label, children) -> ft.Container:
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, size=15, color=icon_color),
                        bgcolor=icon_bg,
                        border_radius=ft.border_radius.all(7),
                        padding=ft.padding.all(6),
                        width=30, height=30,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(
                        label,
                        size=13,
                        weight=ft.FontWeight.W_600,
                        color=self._text_primary(),
                    ),
                ], spacing=10),
                ft.Container(height=14),
                *children,
            ], spacing=0),
            padding=ft.padding.all(18),
            bgcolor=self._surface(),
            border=ft.border.all(1, self._border()),
            border_radius=ft.border_radius.all(10),
        )

    # ── Content ───────────────────────────────────────────────────────────────

    def _build_content(self, server_input, db_input, history_dropdown) -> ft.Container:
        recent_card = self._section_card(
            ft.Icons.HISTORY,
            "#2563EB",
            ft.Colors.with_opacity(0.12, "#2563EB"),
            "Recent Connections",
            [history_dropdown],
        )

        manual_card = self._section_card(
            ft.Icons.EDIT_OUTLINED,
            "#16A34A",
            ft.Colors.with_opacity(0.12, "#16A34A"),
            "Manual Entry",
            [
                server_input,
                ft.Container(height=10),
                db_input,
                ft.Container(height=8),
                ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=12, color=self._text_secondary()),
                    ft.Text(
                        "Ensure SQL Server is running and accessible.",
                        size=11,
                        color=self._text_secondary(),
                    ),
                ], spacing=5),
            ],
        )

        or_divider = ft.Row([
            ft.Container(expand=True, height=1, bgcolor=self._border()),
            ft.Container(
                content=ft.Text("OR", size=10, weight=ft.FontWeight.W_700,
                                color=self._text_secondary()),
                padding=ft.padding.symmetric(horizontal=12),
            ),
            ft.Container(expand=True, height=1, bgcolor=self._border()),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)

        return ft.Container(
            content=ft.Column(
                [recent_card, or_divider, manual_card],
                spacing=14,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=490,
            height=420,
            padding=ft.padding.only(left=24, right=24, top=20, bottom=0),
        )

    # ── Buttons ───────────────────────────────────────────────────────────────

    def _outline_button(self, icon, label, color, on_click, tooltip="") -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=14, color=color),
                ft.Text(label, size=12, weight=ft.FontWeight.W_500, color=color),
            ], spacing=7),
            on_click=on_click,
            bgcolor=ft.Colors.with_opacity(0.07, color),
            border=ft.border.all(1, ft.Colors.with_opacity(0.25, color)),
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.symmetric(horizontal=14, vertical=9),
            ink=True,
            tooltip=tooltip,
        )

    def _solid_button(self, icon, label, bgcolor, on_click) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=15, color="#FFFFFF"),
                ft.Text(label, size=13, weight=ft.FontWeight.W_600, color="#FFFFFF"),
            ], spacing=8),
            on_click=on_click,
            bgcolor=bgcolor,
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            ink=True,
        )

    def _build_actions(self, server_input, db_input, history_dropdown) -> ft.Container:
        return ft.Container(
            content=ft.Row([
                self._outline_button(
                    ft.Icons.DELETE_SWEEP_ROUNDED,
                    "Clear History",
                    "#DC2626",
                    lambda e: self._clear_history(history_dropdown),
                    tooltip="Remove all connection history",
                ),
                ft.Container(expand=True),
                self._outline_button(
                    ft.Icons.CLOSE_ROUNDED,
                    "Cancel",
                    self._text_secondary(),
                    lambda e: self._close_dialog(),
                ),
                ft.Container(width=10),
                # Green — matches the app's "Create Species" primary action button
                self._solid_button(
                    ft.Icons.CLOUD_DONE_ROUNDED,
                    "Connect",
                    "#16A34A",
                    lambda e: self._submit_connection(server_input, db_input),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(left=24, right=24, top=16, bottom=20),
            border=ft.border.only(top=ft.border.BorderSide(1, self._border())),
            margin=ft.margin.only(top=18),
        )

    # ── Handlers ──────────────────────────────────────────────────────────────

    def _close_dialog(self):
        self.current_dialog.open = False
        self.page.update()

    def _clear_history(self, history_dropdown):
        confirm_dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor=self._bg(),
            title=ft.Text("Clear History", weight=ft.FontWeight.W_700,
                          color=self._text_primary(), size=16),
            content=ft.Text(
                "Are you sure you want to clear all connection history?",
                color=self._text_secondary(), size=13,
            ),
            actions=[
                ft.Container(
                    content=ft.Row([
                        self._outline_button(
                            ft.Icons.CLOSE_ROUNDED, "Cancel",
                            self._text_secondary(),
                            lambda e: self.page.close(confirm_dialog),
                        ),
                        ft.Container(width=8),
                        self._solid_button(
                            ft.Icons.DELETE_SWEEP_ROUNDED, "Clear",
                            "#DC2626",
                            lambda e: self._confirm_clear_history(history_dropdown, confirm_dialog),
                        ),
                    ], alignment=ft.MainAxisAlignment.END),
                    padding=ft.padding.only(right=4, bottom=8),
                )
            ],
        )
        self.page.open(confirm_dialog)
        self.page.update()

    def _confirm_clear_history(self, history_dropdown, confirm_dialog):
        self.history_manager.clear_history()
        history_dropdown.options = [
            ft.dropdown.Option("empty", "No saved connections", disabled=True)
        ]
        history_dropdown.update()
        self.page.close(confirm_dialog)
        Custom_Alert_Dialog(
            self.page,
            title_icon=ft.Icons.HISTORY,
            title_icon_color=ft.Colors.PRIMARY,
            title_color=ft.Colors.PRIMARY,
            title="History Cleared",
            message="Connection history has been cleared successfully.",
        ).show()

    def _submit_connection(self, server_input, db_input):
        server   = server_input.value.strip()
        database = db_input.value.strip()

        if not server or not database:
            Display_Error_Dialog(
                self.page,
                "Missing Information",
                "Please fill in both Server and Database fields.",
            ).show()
            return

        self.history_manager.add_connection(server, database)
        self._close_dialog()

        if self.on_connect_callback:
            self.on_connect_callback(server, database)