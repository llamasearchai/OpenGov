#!/usr/bin/env python3
"""
Quick Test Runner - Validates core CI/CD functionality
Author: Nik Jois <nikjois@llamasearch.ai>
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run command and return result"""
    print(f"Testing {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"  PASS: {description}")
            return True
        else:
            print(f"  FAIL: {description}")
            if result.stderr:
                print(f"    Error: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: {description}")
        return False
    except Exception as e:
        print(f"  ERROR: {description} - {e}")
        return False


def main():
    """Run quick validation tests"""
    print("Quick CI/CD Validation")
    print("=" * 40)
    
    tests = [
        ([sys.executable, "-c", "import backend; print('Backend imports OK')"], "Backend imports"),
        ([sys.executable, "-m", "black", "--check", "--diff", "backend/core/config.py"], "Code formatting"),
        ([sys.executable, "-m", "build", "--wheel"], "Package build"),
        ([sys.executable, "-c", "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"], "Workflow YAML"),
    ]
    
    passed = 0
    total = len(tests)
    
    for cmd, desc in tests:
        if run_command(cmd, desc):
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All core tests PASSED")
        
        # Update README badges
        badge_script = Path("scripts/update-badges.py")
        if badge_script.exists():
            print("\nUpdating README badges...")
            subprocess.run([sys.executable, str(badge_script)], timeout=30)
        
        return 0
    else:
        print("Some tests FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 