"""Unit tests for tool registry"""

import pytest
from src.tools.registry import ToolRegistry, Tool

class TestToolRegistry:
    """Tests for ToolRegistry"""
    
    @pytest.fixture
    def registry(self):
        """Create registry instance"""
        return ToolRegistry()
    
    def test_default_tools_registered(self, registry):
        """Test that default tools are registered"""
        tools = registry.get_all_tools()
        assert len(tools) > 0
    
    def test_get_tool(self, registry):
        """Test getting a tool"""
        tool = registry.get_tool('search_customer')
        assert tool is not None
        assert tool.name == 'Search Customer'
    
    def test_read_only_tools(self, registry):
        """Test getting read-only tools"""
        read_only = registry.get_read_only_tools()
        assert len(read_only) > 0
        
        for tool in read_only:
            assert tool.is_read_only is True
    
    def test_write_tools(self, registry):
        """Test getting write tools"""
        write_tools = registry.get_write_tools()
        assert len(write_tools) > 0
        
        for tool in write_tools:
            assert tool.is_read_only is False
    
    def test_confirmation_required(self, registry):
        """Test confirmation requirement"""
        requires_conf = registry.tool_requires_confirmation('activate_package')
        assert requires_conf is True
        
        no_conf = registry.tool_requires_confirmation('search_customer')
        assert no_conf is False
    
    def test_register_custom_tool(self, registry):
        """Test registering custom tool"""
        custom_tool = Tool(
            id='test_tool',
            name='Test Tool',
            description='Test tool',
            requires_confirmation=False,
            is_read_only=True
        )
        registry.register(custom_tool)
        
        retrieved = registry.get_tool('test_tool')
        assert retrieved is not None
        assert retrieved.name == 'Test Tool'
