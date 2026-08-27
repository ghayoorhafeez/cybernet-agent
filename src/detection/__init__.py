"""Threat detection module"""

from typing import Dict, Any, List, Tuple
from datetime import datetime
import re
from src.logger import get_logger
from src.config import Config

logger = get_logger()
config = Config()

class ThreatLevel:
    """Threat level constants"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class Threat:
    """Represents a detected threat"""
    
    def __init__(self, threat_type: str, level: str, description: str, 
                 source: str, confidence: float, details: Dict[str, Any] = None):
        self.threat_type = threat_type
        self.level = level
        self.description = description
        self.source = source
        self.confidence = confidence
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()
        self.id = f"{threat_type}_{int(datetime.now().timestamp() * 1000)}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert threat to dictionary"""
        return {
            'id': self.id,
            'type': self.threat_type,
            'level': self.level,
            'description': self.description,
            'source': self.source,
            'confidence': self.confidence,
            'timestamp': self.timestamp,
            'details': self.details,
        }


class PatternDetector:
    """Detect threats based on patterns"""
    
    def __init__(self):
        self.suspicious_ports = [
            23,    # Telnet
            21,    # FTP
            139,   # NetBIOS
            445,   # SMB
            3389,  # RDP
        ]
        
        self.patterns = {
            'sql_injection': r"(union|select|insert|delete|drop|update|exec|script)",
            'xss': r"(<script|javascript:|onerror|onload)",
            'path_traversal': r"(\.\./|\.\.\\|%2e%2e)",
        }
    
    def detect_sql_injection(self, text: str) -> Tuple[bool, float]:
        """Detect SQL injection patterns"""
        if not text:
            return False, 0.0
        
        matches = len(re.findall(self.patterns['sql_injection'], text, re.IGNORECASE))
        confidence = min(matches * 0.3, 1.0)
        return confidence > 0.5, confidence
    
    def detect_xss(self, text: str) -> Tuple[bool, float]:
        """Detect XSS patterns"""
        if not text:
            return False, 0.0
        
        matches = len(re.findall(self.patterns['xss'], text, re.IGNORECASE))
        confidence = min(matches * 0.4, 1.0)
        return confidence > 0.5, confidence
    
    def detect_path_traversal(self, text: str) -> Tuple[bool, float]:
        """Detect path traversal patterns"""
        if not text:
            return False, 0.0
        
        matches = len(re.findall(self.patterns['path_traversal'], text))
        confidence = min(matches * 0.5, 1.0)
        return confidence > 0.5, confidence
    
    def analyze_string(self, text: str) -> List[Threat]:
        """Analyze string for multiple patterns"""
        threats = []
        
        # Check for SQL injection
        is_threat, confidence = self.detect_sql_injection(text)
        if is_threat:
            threats.append(Threat(
                threat_type='SQL_INJECTION',
                level=ThreatLevel.HIGH,
                description='Potential SQL injection detected',
                source='PATTERN_DETECTOR',
                confidence=confidence,
                details={'pattern': self.patterns['sql_injection']}
            ))
        
        # Check for XSS
        is_threat, confidence = self.detect_xss(text)
        if is_threat:
            threats.append(Threat(
                threat_type='XSS_ATTACK',
                level=ThreatLevel.HIGH,
                description='Potential XSS attack detected',
                source='PATTERN_DETECTOR',
                confidence=confidence,
                details={'pattern': self.patterns['xss']}
            ))
        
        # Check for path traversal
        is_threat, confidence = self.detect_path_traversal(text)
        if is_threat:
            threats.append(Threat(
                threat_type='PATH_TRAVERSAL',
                level=ThreatLevel.MEDIUM,
                description='Potential path traversal detected',
                source='PATTERN_DETECTOR',
                confidence=confidence,
                details={'pattern': self.patterns['path_traversal']}
            ))
        
        return threats


