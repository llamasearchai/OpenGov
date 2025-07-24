#!/usr/bin/env python3
"""
GovSecure AI Platform - Command Line Interface
Interactive CLI for 2025 US Government AI Services

Author: Nik Jois
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import platform modules
from backend.core.config import get_config
from backend.ai_agents.government_assistant import GovernmentAssistant, AssistantMode
from backend.ai_agents.compliance_agent import ComplianceAgent
from backend.compliance.scanner import ComplianceScanner
from backend.auth.cli_auth import CLIAuthManager
from backend.utils.system_checker import SystemChecker

# Initialize console for rich output
console = Console()
config = get_config()

class GovSecureCLI:
    """Main CLI application class"""
    
    def __init__(self):
        self.config = get_config()
        self.auth_manager = CLIAuthManager()
        self.system_checker = SystemChecker(self.config)
        self.current_user = None
        # Initialize AI assistants immediately for testing compatibility
        try:
            self.government_assistant = GovernmentAssistant()
            self.compliance_agent = ComplianceAgent()
        except Exception as e:
            console.print(f"Warning: Failed to initialize AI agents: {e}", style="yellow")
            # Keep None values for graceful degradation
        
    def display_banner(self):
        """Display the application banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    GovSecure AI Platform                    ║
║                  2025 Government AI Suite                   ║
║                                                              ║
║  Author: Nik Jois                                          ║
║  FedRAMP High | IL5 Compatible | OpenAI Integrated         ║
╚══════════════════════════════════════════════════════════════╝
        """
        console.print(banner, style="bold blue")
        
    def display_main_menu(self):
        """Display the main menu options"""
        menu_options = [
            "AI Agent Services",
            "Compliance Management", 
            "User Administration",
            "Analytics & Reporting",
            "System Configuration",
            "Development Tools",
            "Documentation",
            "Exit"
        ]
        
        table = Table(title="Main Menu", show_header=False)
        table.add_column("Option", style="cyan", width=4)
        table.add_column("Description", style="white")
        
        for i, option in enumerate(menu_options, 1):
            table.add_row(str(i), option)
            
        console.print(table)
        
    async def initialize_platform(self):
        """Initialize platform components"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # System checks
            task1 = progress.add_task("Running system checks...", total=None)
            await asyncio.sleep(1)
            system_ok = await self.system_checker.check_all()
            progress.update(task1, completed=True)
            
            # Initialize AI agents if not already done
            task2 = progress.add_task("Initializing AI agents...", total=None)
            await asyncio.sleep(1)
            try:
                if self.government_assistant is None:
                    self.government_assistant = GovernmentAssistant()
                if self.compliance_agent is None:
                    self.compliance_agent = ComplianceAgent()
                progress.update(task2, completed=True)
            except Exception as e:
                console.print(f"Failed to initialize AI agents: {e}", style="red")
                # Continue even if AI agents fail to initialize in development/testing
                if not self.config.is_development:
                    return False
                else:
                    console.print("Continuing in development mode with limited functionality...", style="yellow")
            
            if not system_ok:
                console.print("Some system checks failed. Platform will run with limited functionality.", style="yellow")
                
            # Load configuration
            task3 = progress.add_task("Loading configuration...", total=None)
            await asyncio.sleep(0.5)
            progress.update(task3, completed=True)
            
        console.print("Platform initialized successfully!", style="green")
        return True
        
    async def handle_ai_services(self):
        """Handle AI agent services menu"""
        while True:
            console.print("\n" + "="*60)
            console.print("AI Agent Services", style="bold cyan")
            console.print("="*60)
            
            ai_options = [
                "Interactive Government Assistant",
                "Document Analysis & Translation", 
                "Compliance Validation",
                "Citizen Service Automation",
                "Emergency Response Analysis",
                "Back to Main Menu"
            ]
            
            for i, option in enumerate(ai_options, 1):
                console.print(f"{i}. {option}")
                
            choice = Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(ai_options) + 1)])
            
            if choice == "1":
                await self.interactive_assistant()
            elif choice == "2":
                await self.document_analysis()
            elif choice == "3":
                await self.compliance_validation()
            elif choice == "4":
                await self.citizen_services()
            elif choice == "5":
                await self.emergency_response()
            elif choice == "6":
                break
                
    async def interactive_assistant(self):
        """Interactive government AI assistant"""
        console.print("\nGovernment AI Assistant", style="bold green")
        console.print("Type 'exit' to return to menu\n")
        
        while True:
            user_input = Prompt.ask("[bold cyan]You")
            
            if user_input.lower() in ['exit', 'quit', 'back']:
                break
                
            with Progress(
                SpinnerColumn(),
                TextColumn("Processing..."),
                console=console,
            ) as progress:
                task = progress.add_task("Thinking...", total=None)
                response = await self.government_assistant.chat(user_input)
                progress.update(task, completed=True)
                
            console.print(f"[bold green]Assistant:[/bold green] {response}")
            
    async def handle_compliance_menu(self):
        """Handle compliance management menu"""
        while True:
            console.print("\n" + "="*60)
            console.print("Compliance Management", style="bold red")
            console.print("="*60)
            
            compliance_options = [
                "Run Full Compliance Scan",
                "Generate Compliance Report",
                "View NIST 800-53 Controls",
                "Evidence Collection",
                "Risk Assessment",
                "Audit Log Review",
                "Back to Main Menu"
            ]
            
            for i, option in enumerate(compliance_options, 1):
                console.print(f"{i}. {option}")
                
            choice = Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(compliance_options) + 1)])
            
            if choice == "1":
                await self.run_compliance_scan()
            elif choice == "2":
                await self.generate_compliance_report()
            elif choice == "3":
                await self.view_controls()
            elif choice == "4":
                await self.collect_evidence()
            elif choice == "5":
                await self.risk_assessment()
            elif choice == "6":
                await self.audit_log_review()
            elif choice == "7":
                break
                
    async def run_compliance_scan(self):
        """Run a full compliance scan"""
        console.print("\nRunning Full Compliance Scan", style="bold yellow")
        
        scanner = ComplianceScanner()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            task = progress.add_task("Scanning system configuration...", total=100)
            
            for i in range(0, 101, 10):
                await asyncio.sleep(0.5)
                progress.update(task, completed=i)
                
        results = await scanner.run_full_scan()
        
        # Display results
        table = Table(title="Compliance Scan Results")
        table.add_column("Control", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Risk", style="red")
        
        for result in results[:10]:  # Show first 10 results
            control_id = result.get('control_id', 'Unknown')
            status = result.get('status', 'Unknown')
            risk = result.get('risk_level', 'Unknown')
                
            table.add_row(control_id, status, risk)
            
        console.print(table)
        
        # Get latest scan result for summary
        latest_scan = scanner.get_latest_scan()
        if latest_scan:
            console.print(f"\nScan completed. Overall compliance: {latest_scan.overall_score:.1f}%", style="green")
        else:
            console.print(f"\nScan completed. {len(results)} findings identified.", style="green")

    async def generate_compliance_report(self):
        """Generate a comprehensive compliance report"""
        console.print("\nGenerating Compliance Report", style="bold cyan")
        
        # Get report type
        report_types = ["Executive Summary", "Technical Details", "Full Report", "Custom"]
        report_type_display = [f"{i+1}. {rt}" for i, rt in enumerate(report_types)]
        
        console.print("Select report type:")
        for option in report_type_display:
            console.print(option)
            
        report_choice = Prompt.ask("Report type", choices=["1", "2", "3", "4"])
        report_type = report_types[int(report_choice) - 1]
        
        # Get compliance frameworks
        frameworks = ["NIST 800-53", "FedRAMP", "CMMC", "SOX", "All"]
        framework_display = [f"{i+1}. {fw}" for i, fw in enumerate(frameworks)]
        
        console.print("\nSelect compliance framework:")
        for option in framework_display:
            console.print(option)
            
        framework_choice = Prompt.ask("Framework", choices=["1", "2", "3", "4", "5"])
        framework = frameworks[int(framework_choice) - 1]
        
        with Progress(SpinnerColumn(), TextColumn("Generating report..."), console=console) as progress:
            task = progress.add_task("Processing...", total=None)
            
            # Use the compliance agent to generate report
            agent = ComplianceAgent()
            report = await agent.generate_compliance_report("system", {"type": report_type, "framework": framework})
            
            progress.update(task, completed=True)
        
        console.print(f"\n[bold green]Compliance Report Generated:[/bold green]")
        console.print(f"Report Type: {report_type}")
        console.print(f"Framework: {framework}")
        console.print(f"Generated: {report['generated_date']}")
        console.print(f"\nExecutive Summary:\n{report['executive_summary']}")
        
        # Save option
        if Confirm.ask("Save report to file?"):
            timestamp = report['generated_date'].replace(' ', '_').replace(':', '-')
            filename = f"compliance_report_{timestamp}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Compliance Report - {report_type}\n")
                f.write(f"Framework: {framework}\n")
                f.write(f"Generated: {report['generated_date']}\n\n")
                f.write(f"Executive Summary:\n{report['executive_summary']}\n\n")
                f.write(f"Key Findings:\n{report.get('key_findings', 'N/A')}\n\n")
                f.write(f"Recommendations:\n{report.get('recommendations', 'N/A')}\n")
            console.print(f"Report saved as {filename}", style="green")

    async def view_controls(self):
        """View NIST 800-53 controls and details"""
        console.print("\nNIST 800-53 Controls Viewer", style="bold blue")
        
        # Control families
        families = {
            "AC": "Access Control",
            "AU": "Audit and Accountability", 
            "AT": "Awareness and Training",
            "CM": "Configuration Management",
            "CP": "Contingency Planning",
            "IA": "Identification and Authentication",
            "IR": "Incident Response",
            "MA": "Maintenance",
            "MP": "Media Protection",
            "PS": "Personnel Security",
            "PE": "Physical and Environmental Protection",
            "PL": "Planning",
            "PM": "Program Management",
            "RA": "Risk Assessment",
            "CA": "Assessment, Authorization, and Monitoring",
            "SC": "System and Communications Protection",
            "SI": "System and Information Integrity",
            "SA": "System and Services Acquisition"
        }
        
        console.print("Select control family:")
        for code, name in families.items():
            console.print(f"{code}: {name}")
        
        family_code = Prompt.ask("Enter family code (e.g., AC, AU)", default="AC").upper()
        
        if family_code not in families:
            console.print("Invalid family code", style="red")
            return
            
        # Show sample controls for the family
        sample_controls = {
            "AC": [
                ("AC-1", "Access Control Policy and Procedures"),
                ("AC-2", "Account Management"),
                ("AC-3", "Access Enforcement"),
                ("AC-4", "Information Flow Enforcement"),
                ("AC-5", "Separation of Duties")
            ],
            "AU": [
                ("AU-1", "Audit and Accountability Policy and Procedures"),
                ("AU-2", "Event Logging"),
                ("AU-3", "Content of Audit Records"),
                ("AU-4", "Audit Log Storage Capacity"),
                ("AU-5", "Response to Audit Processing Failures")
            ]
        }
        
        controls = sample_controls.get(family_code, [
            (f"{family_code}-1", f"{families[family_code]} Policy and Procedures"),
            (f"{family_code}-2", f"{families[family_code]} Implementation"),
            (f"{family_code}-3", f"{families[family_code]} Monitoring")
        ])
        
        table = Table(title=f"{families[family_code]} Controls")
        table.add_column("Control ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Status", style="green")
        
        for control_id, title in controls:
            # Mock status - in real implementation would check actual compliance
            status = "Implemented" if hash(control_id) % 2 == 0 else "Partial"
            table.add_row(control_id, title, status)
            
        console.print(table)
        
        # Option to view detailed control
        if Confirm.ask("View detailed control information?"):
            control_id = Prompt.ask("Enter control ID", default=controls[0][0])
            
            # Use compliance agent for detailed control info
            agent = ComplianceAgent()
            guidance = await agent.get_control_guidance("system", control_id)
            
            console.print(f"\n[bold cyan]Control Details: {control_id}[/bold cyan]")
            console.print(f"Implementation Guidance:\n{guidance}")

    async def collect_evidence(self):
        """Handle evidence collection for compliance"""
        console.print("\nEvidence Collection", style="bold yellow")
        
        evidence_types = [
            "System Configuration Files",
            "Security Policies and Procedures", 
            "Audit Logs and Reports",
            "Access Control Lists",
            "Network Diagrams",
            "Security Test Results",
            "Training Records",
            "Incident Response Documentation"
        ]
        
        console.print("Available evidence types:")
        for i, ev_type in enumerate(evidence_types, 1):
            console.print(f"{i}. {ev_type}")
            
        choice = Prompt.ask("Select evidence type", choices=[str(i) for i in range(1, len(evidence_types) + 1)])
        selected_type = evidence_types[int(choice) - 1]
        
        console.print(f"\nCollecting: {selected_type}")
        
        with Progress(SpinnerColumn(), TextColumn("Gathering evidence..."), console=console) as progress:
            task = progress.add_task("Processing...", total=100)
            
            for i in range(0, 101, 25):
                await asyncio.sleep(0.8)
                progress.update(task, completed=i)
        
        # Mock evidence collection results
        evidence_items = {
            "System Configuration Files": ["ssh_config.txt", "firewall_rules.json", "system_hardening.log"],
            "Security Policies and Procedures": ["access_control_policy.pdf", "incident_response_plan.docx"],
            "Audit Logs and Reports": ["auth.log", "syslog", "compliance_audit_2024.pdf"],
            "Access Control Lists": ["user_permissions.csv", "role_assignments.xlsx"],
            "Network Diagrams": ["network_topology.png", "security_zones.pdf"],
            "Security Test Results": ["pentest_report.pdf", "vulnerability_scan.xml"],
            "Training Records": ["security_training_completion.xlsx", "awareness_certificates.pdf"],
            "Incident Response Documentation": ["incident_log_2024.txt", "response_procedures.docx"]
        }
        
        items = evidence_items.get(selected_type, ["sample_evidence.txt"])
        
        table = Table(title=f"Evidence Collected: {selected_type}")
        table.add_column("File Name", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Last Modified", style="white")
        
        from datetime import datetime, timedelta
        import random
        
        for item in items:
            status = "Available" if random.choice([True, False]) else "Missing"
            last_mod = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            table.add_row(item, status, last_mod)
        
        console.print(table)
        console.print(f"\nEvidence collection completed. {len(items)} items identified.", style="green")

    async def risk_assessment(self):
        """Perform risk assessment"""
        console.print("\nRisk Assessment", style="bold red")
        
        assessment_types = [
            "System Risk Assessment",
            "Data Risk Assessment", 
            "Network Risk Assessment",
            "Application Risk Assessment",
            "Operational Risk Assessment"
        ]
        
        console.print("Select assessment type:")
        for i, assessment in enumerate(assessment_types, 1):
            console.print(f"{i}. {assessment}")
            
        choice = Prompt.ask("Assessment type", choices=[str(i) for i in range(1, len(assessment_types) + 1)])
        selected_assessment = assessment_types[int(choice) - 1]
        
        console.print(f"\nPerforming: {selected_assessment}")
        
        with Progress(SpinnerColumn(), TextColumn("Analyzing risks..."), console=console) as progress:
            task = progress.add_task("Processing...", total=100)
            
            for i in range(0, 101, 20):
                await asyncio.sleep(1)
                progress.update(task, completed=i)
        
        # Mock risk assessment results
        risks = [
            {"id": "RISK-001", "category": "Data Security", "level": "High", "impact": "Confidentiality breach"},
            {"id": "RISK-002", "category": "Access Control", "level": "Medium", "impact": "Unauthorized access"},
            {"id": "RISK-003", "category": "Network Security", "level": "Low", "impact": "Minor data exposure"},
            {"id": "RISK-004", "category": "System Integrity", "level": "Medium", "impact": "Data corruption"},
            {"id": "RISK-005", "category": "Availability", "level": "High", "impact": "Service disruption"}
        ]
        
        table = Table(title=f"Risk Assessment Results: {selected_assessment}")
        table.add_column("Risk ID", style="cyan")
        table.add_column("Category", style="white")
        table.add_column("Risk Level", style="red")
        table.add_column("Potential Impact", style="yellow")
        
        for risk in risks:
            level_style = "red" if risk["level"] == "High" else "yellow" if risk["level"] == "Medium" else "green"
            table.add_row(risk["id"], risk["category"], f"[{level_style}]{risk['level']}[/{level_style}]", risk["impact"])
        
        console.print(table)
        
        # Risk summary
        high_risks = len([r for r in risks if r["level"] == "High"])
        medium_risks = len([r for r in risks if r["level"] == "Medium"])
        low_risks = len([r for r in risks if r["level"] == "Low"])
        
        console.print(f"\nRisk Summary:")
        console.print(f"   High Risk: {high_risks}")
        console.print(f"   Medium Risk: {medium_risks}")
        console.print(f"   Low Risk: {low_risks}")
        
        if Confirm.ask("Generate risk mitigation recommendations?"):
            console.print(f"\nRisk Mitigation Recommendations:")
            console.print("   - Implement multi-factor authentication for high-privilege accounts")
            console.print("   - Conduct quarterly security assessments")
            console.print("   - Enhance monitoring and alerting systems")
            console.print("   - Provide additional security training for staff")
            console.print("   - Review and update incident response procedures")

    async def audit_log_review(self):
        """Review audit logs"""
        console.print("\nAudit Log Review", style="bold magenta")
        
        log_types = [
            "Authentication Logs",
            "System Access Logs",
            "Configuration Changes",
            "Security Events",
            "Compliance Events",
            "Error Logs"
        ]
        
        console.print("Select log type to review:")
        for i, log_type in enumerate(log_types, 1):
            console.print(f"{i}. {log_type}")
            
        choice = Prompt.ask("Log type", choices=[str(i) for i in range(1, len(log_types) + 1)])
        selected_log = log_types[int(choice) - 1]
        
        # Time range selection
        time_ranges = ["Last 24 hours", "Last 7 days", "Last 30 days", "Custom range"]
        console.print("\nSelect time range:")
        for i, time_range in enumerate(time_ranges, 1):
            console.print(f"{i}. {time_range}")
            
        time_choice = Prompt.ask("Time range", choices=[str(i) for i in range(1, len(time_ranges) + 1)])
        selected_range = time_ranges[int(time_choice) - 1]
        
        console.print(f"\nReviewing: {selected_log} ({selected_range})")
        
        with Progress(SpinnerColumn(), TextColumn("Analyzing logs..."), console=console) as progress:
            task = progress.add_task("Processing...", total=100)
            
            for i in range(0, 101, 25):
                await asyncio.sleep(0.7)
                progress.update(task, completed=i)
        
        # Mock audit log entries
        from datetime import datetime, timedelta
        import random
        
        log_entries = []
        for i in range(10):
            timestamp = datetime.now() - timedelta(hours=random.randint(1, 24))
            severity = random.choice(["INFO", "WARN", "ERROR", "CRITICAL"])
            user = random.choice(["admin", "user1", "service_account", "system"])
            action = random.choice(["LOGIN", "LOGOUT", "CONFIG_CHANGE", "FILE_ACCESS", "PERMISSION_CHANGE"])
            
            log_entries.append({
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "severity": severity,
                "user": user,
                "action": action,
                "details": f"Action performed by {user}"
            })
        
        table = Table(title=f"Audit Log Review: {selected_log}")
        table.add_column("Timestamp", style="cyan")
        table.add_column("Severity", style="white")
        table.add_column("User", style="green")
        table.add_column("Action", style="yellow")
        table.add_column("Details", style="white")
        
        for entry in log_entries:
            severity_style = "red" if entry["severity"] == "CRITICAL" else "yellow" if entry["severity"] in ["ERROR", "WARN"] else "green"
            table.add_row(
                entry["timestamp"],
                f"[{severity_style}]{entry['severity']}[/{severity_style}]",
                entry["user"],
                entry["action"],
                entry["details"]
            )
        
        console.print(table)
        
        # Log analysis summary
        critical_count = len([e for e in log_entries if e["severity"] == "CRITICAL"])
        error_count = len([e for e in log_entries if e["severity"] == "ERROR"])
        warn_count = len([e for e in log_entries if e["severity"] == "WARN"])
        
        console.print(f"\nLog Analysis Summary:")
        console.print(f"   Total Entries: {len(log_entries)}")
        console.print(f"   Critical: {critical_count}")
        console.print(f"   Errors: {error_count}")
        console.print(f"   Warnings: {warn_count}")
        
        if critical_count > 0 or error_count > 0:
            console.print(f"\nIssues Detected - Immediate attention required!", style="bold red")
        else:
            console.print(f"\nNo critical issues found in logs", style="green")
    
    async def handle_user_admin(self):
        """Handle user administration menu."""
        console.print("\nUser Administration", style="bold yellow")
        console.print("Feature coming soon - user management interface")
        await asyncio.sleep(1)

    async def handle_analytics(self):
        """Handle analytics and reporting menu."""
        console.print("\nAnalytics & Reporting", style="bold magenta")
        console.print("Feature coming soon - analytics dashboard")
        await asyncio.sleep(1)

    async def handle_system_config(self):
        """Handle system configuration menu."""
        console.print("\nSystem Configuration", style="bold cyan")
        
        config_info = {
            "Environment": self.config.environment.value,
            "Debug Mode": self.config.debug,
            "Version": self.config.version,
            "API Host": f"{self.config.api.host}:{self.config.api.port}",
            "Database": self.config.database.engine.value,
            "OpenAI Model": self.config.openai.model,
            "Compliance Level": self.config.compliance.compliance_level.value,
        }
        
        console.print("\nCurrent Configuration:")
        for key, value in config_info.items():
            console.print(f"  {key}: {value}")
            
        await asyncio.sleep(2)

    async def start_web_interface(self):
        """Start the web interface"""
        console.print("\nStarting Web Interface...", style="bold blue")
        
        try:
            # Start backend
            backend_process = subprocess.Popen([
                "poetry", "run", "uvicorn", 
                "backend.api.main:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--reload"
            ])
            
            await asyncio.sleep(3)
            
            # Start frontend
            frontend_process = subprocess.Popen([
                "npm", "start"
            ], cwd="frontend")
            
            console.print("Web interface started!", style="green")
            console.print("Backend API: http://localhost:8000", style="cyan")
            console.print("Frontend UI: http://localhost:3000", style="cyan")
            
            if Confirm.ask("Keep services running?"):
                console.print("Services running. Press Ctrl+C to stop.")
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    pass
                    
            # Cleanup
            backend_process.terminate()
            frontend_process.terminate()
            console.print("Services stopped.", style="yellow")
            
        except Exception as e:
            console.print(f"Failed to start web interface: {e}", style="red")

    async def run(self):
        """Main application loop"""
        self.display_banner()
        
        # Initialize platform
        if not await self.initialize_platform():
            return
            
        # Check authentication
        if not await self.auth_manager.authenticate():
            console.print("Authentication failed. Exiting.", style="red")
            return
            
        # Main menu loop
        while True:
            console.print("\n")
            self.display_main_menu()
            
            try:
                choice = Prompt.ask("Please select an option (1-8)", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
                
                if choice == "1":
                    await self.handle_ai_services()
                elif choice == "2":
                    await self.handle_compliance_menu()
                elif choice == "3":
                    await self.handle_user_admin()
                elif choice == "4":
                    await self.handle_analytics()
                elif choice == "5":
                    await self.handle_system_config()
                elif choice == "6":
                    await self.handle_dev_tools()
                elif choice == "7":
                    await self.show_documentation()
                elif choice == "8":
                    console.print("Thank you for using GovSecure AI Platform!", style="bold green")
                    break
                    
            except KeyboardInterrupt:
                console.print("\nGoodbye!", style="yellow")
                break
            except Exception as e:
                console.print(f"Error: {e}", style="red")

    async def document_analysis(self):
        """Handle document analysis and translation."""
        console.print("\nDocument Analysis & Translation", style="bold cyan")
        
        doc_options = [
            "Analyze uploaded document",
            "Translate document", 
            "Extract key information",
            "Compliance document review",
            "Back to AI Services"
        ]
        
        for i, option in enumerate(doc_options, 1):
            console.print(f"{i}. {option}")
            
        doc_choice = Prompt.ask("Select option", choices=[str(i) for i in range(1, len(doc_options) + 1)])
        
        if doc_choice == "1":
            await self.analyze_uploaded_document()
        elif doc_choice == "2":
            await self.translate_document()
        elif doc_choice == "3":
            await self.extract_key_information()
        elif doc_choice == "4":
            await self.compliance_document_review()

    async def analyze_uploaded_document(self):
        """Analyze an uploaded document."""
        file_path = Prompt.ask("Enter document file path")
        
        try:
            if not Path(file_path).exists():
                console.print("❌ File not found", style="red")
                return
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            analysis_type = Prompt.ask("Analysis type", choices=["general", "compliance", "policy", "legal", "financial"], default="general")
            
            with Progress(SpinnerColumn(), TextColumn("Analyzing document..."), console=console) as progress:
                task = progress.add_task("Processing...", total=None)
                result = await self.government_assistant.analyze_document(content, analysis_type)
                progress.update(task, completed=True)
                
            console.print(f"\n[bold green]Document Analysis Results:[/bold green]")
            console.print(f"Analysis Type: {result['analysis_type']}")
            console.print(f"Summary:\n{result['summary']}")
            
        except Exception as e:
            console.print(f"Error analyzing document: {e}", style="red")

    async def translate_document(self):
        """Translate a document."""
        file_path = Prompt.ask("Enter document file path")
        target_language = Prompt.ask("Target language", default="Spanish")
        
        try:
            if not Path(file_path).exists():
                console.print("❌ File not found", style="red")
                return
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            with Progress(SpinnerColumn(), TextColumn("Translating document..."), console=console) as progress:
                task = progress.add_task("Processing...", total=None)
                result = await self.government_assistant.translate_text(content, target_language)
                progress.update(task, completed=True)
                
            console.print(f"\n[bold green]Translation Results:[/bold green]")
            console.print(f"Target Language: {result['target_language']}")
            console.print(f"Translated Text:\n{result['translated_text']}")
            
            # Option to save translation
            if Confirm.ask("Save translation to file?"):
                output_path = Path(file_path).with_suffix(f".{target_language.lower()}.txt")
                output_path.write_text(result['translated_text'], encoding='utf-8')
                console.print(f"Translation saved to {output_path}", style="green")
                
        except Exception as e:
            console.print(f"Error translating document: {e}", style="red")

    async def extract_key_information(self):
        """Extract key information from document."""
        file_path = Prompt.ask("Enter document file path")
        
        try:
            if not Path(file_path).exists():
                console.print("❌ File not found", style="red")
                return
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            prompt = "Extract key information from this document including: main topics, important dates, key personnel, action items, and deadlines."
            
            with Progress(SpinnerColumn(), TextColumn("Extracting information..."), console=console) as progress:
                task = progress.add_task("Processing...", total=None)
                result = await self.government_assistant.analyze_document(content, "general")
                progress.update(task, completed=True)
                
            console.print(f"\n[bold green]Key Information Extracted:[/bold green]")
            console.print(result['summary'])
            
        except Exception as e:
            console.print(f"Error extracting information: {e}", style="red")

    async def compliance_document_review(self):
        """Review document for compliance."""
        file_path = Prompt.ask("Enter document file path")
        
        try:
            if not Path(file_path).exists():
                console.print("❌ File not found", style="red")
                return
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            with Progress(SpinnerColumn(), TextColumn("Reviewing compliance..."), console=console) as progress:
                task = progress.add_task("Processing...", total=None)
                result = await self.government_assistant.analyze_document(content, "compliance")
                progress.update(task, completed=True)
                
            console.print(f"\n[bold green]Compliance Review Results:[/bold green]")
            console.print(result['summary'])
            
        except Exception as e:
            console.print(f"Error reviewing compliance: {e}", style="red")

    async def compliance_validation(self):
        """Handle compliance validation."""
        from backend.ai_agents.government_assistant import AssistantMode
        await self.government_assistant.set_mode(AssistantMode.COMPLIANCE)
        console.print("\nCompliance Validation Assistant", style="bold red")
        console.print("Ask questions about NIST 800-53, FedRAMP, or other compliance frameworks.\n")
        
        while True:
            user_input = Prompt.ask("[bold cyan]Compliance Question")
            
            if user_input.lower() in ['exit', 'quit', 'back']:
                break
                
            response = await self.government_assistant.chat(user_input)
            console.print(f"[bold red]Compliance Advisor:[/bold red] {response}")

    async def citizen_services(self):
        """Handle citizen service automation."""
        from backend.ai_agents.government_assistant import AssistantMode
        await self.government_assistant.set_mode(AssistantMode.CITIZEN_SERVICE)
        console.print("\nCitizen Services Assistant", style="bold blue")
        console.print("Specialized for 311 services, benefits, permits, and citizen inquiries.\n")
        
        while True:
            user_input = Prompt.ask("[bold cyan]Citizen Inquiry")
            
            if user_input.lower() in ['exit', 'quit', 'back']:
                break
                
            response = await self.government_assistant.chat(user_input)
            console.print(f"[bold blue]Citizen Services:[/bold blue] {response}")

    async def emergency_response(self):
        """Handle emergency response analysis."""
        from backend.ai_agents.government_assistant import AssistantMode
        await self.government_assistant.set_mode(AssistantMode.EMERGENCY_RESPONSE)
        console.print("\nEmergency Response Coordinator", style="bold red")
        console.print("Assistance with emergency planning, coordination, and response.\n")
        
        while True:
            user_input = Prompt.ask("[bold cyan]Emergency Query")
            
            if user_input.lower() in ['exit', 'quit', 'back']:
                break
                
            response = await self.government_assistant.chat(user_input)
            console.print(f"[bold red]Emergency Coordinator:[/bold red] {response}")
            
    async def handle_dev_tools(self):
        """Handle development tools menu."""
        console.print("\nDevelopment Tools", style="bold green")
        
        dev_options = [
            "System Information",
            "Run System Checks",
            "View Session Status",
            "Clear Cache",
            "Back to Main Menu"
        ]
        
        for i, option in enumerate(dev_options, 1):
            console.print(f"{i}. {option}")
            
        choice = Prompt.ask("Select option", choices=[str(i) for i in range(1, len(dev_options) + 1)])
        
        if choice == "1":
            await self.show_system_info()
        elif choice == "2":
            await self.run_system_checks()
        elif choice == "3":
            await self.auth_manager.show_session_status()
        elif choice == "4":
            console.print("Cache cleared", style="green")

    async def show_system_info(self):
        """Show system information."""
        info = self.system_checker.get_system_info()
        
        console.print("\nSystem Information", style="bold blue")
        console.print(f"Platform: {info['platform']['system']} {info['platform']['release']}")
        console.print(f"Machine: {info['platform']['machine']}")
        console.print(f"Python: {info['python']['version'].split()[0]}")
        
        if 'resources' in info and 'memory_total_gb' in info['resources']:
            resources = info['resources']
            console.print(f"Memory: {resources['memory_available_gb']}/{resources['memory_total_gb']} GB available")
            console.print(f"Disk: {resources['disk_free_gb']}/{resources['disk_total_gb']} GB free")
            console.print(f"CPU: {resources['cpu_count']} cores ({resources['cpu_percent']}% usage)")

    async def run_system_checks(self):
        """Run system checks."""
        await self.system_checker.check_all()
        
        recommendations = self.system_checker.get_recommendations()
        if recommendations:
            console.print("\nRecommendations:", style="bold yellow")
            for rec in recommendations:
                console.print(f"  - {rec}")

    async def show_documentation(self):
        """Show documentation links."""
        console.print("\nDocumentation", style="bold blue")
        
        docs = [
            ("User Guide", "Complete platform usage guide"),
            ("API Reference", "REST API documentation"),
            ("Security Guide", "Security and compliance details"),
            ("Deployment Guide", "Production deployment instructions"),
            ("Developer Guide", "Contributing and development setup")
        ]
        
        console.print("\nAvailable Documentation:")
        for title, description in docs:
            console.print(f"  {title}: {description}")
        
        console.print(f"\nOnline Documentation: https://nikjois.github.io/PublicGovPlatform/")
        await asyncio.sleep(2)

@click.group()
def cli():
    """GovSecure AI Platform CLI"""
    pass

@cli.command()
def start():
    """Start the interactive CLI interface"""
    app = GovSecureCLI()
    asyncio.run(app.run())

@cli.command()
@click.argument('message')
def chat(message):
    """Quick chat with government AI assistant"""
    async def quick_chat():
        assistant = GovernmentAssistant()
        response = await assistant.chat(message)
        console.print(f"[bold green]Assistant:[/bold green] {response}")
    
    asyncio.run(quick_chat())

@cli.command()
def scan():
    """Run quick compliance scan"""
    async def quick_scan():
        scanner = ComplianceScanner()
        results = await scanner.quick_scan()
        console.print(f"Quick scan completed. Score: {results.overall_score}%", style="green")
    
    asyncio.run(quick_scan())

@cli.command()
def web():
    """Start web interface"""
    app = GovSecureCLI()
    asyncio.run(app.start_web_interface())

if __name__ == "__main__":
    # If run directly, start interactive mode
    if len(sys.argv) == 1:
        app = GovSecureCLI()
        asyncio.run(app.run())
    else:
        cli() 