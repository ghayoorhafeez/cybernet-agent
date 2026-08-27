"""Live Cybernet NBB Portal using Playwright - Inspection Only (Phase 1)"""

import logging
import asyncio
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from src.cybernet.inspector import PortalInspector

logger = logging.getLogger(__name__)

class LiveCybernetPortal:
    """Live Cybernet NBB portal with Playwright - Inspection only for Phase 1"""
    
    def __init__(self, headless: bool = False):
        self.portal_url = "https://partner.nationalbroadband.pk/"
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.inspector: Optional[PortalInspector] = None
        self.authenticated = False
        self.is_connected = False
    
    async def connect(self) -> bool:
        """Connect to the Cybernet portal"""
        try:
            logger.info("Connecting to Cybernet NBB portal...")
            logger.info(f"Portal URL: {self.portal_url}")
            logger.info(f"Headless mode: {self.headless}")
            
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=self.headless)
            self.context = await self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            self.page = await self.context.new_page()
            self.inspector = PortalInspector(self.page)
            
            logger.info("Navigating to portal...")
            await self.page.goto(self.portal_url, wait_until="networkidle", timeout=30000)
            
            self.is_connected = True
            logger.info("Successfully connected to portal")
            return True
        
        except Exception as e:
            logger.error(f"Failed to connect: {str(e)}")
            self.is_connected = False
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect from portal"""
        try:
            logger.info("Disconnecting from portal...")
            
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            
            self.is_connected = False
            self.authenticated = False
            logger.info("Disconnected")
            return True
        
        except Exception as e:
            logger.error(f"Error disconnecting: {str(e)}")
            return False
    
    async def wait_for_manual_authentication(self, timeout_seconds: int = 600) -> bool:
        """Wait for user to manually log in"""
        if not self.page:
            logger.error("Browser not connected")
            return False
        
        try:
            timeout_ms = timeout_seconds * 1000
            logger.info(f"Waiting for manual authentication (timeout: {timeout_seconds}s)")
            logger.info("Please log in to the portal in the browser window")
            
            # Wait for logout button (common authentication indicator)
            await self.page.wait_for_selector(
                'button:has-text("Logout"), button:has-text("Sign Out"), button:has-text("Log Out")',
                timeout=timeout_ms
            )
            
            self.authenticated = True
            logger.info("User authenticated successfully")
            
            # Wait a bit for page to fully load
            await self.page.wait_for_timeout(2000)
            
            return True
        
        except Exception as e:
            logger.warning(f"Authentication timeout or failed: {str(e)}")
            self.authenticated = False
            return False
    
    async def check_authentication_status(self) -> Dict[str, Any]:
        """Check current authentication status"""
        if not self.inspector:
            return {'error': 'Inspector not initialized'}
        
        auth_status = await self.inspector.check_authentication()
        self.authenticated = auth_status.get('authenticated', False)
        
        return auth_status
    
    async def inspect_current_page(self) -> Dict[str, Any]:
        """Inspect the current page structure"""
        if not self.inspector:
            return {'error': 'Inspector not initialized'}
        
        logger.info("Inspecting current page...")
        inspection_result = await self.inspector.inspect_page()
        
        # Add connection status to result
        inspection_result['connection_status'] = {
            'connected': self.is_connected,
            'authenticated': self.authenticated,
            'url': self.page.url if self.page else 'N/A'
        }
        
        return inspection_result
    
    async def get_page_title(self) -> str:
        """Get current page title"""
        if not self.page:
            return "Not connected"
        
        try:
            return await self.page.title()
        except Exception as e:
            logger.error(f"Error getting page title: {str(e)}")
            return "Error"
    
    async def get_page_url(self) -> str:
        """Get current page URL"""
        if not self.page:
            return "Not connected"
        
        return self.page.url
    
    # Phase 1: Inspection Only (No automation of login, activation, renewal)
    # Phase 2+: Will add actual portal operations
