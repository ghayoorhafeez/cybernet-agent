"""Monitoring module for system and network metrics"""

import time
import psutil
from typing import Dict, Any, List
from datetime import datetime
from src.logger import get_logger

logger = get_logger()

class SystemMetrics:
    """Collect system metrics"""
    
    def __init__(self):
        self.metrics_history: List[Dict[str, Any]] = []
        self.max_history = 1000
    
    def collect(self) -> Dict[str, Any]:
        """Collect current system metrics"""
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory': self._get_memory_info(),
                'disk': self._get_disk_info(),
                'network': self._get_network_info(),
                'processes': len(psutil.pids()),
            }
            
            # Store in history
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > self.max_history:
                self.metrics_history.pop(0)
            
            logger.debug(f"Collected system metrics: CPU={metrics['cpu_percent']}%")
            return metrics
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
            return {}
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Get memory information"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'percent': mem.percent,
            'used': mem.used,
            'free': mem.free,
        }
    
    def _get_disk_info(self) -> Dict[str, Any]:
        """Get disk information"""
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent,
        }
    
    def _get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        try:
            net_if_stats = psutil.net_if_stats()
            net_io = psutil.net_io_counters()
            
            interfaces = {}
            for iface, stats in net_if_stats.items():
                interfaces[iface] = {
                    'isup': stats.isup,
                    'speed': stats.speed,
                    'mtu': stats.mtu,
                    'duplex': str(stats.duplex),
                }
            
            return {
                'interfaces': interfaces,
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
            }
        except Exception as e:
            logger.warning(f"Error collecting network metrics: {str(e)}")
            return {}
    
    def get_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get metrics history"""
        return self.metrics_history[-limit:]
    
    def get_average_metrics(self, window: int = 10) -> Dict[str, float]:
        """Get average metrics over a time window"""
        if not self.metrics_history or window <= 0:
            return {}
        
        recent = self.metrics_history[-window:]
        cpu_values = [m['cpu_percent'] for m in recent if 'cpu_percent' in m]
        
        avg_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else 0
        
        return {
            'avg_cpu_percent': avg_cpu,
            'samples': len(recent),
        }


class NetworkMonitor:
    """Monitor network connections and activity"""
    
    def __init__(self):
        self.connection_history: List[Dict[str, Any]] = []
        self.max_history = 1000
    
    def get_active_connections(self) -> List[Dict[str, Any]]:
        """Get active network connections"""
        try:
            connections = []
            for conn in psutil.net_connections():
                connections.append({
                    'fd': conn.fd,
                    'family': str(conn.family),
                    'type': str(conn.type),
                    'laddr': str(conn.laddr) if conn.laddr else None,
                    'raddr': str(conn.raddr) if conn.raddr else None,
                    'status': conn.status,
                    'pid': conn.pid,
                })
            
            # Store in history
            self.connection_history.append({
                'timestamp': datetime.now().isoformat(),
                'connections': connections,
                'count': len(connections),
            })
            
            if len(self.connection_history) > self.max_history:
                self.connection_history.pop(0)
            
            logger.debug(f"Found {len(connections)} active connections")
            return connections
        except Exception as e:
            logger.error(f"Error monitoring network connections: {str(e)}")
            return []
    
    def get_connection_count_by_status(self) -> Dict[str, int]:
        """Get count of connections by status"""
        try:
            connections = psutil.net_connections()
            status_counts = {}
            for conn in connections:
                status = conn.status
                status_counts[status] = status_counts.get(status, 0) + 1
            return status_counts
        except Exception as e:
            logger.error(f"Error getting connection status counts: {str(e)}")
            return {}
    
    def get_connection_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get connection history"""
        return self.connection_history[-limit:]


class ProcessMonitor:
    """Monitor running processes"""
    
    def __init__(self):
        self.process_history: List[Dict[str, Any]] = []
        self.max_history = 500
    
    def get_top_processes(self, by: str = 'cpu', limit: int = 10) -> List[Dict[str, Any]]:
        """Get top processes by CPU or memory usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by specified metric
            if by == 'cpu':
                processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            elif by == 'memory':
                processes.sort(key=lambda x: x.get('memory_percent', 0), reverse=True)
            
            result = processes[:limit]
            logger.debug(f"Found top {limit} processes by {by}")
            return result
        except Exception as e:
            logger.error(f"Error getting top processes: {str(e)}")
            return []
    
    def get_process_count(self) -> int:
        """Get total number of running processes"""
        try:
            return len(psutil.pids())
        except Exception as e:
            logger.error(f"Error getting process count: {str(e)}")
            return 0


class Monitor:
    """Main monitoring orchestrator"""
    
    def __init__(self):
        self.system_metrics = SystemMetrics()
        self.network_monitor = NetworkMonitor()
        self.process_monitor = ProcessMonitor()
        self.is_running = False
    
    def collect_all_metrics(self) -> Dict[str, Any]:
        """Collect all metrics"""
        return {
            'timestamp': datetime.now().isoformat(),
            'system': self.system_metrics.collect(),
            'network': {
                'active_connections': len(self.network_monitor.get_active_connections()),
                'connection_status': self.network_monitor.get_connection_count_by_status(),
            },
            'processes': {
                'total': self.process_monitor.get_process_count(),
                'top_by_cpu': self.process_monitor.get_top_processes('cpu', 5),
                'top_by_memory': self.process_monitor.get_top_processes('memory', 5),
            },
        }
    
    def start(self):
        """Start monitoring"""
        self.is_running = True
        logger.info("Monitor started")
    
    def stop(self):
        """Stop monitoring"""
        self.is_running = False
        logger.info("Monitor stopped")
