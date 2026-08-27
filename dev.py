#!/usr/bin/env python3
"""Run the application in development mode"""

import sys
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup path
Path('data').mkdir(exist_ok=True)
Path('logs').mkdir(exist_ok=True)

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    try:
        from src.main import main as app_main
        return app_main()
    except ImportError as e:
        logger.error(f"Import error: {str(e)}")
        logger.error("Make sure all dependencies are installed: pip install -r requirements.txt")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
