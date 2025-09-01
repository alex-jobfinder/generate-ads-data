#!/usr/bin/env python3
"""
Textual Database CLI App
A modern terminal GUI for database operations using Textual.
"""

import sys
import os
import sqlite3
from typing import Optional, List, Tuple
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Button, Input, Select, Static, TextArea, Header, Footer, 
    DataTable, Label, Collapsible, Rule, TabbedContent, TabPane
)
from textual.reactive import reactive
from textual.worker import Worker, get_current_worker, WorkerState
from textual.binding import Binding
from textual.message import Message

# Import CLI functions
from cli_groups.db import cb_init_db, cb_migrate_db


class DatabaseTextualApp(App):
    """Enhanced Database Operations Manager with Textual."""
    
    CSS = """
    Screen {
        layout: vertical;
        background: $surface;
    }
    
    .header {
        height: 4;
        background: $primary;
        color: $text;
        text-align: center;
        padding: 1;
    }
    
    .main-content {
        layout: horizontal;
        height: 1fr;
    }
    
    .left-panel {
        width: 40%;
        border: solid $primary;
        margin: 1;
        padding: 1;
    }
    
    .right-panel {
        width: 60%;
        border: solid $primary;
        margin: 1;
        padding: 1;
    }
    
    .config-section {
        height: auto;
        border: solid $secondary;
        margin: 1;
        padding: 1;
    }
    
    .buttons-section {
        height: auto;
        border: solid $secondary;
        margin: 1;
        padding: 1;
    }
    
    .log-section {
        height: 1fr;
        border: solid $secondary;
        margin: 1;
        padding: 1;
        min-height: 15;
    }
    
    .db-viewer-section {
        height: 1fr;
        border: solid $secondary;
        margin: 1;
        padding: 1;
        min-height: 15;
    }
    
    TextArea {
        height: 1fr;
        border: none;
        background: $surface;
    }
    
    DataTable {
        height: 1fr;
        border: solid $primary;
        margin: 1;
    }
    
    .status-section {
        height: 3;
        border: solid $secondary;
        margin: 1;
        padding: 1;
    }
    
    Button {
        margin: 1;
        min-width: 20;
    }
    
    Button.primary {
        background: $primary;
        color: $text;
    }
    
    Button.success {
        background: $success;
        color: $text;
    }
    
    Button.warning {
        background: $warning;
        color: $text;
    }
    
    Button.info {
        background: $accent;
        color: $text;
    }
    
    Input {
        margin: 1;
        border: solid $primary;
    }
    
    Select {
        margin: 1;
        border: solid $primary;
    }
    
    .title {
        text-style: bold;
        color: $primary;
        text-align: center;
        margin: 1;
    }
    
    .subtitle {
        text-style: italic;
        color: $text-muted;
        text-align: center;
        margin: 1;
    }
    
    .success {
        color: $success;
    }
    
    .error {
        color: $error;
    }
    
    .warning {
        color: $warning;
    }
    
    .info {
        color: $accent;
    }
    
    .status-ready {
        color: $success;
        text-style: bold;
    }
    
    .status-working {
        color: $warning;
        text-style: bold;
    }
    
    .status-error {
        color: $error;
        text-style: bold;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+r", "refresh", "Refresh"),
        Binding("ctrl+c", "clear_log", "Clear Log"),
        Binding("f1", "help", "Help"),
    ]
    
    # Reactive variables
    db_url = reactive("sqlite:///ads.db")
    log_level = reactive("INFO")
    seed = reactive(42)
    log_output = reactive("🚀 Database Operations GUI ready\n")
    is_loading = reactive(False)
    status_message = reactive("Ready")
    last_operation = reactive("None")
    operation_count = reactive(0)
    current_table = reactive("")
    table_names = reactive([])
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        # Header section
        with Container(classes="header"):
            yield Static("🗄️ Database Operations Manager", classes="title")
            yield Static("Manage your database initialization and migrations with style", classes="subtitle")
        
        # Main content area
        with Container(classes="main-content"):
            # Left panel - Configuration and Controls
            with Container(classes="left-panel"):
                with Collapsible(title="⚙️ Configuration", collapsed=False):
                    with Container(classes="config-section"):
                        yield Static("Database URL:", classes="info")
                        yield Input(
                            placeholder="sqlite:///ads.db",
                            value=self.db_url,
                            id="db_url"
                        )
                        yield Static("Log Level:", classes="info")
                        yield Select(
                            options=[("DEBUG", "DEBUG"), ("INFO", "INFO"), ("WARNING", "WARNING"), ("ERROR", "ERROR")],
                            value=self.log_level,
                            id="log_level"
                        )
                        yield Static("Random Seed:", classes="info")
                        yield Input(
                            placeholder="42",
                            value=str(self.seed),
                            id="seed"
                        )
                
                yield Rule()
                
                with Collapsible(title="🔧 Operations", collapsed=False):
                    with Container(classes="buttons-section"):
                        yield Button("🗄️ Initialize Database", id="init_db", classes="primary")
                        yield Button("🔄 Migrate Database", id="migrate_db", classes="success")
                        yield Button("📊 Show Config", id="show_config", classes="warning")
                        yield Button("🧹 Clear Log", id="clear_log", classes="warning")
                        yield Button("🔄 Refresh DB View", id="refresh_db", classes="info")
            
            # Right panel - Database Viewer and Log
            with Container(classes="right-panel"):
                with TabbedContent():
                    with TabPane("📋 Output Log", id="log_tab"):
                        with Container(classes="log-section"):
                            yield TextArea(
                                "🚀 Database Operations GUI ready\n",
                                id="log_area",
                                read_only=True
                            )
                    
                    with TabPane("🗄️ Database Viewer", id="db_tab"):
                        with Container(classes="db-viewer-section"):
                            yield Static("📊 Database Contents", classes="title")
                            
                            # Table selector
                            yield Static("Select Table:", classes="info")
                            yield Select(
                                options=[],
                                id="table_selector",
                                allow_blank=True
                            )
                            
                            # Table info
                            yield Static("Table Information:", classes="info")
                            yield Static("No table selected", id="table_info")
                            
                            # Data table
                            yield Static("Table Data:", classes="info")
                            yield DataTable(id="data_table")
                
                yield Rule()
                
                with Container(classes="status-section"):
                    yield Static("📊 Status Information", classes="title")
                    yield Static(f"Status: {self.status_message}", id="status_display")
                    yield Static(f"Last Operation: {self.last_operation}", id="last_op_display")
                    yield Static(f"Operations Count: {self.operation_count}", id="op_count_display")
        
        yield Footer()
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if event.input.id == "db_url":
            self.db_url = event.value
        elif event.input.id == "seed":
            try:
                self.seed = int(event.value)
            except ValueError:
                pass
    
    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle select changes."""
        if event.select.id == "log_level":
            self.log_level = event.value
        elif event.select.id == "table_selector":
            if event.value:
                self.load_table_data(event.value)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "init_db":
            self.init_database()
        elif event.button.id == "migrate_db":
            self.migrate_database()
        elif event.button.id == "show_config":
            self.show_configuration()
        elif event.button.id == "clear_log":
            self.clear_log()
        elif event.button.id == "refresh_db":
            self.refresh_database_view()
    
    def get_db_path(self) -> str:
        """Extract database file path from URL."""
        if self.db_url.startswith("sqlite:///"):
            return self.db_url[10:]  # Remove "sqlite:///" prefix
        return self.db_url
    
    def get_table_names(self) -> List[str]:
        """Get list of table names from database."""
        try:
            db_path = self.get_db_path()
            if not os.path.exists(db_path):
                return []
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            return tables
        except Exception as e:
            self.log_message(f"❌ Error getting table names: {str(e)}")
            return []
    
    def get_table_info(self, table_name: str) -> List[Tuple]:
        """Get table schema information."""
        try:
            db_path = self.get_db_path()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            info = cursor.fetchall()
            conn.close()
            return info
        except Exception as e:
            self.log_message(f"❌ Error getting table info: {str(e)}")
            return []
    
    def get_table_data(self, table_name: str, limit: int = 100) -> List[Tuple]:
        """Get table data with limit."""
        try:
            db_path = self.get_db_path()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            self.log_message(f"❌ Error getting table data: {str(e)}")
            return []
    
    def load_table_data(self, table_name: str) -> None:
        """Load and display table data."""
        try:
            self.current_table = table_name
            
            # Get table info
            table_info = self.get_table_info(table_name)
            columns = [col[1] for col in table_info]  # Column names
            
            # Get table data
            data = self.get_table_data(table_name)
            
            # Update table info display
            info_text = f"Table: {table_name}\n"
            info_text += f"Columns: {len(columns)}\n"
            info_text += f"Rows: {len(data)}\n"
            info_text += f"Columns: {', '.join(columns)}"
            
            table_info_display = self.query_one("#table_info", Static)
            table_info_display.update(info_text)
            
            # Update data table
            data_table = self.query_one("#data_table", DataTable)
            data_table.clear(columns=True)
            
            if columns:
                data_table.add_columns(*columns)
                
                for row in data:
                    data_table.add_row(*[str(cell) if cell is not None else "NULL" for cell in row])
            
            self.log_message(f"📊 Loaded table: {table_name} ({len(data)} rows)")
            
        except Exception as e:
            self.log_message(f"❌ Error loading table data: {str(e)}")
    
    def refresh_database_view(self) -> None:
        """Refresh the database view."""
        try:
            # Get table names
            tables = self.get_table_names()
            self.table_names = tables
            
            # Update table selector
            table_selector = self.query_one("#table_selector", Select)
            table_selector.set_options([(table, table) for table in tables])
            
            if tables:
                self.log_message(f"📊 Found {len(tables)} tables: {', '.join(tables)}")
            else:
                self.log_message("📊 No tables found in database")
                
        except Exception as e:
            self.log_message(f"❌ Error refreshing database view: {str(e)}")
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()
    
    def action_refresh(self) -> None:
        """Refresh the interface."""
        self.log_message("🔄 Interface refreshed")
        self.update_status("Refreshed", "Ready")
    
    def action_clear_log(self) -> None:
        """Clear the log."""
        self.clear_log()
    
    def action_help(self) -> None:
        """Show help information."""
        help_text = """
🗄️ Database Operations Manager Help

Keyboard Shortcuts:
• Ctrl+Q: Quit application
• Ctrl+R: Refresh interface  
• Ctrl+C: Clear log
• F1: Show this help

Operations:
• Initialize Database: Creates a fresh database
• Migrate Database: Applies schema migrations
• Show Config: Displays current configuration
• Clear Log: Clears the output log

Configuration:
• Database URL: SQLite database file path
• Log Level: Verbosity level (DEBUG, INFO, WARNING, ERROR)
• Random Seed: For reproducible data generation
        """
        self.notify(help_text, title="Help", severity="information")
    
    def log_message(self, message: str) -> None:
        """Add a message to the log with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output += f"[{timestamp}] {message}\n"
        
        try:
            log_area = self.query_one("#log_area", TextArea)
            if log_area:
                log_area.load_text(self.log_output)
                log_area.scroll_end()
        except Exception as e:
            # Fallback if TextArea is not ready
            print(f"[{timestamp}] {message}")
    
    def update_status(self, status: str, operation: str = None) -> None:
        """Update status information."""
        self.status_message = status
        if operation:
            self.last_operation = operation
            self.operation_count += 1
        
        # Update status display
        status_display = self.query_one("#status_display", Static)
        status_display.update(f"Status: {self.status_message}")
        
        last_op_display = self.query_one("#last_op_display", Static)
        last_op_display.update(f"Last Operation: {self.last_operation}")
        
        op_count_display = self.query_one("#op_count_display", Static)
        op_count_display.update(f"Operations Count: {self.operation_count}")
    
    def show_configuration(self) -> None:
        """Show current configuration in a popup."""
        config_text = f"""
