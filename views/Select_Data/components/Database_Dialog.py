import os
import flet as ft
from data.database_config import get_mssql_data_path
from widgets.Display_Error_Dialog import Display_Error_Dialog
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog

class Database_Dialog:
    """Component for database connection dialog"""
    
    def __init__(self, page: ft.Page, history_manager, on_connect_callback):
        self.page = page
        self.history_manager = history_manager
        self.on_connect_callback = on_connect_callback
    
    def open(self):
        """Open the database connection dialog"""
        # Detect SQL Server instances
        detected_servers = self._detect_sql_servers()
        
        # Create input fields
        server_input = self._create_server_input(detected_servers)
        db_input = self._create_database_input()
        
        # Create history dropdown
        history_dropdown = self._create_history_dropdown(server_input, db_input)
        
        # Create dialog
        dialog = self._create_dialog(server_input, db_input, history_dropdown)
        
        # Open dialog
        self.page.dialog = dialog
        dialog.open = True
        self.page.open(dialog)
        self.page.update()
    
    def _detect_sql_servers(self):
        """Detect SQL Server instances on the machine"""
        detected_path = get_mssql_data_path()
        detected_servers = []
        
        if detected_path:
            folder_name = os.path.basename(os.path.dirname(os.path.dirname(detected_path)))
            if "SQLEXPRESS" in folder_name.upper():
                computer_name = os.environ.get('COMPUTERNAME', 'LOCALHOST')
                detected_servers.append(f"{computer_name}\\SQLEXPRESS")
        
        return detected_servers
    
    def _create_server_input(self, detected_servers):
        """Create server name input field"""
        return ft.TextField(
            label="Server Name",
            value=detected_servers[0] if len(detected_servers) == 1 else "",
            hint_text="e.g., COMPUTER\\SQLEXPRESS",
            prefix_icon=ft.Icons.COMPUTER,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            filled=True,
            color=ft.Colors.PRIMARY,
            capitalization=ft.TextCapitalization.CHARACTERS,
        )
    
    def _create_database_input(self):
        """Create database name input field"""
        return ft.TextField(
            label="Database Name",
            value="",
            prefix_icon=ft.Icons.TABLE_CHART,
            filled=True,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            color=ft.Colors.PRIMARY,
        )
    
    def _create_history_dropdown(self, server_input, db_input):
        """Create connection history dropdown"""
        history = self.history_manager.get_history()
        
        options = [
            ft.dropdown.Option(
                key=str(i), 
                text=f"{c['server']} | {c['database']} ({c['last_used']})"
            )
            for i, c in enumerate(history)
        ] if history else [ft.dropdown.Option("empty", "No history", disabled=True)]
        
        return ft.Dropdown(
            label="Recent Connections",
            prefix_icon=ft.Icons.HISTORY,
            options=options,
            on_change=lambda e: self._on_history_selected(e, server_input, db_input),
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            color=ft.Colors.PRIMARY,
            expand=True,
        )
    
    def _on_history_selected(self, e, server_input, db_input):
        """Handle history selection"""
        if e.control.value != "empty":
            history = self.history_manager.get_history()
            conn = history[int(e.control.value)]
            server_input.value = conn["server"]
            db_input.value = conn["database"]
            server_input.update()
            db_input.update()
    
    def _create_dialog(self, server_input, db_input, history_dropdown):
        """Create the main dialog"""
        dialog = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.Colors.SECONDARY,
            shadow_color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
            elevation=10,
            title=self._create_dialog_title(),
            content=self._create_dialog_content(server_input, db_input, history_dropdown),
            actions=[
                self._create_dialog_actions(server_input, db_input, history_dropdown)
            ],
        )
        
        # Store dialog reference for callbacks
        self.current_dialog = dialog
        return dialog
    
    def _create_dialog_title(self):
        """Create dialog title section"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.CLOUD_QUEUE_ROUNDED,
                            color=ft.Colors.WHITE,
                            size=24
                        ),
                        width=44,
                        height=44,
                        bgcolor=ft.Colors.BLUE_600,
                        border_radius=ft.border_radius.all(12),
                        alignment=ft.alignment.center,
                        shadow=ft.BoxShadow(
                            blur_radius=12,
                            color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_600),
                            offset=ft.Offset(0, 2),
                        ),
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                "Database Connection", 
                                weight=ft.FontWeight.W_700, 
                                size=20,
                                color=ft.Colors.PRIMARY,
                            ),
                            ft.Text(
                                "Establish secure connection to SQL Server", 
                                size=13, 
                                color=ft.Colors.PRIMARY,
                            ),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=16,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.only(bottom=4, top=8, left=24, right=24),
        )
    
    def _create_dialog_content(self, server_input, db_input, history_dropdown):
        """Create dialog content section"""
        return ft.Container(
            content=ft.Column(
                [
                    # Recent Connections Card
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.HISTORY, size=18, color=ft.Colors.PRIMARY),
                                        ft.Text("Recent Connections", color=ft.Colors.PRIMARY, size=14, weight=ft.FontWeight.W_600),
                                    ],
                                    spacing=10,
                                ),
                                ft.Container(height=12),
                                history_dropdown,
                            ],
                            spacing=0,
                        ),
                        padding=ft.padding.all(20),
                        bgcolor=ft.Colors.SECONDARY_CONTAINER,
                        border_radius=ft.border_radius.all(12),
                        border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                    ),
                    
                    ft.Container(height=20),
                    
                    # OR Divider
                    ft.Row(
                        [
                            ft.Container(expand=True, height=1, bgcolor=ft.Colors.PRIMARY),
                            ft.Container(
                                content=ft.Text("OR", size=12, weight=ft.FontWeight.W_600, color=ft.Colors.PRIMARY),
                                padding=ft.padding.symmetric(horizontal=16),
                                bgcolor=ft.Colors.WHITE,
                            ),
                            ft.Container(expand=True, height=1, bgcolor=ft.Colors.PRIMARY),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    
                    ft.Container(height=20),
                    
                    # Manual Connection Card
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.EDIT_SHARP, size=18, color=ft.Colors.PRIMARY),
                                        ft.Text("Manual Connection", color=ft.Colors.PRIMARY, size=14, weight=ft.FontWeight.W_600),
                                    ],
                                    spacing=10,
                                ),
                                ft.Container(height=16),
                                server_input,
                                ft.Container(height=12),
                                db_input,
                                ft.Container(height=8),
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.INFO_OUTLINED, size=14, color=ft.Colors.PRIMARY),
                                        ft.Text("Ensure SQL Server is running and accessible.", size=12, color=ft.Colors.PRIMARY),
                                    ],
                                    spacing=6,
                                ),
                            ],
                            spacing=0,
                        ),
                        padding=ft.padding.all(20),
                        bgcolor=ft.Colors.SECONDARY_CONTAINER,
                        border_radius=ft.border_radius.all(12),
                        border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                    ),
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=480,
            height=420,
            padding=ft.padding.symmetric(horizontal=24),
        )
    
    def _create_dialog_actions(self, server_input, db_input, history_dropdown):
        """Create dialog action buttons"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(expand=True),
                    # Clear History Button
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.DELETE_SWEEP_ROUNDED, size=18),
                                ft.Text("Clear History"),
                            ],
                            spacing=8,
                        ),
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.RED_600,
                            padding=ft.padding.symmetric(horizontal=20, vertical=12),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=2,
                            overlay_color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                        ),
                        on_click=lambda e: self._clear_history(history_dropdown),
                        tooltip="Remove all connection history",
                    ),
                    
                    ft.Container(width=12),
                    
                    # Cancel Button
                    ft.OutlinedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.CLOSE, size=18, color=ft.Colors.WHITE),
                                ft.Text("Cancel", color=ft.Colors.WHITE),
                            ],
                            spacing=8,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLACK87,
                            side=ft.border.BorderSide(1, ft.Colors.WHITE),
                            padding=ft.padding.symmetric(horizontal=24, vertical=12),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            overlay_color=ft.Colors.with_opacity(0.05, ft.Colors.BLUE_GREY_500),
                        ),
                        on_click=lambda e: self._close_dialog(),
                    ),
                    
                    ft.Container(width=12),
                    
                    # Connect Button
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.CLOUD_DONE_ROUNDED,
                                        size=20,
                                        color=ft.Colors.WHITE,
                                    ),
                                ),
                                ft.Text("Connect", weight=ft.FontWeight.W_600, size=14),
                            ],
                            spacing=10,
                        ),
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.TERTIARY,
                            padding=ft.padding.symmetric(horizontal=28, vertical=14),
                            shape=ft.RoundedRectangleBorder(radius=12),
                            elevation=3,
                            shadow_color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_600),
                            overlay_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                        ),
                        on_click=lambda e: self._submit_connection(server_input, db_input),
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            padding=ft.padding.symmetric(vertical=20, horizontal=24),
            border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_100)),
        )
    
    def _close_dialog(self):
        """Close the dialog"""
        self.current_dialog.open = False
        self.page.update()
    
    def _clear_history(self, history_dropdown):
        """Clear connection history with confirmation"""
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Clear History"),
            content=ft.Text("Are you sure you want to clear the connection history?"),
            actions=[
                ft.ElevatedButton(
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE, 
                        bgcolor=ft.Colors.GREY_600
                    ), 
                    text="Cancel", 
                    on_click=lambda e: self.page.close(confirm_dialog)
                ),
                ft.ElevatedButton(
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE, 
                        bgcolor=ft.Colors.RED
                    ), 
                    text="Clear", 
                    on_click=lambda e: self._confirm_clear_history(history_dropdown, confirm_dialog)
                ),
            ],
        )
        self.page.open(confirm_dialog)
        self.page.update()
    
    def _confirm_clear_history(self, history_dropdown, confirm_dialog):
        """Confirm and execute history clearing"""
        self.history_manager.clear_history()
        history_dropdown.options = [ft.dropdown.Option("empty", "No history", disabled=True)]
        history_dropdown.update()
        self.page.close(confirm_dialog)
        Custom_Alert_Dialog(
            self.page, 
            title_icon=ft.Icons.HISTORY, 
            title_icon_color=ft.Colors.PRIMARY, 
            title_color=ft.Colors.PRIMARY, 
            title="History Cleared", 
            message="Connection history has been cleared successfully."
        ).show()
    
    def _submit_connection(self, server_input, db_input):
        """Submit connection details"""
        server = server_input.value.strip()
        database = db_input.value.strip()
        
        if not server or not database:
            Display_Error_Dialog(
                self.page, 
                "Missing Information", 
                "Server and database are required."
            ).show()
            return
        
        # Add to history
        self.history_manager.add_connection(server, database)
        
        # Close dialog
        self._close_dialog()
        
        # Notify callback
        if self.on_connect_callback:
            self.on_connect_callback(server, database)