"""Main application window using PySide6"""

import logging
import asyncio
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QTextEdit, QStatusBar, QGroupBox
)
from PySide6.QtCore import Qt, QTimer
from src.ui.dashboard import DashboardWidget
from src.memory.database import Database
from src.tools.registry import ToolRegistry
from src.plugins.loader import PluginLoader
from src.cybernet.portal_factory import PortalFactory

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, db: Database, tool_registry: ToolRegistry, plugin_loader: PluginLoader):
        super().__init__()
        self.db = db
        self.tool_registry = tool_registry
        self.plugin_loader = plugin_loader
        self.portal = None
        
        self.setWindowTitle("Cybernet NBB AI Voice Operator - Phase 1")
        self.setGeometry(100, 100, 1400, 900)
        
        self._create_ui()
        self._setup_status_bar()
    
    def _create_ui(self):
        """Create UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create tabs
        tabs = QTabWidget()
        
        # Dashboard tab
        self.dashboard = DashboardWidget(self.db, self.tool_registry, self.plugin_loader)
        tabs.addTab(self.dashboard, "Dashboard")
        
        # About tab
        about_widget = self._create_about_tab()
        tabs.addTab(about_widget, "About")
        
        layout.addWidget(tabs)
        central_widget.setLayout(layout)
    
    def _create_about_tab(self) -> QWidget:
        """Create about tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setText("""
Cybernet NBB AI Voice Operator - Phase 1
Made by Ghayoor Hafeez

Phase 1 Features:
- PySide6 Dashboard
- Plugin System with Auto-Discovery
- SQLite Persistent Memory
- Tool Registry & Permission System
- Mock Cybernet Portal
- Live Portal Inspection (Playwright)
- Comprehensive Logging
- Test Suite

Current Mode: MOCK
(Switch to LIVE in settings)

Phone: https://partner.nationalbroadband.pk/
        """)
        
        layout.addWidget(about_text)
        return widget
    
    def _setup_status_bar(self):
        """Setup status bar"""
        status = QStatusBar()
        self.setStatusBar(status)
        
        self.status_label = QLabel("Ready")
        status.addWidget(self.status_label)
        
        self.update_status("Phase 1 Initialized - Mock Mode Active")
    
    def update_status(self, message: str):
        """Update status bar message"""
        self.status_label.setText(message)
        logger.info(f"Status: {message}")
