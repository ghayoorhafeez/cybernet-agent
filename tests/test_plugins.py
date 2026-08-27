"""Unit tests for plugin loader"""

import pytest
import tempfile
import os
from pathlib import Path
from src.plugins.loader import PluginLoader
from src.plugins.base import Plugin

class TestPluginLoader:
    """Tests for PluginLoader"""
    
    @pytest.fixture
    def temp_plugin_dir(self):
        """Create temporary plugin directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_plugin_loader_initialization(self):
        """Test plugin loader initialization"""
        loader = PluginLoader()
        assert loader.plugin_dir is not None
    
    def test_plugin_directory_creation(self):
        """Test plugin directory is created if missing"""
        loader = PluginLoader('test_plugins')
        assert loader.plugin_dir.exists()
    
    def test_load_no_plugins(self, temp_plugin_dir):
        """Test loading when no plugins exist"""
        loader = PluginLoader(temp_plugin_dir)
        plugins = loader.load_plugins()
        assert len(plugins) == 0
    
    def test_get_all_plugins(self):
        """Test getting all loaded plugins"""
        loader = PluginLoader()
        plugins = loader.get_all_plugins()
        assert isinstance(plugins, dict)
