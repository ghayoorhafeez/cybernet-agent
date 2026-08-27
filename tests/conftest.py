"""Pytest configuration"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set environment to test mode
os.environ['MOCK_MODE'] = 'true'
os.environ['LOG_LEVEL'] = 'ERROR'
os.environ['DATABASE_PATH'] = ':memory:'
