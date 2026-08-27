#!/usr/bin/env python3
"""Run all tests and report results"""

import subprocess
import sys

def run_tests():
    """Run pytest with coverage"""
    print("\n" + "="*60)
    print("Running Phase 1 Tests")
    print("="*60 + "\n")
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd="."
    )
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
