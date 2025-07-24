"""
Test suite for GovSecure AI Platform CLI
Comprehensive testing of command-line interface functionality.

Author: Nik Jois
"""

import os
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from backend.ai_agents.government_assistant import AssistantMode
from backend.core.config import get_config
from cli import GovSecureCLI, cli


class TestCLICommands:
    """Test CLI command functionality"""

    def setup_method(self):
        """Set up test environment"""
        self.runner = CliRunner()
        self.config = get_config()

    def test_cli_help(self):
        """Test CLI help command"""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "GovSecure AI Platform CLI" in result.output
        assert "start" in result.output
        assert "chat" in result.output
        assert "scan" in result.output

    def test_chat_command(self):
        """Test quick chat command"""
        result = self.runner.invoke(cli, ['chat', 'Hello, test message'])
        assert result.exit_code == 0
        assert "Assistant:" in result.output
        # Should show mock response when OpenAI not configured
        assert any(keyword in result.output.lower() for keyword in ['mock', 'government services', 'assistance'])

    def test_scan_command(self):
        """Test compliance scan command"""
        result = self.runner.invoke(cli, ['scan'])
        assert result.exit_code == 0
        assert "scan completed" in result.output.lower()
        # Should show a percentage score
        assert "%" in result.output


class TestGovSecureCLI:
    """Test main CLI application class"""

    def setup_method(self):
        """Set up test environment"""
        self.cli_app = GovSecureCLI()

    def test_cli_initialization(self):
        """Test CLI app initialization"""
        assert self.cli_app.config is not None
        assert self.cli_app.government_assistant is not None
        assert self.cli_app.auth_manager is not None
        assert self.cli_app.system_checker is not None

    def test_display_banner(self):
        """Test banner display"""
        # Should not raise any exceptions
        self.cli_app.display_banner()

    def test_display_main_menu(self):
        """Test main menu display"""
        # Should not raise any exceptions
        self.cli_app.display_main_menu()

    @pytest.mark.asyncio
    async def test_initialize_platform(self):
        """Test platform initialization"""
        result = await self.cli_app.initialize_platform()
        # Should return True (platform initialized successfully)
        assert result is True


class TestAIAssistantIntegration:
    """Test AI assistant integration in CLI"""

    def setup_method(self):
        """Set up test environment"""
        self.cli_app = GovSecureCLI()

    @pytest.mark.asyncio
    async def test_interactive_assistant_mock(self):
        """Test interactive assistant with mock responses"""
        assistant = self.cli_app.government_assistant

        # Test general mode
        response = await assistant.chat("What services do you provide?")
        assert response is not None
        assert len(response) > 0
        assert isinstance(response, str)

    @pytest.mark.asyncio
    async def test_citizen_service_mode(self):
        """Test citizen service mode"""
        assistant = self.cli_app.government_assistant

        # Set to citizen service mode
        await assistant.set_mode(AssistantMode.CITIZEN_SERVICE)
        assert assistant.get_current_mode() == "citizen_service"

        # Test citizen service query
        response = await assistant.chat("I need help with my benefits application")
        assert response is not None
        assert any(keyword in response.lower() for keyword in ['benefits', 'assistance', 'application'])

    @pytest.mark.asyncio
    async def test_compliance_mode(self):
        """Test compliance mode"""
        assistant = self.cli_app.government_assistant

        # Set to compliance mode
        await assistant.set_mode(AssistantMode.COMPLIANCE)
        assert assistant.get_current_mode() == "compliance"

        # Test compliance query
        response = await assistant.chat("What are NIST 800-53 requirements?")
        assert response is not None
        assert any(keyword in response.lower() for keyword in ['nist', 'compliance', 'controls'])

    @pytest.mark.asyncio
    async def test_emergency_response_mode(self):
        """Test emergency response mode"""
        assistant = self.cli_app.government_assistant

        # Set to emergency response mode
        await assistant.set_mode(AssistantMode.EMERGENCY_RESPONSE)
        assert assistant.get_current_mode() == "emergency_response"

        # Test emergency query
        response = await assistant.chat("We have a natural disaster situation")
        assert response is not None
        assert any(keyword in response.lower() for keyword in ['emergency', 'response', 'coordination'])


