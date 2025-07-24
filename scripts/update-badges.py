#!/usr/bin/env python3
"""
Badge Status Updater for CI/CD Pipeline
Verifies all components and updates README badges with current status

Author: Nik Jois <nikjois@llamasearch.ai>
"""

import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Tuple


class BadgeUpdater:
    """Updates README badges based on actual CI/CD status"""

    def __init__(self, readme_path: str = "README.md"):
        self.readme_path = Path(readme_path)
        self.badge_status = {}
        self.repository = "llamasearchai/OpenGov"

    def run_command(self, cmd: list, timeout: int = 60) -> Tuple[int, str, str]:
        """Execute command and return status"""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Timeout"
        except Exception as e:
            return 1, "", str(e)

    def check_test_status(self) -> str:
        """Check if tests are passing"""
        print("Checking test status...")
        exit_code, stdout, stderr = self.run_command(
            [sys.executable, "-m", "pytest", "tests/", "--tb=no", "-q"]
        )

        if exit_code == 0:
            return "passing"
        else:
            print(f"   Tests failing: {stderr}")
            return "failing"

    def check_build_status(self) -> str:
        """Check if package builds successfully"""
        print("Checking build status...")
        exit_code, stdout, stderr = self.run_command([sys.executable, "-m", "build", "--wheel"])

        if exit_code == 0:
            return "passing"
        else:
            print(f"   Build failing: {stderr}")
            return "failing"

    def check_code_quality(self) -> str:
        """Check code quality status"""
        print("Checking code quality...")

        # Check black formatting
        exit_code, _, _ = self.run_command([sys.executable, "-m", "black", "--check", "."])
        if exit_code != 0:
            print("   Black formatting: FAIL")
            return "failing"

        # Check import sorting
        exit_code, _, _ = self.run_command([sys.executable, "-m", "isort", "--check-only", "."])
        if exit_code != 0:
            print("   Import sorting: FAIL")
            return "failing"

        return "passing"

    def check_security_status(self) -> str:
        """Check security scan status"""
        print("Checking security status...")

        # Check bandit
        exit_code, stdout, stderr = self.run_command(
            [sys.executable, "-m", "bandit", "-r", "backend/", "-f", "json"]
        )

        if exit_code == 0 or "No issues identified" in stdout:
            return "passing"
        else:
            return "warning"

    def get_version(self) -> str:
        """Get current version from pyproject.toml"""
        try:
            with open("pyproject.toml", "r") as f:
                content = f.read()
                match = re.search(r'version = "([^"]+)"', content)
                if match:
                    return match.group(1)
        except Exception:
            pass
        return "unknown"

    def generate_badge_url(self, label: str, message: str, color: str) -> str:
        """Generate badge URL"""
        return f"https://img.shields.io/badge/{label}-{message}-{color}.svg"

    def get_status_color(self, status: str) -> str:
        """Get color for status"""
        colors = {
            "passing": "brightgreen",
            "failing": "red",
            "warning": "yellow",
            "unknown": "lightgrey",
        }
        return colors.get(status, "lightgrey")

    def update_badges(self):
        """Update all badges in README"""
        print("Starting CI/CD status verification and badge update...")

        # Check all statuses
        test_status = self.check_test_status()
        build_status = self.check_build_status()
        quality_status = self.check_code_quality()
        security_status = self.check_security_status()
        version = self.get_version()

        # Read current README
        if not self.readme_path.exists():
            print("ERROR: README.md not found")
            return False

        with open(self.readme_path, "r") as f:
            content = f.read()

        # Update CI/CD Pipeline badge
        ci_status = (
            "passing"
            if all(s == "passing" for s in [test_status, build_status, quality_status])
            else "failing"
        )
        ci_color = self.get_status_color(ci_status)

        # Generate new badges
        badges = {
            # CI/CD Pipeline - points to actual GitHub Actions
            r'\[!\[CI/CD Pipeline\].*?\]\(.*?\)': f'[![CI/CD Pipeline](https://github.com/{self.repository}/actions/workflows/ci.yml/badge.svg)](https://github.com/{self.repository}/actions/workflows/ci.yml)',
            # PyPI version badge
            r'\[!\[PyPI version\].*?\]\(.*?\)': f'[![PyPI version](https://badge.fury.io/py/govsecure-ai-platform.svg)](https://badge.fury.io/py/govsecure-ai-platform)',
            # Python version badge
            r'\[!\[Python 3\.9\+\].*?\]\(.*?\)': f'[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)',
            # Tests badge
            r'\[!\[Tests\].*?\]\(.*?\)': f'[![Tests](https://img.shields.io/badge/tests-{test_status}-{self.get_status_color(test_status)}.svg)](#testing)',
            # Build badge
            r'\[!\[Build\].*?\]\(.*?\)': f'[![Build](https://img.shields.io/badge/build-{build_status}-{self.get_status_color(build_status)}.svg)](#deployment)',
            # Code quality badge
            r'\[!\[Code style: black\].*?\]\(.*?\)': f'[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)',
            # Security badge
            r'\[!\[Security: bandit\].*?\]\(.*?\)': f'[![Security: bandit](https://img.shields.io/badge/security-bandit-{self.get_status_color(security_status)}.svg)](https://github.com/PyCQA/bandit)',
        }

        # Apply badge updates
        updated_content = content
        for pattern, replacement in badges.items():
            updated_content = re.sub(pattern, replacement, updated_content)

        # Add test and build badges if they don't exist
        if "![Tests]" not in updated_content and "[![Tests]" not in updated_content:
            # Insert after Python version badge
            python_badge_pattern = r'(\[!\[Python 3\.9\+\].*?\]\(.*?\))'
            replacement_with_tests = f'\\1\n[![Tests](https://img.shields.io/badge/tests-{test_status}-{self.get_status_color(test_status)}.svg)](#testing)\n[![Build](https://img.shields.io/badge/build-{build_status}-{self.get_status_color(build_status)}.svg)](#deployment)'
            updated_content = re.sub(python_badge_pattern, replacement_with_tests, updated_content)

        # Write updated content
        with open(self.readme_path, "w") as f:
            f.write(updated_content)

        # Print summary
        print("\nCI/CD Status Summary:")
        print(f"   Tests: {test_status}")
        print(f"   Build: {build_status}")
        print(f"   Code Quality: {quality_status}")
        print(f"   Security: {security_status}")
        print(f"   Version: {version}")
        print(f"   Overall CI/CD: {ci_status}")

        print(f"\nREADME badges updated successfully!")
        return True


def main():
    """Main execution"""
    updater = BadgeUpdater()
    success = updater.update_badges()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
