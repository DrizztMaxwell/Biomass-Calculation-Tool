import pyodbc
import flet as ft
import json
import os
from datetime import datetime
from widgets.Display_Error_Dialog import Display_Error_Dialog
from widgets.Custom_Alert_Dialog import Custom_Alert_Dialog

class Connect_To_Database_Dialog_Widget:
    def __init__(self, page: ft.Page):
        self.page = page
        self.on_connect_callback = None  # Callback for connection result
        self.history_file = "connection_history.json"
        self.connection_history = []
        self.max_history_items = 5
        
        # Add this to track connection status
        self.connection = None
        self.cursor = None
        self.status = False
        
        # Load connection history
        self.load_connection_history()
        
        # Create UI components with consistent styling
        self.server_input = ft.TextField(
            label="Server Name",
            hint_text="e.g., OPS-PF4S0SKY\\SQLEXPRESS",
            prefix_icon=ft.Icons.COMPUTER,
            border_color=ft.Colors.BLUE_GREY_300,
            focused_border_color=ft.Colors.BLUE_700,
            filled=True,
            fill_color=ft.Colors.BLUE_GREY_50,
            text_size=14,
            height=48,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=14),
            border_radius=8,
            capitalization=ft.TextCapitalization.CHARACTERS,
        )
        
        self.db_input = ft.TextField(
            label="Database Name",
            hint_text="e.g., gyNFI_A",
            prefix_icon=ft.Icons.TABLE_CHART,
            border_color=ft.Colors.BLUE_GREY_300,
            focused_border_color=ft.Colors.BLUE_700,
            filled=True,
            fill_color=ft.Colors.BLUE_GREY_50,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=14),
            border_radius=8,
            capitalization=ft.TextCapitalization.CHARACTERS,
        )
        
        # Create history dropdown/datalist
        self.history_dropdown = ft.Dropdown(
            label="Recent Connections",
            hint_text="Select a previous connection",
            prefix_icon=ft.Icons.HISTORY_ROUNDED,
            options=[],
            filled=True,
            fill_color=ft.Colors.BLUE_GREY_50,
            border_color=ft.Colors.BLUE_GREY_300,
            focused_border_color=ft.Colors.BLUE_700,
            text_size=14,
            expand=True,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=8,
            on_change=self.on_history_selected,
            menu_height=200,
            autofocus=False,
            alignment=ft.alignment.center_left,
            dense=True,
        )
        
        # Initialize dropdown options WITHOUT calling update()
        self._initialize_dropdown_options()
        
        # Create a form for better structure
        form_column = ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Enter your SQL Server credentials to establish a secure connection.",
                        size=13,
                        color=ft.Colors.BLUE_GREY_600,
                        weight=ft.FontWeight.W_400,
                    ),
                    margin=ft.margin.only(bottom=8),
                ),
                ft.Container(
                    height=1,
                    bgcolor=ft.Colors.BLUE_GREY_100,
                    margin=ft.margin.symmetric(vertical=8),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Connection Details",
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.BLUE_GREY_800,
                            ),
                            ft.Container(height=16),
                            
                            # History section
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Icon(ft.Icons.HISTORY, size=18, color=ft.Colors.BLUE_GREY_600),
                                        ft.Text(
                                            "Connection History",
                                            size=13,
                                            weight=ft.FontWeight.W_500,
                                            color=ft.Colors.BLUE_GREY_700,
                                        ),
                                    ], spacing=8),
                                    self.history_dropdown,
                                ], spacing=8),
                                bgcolor=ft.Colors.BLUE_GREY_50,
                                padding=ft.padding.all(12),
                                border_radius=8,
                                border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                            ),
                            
                            ft.Container(height=8),
                            
                            # Or manual entry divider
                            ft.Row(
                                [
                                    ft.Container(width=20),
                                    ft.Text(
                                        "OR",
                                        size=12,
                                        weight=ft.FontWeight.W_500,
                                        color=ft.Colors.BLUE_GREY_500,
                                    ),
                                    ft.Container(width=20),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            
                            ft.Container(height=8),
                            
                            # Manual entry section
                            ft.Text(
                                "Manual Entry",
                                size=13,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.BLUE_GREY_700,
                            ),
                            ft.Container(height=12),
                            self.server_input,
                            ft.Container(height=12),
                            self.db_input,
                        ],
                        spacing=0,
                    ),
                ),
                ft.Container(height=8),
            ],
            spacing=0,
            tight=True,
        )
        
        # Create the dialog with professional styling
        self.dialog = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=12),
            title=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.CLOUD_QUEUE, color=ft.Colors.BLUE_700, size=24),
                        ft.Text(
                            "Database Connection",
                            size=18,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.BLUE_GREY_900,
                        ),
                    ],
                    spacing=12,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.only(bottom=8),
            ),
            content=ft.Container(
                content=form_column,
                width=500,
                padding=ft.padding.symmetric(horizontal=4, vertical=0),
            ),
            actions=[
                ft.Container(
                    content=ft.Row(
                        [
                            ft.TextButton(
                                "Add Test Data",
                                on_click=self.add_test_history,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.ORANGE_700,
                                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                                ),
                                icon=ft.Icons.DATA_USAGE,
                            ),
                            ft.TextButton(
                                "Clear History",
                                on_click=self.clear_history,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.BLUE_GREY_500,
                                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                                ),
                                icon=ft.Icons.DELETE_OUTLINE,
                            ),
                            ft.Container(width=8),
                            ft.TextButton(
                                "Cancel",
                                on_click=self.handle_close,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.BLUE_GREY_600,
                                    padding=ft.padding.symmetric(horizontal=20, vertical=12),
                                )
                            ),
                            ft.Container(width=8),
                            ft.ElevatedButton(
                                "Connect",
                                icon=ft.Icons.LOCK_OPEN_ROUNDED,
                                on_click=self.handle_connect,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLUE_700,
                                    color=ft.Colors.WHITE,
                                    padding=ft.padding.symmetric(horizontal=24, vertical=14),
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    elevation=1,
                                ),
                                height=44,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=0,
                    ),
                    padding=ft.padding.only(top=16),
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def _initialize_dropdown_options(self):
        """Initialize dropdown options without calling update()"""
        self.history_dropdown.options = []
        
        if self.connection_history:
            for i, conn in enumerate(self.connection_history):
                display_text = f"{conn['server']} | {conn['database']}"
                self.history_dropdown.options.append(
                    ft.dropdown.Option(
                        key=str(i),
                        text=display_text,
                        data=conn,
                    )
                )
        else:
            self.history_dropdown.options.append(
                ft.dropdown.Option(
                    key="empty",
                    text="No connection history",
                    disabled=True,
                )
            )
        
        # Set hint text based on whether there's history
        if self.connection_history:
            self.history_dropdown.hint_text = "Select a previous connection"
        else:
            self.history_dropdown.hint_text = "No previous connections"

    def load_connection_history(self):
        """Load connection history from JSON file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.connection_history = json.load(f)
            else:
                self.connection_history = []
        except Exception as e:
            print(f"Error loading connection history: {e}")
            self.connection_history = []

    def save_connection_history(self):
        """Save connection history to JSON file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.connection_history, f, indent=2)
        except Exception as e:
            print(f"Error saving connection history: {e}")
    
    def add_test_history(self, e=None):
        """Add some test history entries for demonstration"""
        test_connections = [
            {"server": "DESKTOP-EJ33BVS\\SQLEXPRESS", "database": "gyPSPPGP"},
            {"server": "LOCALHOST\\SQL2019", "database": "TestDB"},
            {"server": "SERVER01\\MSSQLSERVER", "database": "ProductionDB"},
            {"server": "DEV-SERVER\\SQLDEV", "database": "DevelopmentDB"},
            {"server": "REMOTE-SRV\\SQLEXPRESS", "database": "InventoryDB"}
        ]
        
        self.connection_history = []
        for conn in test_connections:
            self.connection_history.append({
                'server': conn['server'],
                'database': conn['database'],
                'timestamp': datetime.now().isoformat(),
                'last_used': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        
        self.save_connection_history()
        self._initialize_dropdown_options()
        
        # Show success message
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Test history added successfully!"),
            bgcolor=ft.Colors.GREEN_700
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def add_to_history(self, server, database):
        """Add a new connection to history"""
        # Remove duplicates
        self.connection_history = [conn for conn in self.connection_history 
                                  if not (conn['server'] == server and conn['database'] == database)]
        
        # Add new connection at the beginning
        new_connection = {
            'server': server,
            'database': database,
            'timestamp': datetime.now().isoformat(),
            'last_used': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.connection_history.insert(0, new_connection)
        
        # Keep only max_history_items
        if len(self.connection_history) > self.max_history_items:
            self.connection_history = self.connection_history[:self.max_history_items]
        
        # Save to file
        self.save_connection_history()
        
        # Update dropdown (now safe to call update since dialog is open)
        self._initialize_dropdown_options()
        if self.dialog.open:
            self.history_dropdown.update()

    def update_history_dropdown(self):
        """Update dropdown options based on connection history - only call when dialog is open"""
        self._initialize_dropdown_options()
        if hasattr(self, 'history_dropdown') and self.dialog.open:
            self.history_dropdown.update()

    def on_history_selected(self, e):
        """Handle selection from history dropdown"""
        if e.control.value and e.control.value != "empty":
            try:
                index = int(e.control.value)
                if 0 <= index < len(self.connection_history):
                    conn = self.connection_history[index]
                    self.server_input.value = conn['server']
                    self.db_input.value = conn['database']
                    
                    # Clear dropdown selection after populating fields
                    self.history_dropdown.value = None
                    
                    # Update the page to show the populated fields
                    self.page.update()
            except (ValueError, IndexError):
                pass

    def clear_history(self, e):
        """Clear all connection history"""
        def confirm_clear(e):
            self.connection_history = []
            self.save_connection_history()
            self._initialize_dropdown_options()
            if self.dialog.open:
                self.history_dropdown.update()
            self.page.dialog.open = False
            self.page.update()
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Connection history cleared"),
                bgcolor=ft.Colors.GREEN_700
            )
            self.page.snack_bar.open = True
            self.page.update()
        
        def cancel_clear(e):
            self.page.dialog.open = False
            self.page.update()
        
        # Show confirmation dialog
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Clear History?"),
            content=ft.Text("Are you sure you want to clear all connection history? This action cannot be undone."),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_clear),
                ft.ElevatedButton("Clear All", on_click=confirm_clear, bgcolor=ft.Colors.RED_700),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()

    def open_dialog(self, e=None):
        """Open the dialog"""
        # Clear any previous values
        self.server_input.value = "DESKTOP-EJ33BVS\\SQLEXPRESS"  # Pre-fill your server
        self.db_input.value = "gyPSPPGP"  # Pre-fill your database
        self.server_input.error_text = None
        self.db_input.error_text = None
        self.history_dropdown.value = None
        
        # Reload history in case it was updated elsewhere
        self.load_connection_history()
        self._initialize_dropdown_options()
        
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.open(self.dialog)
        self.page.update()

    def handle_close(self, e):
        """Close the dialog"""
        self.dialog.open = False
        self.page.update()

    def handle_connect(self, e):
        """Handle connect button click"""
        # Clear previous errors
        self.server_input.error_text = None
        self.db_input.error_text = None
        
        has_error = False
        
        # Validate inputs
        if not self.server_input.value or self.server_input.value.strip() == "":
            self.server_input.error_text = "Server name is required"
            self.server_input.focus()
            has_error = True
            
        if not self.db_input.value or self.db_input.value.strip() == "":
            self.db_input.error_text = "Database name is required"
            if not has_error:
                self.db_input.focus()
            has_error = True
            
        # If both fields are filled
        if not has_error:
            server = self.server_input.value.strip()
            database = self.db_input.value.strip()
            
            # Show loading indicator
            self.show_loading()
            
            # Try to connect to database
            success = self.connect_to_database(server, database)
            
            if success:
                # Add to history
                self.add_to_history(server, database)
                
                # Call the callback if it exists
                if self.on_connect_callback:
                    self.on_connect_callback(True, server, database, self.connection)
                
                self.handle_close(e)
            else:
                # Remove loading indicator
                self.hide_loading()
                
                # Call the callback if it exists
                if self.on_connect_callback:
                    self.on_connect_callback(False, server, database, None)
        else:
            # Update the dialog to show error messages
            self.page.update()
    
    def show_loading(self):
        """Show loading indicator in dialog"""
        # Update connection button to show loading (simplified)
        self.page.update()
    
    def hide_loading(self):
        """Hide loading indicator"""
        self.page.update()
    
    def connect_to_database(self, server, database):
        """Connect to SQL Server database"""
        try:
            # Close existing connection if any
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            
            # Build connection string for Windows Authentication
            connection_string = (
                f"DRIVER={{SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"Trusted_Connection=yes;"
            )
            
            print(f"Attempting to connect with string: {connection_string}")
            
            # Try to establish connection
            self.connection = pyodbc.connect(connection_string, timeout=5)
            
            if not self.connection:
                raise pyodbc.Error("Failed to create connection object.")
            self.cursor = self.connection.cursor()
            
            # Show success message
            Custom_Alert_Dialog(
                self.page, 
                title_color=ft.Colors.PRIMARY, 
                title="Connection Successful", 
                title_icon=ft.Icons.CHECK_CIRCLE, 
                title_icon_color=ft.Colors.GREEN, 
                message=f"Successfully connected to {database} on {server}"
            ).show()
            
            # Save connection info to JSON
            with open('data/selected_database.json', 'w') as f:
                json.dump({"server": server, "database": database}, f)
                
            print(f"Connected to SQL Server: {server}")
            print(f"Database: {database}")
            self.status = True
            self.page.update()
            return True
            
        except pyodbc.Error as e:
            # Show error message
            error_message = str(e)
            with open('data/selected_database.json', 'w') as f:
                json.dump({}, f)  # empty the file on error
            
            Display_Error_Dialog(self.page, title="Connection Error", description=error_message).show()
            print(f"Database connection error: {error_message}")
            
            # Show error on specific field if possible
            if "Server" in error_message or "server" in error_message:
                self.server_input.error_text = "Cannot connect to server"
            elif "Database" in error_message or "database" in error_message:
                self.db_input.error_text = "Database not found"
            else:
                self.server_input.error_text = "Connection failed"
            
            self.status = False
            self.page.update()
            return False
            
        except Exception as e:
            # Generic error handling
            print(f"Unexpected error during connection: {e}")
            with open('data/selected_database.json', 'w') as f:
                json.dump({}, f)  # empty the file on error
            Display_Error_Dialog(self.page, f"Unexpected error: {str(e)}").show()
            
            print(f"Unexpected error: {e}")
            self.status = False
            self.page.update()
            return False
    
    def close_connection(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            
            self.cursor = None
            self.connection = None
            print("Database connection closed")
            
        except Exception as e:
            print(f"Error closing connection: {e}")