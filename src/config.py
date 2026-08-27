import os
import logging
from typing import Dict, Any
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = False
    
    # API Configuration
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    
    # Monitoring Configuration
    MONITOR_INTERVAL = int(os.getenv('MONITOR_INTERVAL', 60))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/cybernet-agent.log')
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///cybernet.db')
    
    # Alerting Configuration
    ALERT_THRESHOLD = float(os.getenv('ALERT_THRESHOLD', 0.7))
    ALERT_EMAIL = os.getenv('ALERT_EMAIL', '')
    
    # Security Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key-change-in-production')
    
    # Detection Configuration
    MAX_CONNECTIONS_THRESHOLD = int(os.getenv('MAX_CONNECTIONS_THRESHOLD', 1000))
    SUSPICIOUS_PORT_THRESHOLD = int(os.getenv('SUSPICIOUS_PORT_THRESHOLD', 5))
    
    @classmethod
    def from_file(cls, filepath: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(filepath, 'r') as f:
                config_dict = yaml.safe_load(f)
                return config_dict if config_dict else {}
        except FileNotFoundError:
            logging.warning(f"Configuration file {filepath} not found")
            return {}
    
    @classmethod
    def get_config(cls) -> 'Config':
        """Get the appropriate configuration based on environment"""
        env = os.getenv('FLASK_ENV', 'development')
        if env == 'production':
            return ProductionConfig()
        elif env == 'testing':
            return TestingConfig()
        else:
            return DevelopmentConfig()


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    ALERT_EMAIL = ''


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
