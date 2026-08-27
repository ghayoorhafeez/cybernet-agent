"""Unit tests for alerting module"""

import pytest
from src.alerting import AlertManager, Alert, AlertChannel
from src.detection import Threat, ThreatLevel

class TestAlert:
    """Tests for Alert class"""
    
    def test_alert_creation(self):
        """Test creating an alert"""
        threat = Threat(
            threat_type='TEST',
            level=ThreatLevel.HIGH,
            description='Test threat',
            source='TEST',
            confidence=0.9
        )
        
        alert = Alert(threat, AlertChannel.LOG)
        assert alert.threat == threat
        assert alert.channel == AlertChannel.LOG
        assert not alert.sent
    
    def test_alert_to_dict(self):
        """Test converting alert to dictionary"""
        threat = Threat(
            threat_type='TEST',
            level=ThreatLevel.MEDIUM,
            description='Test',
            source='TEST',
            confidence=0.5
        )
        
        alert = Alert(threat, AlertChannel.LOG)
        alert_dict = alert.to_dict()
        
        assert 'alert_id' in alert_dict
        assert 'threat' in alert_dict
        assert 'channel' in alert_dict
        assert alert_dict['channel'] == 'log'


class TestAlertManager:
    """Tests for AlertManager"""
    
    def test_create_alert(self):
        """Test creating alerts"""
        manager = AlertManager()
        threat = Threat(
            threat_type='TEST',
            level=ThreatLevel.HIGH,
            description='Test threat',
            source='TEST',
            confidence=0.9
        )
        
        alerts = manager.create_alert(threat, [AlertChannel.LOG])
        assert len(alerts) > 0
        assert alerts[0].sent
    
    def test_critical_threat_channels(self):
        """Test critical threat uses correct channels"""
        manager = AlertManager()
        threat = Threat(
            threat_type='TEST',
            level=ThreatLevel.CRITICAL,
            description='Critical threat',
            source='TEST',
            confidence=1.0
        )
        
        channels = manager._get_default_channels(ThreatLevel.CRITICAL)
        assert AlertChannel.LOG in channels
        assert AlertChannel.EMAIL in channels
        assert AlertChannel.WEBHOOK in channels
    
    def test_high_threat_channels(self):
        """Test high threat uses correct channels"""
        manager = AlertManager()
        channels = manager._get_default_channels(ThreatLevel.HIGH)
        assert AlertChannel.LOG in channels
    
    def test_get_alerts(self):
        """Test getting alert history"""
        manager = AlertManager()
        threat = Threat(
            threat_type='TEST',
            level=ThreatLevel.MEDIUM,
            description='Test',
            source='TEST',
            confidence=0.5
        )
        
        manager.create_alert(threat)
        alerts = manager.get_alerts()
        
        assert isinstance(alerts, list)
        assert len(alerts) > 0
    
    def test_alert_count_by_channel(self):
        """Test getting alert count by channel"""
        manager = AlertManager()
        threat = Threat(
            threat_type='TEST',
            level=ThreatLevel.MEDIUM,
            description='Test',
            source='TEST',
            confidence=0.5
        )
        
        manager.create_alert(threat, [AlertChannel.LOG, AlertChannel.DATABASE])
        counts = manager.get_alert_count_by_channel()
        
        assert 'log' in counts
        assert 'database' in counts
    
    def test_critical_alert_tracking(self):
        """Test tracking critical alerts"""
        manager = AlertManager()
        threat = Threat(
            threat_type='TEST',
            level=ThreatLevel.CRITICAL,
            description='Critical',
            source='TEST',
            confidence=1.0
        )
        
        manager.create_alert(threat)
        assert manager.critical_count > 0
    
    def test_get_critical_alerts(self):
        """Test getting critical alerts"""
        manager = AlertManager()
        threat = Threat(
            threat_type='TEST',
            level=ThreatLevel.CRITICAL,
            description='Critical',
            source='TEST',
            confidence=1.0
        )
        
        manager.create_alert(threat)
        critical = manager.get_critical_alerts()
        
        assert len(critical) > 0
        assert critical[0]['threat']['level'] == ThreatLevel.CRITICAL
