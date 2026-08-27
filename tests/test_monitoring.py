"""Unit tests for monitoring module"""

import pytest
from src.monitoring import SystemMetrics, NetworkMonitor, ProcessMonitor, Monitor
from src.logger import get_logger

logger = get_logger()

class TestSystemMetrics:
    """Tests for SystemMetrics"""
    
    def test_collect_metrics(self):
        """Test collecting system metrics"""
        metrics = SystemMetrics()
        result = metrics.collect()
        
        assert isinstance(result, dict)
        assert 'timestamp' in result
        assert 'cpu_percent' in result
        assert 'memory' in result
        assert 'disk' in result
        assert 'network' in result
    
    def test_memory_info(self):
        """Test memory info collection"""
        metrics = SystemMetrics()
        memory = metrics._get_memory_info()
        
        assert 'total' in memory
        assert 'available' in memory
        assert 'percent' in memory
        assert 0 <= memory['percent'] <= 100
    
    def test_disk_info(self):
        """Test disk info collection"""
        metrics = SystemMetrics()
        disk = metrics._get_disk_info()
        
        assert 'total' in disk
        assert 'used' in disk
        assert 'free' in disk
        assert 'percent' in disk
    
    def test_metrics_history(self):
        """Test metrics history tracking"""
        metrics = SystemMetrics()
        metrics.collect()
        metrics.collect()
        
        history = metrics.get_history(limit=5)
        assert len(history) >= 2
    
    def test_average_metrics(self):
        """Test average metrics calculation"""
        metrics = SystemMetrics()
        for _ in range(5):
            metrics.collect()
        
        avg = metrics.get_average_metrics(window=3)
        assert 'avg_cpu_percent' in avg
        assert avg['samples'] > 0


class TestNetworkMonitor:
    """Tests for NetworkMonitor"""
    
    def test_get_active_connections(self):
        """Test getting active connections"""
        monitor = NetworkMonitor()
        connections = monitor.get_active_connections()
        
        assert isinstance(connections, list)
        if connections:
            conn = connections[0]
            assert 'status' in conn
            assert 'laddr' in conn
    
    def test_connection_count_by_status(self):
        """Test connection status counts"""
        monitor = NetworkMonitor()
        status_counts = monitor.get_connection_count_by_status()
        
        assert isinstance(status_counts, dict)
    
    def test_connection_history(self):
        """Test connection history tracking"""
        monitor = NetworkMonitor()
        monitor.get_active_connections()
        monitor.get_active_connections()
        
        history = monitor.get_connection_history(limit=5)
        assert len(history) >= 1


class TestProcessMonitor:
    """Tests for ProcessMonitor"""
    
    def test_get_process_count(self):
        """Test getting process count"""
        monitor = ProcessMonitor()
        count = monitor.get_process_count()
        
        assert isinstance(count, int)
        assert count > 0
    
    def test_get_top_processes_cpu(self):
        """Test getting top processes by CPU"""
        monitor = ProcessMonitor()
        processes = monitor.get_top_processes('cpu', 5)
        
        assert isinstance(processes, list)
        assert len(processes) <= 5
    
    def test_get_top_processes_memory(self):
        """Test getting top processes by memory"""
        monitor = ProcessMonitor()
        processes = monitor.get_top_processes('memory', 5)
        
        assert isinstance(processes, list)
        assert len(processes) <= 5


class TestMonitor:
    """Tests for Monitor orchestrator"""
    
    def test_collect_all_metrics(self):
        """Test collecting all metrics"""
        monitor = Monitor()
        metrics = monitor.collect_all_metrics()
        
        assert 'timestamp' in metrics
        assert 'system' in metrics
        assert 'network' in metrics
        assert 'processes' in metrics
    
    def test_start_stop(self):
        """Test starting and stopping monitor"""
        monitor = Monitor()
        assert not monitor.is_running
        
        monitor.start()
        assert monitor.is_running
        
        monitor.stop()
        assert not monitor.is_running
