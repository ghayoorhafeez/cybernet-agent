"""REST API for Cybernet Agent"""

from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from typing import Dict, Any
from src.logger import get_logger
from src.config import Config
from src.monitoring import Monitor
from src.detection import ThreatDetector
from src.alerting import AlertManager, AlertChannel

logger = get_logger()
config = Config()

class CybernetAPI:
    """Cybernet Agent API"""
    
    def __init__(self, app: Flask = None):
        self.app = app or Flask(__name__)
        self.monitor = Monitor()
        self.threat_detector = ThreatDetector()
        self.alert_manager = AlertManager()
        self.setup_api()
    
    def setup_api(self):
        """Setup API routes"""
        CORS(self.app)
        
        # Health check
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({
                'status': 'healthy',
                'service': 'cybernet-agent',
                'version': '0.1.0',
                'timestamp': self._get_timestamp()
            })
        
        # System metrics
        @self.app.route('/api/v1/metrics/system', methods=['GET'])
        def get_system_metrics():
            try:
                metrics = self.monitor.system_metrics.collect()
                return jsonify({
                    'success': True,
                    'data': metrics,
                    'timestamp': self._get_timestamp()
                })
            except Exception as e:
                return self._error_response(str(e), 500)
        
        # Network monitoring
        @self.app.route('/api/v1/metrics/network', methods=['GET'])
        def get_network_metrics():
            try:
                connections = self.monitor.network_monitor.get_active_connections()
                status_counts = self.monitor.network_monitor.get_connection_count_by_status()
                return jsonify({
                    'success': True,
                    'data': {
                        'active_connections': len(connections),
                        'connection_status': status_counts,
                        'connections': connections[:50]  # Limit response size
                    },
                    'timestamp': self._get_timestamp()
                })
            except Exception as e:
                return self._error_response(str(e), 500)
        
        # Process monitoring
        @self.app.route('/api/v1/metrics/processes', methods=['GET'])
        def get_process_metrics():
            try:
                top_cpu = self.monitor.process_monitor.get_top_processes('cpu', 10)
                top_memory = self.monitor.process_monitor.get_top_processes('memory', 10)
                total = self.monitor.process_monitor.get_process_count()
                return jsonify({
                    'success': True,
                    'data': {
                        'total_processes': total,
                        'top_by_cpu': top_cpu,
                        'top_by_memory': top_memory,
                    },
                    'timestamp': self._get_timestamp()
                })
            except Exception as e:
                return self._error_response(str(e), 500)
        
        # Collect all metrics
        @self.app.route('/api/v1/metrics', methods=['GET'])
        def get_all_metrics():
            try:
                metrics = self.monitor.collect_all_metrics()
                threats = self.threat_detector.detect_threats(metrics)
                
                # Create alerts for threats
                for threat in threats:
                    self.alert_manager.create_alert(threat)
                
                return jsonify({
                    'success': True,
                    'data': {
                        'metrics': metrics,
                        'threats_detected': len(threats),
                        'threats': [t.to_dict() for t in threats]
                    },
                    'timestamp': self._get_timestamp()
                })
            except Exception as e:
                return self._error_response(str(e), 500)
        
        # Threat analysis endpoint
        @self.app.route('/api/v1/threats/analyze', methods=['POST'])
        def analyze_threats():
            try:
                data = request.get_json()
                if not data or 'input' not in data:
                    return self._error_response('Missing input field', 400)
                
                text_input = data.get('input', '')
                threats = self.threat_detector.analyze_input(text_input)
                
                # Create alerts
                for threat in threats:
                    self.alert_manager.create_alert(threat)
                
                return jsonify({
                    'success': True,
                    'data': {
                        'input_analyzed': True,
                        'threats_found': len(threats),
                        'threats': [t.to_dict() for t in threats]
                    },
                    'timestamp': self._get_timestamp()
                })
            except Exception as e:
                return self._error_response(str(e), 500)
        
        # Get threats history
        @self.app.route('/api/v1/threats', methods=['GET'])
        def get_threats():
            try:
                limit = request.args.get('limit', 100, type=int)
                threats = self.threat_detector.get_threats(limit)
                counts = self.threat_detector.get_threat_count_by_level()
                return jsonify({
                    'success': True,
                    'data': {
                        'threats': threats,
                        'total': len(threats),
                        'count_by_level': counts
                    },
                    'timestamp': self._get_timestamp()
                })
            except Exception as e:
                return self._error_response(str(e), 500)
        
        # Get alerts history
        @self.app.route('/api/v1/alerts', methods=['GET'])
        def get_alerts():
            try:
                limit = request.args.get('limit', 100, type=int)
                alerts = self.alert_manager.get_alerts(limit)
                counts = self.alert_manager.get_alert_count_by_channel()
                return jsonify({
                    'success': True,
                    'data': {
                        'alerts': alerts,
                        'total': len(alerts),
                        'count_by_channel': counts,
                        'critical_count': self.alert_manager.critical_count,
                        'high_count': self.alert_manager.high_count,
                    },
                    'timestamp': self._get_timestamp()
                })
            except Exception as e:
                return self._error_response(str(e), 500)
        
        # Status endpoint
        @self.app.route('/api/v1/status', methods=['GET'])
        def get_status():
            try:
                return jsonify({
                    'success': True,
                    'data': {
                        'agent_running': self.monitor.is_running,
                        'threats_detected': len(self.threat_detector.threats),
                        'alerts_sent': len(self.alert_manager.alerts),
                        'critical_alerts': len(self.alert_manager.get_critical_alerts()),
                    },
                    'timestamp': self._get_timestamp()
                })
            except Exception as e:
                return self._error_response(str(e), 500)
        
        # Start monitoring
        @self.app.route('/api/v1/control/start', methods=['POST'])
        def start_monitoring():
            try:
                self.monitor.start()
                return jsonify({
                    'success': True,
                    'message': 'Monitoring started',
                    'timestamp': self._get_timestamp()
                })
            except Exception as e:
                return self._error_response(str(e), 500)
        
        # Stop monitoring
        @self.app.route('/api/v1/control/stop', methods=['POST'])
        def stop_monitoring():
            try:
                self.monitor.stop()
                return jsonify({
                    'success': True,
                    'message': 'Monitoring stopped',
                    'timestamp': self._get_timestamp()
                })
            except Exception as e:
                return self._error_response(str(e), 500)
        
        # Error handler
        @self.app.errorhandler(404)
        def not_found(error):
            return self._error_response('Endpoint not found', 404)
        
        @self.app.errorhandler(500)
        def server_error(error):
            return self._error_response('Internal server error', 500)
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    @staticmethod
    def _error_response(message: str, status_code: int) -> tuple:
        """Create error response"""
        return jsonify({
            'success': False,
            'error': message,
            'timestamp': CybernetAPI._get_timestamp()
        }), status_code
    
    def run(self, host: str = None, port: int = None, debug: bool = None):
        """Run the API server"""
        host = host or config.API_HOST
        port = port or config.API_PORT
        debug = debug if debug is not None else config.DEBUG
        
        logger.info(f"Starting API server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


def create_app() -> Flask:
    """Factory function to create Flask app"""
    app = Flask(__name__)
    api = CybernetAPI(app)
    return app
