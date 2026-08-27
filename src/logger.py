import logging
import logging.handlers
import os
from typing import Optional
from src.config import Config

class Logger:
    """Custom logger for Cybernet Agent"""
    
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the logger"""
        config = Config()
        
        # Create logger
        self._logger = logging.getLogger('cybernet-agent')
        self._logger.setLevel(getattr(logging, config.LOG_LEVEL))
        
        # Ensure logs directory exists
        log_dir = os.path.dirname(config.LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # File handler
        file_handler = logging.handlers.RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, config.LOG_LEVEL))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    @staticmethod
    def get_logger() -> logging.Logger:
        """Get the logger instance"""
        return Logger()._logger


def get_logger() -> logging.Logger:
    """Convenience function to get logger"""
    return Logger.get_logger()
