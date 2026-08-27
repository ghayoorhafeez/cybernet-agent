"""Playwright selector abstraction using modern APIs"""

import logging
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class SelectorStrategy(Enum):
    """Playwright selector strategies using modern APIs"""
    ROLE = "role"              # page.get_by_role()
    LABEL = "label"            # page.get_by_label()
    TEXT = "text"              # page.get_by_text()
    TEST_ID = "test_id"        # page.get_by_test_id()
    PLACEHOLDER = "placeholder" # page.get_by_placeholder()
    CSS = "css"                # page.locator() with CSS
    XPATH = "xpath"            # page.locator() with XPath

@dataclass
class PortalSelector:
    """Represents a portal element selector"""
    name: str                      # Human-readable name
    strategy: SelectorStrategy     # Selection strategy
    value: str                     # Selector value
    description: str = ""          # What this element does

class SelectorBuilder:
    """Build Playwright locators using appropriate strategy"""
    
    @staticmethod
    def build(page, selector: PortalSelector):
        """Build a Playwright locator for the given selector"""
        if selector.strategy == SelectorStrategy.ROLE:
            # page.get_by_role('button', name='Login')
            parts = selector.value.split(':')
            role = parts[0]
            name = parts[1] if len(parts) > 1 else None
            if name:
                return page.get_by_role(role, name=name)
            return page.get_by_role(role)
        
        elif selector.strategy == SelectorStrategy.LABEL:
            # page.get_by_label('Email')
            return page.get_by_label(selector.value)
        
        elif selector.strategy == SelectorStrategy.TEXT:
            # page.get_by_text('Search')
            return page.get_by_text(selector.value)
        
        elif selector.strategy == SelectorStrategy.TEST_ID:
            # page.get_by_test_id('customer-search-field')
            return page.get_by_test_id(selector.value)
        
        elif selector.strategy == SelectorStrategy.PLACEHOLDER:
            # page.get_by_placeholder('Search customer...')
            return page.get_by_placeholder(selector.value)
        
        elif selector.strategy == SelectorStrategy.CSS:
            # page.locator('button.primary')
            return page.locator(selector.value)
        
        elif selector.strategy == SelectorStrategy.XPATH:
            # page.locator('//button[contains(text(), "Login")]')
            return page.locator(selector.value)
        
        else:
            raise ValueError(f"Unknown selector strategy: {selector.strategy}")
