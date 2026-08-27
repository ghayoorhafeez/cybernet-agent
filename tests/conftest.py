"""Conftest for pytest"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))
