"""Alerting system for threat notifications"""

from typing import Dict, Any, List, Callable
from datetime import datetime
from enum import Enum
from src.logger import get_logger
from src.detection import Threat, ThreatLevel

logger = get_logger()

class AlertChannel(Enum):
    """Alert notification channels"""
    EMAIL = "email"
    LOG = "log"
    WEBHOOK = "webhook"
    DATABASE = "database"


class Alert:
    """Represents an alert"""
    
    def __init__(self, threat: Threat, channel: AlertChannel):
        self.alert_id = f"alert_{threat.id}"
        self.threat = threat
        self.channel = channel
        self.timestamp = datetime.now().isoformat()
        self.sent = False
        self.sent_at = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'threat': self.threat.to_dict(),
            'channel': self.channel.value,
            'timestamp': self.timestamp,
            'sent': self.sent,
            'sent_at': self.sent_at,
        }


class AlertManager:
    """Manage alerts and notifications"""
    
    def __init__(self):
        self.alerts: List[Alert] = []
        self.max_alerts = 5000
        self.handlers: Dict[AlertChannel, Callable] = {
            AlertChannel.LOG: self._handle_log_alert,
            AlertChannel.EMAIL: self._handle_email_alert,
            AlertChannel.WEBHOOK: self._handle_webhook_alert,
            AlertChannel.DATABASE: self._handle_database_alert,
        }
        self.critical_count = 0
        self.high_count = 0
    
    def create_alert(self, threat: Threat, channels: List[AlertChannel] = None) -> List[Alert]:
        """Create and send alerts for a threat"""
        if channels is None:
            # Default channels based on threat level
            channels = self._get_default_channels(threat.level)
        
        created_alerts = []
        for channel in channels:
            alert = Alert(threat, channel)
            self._send_alert(alert)
            self.alerts.append(alert)
            created_alerts.append(alert)
        
        # Count critical and high threats
        if threat.level == ThreatLevel.CRITICAL:
            self.critical_count += 1
        elif threat.level == ThreatLevel.HIGH:
            self.high_count += 1
        
        # Maintain alert history size
        if len(self.alerts) > self.max_alerts:
            self.alerts = self.alerts[-self.max_alerts:]
        
        return created_alerts
    
    def _get_default_channels(self, threat_level: str) -> List[AlertChannel]:
        """Get default alert channels for threat level"""
        if threat_level == ThreatLevel.CRITICAL:
            return [AlertChannel.LOG, AlertChannel.EMAIL, AlertChannel.WEBHOOK]
        elif threat_level == ThreatLevel.HIGH:
            return [AlertChannel.LOG, AlertChannel.WEBHOOK]
        else:
            return [AlertChannel.LOG, AlertChannel.DATABASE]
    
    def _send_alert(self, alert: Alert):
        """Send alert through appropriate channel"""
        try:
            handler = self.handlers.get(alert.channel)
            if handler:
                handler(alert)
                alert.sent = True
                alert.sent_at = datetime.now().isoformat()
            else:
                logger.warning(f"No handler for alert channel: {alert.channel}")
        except Exception as e:
            logger.error(f"Error sending alert: {str(e)}")
    
    def _handle_log_alert(self, alert: Alert):
        """Handle log-based alerts"""
        threat = alert.threat
        log_level = self._get_log_level(threat.level)
        getattr(logger, log_level.lower())(f"ALERT: {threat.threat_type} - {threat.description}")
    
    def _handle_email_alert(self, alert: Alert):
        """Handle email-based alerts"""
        # TODO: Implement email sending
        logger.info(f"Email alert created (not yet implemented): {alert.alert_id}")
    
    def _handle_webhook_alert(self, alert: Alert):
        """Handle webhook-based alerts"""
        # TODO: Implement webhook sending
        logger.info(f"Webhook alert created (not yet implemented): {alert.alert_id}")
    
    def _handle_database_alert(self, alert: Alert):
        """Handle database-based alerts"""
        logger.info(f"Database alert stored: {alert.alert_id}")
    
    def _get_log_level(self, threat_level: str) -> str:
        """Get logger level for threat level"""
        mapping = {
            ThreatLevel.CRITICAL: 'ERROR',
            ThreatLevel.HIGH: 'WARNING',
            ThreatLevel.MEDIUM: 'INFO',
            ThreatLevel.LOW: 'INFO',
            ThreatLevel.INFO: 'DEBUG',
        }
        return mapping.get(threat_level, 'INFO')
    
    def get_alerts(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get alert history"""
        return [a.to_dict() for a in self.alerts[-limit:]]
    
    def get_alert_count_by_channel(self) -> Dict[str, int]:
        """Get alert count by channel"""
        counts = {}
        for alert in self.alerts:
            channel = alert.channel.value
            counts[channel] = counts.get(channel, 0) + 1
        return counts
    
    def get_critical_alerts(self) -> List[Dict[str, Any]]:
        """Get critical alerts"""
        critical = [a for a in self.alerts if a.threat.level == ThreatLevel.CRITICAL]
        return [a.to_dict() for a in critical]