class AnomalyDetector:
    """Detect anomalous behavior"""
    
    def __init__(self):
        self.baseline = {}
        self.threshold = config.ALERT_THRESHOLD
    
    def analyze_cpu(self, cpu_percent: float, baseline: float = 30.0) -> Threat | None:
        """Detect CPU anomalies"""
        if cpu_percent > baseline * 3:  # 3x baseline is anomalous
            confidence = min(cpu_percent / 100.0, 1.0)
            return Threat(
                threat_type='CPU_ANOMALY',
                level=ThreatLevel.MEDIUM,
                description=f'High CPU usage detected: {cpu_percent}%',
                source='ANOMALY_DETECTOR',
                confidence=confidence,
                details={'cpu_percent': cpu_percent, 'baseline': baseline}
            )
        return None
    
    def analyze_memory(self, memory_percent: float, baseline: float = 60.0) -> Threat | None:
        """Detect memory anomalies"""
        if memory_percent > baseline * 1.5:
            confidence = min(memory_percent / 100.0, 1.0)
            return Threat(
                threat_type='MEMORY_ANOMALY',
                level=ThreatLevel.MEDIUM,
                description=f'High memory usage detected: {memory_percent}%',
                source='ANOMALY_DETECTOR',
                confidence=confidence,
                details={'memory_percent': memory_percent, 'baseline': baseline}
            )
        return None
    
    def analyze_connections(self, connection_count: int, baseline: int = 100) -> Threat | None:
        """Detect connection anomalies"""
        if connection_count > baseline * 3:
            confidence = min(connection_count / (baseline * 5), 1.0)
            return Threat(
                threat_type='CONNECTION_ANOMALY',
                level=ThreatLevel.HIGH,
                description=f'Abnormal connection count: {connection_count}',
                source='ANOMALY_DETECTOR',
                confidence=confidence,
                details={'connection_count': connection_count, 'baseline': baseline}
            )
        return None
    
    def analyze_port_activity(self, port: int, is_listening: bool) -> Threat | None:
        """Detect suspicious port activity"""
        suspicious_ports = [23, 21, 139, 445, 3389]
        if port in suspicious_ports and is_listening:
            return Threat(
                threat_type='SUSPICIOUS_PORT',
                level=ThreatLevel.MEDIUM,
                description=f'Suspicious service on port {port}',
                source='ANOMALY_DETECTOR',
                confidence=0.8,
                details={'port': port}
            )
        return None


class ThreatDetector:
    """Main threat detection orchestrator"""
    
    def __init__(self):
        self.pattern_detector = PatternDetector()
        self.anomaly_detector = AnomalyDetector()
        self.threats: List[Threat] = []
        self.max_threats = 10000
    
    def detect_threats(self, metrics: Dict[str, Any]) -> List[Threat]:
        """Detect threats from metrics"""
        detected_threats = []
        
        try:
            # Analyze system metrics
            if 'system' in metrics:
                system = metrics['system']
                
                # CPU analysis
                if 'cpu_percent' in system:
                    cpu_threat = self.anomaly_detector.analyze_cpu(system['cpu_percent'])
                    if cpu_threat:
                        detected_threats.append(cpu_threat)
                
                # Memory analysis
                if 'memory' in system and 'percent' in system['memory']:
                    mem_threat = self.anomaly_detector.analyze_memory(system['memory']['percent'])
                    if mem_threat:
                        detected_threats.append(mem_threat)
            
            # Analyze network metrics
            if 'network' in metrics:
                network = metrics['network']
                if 'active_connections' in network:
                    conn_threat = self.anomaly_detector.analyze_connections(network['active_connections'])
                    if conn_threat:
                        detected_threats.append(conn_threat)
        
        except Exception as e:
            logger.error(f"Error during threat detection: {str(e)}")
        
        # Store threats in history
        self.threats.extend(detected_threats)
        if len(self.threats) > self.max_threats:
            self.threats = self.threats[-self.max_threats:]
        
        return detected_threats
    
    def analyze_input(self, text: str) -> List[Threat]:
        """Analyze input for security threats"""
        return self.pattern_detector.analyze_string(text)
    
    def get_threats(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get threat history"""
        return [t.to_dict() for t in self.threats[-limit:]]
    
    def get_threat_count_by_level(self) -> Dict[str, int]:
        """Get threat count by severity level"""
        counts = {}
        for threat in self.threats:
            level = threat.level
            counts[level] = counts.get(level, 0) + 1
        return counts
