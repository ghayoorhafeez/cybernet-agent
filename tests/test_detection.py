"""Unit tests for threat detection module"""

import pytest
from src.detection import (
    PatternDetector, AnomalyDetector, ThreatDetector,
    Threat, ThreatLevel
)

class TestThreat:
    """Tests for Threat class"""
    
    def test_threat_creation(self):
        """Test creating a threat"""
        threat = Threat(
            threat_type='TEST_THREAT',
            level=ThreatLevel.HIGH,
            description='Test threat',
            source='TEST',
            confidence=0.9
        )
        
        assert threat.threat_type == 'TEST_THREAT'
        assert threat.level == ThreatLevel.HIGH
        assert threat.confidence == 0.9
        assert threat.id is not None
    
    def test_threat_to_dict(self):
        """Test converting threat to dictionary"""
        threat = Threat(
            threat_type='TEST',
            level=ThreatLevel.MEDIUM,
            description='Test',
            source='TEST',
            confidence=0.5
        )
        
        threat_dict = threat.to_dict()
        assert threat_dict['type'] == 'TEST'
        assert threat_dict['level'] == ThreatLevel.MEDIUM


class TestPatternDetector:
    """Tests for PatternDetector"""
    
    def test_sql_injection_detection(self):
        """Test SQL injection detection"""
        detector = PatternDetector()
        
        # Positive case
        is_threat, confidence = detector.detect_sql_injection(
            "'; DROP TABLE users; --"
        )
        assert is_threat or confidence > 0
        
        # Negative case
        is_threat, confidence = detector.detect_sql_injection(
            "normal input"
        )
        assert not is_threat
    
    def test_xss_detection(self):
        """Test XSS detection"""
        detector = PatternDetector()
        
        # Positive case
        is_threat, confidence = detector.detect_xss(
            "<script>alert('xss')</script>"
        )
        assert is_threat or confidence > 0
        
        # Negative case
        is_threat, confidence = detector.detect_xss(
            "normal text"
        )
        assert not is_threat
    
    def test_path_traversal_detection(self):
        """Test path traversal detection"""
        detector = PatternDetector()
        
        # Positive case
        is_threat, confidence = detector.detect_path_traversal(
            "../../etc/passwd"
        )
        assert is_threat or confidence > 0
    
    def test_analyze_string(self):
        """Test analyzing string for multiple threats"""
        detector = PatternDetector()
        threats = detector.analyze_string(
            "'; DROP TABLE; <script>alert('xss')</script>"
        )
        
        assert isinstance(threats, list)
        assert len(threats) > 0


class TestAnomalyDetector:
    """Tests for AnomalyDetector"""
    
    def test_cpu_anomaly_detection(self):
        """Test CPU anomaly detection"""
        detector = AnomalyDetector()
        
        # High CPU
        threat = detector.analyze_cpu(95.0, baseline=30.0)
        assert threat is not None
        
        # Normal CPU
        threat = detector.analyze_cpu(15.0, baseline=30.0)
        assert threat is None
    
    def test_memory_anomaly_detection(self):
        """Test memory anomaly detection"""
        detector = AnomalyDetector()
        
        # High memory
        threat = detector.analyze_memory(95.0, baseline=60.0)
        assert threat is not None
        
        # Normal memory
        threat = detector.analyze_memory(50.0, baseline=60.0)
        assert threat is None
    
    def test_connection_anomaly_detection(self):
        """Test connection anomaly detection"""
        detector = AnomalyDetector()
        
        # Abnormal connections
        threat = detector.analyze_connections(500, baseline=100)
        assert threat is not None
        
        # Normal connections
        threat = detector.analyze_connections(50, baseline=100)
        assert threat is None


class TestThreatDetector:
    """Tests for ThreatDetector orchestrator"""
    
    def test_detect_threats_from_metrics(self):
        """Test detecting threats from metrics"""
        detector = ThreatDetector()
        metrics = {
            'system': {
                'cpu_percent': 95.0,
                'memory': {'percent': 85.0}
            },
            'network': {'active_connections': 500}
        }
        
        threats = detector.detect_threats(metrics)
        assert isinstance(threats, list)
    
    def test_analyze_input(self):
        """Test analyzing input for threats"""
        detector = ThreatDetector()
        threats = detector.analyze_input("'; DROP TABLE; <script>alert('xss')</script>")
        
        assert isinstance(threats, list)
        assert len(threats) > 0
    
    def test_get_threats(self):
        """Test getting threat history"""
        detector = ThreatDetector()
        detector.analyze_input("<script>alert('xss')</script>")
        
        threats = detector.get_threats()
        assert isinstance(threats, list)
        assert len(threats) > 0
    
    def test_threat_count_by_level(self):
        """Test getting threat count by level"""
        detector = ThreatDetector()
        detector.analyze_input("<script>alert('xss')</script>")
        
        counts = detector.get_threat_count_by_level()
        assert isinstance(counts, dict)
