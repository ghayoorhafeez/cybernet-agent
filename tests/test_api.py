"""Integration tests for API"""

import pytest
import json
from src.api import create_app

@pytest.fixture
def client():
    """Create Flask test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestHealthEndpoint:
    """Tests for health endpoint"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'cybernet-agent'

class TestMetricsEndpoints:
    """Tests for metrics endpoints"""
    
    def test_system_metrics(self, client):
        """Test system metrics endpoint"""
        response = client.get('/api/v1/metrics/system')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        assert 'data' in data
    
    def test_network_metrics(self, client):
        """Test network metrics endpoint"""
        response = client.get('/api/v1/metrics/network')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        assert 'data' in data
    
    def test_process_metrics(self, client):
        """Test process metrics endpoint"""
        response = client.get('/api/v1/metrics/processes')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        assert 'data' in data
    
    def test_all_metrics(self, client):
        """Test all metrics endpoint"""
        response = client.get('/api/v1/metrics')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        assert 'metrics' in data['data']
        assert 'threats_detected' in data['data']

class TestThreatAnalysisEndpoint:
    """Tests for threat analysis endpoint"""
    
    def test_analyze_threats(self, client):
        """Test threat analysis endpoint"""
        response = client.post(
            '/api/v1/threats/analyze',
            data=json.dumps({'input': "'; DROP TABLE; <script>alert('xss')</script>"}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        assert 'threats' in data['data']
    
    def test_analyze_threats_missing_input(self, client):
        """Test threat analysis with missing input"""
        response = client.post(
            '/api/v1/threats/analyze',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert not data['success']

class TestThreatHistoryEndpoint:
    """Tests for threat history endpoint"""
    
    def test_get_threats(self, client):
        """Test getting threat history"""
        response = client.get('/api/v1/threats')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        assert 'threats' in data['data']
        assert 'count_by_level' in data['data']

class TestAlertEndpoint:
    """Tests for alerts endpoint"""
    
    def test_get_alerts(self, client):
        """Test getting alerts"""
        response = client.get('/api/v1/alerts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        assert 'alerts' in data['data']
        assert 'count_by_channel' in data['data']

class TestStatusEndpoint:
    """Tests for status endpoint"""
    
    def test_get_status(self, client):
        """Test getting agent status"""
        response = client.get('/api/v1/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
        assert 'threats_detected' in data['data']
        assert 'alerts_sent' in data['data']

class TestControlEndpoints:
    """Tests for control endpoints"""
    
    def test_start_monitoring(self, client):
        """Test starting monitoring"""
        response = client.post('/api/v1/control/start')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']
    
    def test_stop_monitoring(self, client):
        """Test stopping monitoring"""
        response = client.post('/api/v1/control/stop')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success']

class TestErrorHandling:
    """Tests for error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error handling"""
        response = client.get('/api/v1/nonexistent')
        assert response.status_code == 404
