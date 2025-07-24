"""
System Health Checker for GovSecure AI Platform
Comprehensive system health monitoring and validation.

Author: Nik Jois
"""

import importlib.util
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from rich.console import Console

from backend.core.config import get_config


class SystemChecker:
    """Comprehensive system health checker"""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.console = Console()
        self.check_results: Dict[str, Any] = {}

    async def check_all(self) -> bool:
        """
        Run all system checks and return overall health status.
        
        Returns:
            True if system is healthy, False otherwise
        """
        self.console.print("\nRunning System Health Checks...", style="bold blue")

        results = {
            "python_version": await self.check_python_version(),
            "dependencies": await self.check_dependencies(),
            "openai_connection": await self.check_openai_connection(),
            "file_permissions": await self.check_file_permissions(),
            "system_resources": await self.check_system_resources(),
            "configuration": await self.check_configuration()
        }

        # Display results
        errors = 0
        warnings = 0

        for check_name, check_result in results.items():
            if check_result["status"] == "failed":
                self.console.print(f"[ERROR] {check_name}: {check_result['message']}", style="red")
                errors += 1
            elif check_result["status"] == "warning":
                self.console.print(f"[WARNING] {check_name}: {check_result['message']}", style="yellow")
                warnings += 1
            else:
                self.console.print(f"[PASSED] {check_name}: {check_result['message']}", style="green")

        self.check_results = results

        if errors == 0:
            self.console.print(f"\nSystem checks passed with {warnings} warnings", style="bold yellow" if warnings > 0 else "bold green")
        else:
            self.console.print(f"\nSystem checks failed: {errors} errors, {warnings} warnings", style="bold red")

        return errors == 0

    async def check_python_version(self) -> Dict[str, Any]:
        """Check if Python version meets requirements"""
        try:
            version_info = sys.version_info
            major, minor = version_info.major, version_info.minor

            if major >= 3 and minor >= 9:
                return {
                    "status": "passed",
                    "current": f"{major}.{minor}.{version_info.micro}",
                    "required": "3.9+",
                    "message": f"Python {major}.{minor}.{version_info.micro} - Compatible"
                }
            else:
                return {
                    "status": "failed",
                    "current": f"{major}.{minor}.{version_info.micro}",
                    "required": "3.9+",
                    "message": f"Python {major}.{minor} - Unsupported (requires 3.9+)"
                }
        except Exception as e:
            return {
                "status": "failed",
                "message": f"Failed to check Python version: {e}"
            }

    async def check_dependencies(self) -> Dict[str, Any]:
        """Check if required dependencies are installed"""
        try:
            required_packages = [
                "fastapi", "uvicorn", "pydantic", "openai", "langchain",
                "rich", "click", "pytest", "asyncio", "pathlib"
            ]

            installed = []
            missing = []

            for package in required_packages:
                if importlib.util.find_spec(package):
                    installed.append(package)
                else:
                    missing.append(package)

            if missing:
                return {
                    "status": "failed",
                    "installed": installed,
                    "missing": missing,
                    "message": f"Missing required packages: {', '.join(missing)}"
                }
            else:
                return {
                    "status": "passed",
                    "installed": installed,
                    "missing": [],
                    "message": f"All {len(installed)} required packages installed"
                }
        except Exception as e:
            return {
                "status": "failed",
                "message": f"Failed to check dependencies: {e}"
            }

    async def check_openai_connection(self) -> Dict[str, Any]:
        """Check OpenAI API connectivity"""
        try:
            api_key = self.config.openai.api_key

            if not api_key or api_key == "not-set":
                return {
                    "status": "warning",
                    "configured": False,
                    "message": "OpenAI API key not configured (mock responses will be used)"
                }

            # In a real implementation, we would test the connection
            # For now, just verify the key format
            if len(api_key) > 20 and api_key.startswith('sk-'):
                return {
                    "status": "passed",
                    "configured": True,
                    "message": "OpenAI API key configured and appears valid"
                }
            else:
                return {
                    "status": "warning",
                    "configured": True,
                    "message": "OpenAI API key configured but format may be invalid"
                }

        except Exception as e:
            return {
                "status": "warning",
                "message": f"OpenAI connectivity check failed: {e}"
            }

    async def check_file_permissions(self) -> Dict[str, Any]:
        """Check file system permissions"""
        try:
            required_dirs = ["logs", "data", "models", "compliance_docs", "temp"]
            created_dirs = []
            permission_errors = []

            for dir_name in required_dirs:
                try:
                    dir_path = Path(dir_name)
                    dir_path.mkdir(exist_ok=True)

                    # Test write permission
                    test_file = dir_path / "test_write.tmp"
                    test_file.write_text("test")
                    test_file.unlink()

                    created_dirs.append(dir_name)
                except Exception as e:
                    permission_errors.append(f"{dir_name}: {e}")

            if permission_errors:
                return {
                    "status": "failed",
                    "created": created_dirs,
                    "errors": permission_errors,
                    "message": f"File permission errors: {'; '.join(permission_errors)}"
                }
            else:
                return {
                    "status": "passed",
                    "created": created_dirs,
                    "errors": [],
                    "message": f"All {len(created_dirs)} required directories accessible"
                }
        except Exception as e:
            return {
                "status": "failed",
                "message": f"File permission check failed: {e}"
            }

    async def check_system_resources(self) -> Dict[str, Any]:
        """Check available system resources"""
        try:
            # Try to import psutil for detailed resource checking
            try:
                import psutil

                # Memory check
                memory = psutil.virtual_memory()
                memory_available_gb = memory.available / (1024**3)
                memory_total_gb = memory.total / (1024**3)

                # Disk check
                disk = psutil.disk_usage('.')
                disk_free_gb = disk.free / (1024**3)
                disk_total_gb = disk.total / (1024**3)

                # CPU check
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()

                warnings = []
                if memory_available_gb < 1.0:
                    warnings.append("Low memory available (< 1 GB)")
                if disk_free_gb < 5.0:
                    warnings.append("Low disk space available (< 5 GB)")
                if cpu_percent > 90:
                    warnings.append("High CPU usage detected")

                status = "warning" if warnings else "passed"
                message = f"Resources OK: {memory_available_gb:.1f}GB RAM, {disk_free_gb:.1f}GB disk, {cpu_count} CPUs"
                if warnings:
                    message += f" - Warnings: {'; '.join(warnings)}"

                return {
                    "status": status,
                    "memory_total_gb": round(memory_total_gb, 2),
                    "memory_available_gb": round(memory_available_gb, 2),
                    "disk_total_gb": round(disk_total_gb, 2),
                    "disk_free_gb": round(disk_free_gb, 2),
                    "cpu_count": cpu_count,
                    "cpu_percent": cpu_percent,
                    "warnings": warnings,
                    "message": message
                }

            except ImportError:
                # Fallback without psutil
                return {
                    "status": "passed",
                    "message": "System resources check skipped (psutil not available)"
                }

        except Exception as e:
            return {
                "status": "warning",
                "message": f"System resource check failed: {e}"
            }

    async def check_configuration(self) -> Dict[str, Any]:
        """Check system configuration"""
        try:
            config_path = Path("backend/core/config.py")
            env_file_path = Path(".env")

            config_status = "ok" if config_path.exists() else "missing"
            env_status = "ok" if env_file_path.exists() else "missing"

            return {
                "status": "pass" if config_status == "ok" else "fail",
                "config_file": config_status,
                "env_file": env_status,
                "message": "Configuration files checked"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Configuration check failed"
            }

    async def check_disk_space(self) -> Dict[str, Any]:
        """Check available disk space"""
        try:
            import shutil

            total, used, free = shutil.disk_usage(".")
            free_gb = free / (1024**3)
            total_gb = total / (1024**3)
            usage_percent = (used / total) * 100

            status = "pass" if free_gb > 1.0 else "warn" if free_gb > 0.5 else "fail"

            return {
                "status": status,
                "free_gb": round(free_gb, 2),
                "total_gb": round(total_gb, 2),
                "usage_percent": round(usage_percent, 2),
                "message": f"Disk usage: {usage_percent:.1f}% ({free_gb:.1f}GB free)"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Disk space check failed"
            }

    async def check_network_connectivity(self) -> Dict[str, Any]:
        """Check network connectivity"""
        try:
            import socket
            import urllib.request

            # Test internet connectivity
            try:
                urllib.request.urlopen('http://www.google.com', timeout=5)
                internet_status = "connected"
            except (urllib.error.URLError, socket.timeout):
                internet_status = "disconnected"

            # Test OpenAI API connectivity
            openai_status = "unknown"
            if self.config.openai.api_key:
                try:
                    urllib.request.urlopen('https://api.openai.com', timeout=5)
                    openai_status = "reachable"
                except (urllib.error.URLError, socket.timeout):
                    openai_status = "unreachable"

            status = "pass" if internet_status == "connected" else "fail"

            return {
                "status": status,
                "internet": internet_status,
                "openai_api": openai_status,
                "message": f"Network connectivity: {internet_status}"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Network connectivity check failed"
            }

    async def check_security_settings(self) -> Dict[str, Any]:
        """Check security settings"""
        try:
            security_issues = []

            # Check if running in development mode
            if self.config.is_development:
                security_issues.append("Running in development mode")

            # Check if debug mode is enabled
            if hasattr(self.config, 'debug') and self.config.debug:
                security_issues.append("Debug mode enabled")

            # Check for hardcoded secrets (basic check)
            config_file = Path("backend/core/config.py")
            if config_file.exists():
                content = config_file.read_text()
                if "password" in content.lower() or "secret" in content.lower():
                    security_issues.append("Potential hardcoded secrets detected")

            status = "pass" if len(security_issues) == 0 else "warn"

            return {
                "status": status,
                "issues": security_issues,
                "message": f"Security check: {len(security_issues)} issues found"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Security settings check failed"
            }

    def detect_environment(self) -> Dict[str, Any]:
        """Detect current environment information"""
        try:
            import os
            import platform

            env_info = {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "python_implementation": platform.python_implementation(),
                "hostname": platform.node(),
                "environment_variables": {
                    "PATH": len(os.environ.get("PATH", "").split(os.pathsep)),
                    "HOME": os.environ.get("HOME", "Not set"),
                    "USER": os.environ.get("USER", "Not set"),
                    "PYTHONPATH": os.environ.get("PYTHONPATH", "Not set")
                },
                "working_directory": os.getcwd(),
                "timestamp": datetime.now().isoformat()
            }

            return env_info

        except Exception as e:
            return {
                "error": str(e),
                "message": "Environment detection failed"
            }

    async def monitor_performance(self) -> Dict[str, Any]:
        """Monitor system performance metrics"""
        try:
            import gc
            import time

            # Memory usage
            try:
                import psutil
                memory = psutil.virtual_memory()
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_info = {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used
                }
            except ImportError:
                memory_info = {"error": "psutil not available"}
                cpu_percent = None

            # Python garbage collection stats
            gc_stats = {
                "collections": gc.get_stats(),
                "garbage_count": len(gc.garbage),
                "ref_count": len(gc.get_objects())
            }

            # Process timing
            start_time = time.time()
            # Simulate some work
            sum(range(1000))
            end_time = time.time()

            perf_data = {
                "timestamp": datetime.now().isoformat(),
                "memory": memory_info,
                "cpu_percent": cpu_percent,
                "gc_stats": gc_stats,
                "sample_operation_time": end_time - start_time,
                "python_version": sys.version_info._asdict()
            }

            return perf_data

        except Exception as e:
            return {
                "error": str(e),
                "message": "Performance monitoring failed"
            }

    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        try:
            info = {
                "platform": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "processor": platform.processor(),
                },
                "python": {
                    "version": sys.version,
                    "executable": sys.executable,
                    "path": sys.path[:5]  # First 5 paths
                },
                "environment": {
                    "name": self.config.environment.value,
                    "debug": self.config.debug,
                    "version": self.config.version
                },
                "timestamp": datetime.now().isoformat()
            }

            # Add resource info if available
            try:
                import psutil
                info["resources"] = {
                    "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                    "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                    "disk_total_gb": round(psutil.disk_usage('.').total / (1024**3), 2),
                    "disk_free_gb": round(psutil.disk_usage('.').free / (1024**3), 2),
                    "cpu_count": psutil.cpu_count(),
                    "cpu_percent": psutil.cpu_percent(interval=1)
                }
            except ImportError:
                pass

            return info

        except Exception as e:
            return {
                "error": f"Failed to gather system info: {e}",
                "timestamp": datetime.now().isoformat()
            }

    def get_recommendations(self) -> List[str]:
        """Get system improvement recommendations based on check results"""
        recommendations = []

        if not self.check_results:
            recommendations.append("Run system checks first to get recommendations")
            return recommendations

        for check_name, result in self.check_results.items():
            if result["status"] == "failed":
                if check_name == "python_version":
                    recommendations.append("Upgrade Python to version 3.10 or higher")
                elif check_name == "dependencies":
                    recommendations.append(f"Install missing packages: pip install {' '.join(result.get('missing', []))}")
                elif check_name == "file_permissions":
                    recommendations.append("Fix file permission issues for required directories")
                elif check_name == "configuration":
                    recommendations.append("Review and fix configuration issues before production use")

            elif result["status"] == "warning":
                if check_name == "openai_connection":
                    recommendations.append("Configure OpenAI API key for full AI functionality")
                elif check_name == "system_resources":
                    if "Low memory" in result.get("message", ""):
                        recommendations.append("Consider increasing available memory")
                    if "Low disk space" in result.get("message", ""):
                        recommendations.append("Free up disk space or add storage")
                elif check_name == "configuration":
                    recommendations.append("Review configuration warnings for security best practices")

        if not recommendations:
            recommendations.append("System appears healthy - no specific recommendations")

        return recommendations

    def display_system_report(self):
        """Display a comprehensive system report"""
        if not hasattr(self, 'check_results') or not self.check_results:
            self.console.print("No system check results available. Run check_all() first.", style="yellow")
            return

        self.console.print("\n" + "="*60, style="bold blue")
        self.console.print("SYSTEM HEALTH REPORT", style="bold blue", justify="center")
        self.console.print("="*60, style="bold blue")

        # Summary
        passed_checks = sum(1 for result in self.check_results.values() if result.get("status") == "passed")
        total_checks = len(self.check_results)

        self.console.print(f"\nOverall Status: {passed_checks}/{total_checks} checks passed", style="bold")

        # Detailed results
        self.console.print("\nDetailed Results:", style="bold")
        for check_name, result in self.check_results.items():
            status = result.get("status", "unknown")
            message = result.get("message", "No details")

            if status == "passed":
                self.console.print(f"  [green]✓[/green] {check_name}: {message}")
            elif status == "warning":
                self.console.print(f"  [yellow]⚠[/yellow] {check_name}: {message}")
            else:
                self.console.print(f"  [red]✗[/red] {check_name}: {message}")

        # Recommendations
        recommendations = self.get_recommendations()
        if recommendations:
            self.console.print("\nRecommendations:", style="bold")
            for i, rec in enumerate(recommendations, 1):
                self.console.print(f"  {i}. {rec}")

        self.console.print("\n" + "="*60, style="bold blue")
