"""Dashboard widget"""

import logging
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QGroupBox, QCheckBox, QComboBox, QScrollArea
)
from PySide6.QtCore import Qt, QTimer
from src.memory.database import Database
from src.tools.registry import ToolRegistry
from src.plugins.loader import PluginLoader

logger = logging.getLogger(__name__)

class DashboardWidget(QWidget):
    """Main dashboard widget"""
    
    def __init__(self, db: Database, tool_registry: ToolRegistry, plugin_loader: PluginLoader):
        super().__init__()
        self.db = db
        self.tool_registry = tool_registry
        self.plugin_loader = plugin_loader
        
        self._create_ui()
    
    def _create_ui(self):
        """Create dashboard UI"""
        layout = QVBoxLayout(self)
        
        # Status section
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()
        
        self.mode_label = QLabel("MODE: MOCK")
        self.browser_status = QLabel("Browser: Not Connected")
        self.portal_status = QLabel("Portal: Not Authenticated")
        self.ai_status = QLabel("AI Engine: Ready")
        
        status_layout.addWidget(self.mode_label)
        status_layout.addWidget(self.browser_status)
        status_layout.addWidget(self.portal_status)
        status_layout.addWidget(self.ai_status)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Controls section
        controls_group = QGroupBox("Controls")
        controls_layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        self.open_portal_btn = QPushButton("Open Cybernet Portal")
        self.open_portal_btn.clicked.connect(self.open_portal)
        button_layout.addWidget(self.open_portal_btn)
        
        self.inspect_btn = QPushButton("Inspect Current Page")
        self.inspect_btn.clicked.connect(self.inspect_page)
        self.inspect_btn.setEnabled(False)
        button_layout.addWidget(self.inspect_btn)
        
        controls_layout.addLayout(button_layout)
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        # Mode selection
        mode_group = QGroupBox("Portal Mode")
        mode_layout = QVBoxLayout()
        
        mode_combo = QComboBox()
        mode_combo.addItem("MOCK (Safe Development)")
        mode_combo.addItem("LIVE (Real Portal)")
        mode_combo.currentIndexChanged.connect(self.change_mode)
        
        mode_layout.addWidget(QLabel("Select Portal Mode:"))
        mode_layout.addWidget(mode_combo)
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # Plugins section
        plugins_group = QGroupBox("Plugins")
        plugins_layout = QVBoxLayout()
        
        plugins = self.plugin_loader.get_all_plugins()
        for plugin_name, plugin in plugins.items():
            checkbox = QCheckBox(f"{plugin_name} (v{plugin.version})")
            checkbox.setChecked(plugin.enabled)
            checkbox.stateChanged.connect(lambda state, p=plugin: self.toggle_plugin(p, state))
            plugins_layout.addWidget(checkbox)
        
        if not plugins:
            plugins_layout.addWidget(QLabel("No plugins loaded"))
        
        plugins_group.setLayout(plugins_layout)
        layout.addWidget(plugins_group)
        
        # Inspection results
        results_group = QGroupBox("Inspection Results")
        results_layout = QVBoxLayout()
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlainText("No inspection performed yet")
        results_layout.addWidget(self.results_text)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        # Tools section
        tools_group = QGroupBox("Available Tools")
        tools_layout = QVBoxLayout()
        
        tools = self.tool_registry.get_all_tools()
        tools_text = "\n".join([
            f"- {tool.name} ({'READ' if tool.is_read_only else 'WRITE'})"
            for tool in tools
        ])
        tools_display = QTextEdit()
        tools_display.setReadOnly(True)
        tools_display.setPlainText(tools_text)
        tools_layout.addWidget(tools_display)
        
        tools_group.setLayout(tools_layout)
        layout.addWidget(tools_group)
        
        layout.addStretch()
    
    def open_portal(self):
        """Open Cybernet portal"""
        logger.info("Opening portal...")
        self.results_text.setPlainText("Opening portal...")
        self.browser_status.setText("Browser: Connecting...")
    
    def inspect_page(self):
        """Inspect current page"""
        logger.info("Inspecting page...")
        self.results_text.setPlainText("Page inspection complete (demo)\n\nThis is Phase 1 - Full inspection requires live portal connection.")
    
    def change_mode(self, index: int):
        """Change portal mode"""
        mode = "MOCK" if index == 0 else "LIVE"
        logger.info(f"Changing mode to: {mode}")
        self.mode_label.setText(f"MODE: {mode}")
    
    def toggle_plugin(self, plugin, state):
        """Toggle plugin state"""
        enabled = state == 2  # Qt.CheckState.Checked
        logger.info(f"Plugin {plugin.id}: {'enabled' if enabled else 'disabled'}")
