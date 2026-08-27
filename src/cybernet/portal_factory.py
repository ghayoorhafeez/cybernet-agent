"""Portal factory for mode selection"""

import logging
import os
from typing import Union
from src.cybernet.mock_portal import MockCybernetPortal
from src.cybernet.live_portal import LiveCybernetPortal

logger = logging.getLogger(__name__)

class PortalFactory:
    """Factory for creating the appropriate portal implementation"""
    
    @staticmethod
    def create_portal(mode: str = None) -> Union[MockCybernetPortal, LiveCybernetPortal]:
        """Create portal instance based on mode"""
        if mode is None:
            mode = os.getenv('MOCK_MODE', 'true').lower()
        
        if mode == 'true' or mode == 'mock':
            logger.info("Using MOCK portal mode")
            return MockCybernetPortal()
        else:
            logger.info("Using LIVE portal mode")
            return LiveCybernetPortal(headless=False)
