"""Main entry point for Cybernet Agent"""

import sys
import time
from src.logger import get_logger
from src.config import Config
from src.api import create_app, CybernetAPI
from src.monitoring import Monitor
from src.detection import ThreatDetector
from src.alerting import AlertManager

logger = get_logger()
config = Config()

def main():
    """Main entry point"""
    logger.info("="*60)
    logger.info("Cybernet Agent - Phase 1 Initialized")
    logger.info("="*60)
    logger.info(f"Config: DEBUG={config.DEBUG}, LOG_LEVEL={config.LOG_LEVEL}")
    logger.info(f"API: {config.API_HOST}:{config.API_PORT}")
    
    # Create Flask app with API
    app = create_app()
    
    try:
        # Run API server
        logger.info("Starting Cybernet Agent API server...")
        api = CybernetAPI(app)
        api.run(host=config.API_HOST, port=config.API_PORT, debug=config.DEBUG)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
