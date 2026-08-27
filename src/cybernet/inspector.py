"""Portal inspector for dynamic page analysis without hardcoded selectors"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class PageElement:
    """Represents a discovered page element"""
    element_type: str        # button, link, input, table, dropdown, etc
    role: Optional[str]     # accessible role
    visible_text: str        # visible text content
    label: Optional[str]     # associated label (for inputs)
    placeholder: Optional[str] # placeholder text (for inputs)
    is_interactive: bool     # can be clicked/filled
    accessible: bool         # accessible via role/label
    description: str = ""    # what it might do

class PortalInspector:
    """Inspect and analyze the real portal page structure"""
    
    def __init__(self, page):
        self.page = page
        self.last_inspection: Optional[Dict[str, Any]] = None
        self.last_inspection_time: Optional[datetime] = None
    
    async def get_page_info(self) -> Dict[str, Any]:
        """Get basic page information"""
        try:
            title = await self.page.title()
            url = self.page.url
            
            # Get page content summary
            body_text = await self.page.inner_text('body')
            text_length = len(body_text)
            
            return {
                'title': title,
                'url': url,
                'text_length': text_length,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting page info: {str(e)}")
            return {'error': str(e)}
    
    async def inspect_page(self) -> Dict[str, Any]:
        """Perform complete page inspection"""
        logger.info("Starting portal page inspection...")
        
        try:
            inspection = {
                'timestamp': datetime.now().isoformat(),
                'page_info': await self.get_page_info(),
                'buttons': await self._find_buttons(),
                'links': await self._find_links(),
                'inputs': await self._find_inputs(),
                'dropdowns': await self._find_dropdowns(),
                'tables': await self._find_tables(),
                'navigation': await self._find_navigation(),
                'visible_headings': await self._get_visible_headings(),
            }
            
            # Count elements
            total_elements = (
                len(inspection['buttons']) +
                len(inspection['links']) +
                len(inspection['inputs']) +
                len(inspection['dropdowns']) +
                len(inspection['tables'])
            )
            
            inspection['total_interactive_elements'] = total_elements
            
            self.last_inspection = inspection
            self.last_inspection_time = datetime.now()
            
            logger.info(f"Inspection complete: Found {total_elements} interactive elements")
            return inspection
        
        except Exception as e:
            logger.error(f"Inspection failed: {str(e)}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    async def _find_buttons(self) -> List[Dict[str, Any]]:
        """Find all buttons on the page"""
        logger.debug("Scanning for buttons...")
        buttons = []
        
        try:
            # Get buttons by role (most reliable)
            button_locators = await self.page.locator('[role="button"], button').all()
            
            for locator in button_locators:
                try:
                    text = await locator.inner_text()
                    text = text.strip()
                    
                    if not text:  # Skip empty buttons
                        continue
                    
                    is_visible = await locator.is_visible()
                    if not is_visible:
                        continue
                    
                    button_info = {
                        'type': 'button',
                        'text': text,
                        'visible': True,
                        'locator_strategy': 'role=button or tag=button'
                    }
                    
                    buttons.append(button_info)
                
                except Exception as e:
                    logger.debug(f"Error processing button: {str(e)}")
                    continue
            
            logger.debug(f"Found {len(buttons)} buttons")
            return buttons
        
        except Exception as e:
            logger.warning(f"Error finding buttons: {str(e)}")
            return []
    
    async def _find_links(self) -> List[Dict[str, Any]]:
        """Find all links on the page"""
        logger.debug("Scanning for links...")
        links = []
        
        try:
            link_locators = await self.page.locator('a[href]').all()
            
            for locator in link_locators:
                try:
                    text = await locator.inner_text()
                    text = text.strip()
                    href = await locator.get_attribute('href')
                    
                    if not text or not href:
                        continue
                    
                    is_visible = await locator.is_visible()
                    if not is_visible:
                        continue
                    
                    link_info = {
                        'type': 'link',
                        'text': text,
                        'href': href,
                        'visible': True,
                        'locator_strategy': 'tag=a[href]'
                    }
                    
                    links.append(link_info)
                
                except Exception as e:
                    logger.debug(f"Error processing link: {str(e)}")
                    continue
            
            logger.debug(f"Found {len(links)} links")
            return links
        
        except Exception as e:
            logger.warning(f"Error finding links: {str(e)}")
            return []
    
    async def _find_inputs(self) -> List[Dict[str, Any]]:
        """Find all input fields on the page"""
        logger.debug("Scanning for input fields...")
        inputs = []
        
        try:
            input_locators = await self.page.locator('input').all()
            
            for locator in input_locators:
                try:
                    input_type = await locator.get_attribute('type')
                    if input_type in ['hidden', 'submit', 'button']:
                        continue
                    
                    is_visible = await locator.is_visible()
                    if not is_visible:
                        continue
                    
                    placeholder = await locator.get_attribute('placeholder')
                    field_id = await locator.get_attribute('id')
                    field_name = await locator.get_attribute('name')
                    
                    # Find associated label
                    label_text = ""
                    if field_id:
                        try:
                            label_locator = self.page.locator(f"label[for='{field_id}']")
                            if await label_locator.is_visible():
                                label_text = await label_locator.inner_text()
                        except:
                            pass
                    
                    input_info = {
                        'type': 'input',
                        'input_type': input_type or 'text',
                        'placeholder': placeholder or '',
                        'label': label_text.strip() if label_text else '',
                        'id': field_id or '',
                        'name': field_name or '',
                        'visible': True,
                        'locator_strategy': 'tag=input or get_by_label()'
                    }
                    
                    inputs.append(input_info)
                
                except Exception as e:
                    logger.debug(f"Error processing input: {str(e)}")
                    continue
            
            logger.debug(f"Found {len(inputs)} input fields")
            return inputs
        
        except Exception as e:
            logger.warning(f"Error finding inputs: {str(e)}")
            return []
    
    async def _find_dropdowns(self) -> List[Dict[str, Any]]:
        """Find all dropdowns/select elements"""
        logger.debug("Scanning for dropdowns...")
        dropdowns = []
        
        try:
            # Find select elements
            select_locators = await self.page.locator('select').all()
            
            for locator in select_locators:
                try:
                    is_visible = await locator.is_visible()
                    if not is_visible:
                        continue
                    
                    field_id = await locator.get_attribute('id')
                    field_name = await locator.get_attribute('name')
                    
                    # Get options
                    options = []
                    option_locators = await locator.locator('option').all()
                    for opt in option_locators:
                        opt_text = await opt.inner_text()
                        opt_value = await opt.get_attribute('value')
                        if opt_text.strip():
                            options.append({
                                'text': opt_text.strip(),
                                'value': opt_value or opt_text.strip()
                            })
                    
                    dropdown_info = {
                        'type': 'dropdown',
                        'id': field_id or '',
                        'name': field_name or '',
                        'options_count': len(options),
                        'options': options,
                        'visible': True,
                        'locator_strategy': 'tag=select'
                    }
                    
                    dropdowns.append(dropdown_info)
                
                except Exception as e:
                    logger.debug(f"Error processing dropdown: {str(e)}")
                    continue
            
            logger.debug(f"Found {len(dropdowns)} dropdowns")
            return dropdowns
        
        except Exception as e:
            logger.warning(f"Error finding dropdowns: {str(e)}")
            return []
    
    async def _find_tables(self) -> List[Dict[str, Any]]:
        """Find all tables on the page"""
        logger.debug("Scanning for tables...")
        tables = []
        
        try:
            table_locators = await self.page.locator('table').all()
            
            for table_locator in table_locators:
                try:
                    is_visible = await table_locator.is_visible()
                    if not is_visible:
                        continue
                    
                    # Get headers
                    headers = []
                    header_locators = await table_locator.locator('thead th').all()
                    for header in header_locators:
                        text = await header.inner_text()
                        if text.strip():
                            headers.append(text.strip())
                    
                    # Get row count
                    body_rows = await table_locator.locator('tbody tr').all()
                    row_count = len(body_rows)
                    
                    # Get sample row data
                    sample_rows = []
                    for i, row in enumerate(body_rows[:3]):  # First 3 rows
                        cells = await row.locator('td').all()
                        row_data = []
                        for cell in cells:
                            text = await cell.inner_text()
                            row_data.append(text.strip())
                        sample_rows.append(row_data)
                    
                    table_info = {
                        'type': 'table',
                        'headers': headers,
                        'row_count': row_count,
                        'sample_rows': sample_rows,
                        'visible': True,
                        'locator_strategy': 'tag=table'
                    }
                    
                    tables.append(table_info)
                
                except Exception as e:
                    logger.debug(f"Error processing table: {str(e)}")
                    continue
            
            logger.debug(f"Found {len(tables)} tables")
            return tables
        
        except Exception as e:
            logger.warning(f"Error finding tables: {str(e)}")
            return []
    
    async def _find_navigation(self) -> List[Dict[str, str]]:
        """Find navigation menus/links"""
        logger.debug("Scanning for navigation...")
        navigation = []
        
        try:
            # Look for nav element
            nav_items = []
            nav_locators = await self.page.locator('nav a').all()
            for nav in nav_locators:
                text = await nav.inner_text()
                href = await nav.get_attribute('href')
                if text.strip():
                    nav_items.append({
                        'type': 'nav_link',
                        'text': text.strip(),
                        'href': href or '#'
                    })
            
            # Look for menu items
            menu_locators = await self.page.locator('[role="menuitem"]').all()
            for menu in menu_locators:
                text = await menu.inner_text()
                if text.strip():
                    nav_items.append({
                        'type': 'menu_item',
                        'text': text.strip()
                    })
            
            logger.debug(f"Found {len(nav_items)} navigation items")
            return nav_items
        
        except Exception as e:
            logger.warning(f"Error finding navigation: {str(e)}")
            return []
    
    async def _get_visible_headings(self) -> List[str]:
        """Extract visible headings and main text"""
        logger.debug("Extracting visible content...")
        headings = []
        
        try:
            # Get all headings
            for level in range(1, 4):  # h1, h2, h3
                heading_locators = await self.page.locator(f"h{level}").all()
                for heading in heading_locators:
                    text = await heading.inner_text()
                    if text.strip():
                        headings.append(text.strip())
            
            logger.debug(f"Found {len(headings)} headings")
            return headings
        
        except Exception as e:
            logger.warning(f"Error extracting headings: {str(e)}")
            return []
    
    async def check_authentication(self) -> Dict[str, Any]:
        """Check if user is authenticated"""
        logger.info("Checking authentication status...")
        
        try:
            # Method 1: Look for logout button
            logout_btn = await self.page.locator('button:has-text("Logout"), button:has-text("Sign Out"), button:has-text("Log Out")').count()
            if logout_btn > 0:
                logger.info("Authentication detected: Found logout button")
                return {
                    'authenticated': True,
                    'indicator': 'logout_button',
                    'method': 'Found logout button in UI'
                }
            
            # Method 2: Look for user profile display
            profile = await self.page.locator('[data-menu="user-profile"], .user-profile, [class*="profile"]').count()
            if profile > 0:
                logger.info("Authentication detected: Found user profile")
                return {
                    'authenticated': True,
                    'indicator': 'user_profile',
                    'method': 'Found user profile indicator'
                }
            
            # Method 3: Check for login form
            login_form = await self.page.locator('form[id*="login"], [data-form="login"]').count()
            if login_form > 0:
                logger.info("Not authenticated: Login form detected")
                return {
                    'authenticated': False,
                    'indicator': 'login_form',
                    'method': 'Login form is visible'
                }
            
            # Default: Assume not authenticated if no clear indicator
            logger.warning("Could not definitively determine authentication status")
            return {
                'authenticated': False,
                'indicator': 'unknown',
                'method': 'Could not find authentication indicators'
            }
        
        except Exception as e:
            logger.error(f"Error checking authentication: {str(e)}")
            return {
                'authenticated': False,
                'error': str(e),
                'method': 'Error during check'
            }