class TestDocumentAnalysis:
    """Test document analysis functionality"""

    def setup_method(self):
        """Set up test environment"""
        self.cli_app = GovSecureCLI()
        self.assistant = self.cli_app.government_assistant

    @pytest.mark.asyncio
    async def test_document_analysis_general(self):
        """Test general document analysis"""
        test_content = "This is a sample government document with policy information."

        result = await self.assistant.analyze_document(test_content, "general")

        assert result is not None
        assert "analysis_type" in result
        assert "summary" in result
        assert result["analysis_type"] == "general"
        assert len(result["summary"]) > 0

    @pytest.mark.asyncio
    async def test_document_analysis_compliance(self):
        """Test compliance document analysis"""
        test_content = "Security control AC-1 requires access control policies and procedures."

        result = await self.assistant.analyze_document(test_content, "compliance")

        assert result is not None
        assert result["analysis_type"] == "compliance"
        assert any(keyword in result["summary"].lower() for keyword in ['compliance', 'control', 'security'])

    @pytest.mark.asyncio
    async def test_translation_functionality(self):
        """Test text translation"""
        test_text = "Welcome to government services."
        target_language = "Spanish"

        result = await self.assistant.translate_text(test_text, target_language)

        assert result is not None
        assert "original_text" in result
        assert "translated_text" in result
        assert "target_language" in result
        assert result["target_language"] == target_language
        assert result["original_text"] == test_text


class TestComplianceScanning:
    """Test compliance scanning functionality"""

    def setup_method(self):
        """Set up test environment"""
        self.cli_app = GovSecureCLI()

    @pytest.mark.asyncio
    async def test_quick_scan(self):
        """Test quick compliance scan"""
        from backend.compliance.scanner import ComplianceScanner

        scanner = ComplianceScanner()
        result = await scanner.quick_scan()

        assert result is not None
        assert hasattr(result, 'overall_score')
        assert isinstance(result.overall_score, (int, float))
        assert 0 <= result.overall_score <= 100

    @pytest.mark.asyncio
    async def test_full_scan(self):
        """Test full compliance scan"""
        from backend.compliance.scanner import ComplianceScanner

        scanner = ComplianceScanner()
        result = await scanner.run_full_scan()

        assert result is not None
        assert hasattr(result, 'overall_score')  # Returns ScanResult object
        assert hasattr(result, 'findings')

    @pytest.mark.asyncio
    async def test_scan_history(self):
        """Test scan history retrieval"""
        from backend.compliance.scanner import ComplianceScanner

        scanner = ComplianceScanner()

        # Run a scan first
        await scanner.quick_scan()

        # Get history
        history = scanner.get_scan_history()
        assert isinstance(history, list)


class TestSystemChecker:
    """Test system health checking functionality"""

    def setup_method(self):
        """Set up test environment"""
        self.cli_app = GovSecureCLI()
        self.system_checker = self.cli_app.system_checker

    @pytest.mark.asyncio
    async def test_python_version_check(self):
        """Test Python version checking"""
        result = await self.system_checker.check_python_version()

        assert result is not None
        assert "status" in result
        assert "current" in result
        assert "message" in result
        assert result["status"] in ["passed", "warning", "failed"]

    @pytest.mark.asyncio
    async def test_dependencies_check(self):
        """Test dependency checking"""
        result = await self.system_checker.check_dependencies()

        assert result is not None
        assert "status" in result
        assert "installed" in result
        assert "missing" in result
        assert result["status"] in ["passed", "warning", "failed"]

    @pytest.mark.asyncio
    async def test_openai_connection_check(self):
        """Test OpenAI connection checking"""
        result = await self.system_checker.check_openai_connection()

        assert result is not None
        assert "status" in result
        assert "configured" in result
        # Should be warning since API key is not configured in tests
        assert result["status"] in ["passed", "warning", "failed"]

    @pytest.mark.asyncio
    async def test_file_permissions_check(self):
        """Test file permissions checking"""
        result = await self.system_checker.check_file_permissions()

        assert result is not None
        assert "status" in result
        assert result["status"] in ["passed", "warning", "failed"]

    def test_system_info(self):
        """Test system information gathering"""
        info = self.system_checker.get_system_info()

        assert info is not None
        assert "platform" in info
        assert "python" in info
        assert "system" in info["platform"]
        assert "version" in info["python"]

    def test_recommendations(self):
        """Test system recommendations"""
        recommendations = self.system_checker.get_recommendations()

        assert recommendations is not None
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0


class TestAuthenticationSystem:
    """Test CLI authentication system"""

    def setup_method(self):
        """Set up test environment"""
        self.cli_app = GovSecureCLI()
        self.auth_manager = self.cli_app.auth_manager

    @pytest.mark.asyncio
    async def test_bypass_authentication_dev_mode(self):
        """Test authentication bypass in development mode"""
        # Should succeed in development mode
        result = await self.auth_manager.bypass_authentication()
        assert result is True

    def test_session_management(self):
        """Test session management functionality"""
        # Test session info when not authenticated
        assert not self.auth_manager.is_authenticated()

        # Test current user (should be None when not authenticated)
        user = self.auth_manager.get_current_user()
        assert user is None

    def test_role_checking(self):
        """Test role-based access checking"""
        # Should return False when not authenticated
        assert not self.auth_manager.has_role("admin")
        assert not self.auth_manager.has_any_role(["admin", "user"])