🗄️ Current Configuration

Database URL: {self.db_url}
Log Level: {self.log_level}
Random Seed: {self.seed}
Status: {self.status_message}
Last Operation: {self.last_operation}
Operations Count: {self.operation_count}
        """
        
        self.notify(config_text, title="Configuration", severity="information")
    
    def clear_log(self) -> None:
        """Clear the log output."""
        self.log_output = "🧹 Log cleared\n"
        log_area = self.query_one("#log_area", TextArea)
        log_area.load_text(self.log_output)
        self.log_message("Log cleared by user")
        self.update_status("Log Cleared", "Clear Log")
    
    def init_database(self) -> None:
        """Initialize the database."""
        if self.is_loading:
            self.notify("Operation already in progress", severity="warning")
            return
            
        self.is_loading = True
        self.update_status("Working", "Initialize Database")
        self.log_message("🔄 Initializing database...")
        self.log_message(f"   📍 URL: {self.db_url}")
        self.log_message(f"   📊 Log Level: {self.log_level}")
        self.log_message(f"   🎲 Seed: {self.seed}")
        
        # Start worker for async operation
        self.run_worker(self._init_db_worker, name="init_db")
    
    def migrate_database(self) -> None:
        """Migrate the database."""
        if self.is_loading:
            self.notify("Operation already in progress", severity="warning")
            return
            
        self.is_loading = True
        self.update_status("Working", "Migrate Database")
        self.log_message("🔄 Migrating database...")
        self.log_message(f"   📍 URL: {self.db_url}")
        self.log_message(f"   📊 Log Level: {self.log_level}")
        
        # Start worker for async operation
        self.run_worker(self._migrate_db_worker, name="migrate_db")
    
    async def _init_db_worker(self) -> None:
        """Worker function for database initialization."""
        try:
            cb_init_db(
                log_level=self.log_level,
                db_url=self.db_url,
                seed=self.seed
            )
            
            self.log_message("✅ Database initialized successfully!")
            self.log_message(f"   📁 Database file: {self.db_url}")
            self.log_message(f"   🎯 Ready for operations!")
            self.notify("Database initialized successfully!", severity="information")
            self.update_status("Ready", "Initialize Database")
            
        except Exception as e:
            self.log_message(f"❌ Error initializing database: {str(e)}")
            self.notify(f"Error: {str(e)}", severity="error")
            self.update_status("Error", "Initialize Database")
        finally:
            self.is_loading = False
    
    async def _migrate_db_worker(self) -> None:
        """Worker function for database migration."""
        try:
            cb_migrate_db(
                log_level=self.log_level,
                db_url=self.db_url
            )
            
            self.log_message("✅ Database migrated successfully!")
            self.log_message(f"   📁 Database file: {self.db_url}")
            self.log_message(f"   🎯 Schema updated!")
            self.notify("Database migrated successfully!", severity="information")
            self.update_status("Ready", "Migrate Database")
            
        except Exception as e:
            self.log_message(f"❌ Error migrating database: {str(e)}")
            self.notify(f"Error: {str(e)}", severity="error")
            self.update_status("Error", "Migrate Database")
        finally:
            self.is_loading = False
    
    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Handle worker state changes."""
        if event.worker.name in ["init_db", "migrate_db"]:
            if event.state == WorkerState.RUNNING:
                self.is_loading = True
                self.update_status("Working")
            elif event.state in [WorkerState.SUCCESS, WorkerState.ERROR]:
                self.is_loading = False
                if event.state == WorkerState.SUCCESS:
                    self.update_status("Ready")
                else:
                    self.update_status("Error")
    
    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.log_message("🚀 Database Operations Manager started")
        self.log_message("💡 Use the buttons to perform database operations")
        self.log_message("⌨️  Press F1 for help or Ctrl+Q to quit")
        self.update_status("Ready")
        
        # Refresh database view on startup
        self.refresh_database_view()


def main():
    """Main entry point."""
    try:
        app = DatabaseTextualApp()
        app.run()
    except ImportError as e:
        print("❌ Error: Textual not installed")
        print("💡 Install it with: pip install textual")
        print(f"   Import error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting Textual application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
