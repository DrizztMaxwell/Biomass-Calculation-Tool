# widgets/Connect_To_Database_Dialog_Widget.py

import pyodbc
import flet as ft
import json
import os
from datetime import datetime
from data.database_config import get_mssql_data_path

from widgets.Display_Error_Dialog import Display_Error_Dialog
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog
from widgets.Loading_Spinner_Widget import Loading_Spinner_Widget as Loading


class Connect_To_Database_Dialog_Widget:
    def __init__(self, page: ft.Page, detected_servers: list[str] | None = None):
        self.page = page
        self.detected_servers = detected_servers or []
        self.on_connect_callback = None  # Callback for controller to handle connect

        self.history_file = "connection_history.json"
        self.connection_history: list[dict] = []
        self.max_history_items = 10

        # Track connection status
        self.connection = None
        self.cursor = None
        self.status = False

        self.load_connection_history()
        self._build_ui()
        self._prefill_database_name_from_path()

    # -------------------------
    # UI BUILDING
    # -------------------------
    def _build_ui(self):
        self.server_input = ft.TextField(
            label="Server Name",
            hint_text="e.g., COMPUTER\\SQLEXPRESS",
            prefix_icon=ft.Icons.COMPUTER,
            filled=True,
            capitalization=ft.TextCapitalization.CHARACTERS,
        )

        if len(self.detected_servers) == 1:
            self.server_input.value = self.detected_servers[0]

        self.db_input = ft.TextField(
            label="Database Name",
            prefix_icon=ft.Icons.TABLE_CHART,
            filled=True,
        )

        self.history_dropdown = ft.Dropdown(
            label="Recent Connections",
            prefix_icon=ft.Icons.HISTORY,
            options=[],
            on_change=self.on_history_selected,
            filled=True,
        )

        self._initialize_dropdown_options()

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Database Connection", weight=ft.FontWeight.BOLD),
            content=ft.Column(
                [
                    self.history_dropdown,
                    ft.Text("OR", size=12),
                    self.server_input,
                    self.db_input,
                ],
                spacing=12,
                width=450,
            ),
            actions=[
                ft.TextButton("Clear History", on_click=self.clear_history),
                ft.TextButton("Cancel", on_click=self.handle_close),
                ft.ElevatedButton("Connect", on_click=self.handle_connect),
            ],
        )

    # -------------------------
    # PREFILL DATABASE NAME FROM MSSQL PATH
    # -------------------------
    def _prefill_database_name_from_path(self):
        """Auto-fill Database Name if a valid MSSQL data path exists"""
        mssql_path = get_mssql_data_path()
        if mssql_path and os.path.exists(mssql_path):
            # Use folder name of DATA folder as default database name
            db_name = os.path.basename(mssql_path)
            self.db_input.value = db_name
            self.db_input.update()

    # -------------------------
    # HISTORY MANAGEMENT
    # -------------------------
    def load_connection_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    self.connection_history = json.load(f)
            except Exception:
                self.connection_history = []

    def save_connection_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.connection_history, f, indent=2)

    def add_to_history(self, server: str, database: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.connection_history = [
            c for c in self.connection_history
            if not (c["server"] == server and c["database"] == database)
        ]
        self.connection_history.insert(0, {
            "server": server,
            "database": database,
            "last_used": now,
        })
        self.connection_history = self.connection_history[:self.max_history_items]
        self.save_connection_history()

    def _initialize_dropdown_options(self):
        self.history_dropdown.options.clear()
        if not self.connection_history:
            self.history_dropdown.options.append(
                ft.dropdown.Option("empty", "No history", disabled=True)
            )
            return
        for i, conn in enumerate(self.connection_history):
            self.history_dropdown.options.append(
                ft.dropdown.Option(
                    key=str(i),
                    text=f"{conn['server']} | {conn['database']} ({conn['last_used']})",
                )
            )

    def on_history_selected(self, e):
        if e.control.value and e.control.value != "empty":
            conn = self.connection_history[int(e.control.value)]
            self.server_input.value = conn["server"]
            self.db_input.value = conn["database"]
            self.server_input.update()
            self.db_input.update()

    def clear_history(self, e):
        self.connection_history.clear()
        self.save_connection_history()
        self._initialize_dropdown_options()
        self.history_dropdown.update()

    # -------------------------
    # DIALOG CONTROL
    # -------------------------
    def open_dialog(self):
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def handle_close(self, e):
        self.dialog.open = False
        self.page.update()

    # -------------------------
    # CONNECT HANDLER
    # -------------------------
    async def handle_connect(self, e):
        """Validate inputs and call controller callback"""
        server = self.server_input.value.strip()
        database = self.db_input.value.strip()

        if not server or not database:
            Display_Error_Dialog(
                self.page,
                "Missing Information",
                "Server and database are required."
            ).show()
            return

        # Call controller callback
        if self.on_connect_callback:
            await self.on_connect_callback(server, database)

        # Add to history and close dialog
        self.add_to_history(server, database)
        self.handle_close(e)
