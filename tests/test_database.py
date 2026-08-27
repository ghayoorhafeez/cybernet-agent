"""Unit tests for database"""

import pytest
import os
import tempfile
from src.memory.database import Database

class TestDatabase:
    """Tests for Database"""
    
    @pytest.fixture
    def temp_db(self):
        """Create temporary database"""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        db = Database(path)
        db.initialize()
        yield db
        # Cleanup
        if os.path.exists(path):
            os.remove(path)
    
    def test_database_initialization(self, temp_db):
        """Test database initialization"""
        assert temp_db.engine is not None
        assert temp_db.Session is not None
    
    def test_add_conversation(self, temp_db):
        """Test adding conversation"""
        conv_id = temp_db.add_conversation(
            "Test user message",
            "Test AI response",
            "en"
        )
        assert conv_id is not None
    
    def test_get_conversations(self, temp_db):
        """Test getting conversations"""
        temp_db.add_conversation("Message 1", "Response 1", "en")
        temp_db.add_conversation("Message 2", "Response 2", "en")
        
        conversations = temp_db.get_conversations()
        assert len(conversations) >= 2
    
    def test_preferences(self, temp_db):
        """Test preferences storage"""
        result = temp_db.set_preference("language", "urdu")
        assert result is True
        
        value = temp_db.get_preference("language")
        assert value == "urdu"
    
    def test_action_history(self, temp_db):
        """Test action history"""
        action_id = temp_db.add_action(
            "search_customer",
            "Searched for Ali Ahmad",
            requires_confirmation=False
        )
        assert action_id is not None
        
        result = temp_db.update_action(
            action_id,
            "executed",
            "Found 1 customer",
            confirmed=False
        )
        assert result is True
