"""Test runner script"""

import subprocess
import sys
import json
from pathlib import Path

def run_tests():
    """Run all tests and generate report"""
    print("\n" + "="*70)
    print("CYBERNET NBB AI VOICE OPERATOR - PHASE 1 TEST SUITE")
    print("="*70 + "\n")
    
    # Run pytest
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "--color=yes"
        ],
        capture_output=False
    )
    
    print("\n" + "="*70)
    if result.returncode == 0:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("="*70 + "\n")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
