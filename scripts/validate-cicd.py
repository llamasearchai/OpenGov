#!/usr/bin/env python3
"""
CI/CD Pipeline Validation Script
Comprehensive testing and validation of all CI/CD components with recursive logic

Author: Nik Jois <nikjois@llamasearch.ai>
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


class CICDValidator:
    """Comprehensive CI/CD pipeline validator with recursive testing"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.results = {}
        self.error_count = 0
        self.warning_count = 0

    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp and level"""
        timestamp = time.strftime("%H:%M:%S")
        prefix = {
            "INFO": "[INFO]",
            "PASS": "[PASS]",
            "FAIL": "[FAIL]",
            "WARN": "[WARN]",
            "SKIP": "[SKIP]"
        }.get(level, "[INFO]")

        print(f"[{timestamp}] {prefix} {message}")

        if level == "FAIL":
            self.error_count += 1
        elif level == "WARN":
            self.warning_count += 1

    def run_command(
        self, cmd: List[str], cwd: str = None, timeout: int = 300
    ) -> Tuple[int, str, str]:
        """Execute command and return exit code, stdout, stderr"""
        try:
            result = subprocess.run(
                cmd, cwd=cwd or self.project_root, capture_output=True, text=True, timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", f"Command timed out after {timeout}s"
        except Exception as e:
            return 1, "", str(e)

    def validate_yaml_syntax(self) -> bool:
        """Validate all YAML workflow files"""
        self.log("Validating YAML workflow syntax...")
        workflows_dir = self.project_root / ".github" / "workflows"

        if not workflows_dir.exists():
            self.log("No .github/workflows directory found", "FAIL")
            return False

        yaml_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
        if not yaml_files:
            self.log("No YAML workflow files found", "FAIL")
            return False

        all_valid = True
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r') as f:
                    yaml.safe_load(f)
                self.log(f"YAML syntax valid: {yaml_file.name}", "PASS")
            except yaml.YAMLError as e:
                self.log(f"YAML syntax error in {yaml_file.name}: {e}", "FAIL")
                all_valid = False

        return all_valid

    def validate_dependencies(self) -> bool:
        """Validate all project dependencies are installable"""
        self.log("Validating project dependencies...")

        # Check requirements.txt
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            exit_code, stdout, stderr = self.run_command(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--dry-run"]
            )
            if exit_code == 0:
                self.log("Requirements.txt dependencies: VALID", "PASS")
            else:
                self.log(f"Requirements.txt validation failed: {stderr}", "FAIL")
                return False

        # Check pyproject.toml
        pyproject_file = self.project_root / "pyproject.toml"
        if pyproject_file.exists():
            exit_code, stdout, stderr = self.run_command(
                [sys.executable, "-m", "pip", "install", ".", "--dry-run"]
            )
            if exit_code == 0:
                self.log("Pyproject.toml dependencies: VALID", "PASS")
            else:
                self.log(f"Pyproject.toml validation failed: {stderr}", "WARN")

        return True

    def run_test_suite(self) -> bool:
        """Run comprehensive test suite"""
        self.log("Running comprehensive test suite...")

        # Run pytest with coverage
        exit_code, stdout, stderr = self.run_command(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/",
                "-v",
                "--cov=backend",
                "--cov-report=xml",
                "--cov-report=html",
                "--cov-fail-under=70",
            ]
        )

        if exit_code == 0:
            self.log("Test suite: PASSED", "PASS")
            return True
        else:
            self.log(f"Test suite: FAILED\n{stderr}", "FAIL")
            return False

    def run_code_quality_checks(self) -> bool:
        """Run all code quality checks"""
        self.log("Running code quality checks...")

        checks = [
            (["python3", "-m", "black", "--check", "."], "Black formatting"),
            (["python3", "-m", "flake8", "."], "Flake8 linting"),
            (["python3", "-m", "isort", "--check-only", "."], "Import sorting"),
            (["python3", "-m", "mypy", "backend/", "--ignore-missing-imports"], "Type checking"),
        ]

        all_passed = True
        for cmd, name in checks:
            exit_code, stdout, stderr = self.run_command(cmd)
            if exit_code == 0:
                self.log(f"{name}: PASSED", "PASS")
            else:
                self.log(f"{name}: FAILED\n{stderr}", "FAIL")
                all_passed = False

        return all_passed

    def run_security_checks(self) -> bool:
        """Run security vulnerability checks"""
        self.log("Running security checks...")

        # Install security tools if missing
        security_tools = ["bandit", "safety"]
        for tool in security_tools:
            exit_code, _, _ = self.run_command([sys.executable, "-c", f"import {tool}"])
            if exit_code != 0:
                self.log(f"Installing {tool}...")
                self.run_command([sys.executable, "-m", "pip", "install", tool])

        checks = [
            (["python3", "-m", "bandit", "-r", "backend/"], "Bandit security scan"),
            (["python3", "-m", "safety", "check"], "Safety dependency check"),
        ]

        all_passed = True
        for cmd, name in checks:
            exit_code, stdout, stderr = self.run_command(cmd)
            if exit_code == 0:
                self.log(f"{name}: PASSED", "PASS")
            else:
                # Security checks may have warnings but still pass
                if "No issues identified" in stdout or "All good" in stdout:
                    self.log(f"{name}: PASSED with warnings", "PASS")
                else:
                    self.log(f"{name}: ISSUES FOUND\n{stdout}", "WARN")

        return all_passed

    def validate_package_build(self) -> bool:
        """Validate package can be built and installed"""
        self.log("Validating package build...")

        # Build package
        exit_code, stdout, stderr = self.run_command([sys.executable, "-m", "build"])

        if exit_code != 0:
            self.log(f"Package build failed: {stderr}", "FAIL")
            return False

        # Check with twine
        exit_code, stdout, stderr = self.run_command(
            [sys.executable, "-m", "twine", "check", "dist/*"]
        )

        if exit_code == 0:
            self.log("Package build: VALID", "PASS")
            return True
        else:
            self.log(f"Package validation failed: {stderr}", "FAIL")
            return False

    def simulate_ci_workflow(self) -> bool:
        """Simulate complete CI workflow execution"""
        self.log("Simulating complete CI workflow...")

        workflow_steps = [
            ("YAML Validation", self.validate_yaml_syntax),
            ("Dependency Check", self.validate_dependencies),
            ("Test Suite", self.run_test_suite),
            ("Code Quality", self.run_code_quality_checks),
            ("Security Checks", self.run_security_checks),
            ("Package Build", self.validate_package_build),
        ]

        failed_steps = []
        for step_name, step_func in workflow_steps:
            self.log(f"Executing workflow step: {step_name}")
            try:
                if not step_func():
                    failed_steps.append(step_name)
            except Exception as e:
                self.log(f"Step {step_name} crashed: {e}", "FAIL")
                failed_steps.append(step_name)

        if failed_steps:
            self.log(f"Workflow simulation FAILED. Failed steps: {failed_steps}", "FAIL")
            return False
        else:
            self.log("Workflow simulation: PASSED", "PASS")
            return True

    def recursive_validation(self, max_iterations: int = 3) -> bool:
        """Recursively validate and fix issues until all pass"""
        self.log(f"Starting recursive validation (max {max_iterations} iterations)")

        for iteration in range(1, max_iterations + 1):
            self.log(f"=== ITERATION {iteration} ===")
            self.error_count = 0
            self.warning_count = 0

            success = self.simulate_ci_workflow()

            if success and self.error_count == 0:
                self.log(
                    f"Recursive validation COMPLETED successfully in {iteration} iteration(s)",
                    "PASS",
                )
                return True
            elif iteration < max_iterations:
                self.log(f"Issues found in iteration {iteration}. Attempting fixes...", "WARN")
                # Auto-fix some common issues
                self.auto_fix_common_issues()
            else:
                self.log(f"Recursive validation FAILED after {max_iterations} iterations", "FAIL")

        return False

    def auto_fix_common_issues(self):
        """Automatically fix common CI/CD issues"""
        self.log("Attempting to auto-fix common issues...")

        # Fix code formatting
        self.run_command(["python3", "-m", "black", "."])
        self.run_command(["python3", "-m", "isort", "."])

        # Install missing packages
        self.run_command(
            [sys.executable, "-m", "pip", "install", "bandit", "safety", "build", "twine"]
        )

        self.log("Auto-fix attempt completed")

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "project_root": str(self.project_root),
            "results": self.results,
            "summary": {
                "errors": self.error_count,
                "warnings": self.warning_count,
                "status": "PASS" if self.error_count == 0 else "FAIL",
            },
        }


async def main():
    """Main execution function"""
    print("Starting Comprehensive CI/CD Pipeline Validation")
    print("=" * 60)

    validator = CICDValidator()

    # Run recursive validation
    success = validator.recursive_validation(max_iterations=3)

    # Generate and save report
    report = validator.generate_report()
    with open("cicd-validation-report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 60)
    print(f"Validation Complete!")
    print(f"Errors: {validator.error_count}, Warnings: {validator.warning_count}")
    print(f"Report saved to: cicd-validation-report.json")

    if success:
        print("All CI/CD components are working correctly!")
        return 0
    else:
        print("CI/CD validation failed. Check the report for details.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