class TestIntegrationScenarios:
    """Test end-to-end integration scenarios"""

    def setup_method(self):
        """Set up test environment"""
        self.cli_app = GovSecureCLI()

    @pytest.mark.asyncio
    async def test_citizen_service_workflow(self):
        """Test complete citizen service workflow"""
        assistant = self.cli_app.government_assistant

        # 1. Set citizen service mode
        await assistant.set_mode(AssistantMode.CITIZEN_SERVICE)

        # 2. Process citizen inquiry
        inquiry = "I need help with my unemployment benefits application"
        response = await assistant.chat(inquiry)

        # 3. Validate response
        assert response is not None
        assert len(response) > 0
        assert any(keyword in response.lower() for keyword in ['benefits', 'unemployment', 'assistance'])

    @pytest.mark.asyncio
    async def test_compliance_workflow(self):
        """Test complete compliance assessment workflow"""
        # 1. Run compliance scan
        from backend.compliance.scanner import ComplianceScanner
        scanner = ComplianceScanner()
        scan_result = await scanner.quick_scan()

        # 2. Analyze results
        assert scan_result is not None
        assert hasattr(scan_result, 'overall_score')

        # 3. Get compliance assistance
        assistant = self.cli_app.government_assistant
        await assistant.set_mode(AssistantMode.COMPLIANCE)
        guidance = await assistant.chat("How can I improve my compliance score?")

        assert guidance is not None
        assert len(guidance) > 0

    @pytest.mark.asyncio
    async def test_document_processing_workflow(self):
        """Test complete document processing workflow"""
        assistant = self.cli_app.government_assistant

        # 1. Analyze document
        test_document = "This is a policy document outlining security procedures for government agencies."
        analysis = await assistant.analyze_document(test_document, "policy")

        assert analysis["analysis_type"] == "policy"
        assert len(analysis["summary"]) > 0

        # 2. Translate document
        translation = await assistant.translate_text(test_document, "Spanish")

        assert translation["target_language"] == "Spanish"
        assert translation["original_text"] == test_document


class TestErrorHandling:
    """Test error handling and edge cases"""

    def setup_method(self):
        """Set up test environment"""
        self.cli_app = GovSecureCLI()

    @pytest.mark.asyncio
    async def test_invalid_assistant_mode(self):
        """Test handling of invalid assistant modes"""
        assistant = self.cli_app.government_assistant

        # Test with invalid mode
        with pytest.raises(ValueError):
            await assistant.set_mode("invalid_mode")

    @pytest.mark.asyncio
    async def test_empty_document_analysis(self):
        """Test document analysis with empty content"""
        assistant = self.cli_app.government_assistant

        # Should handle empty content gracefully
        with pytest.raises(Exception):
            await assistant.analyze_document("", "general")

    @pytest.mark.asyncio
    async def test_system_check_resilience(self):
        """Test system checker resilience to errors"""
        system_checker = self.cli_app.system_checker

        # Should not crash even if some checks fail
        results = await system_checker.check_all()

        assert results is not None
        assert isinstance(results, bool)

    def test_cli_with_missing_config(self):
        """Test CLI behavior with missing configuration"""
        # CLI should still initialize with default config
        with patch('backend.core.config.get_config') as mock_config:
            mock_config.return_value = Mock()
            cli_app = GovSecureCLI()
            assert cli_app is not None


class TestPerformance:
    """Test performance characteristics"""

    def setup_method(self):
        """Set up test environment"""
        self.cli_app = GovSecureCLI()

    @pytest.mark.asyncio
    async def test_chat_response_time(self):
        """Test chat response time is reasonable"""
        import time

        assistant = self.cli_app.government_assistant

        start_time = time.time()
        response = await assistant.chat("What services do you offer?")
        end_time = time.time()

        # Response should be received within 5 seconds (mock responses should be fast)
        assert end_time - start_time < 5.0
        assert response is not None

    @pytest.mark.asyncio
    async def test_compliance_scan_performance(self):
        """Test compliance scan performance"""
        import time

        from backend.compliance.scanner import ComplianceScanner
        scanner = ComplianceScanner()

        start_time = time.time()
        result = await scanner.quick_scan()
        end_time = time.time()

        # Quick scan should complete within 10 seconds
        assert end_time - start_time < 10.0
        assert result is not None

    def test_memory_usage(self):
        """Test memory usage is reasonable"""
        import psutil

        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss

        # Create multiple CLI instances
        cli_instances = [GovSecureCLI() for _ in range(5)]

        memory_after = process.memory_info().rss
        memory_increase = memory_after - memory_before

        # Memory increase should be reasonable (less than 100MB for 5 instances)
        assert memory_increase < 100 * 1024 * 1024  # 100MB

        # Clean up
        del cli_instances


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
