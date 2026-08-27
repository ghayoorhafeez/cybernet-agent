"""Unit tests for mock portal"""

import pytest
from src.cybernet.mock_portal import MockCybernetPortal

class TestMockPortal:
    """Tests for MockCybernetPortal"""
    
    @pytest.fixture
    def portal(self):
        """Create mock portal instance"""
        return MockCybernetPortal()
    
    def test_authentication(self, portal):
        """Test authentication"""
        assert not portal.is_authenticated()
        portal.authenticate()
        assert portal.is_authenticated()
    
    def test_search_customer(self, portal):
        """Test customer search"""
        portal.authenticate()
        results = portal.search_customer("Ali Ahmad")
        assert len(results) > 0
        assert results[0].name == "Ali Ahmad"
    
    def test_get_customer_details(self, portal):
        """Test getting customer details"""
        portal.authenticate()
        customer = portal.get_customer_details('cust_001')
        assert customer is not None
        assert customer.id == 'cust_001'
        assert customer.name == 'Ali Ahmad'
    
    def test_get_customer_status(self, portal):
        """Test getting customer status"""
        portal.authenticate()
        status = portal.get_customer_status('cust_001')
        assert status is not None
        assert status['account_status'] == 'active'
        assert status['service_status'] == 'active'
        assert status['device_status'] == 'online'
    
    def test_get_current_package(self, portal):
        """Test getting current package"""
        portal.authenticate()
        package = portal.get_current_package('cust_001')
        assert package == '20 Mbps'
    
    def test_activate_package(self, portal):
        """Test package activation"""
        portal.authenticate()
        result = portal.activate_package('cust_001', '50 Mbps')
        assert result is True
        # Verify package changed
        new_package = portal.get_current_package('cust_001')
        assert new_package == '50 Mbps'
    
    def test_renew_package(self, portal):
        """Test package renewal"""
        portal.authenticate()
        result = portal.renew_package('cust_001')
        assert result is True
    
    def test_get_available_packages(self, portal):
        """Test getting available packages"""
        packages = portal.get_available_packages()
        assert len(packages) > 0
        assert '20 Mbps' in packages
