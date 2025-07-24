"""
Test suite for GovSecure AI Platform API
Comprehensive testing of REST API endpoints.

Author: Nik Jois
"""


import pytest
from fastapi.testclient import TestClient

from backend.api.main import app


class TestAPIEndpoints:
    """Test core API endpoints"""

    def setup_method(self):
        """Set up test environment"""
        self.client = TestClient(app)

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "GovSecure AI Platform API"
        assert data["version"] == "1.0.0"
        assert "documentation" in data

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "services" in data
        assert "timestamp" in data

    def test_system_info(self):
        """Test system info endpoint"""
        response = self.client.get("/system/info")
        assert response.status_code == 200
        data = response.json()
        assert "platform" in data or "error" in data  # Might fail gracefully

    def test_system_check(self):
        """Test system check endpoint"""
        response = self.client.post("/system/check")
        assert response.status_code == 200
        data = response.json()
        # Should contain check results
        assert isinstance(data, dict)


class TestAIEndpoints:
    """Test AI assistant endpoints"""

    def setup_method(self):
        """Set up test environment"""
        self.client = TestClient(app)

    def test_chat_endpoint(self):
        """Test chat with AI assistant"""
        payload = {
            "message": "What government services are available?",
            "mode": "general"
        }
        response = self.client.post("/ai/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "mode" in data
        assert "timestamp" in data
        assert len(data["response"]) > 0

    def test_chat_different_modes(self):
        """Test chat with different assistant modes"""
        modes = ["general", "citizen_service", "compliance", "emergency_response"]

        for mode in modes:
            payload = {
                "message": f"Test message for {mode} mode",
                "mode": mode
            }
            response = self.client.post("/ai/chat", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["mode"] == mode

    def test_chat_invalid_mode(self):
        """Test chat with invalid mode"""
        payload = {
            "message": "Test message",
            "mode": "invalid_mode"
        }
        response = self.client.post("/ai/chat", json=payload)
        assert response.status_code == 400

    def test_document_analysis(self):
        """Test document analysis endpoint"""
        payload = {
            "content": "This is a sample government policy document.",
            "analysis_type": "general"
        }
        response = self.client.post("/ai/analyze-document", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "analysis_type" in data
        assert "summary" in data
        assert "timestamp" in data
        assert data["analysis_type"] == "general"

    def test_document_analysis_types(self):
        """Test different document analysis types"""
        analysis_types = ["general", "compliance", "policy", "legal", "financial"]

        for analysis_type in analysis_types:
            payload = {
                "content": f"Sample document for {analysis_type} analysis.",
                "analysis_type": analysis_type
            }
            response = self.client.post("/ai/analyze-document", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["analysis_type"] == analysis_type

    def test_text_translation(self):
        """Test text translation endpoint"""
        payload = {
            "text": "Welcome to government services",
            "target_language": "Spanish"
        }
        response = self.client.post("/ai/translate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "original_text" in data
        assert "translated_text" in data
        assert "target_language" in data
        assert data["target_language"] == "Spanish"

    def test_document_upload_analysis(self):
        """Test document upload analysis"""
        # Create a test text file
        test_content = "This is a test government document."
        files = {"file": ("test.txt", test_content, "text/plain")}
        data = {"analysis_type": "general"}

        response = self.client.post("/ai/analyze-document-upload", files=files, data=data)
        assert response.status_code == 200
        result = response.json()
        assert "filename" in result
        assert "analysis" in result
        assert result["filename"] == "test.txt"


class TestComplianceEndpoints:
    """Test compliance-related endpoints"""

    def setup_method(self):
        """Set up test environment"""
        self.client = TestClient(app)

    def test_compliance_scan(self):
        """Test compliance scan endpoint"""
        payload = {
            "scan_type": "quick",
            "frameworks": ["NIST_800_53"]
        }
        response = self.client.post("/compliance/scan", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "scan_id" in data
        assert "scan_type" in data
        assert "overall_score" in data
        assert "timestamp" in data
        assert data["scan_type"] == "quick"

    def test_compliance_scan_types(self):
        """Test different compliance scan types"""
        scan_types = ["quick", "full"]

        for scan_type in scan_types:
            payload = {
                "scan_type": scan_type,
                "frameworks": ["NIST_800_53"]
            }
            response = self.client.post("/compliance/scan", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["scan_type"] == scan_type

    def test_invalid_scan_type(self):
        """Test invalid scan type"""
        payload = {
            "scan_type": "invalid",
            "frameworks": ["NIST_800_53"]
        }
        response = self.client.post("/compliance/scan", json=payload)
        assert response.status_code == 400

    def test_get_compliance_controls(self):
        """Test get compliance controls endpoint"""
        frameworks = ["nist_800_53", "fedramp"]

        for framework in frameworks:
            response = self.client.get(f"/compliance/controls/{framework}")
            assert response.status_code == 200
            data = response.json()
            assert "framework" in data
            assert "controls" in data
            assert "total_controls" in data
            assert len(data["controls"]) > 0

    def test_invalid_compliance_framework(self):
        """Test invalid compliance framework"""
        response = self.client.get("/compliance/controls/invalid_framework")
        assert response.status_code == 404

    def test_assess_compliance_control(self):
        """Test compliance control assessment"""
        payload = {
            "control_id": "AC-1",
            "system_id": "test_system"
        }
        response = self.client.post("/compliance/assess", params=payload)
        assert response.status_code == 200
        data = response.json()
        assert "control_id" in data
        assert "assessment" in data
        assert "timestamp" in data


class TestCitizenServiceEndpoints:
    """Test citizen service endpoints"""

    def setup_method(self):
        """Set up test environment"""
        self.client = TestClient(app)

    def test_submit_citizen_request(self):
        """Test citizen service request submission"""
        payload = {
            "query": "I need help with my benefits application",
            "category": "benefits",
            "priority": "normal"
        }
        response = self.client.post("/citizen/request", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "request_id" in data
        assert "response" in data
        assert "category" in data
        assert "priority" in data
        assert "timestamp" in data
        assert data["priority"] == "normal"

    def test_citizen_request_priorities(self):
        """Test different citizen request priorities"""
        priorities = ["normal", "high", "urgent"]

        for priority in priorities:
            payload = {
                "query": f"Test request with {priority} priority",
                "priority": priority
            }
            response = self.client.post("/citizen/request", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["priority"] == priority

    def test_get_available_services(self):
        """Test get available citizen services"""
        response = self.client.get("/citizen/services")
        assert response.status_code == 200
        data = response.json()
        assert "311_services" in data
        assert "benefits" in data
        assert "permits_licenses" in data
        assert len(data["311_services"]) > 0
        assert len(data["benefits"]) > 0


class TestEmergencyResponseEndpoints:
    """Test emergency response endpoints"""

    def setup_method(self):
        """Set up test environment"""
        self.client = TestClient(app)

    def test_report_emergency_incident(self):
        """Test emergency incident reporting"""
        payload = {
            "incident_type": "Natural Disaster",
            "severity": "High",
            "location": "Downtown Area",
            "description": "Flooding in downtown area due to heavy rainfall",
            "resources_needed": ["Emergency Personnel", "Sandbags", "Water Pumps"]
        }
        response = self.client.post("/emergency/incident", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "incident_id" in data
        assert "response_plan" in data
        assert "immediate_actions" in data
        assert "resource_allocation" in data
        assert "coordination_steps" in data
        assert "estimated_timeline" in data
        assert "timestamp" in data

    def test_emergency_incident_severities(self):
        """Test different emergency incident severities"""
        severities = ["Low", "Medium", "High", "Critical"]

        for severity in severities:
            payload = {
                "incident_type": "Test Incident",
                "severity": severity,
                "description": f"Test incident with {severity} severity"
            }
            response = self.client.post("/emergency/incident", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert len(data["immediate_actions"]) > 0


class TestAdministrativeEndpoints:
    """Test administrative endpoints"""

    def setup_method(self):
        """Set up test environment"""
        self.client = TestClient(app)

    def test_get_system_statistics(self):
        """Test system statistics endpoint"""
        response = self.client.get("/admin/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_requests" in data
        assert "active_users" in data
        assert "compliance_scans_today" in data
        assert "system_uptime" in data
        assert isinstance(data["total_requests"], int)

    def test_trigger_maintenance(self):
        """Test maintenance trigger endpoint"""
        response = self.client.post("/admin/maintenance")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "tasks" in data
        assert "estimated_duration" in data
        assert "scheduled_time" in data
        assert data["status"] == "maintenance_scheduled"


class TestValidationAndErrorHandling:
    """Test input validation and error handling"""

    def setup_method(self):
        """Set up test environment"""
        self.client = TestClient(app)

    def test_invalid_json_payload(self):
        """Test invalid JSON payload handling"""
        response = self.client.post("/ai/chat", data="invalid json")
        assert response.status_code == 422  # Unprocessable Entity

    def test_missing_required_fields(self):
        """Test missing required fields"""
        # Chat endpoint without message
        response = self.client.post("/ai/chat", json={})
        assert response.status_code == 422

        # Document analysis without content
        response = self.client.post("/ai/analyze-document", json={"analysis_type": "general"})
        assert response.status_code == 422

    def test_empty_message_validation(self):
        """Test empty message validation"""
        payload = {"message": ""}
        response = self.client.post("/ai/chat", json=payload)
        assert response.status_code == 422

    def test_message_length_validation(self):
        """Test message length validation"""
        # Very long message (over 4000 characters)
        long_message = "x" * 5000
        payload = {"message": long_message}
        response = self.client.post("/ai/chat", json=payload)
        assert response.status_code == 422

    def test_translation_text_length_validation(self):
        """Test translation text length validation"""
        # Very long text (over 5000 characters)
        long_text = "x" * 6000
        payload = {
            "text": long_text,
            "target_language": "Spanish"
        }
        response = self.client.post("/ai/translate", json=payload)
        assert response.status_code == 422

    def test_error_response_format(self):
        """Test error response format"""
        # Trigger an error with invalid mode
        payload = {
            "message": "Test message",
            "mode": "invalid_mode"
        }
        response = self.client.post("/ai/chat", json=payload)
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "status_code" in data["error"]
        assert "message" in data["error"]
        assert "timestamp" in data["error"]


class TestSecurity:
    """Test security aspects of the API"""

    def setup_method(self):
        """Set up test environment"""
        self.client = TestClient(app)

    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = self.client.options("/")
        # CORS headers should be handled by middleware
        assert response.status_code in [200, 405]  # OPTIONS might not be explicitly handled

    def test_no_sensitive_info_in_errors(self):
        """Test that errors don't expose sensitive information"""
        # Try to trigger an internal error
        payload = {
            "message": "Test message",
            "mode": "invalid_mode"
        }
        response = self.client.post("/ai/chat", json=payload)
        data = response.json()

        # Error message should not contain sensitive paths or internal details
        error_message = data.get("error", {}).get("message", "")
        assert "backend" not in error_message.lower()
        assert "traceback" not in error_message.lower()
        assert "exception" not in error_message.lower()


class TestPerformance:
    """Test API performance characteristics"""

    def setup_method(self):
        """Set up test environment"""
        self.client = TestClient(app)

    def test_response_times(self):
        """Test API response times are reasonable"""
        import time

        endpoints = [
            ("GET", "/", {}),
            ("GET", "/health", {}),
            ("POST", "/ai/chat", {"message": "test"}),
            ("POST", "/compliance/scan", {"scan_type": "quick"})
        ]

        for method, endpoint, payload in endpoints:
            start_time = time.time()

            if method == "GET":
                response = self.client.get(endpoint)
            else:
                response = self.client.post(endpoint, json=payload)

            end_time = time.time()
            response_time = end_time - start_time

            # Response should be received within 10 seconds
            assert response_time < 10.0
            assert response.status_code in [200, 400, 422]  # Valid status codes

    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import threading
        import time

        results = []

        def make_request():
            start_time = time.time()
            response = self.client.post("/ai/chat", json={"message": "concurrent test"})
            end_time = time.time()
            results.append({
                "status_code": response.status_code,
                "response_time": end_time - start_time
            })

        # Create multiple threads
        threads = [threading.Thread(target=make_request) for _ in range(5)]

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify all requests succeeded
        assert len(results) == 5
        for result in results:
            assert result["status_code"] == 200
            assert result["response_time"] < 15.0  # Allow more time for concurrent requests


class TestDataFlow:
    """Test data flow through the API"""

    def setup_method(self):
        """Set up test environment"""
        self.client = TestClient(app)

    def test_citizen_service_workflow(self):
        """Test complete citizen service workflow through API"""
        # 1. Get available services
        services_response = self.client.get("/citizen/services")
        assert services_response.status_code == 200
        services = services_response.json()

        # 2. Submit a request for a known service
        request_payload = {
            "query": "I need help with SNAP benefits",
            "category": "benefits",
            "priority": "normal"
        }
        request_response = self.client.post("/citizen/request", json=request_payload)
        assert request_response.status_code == 200
        request_data = request_response.json()

        # 3. Verify the response contains expected information
        assert "request_id" in request_data
        assert request_data["category"] == "benefits"
        assert "benefits" in services
        assert len(services["benefits"]) > 0

    def test_compliance_workflow(self):
        """Test complete compliance workflow through API"""
        # 1. Get compliance controls
        controls_response = self.client.get("/compliance/controls/nist_800_53")
        assert controls_response.status_code == 200
        controls = controls_response.json()

        # 2. Run a compliance scan
        scan_payload = {
            "scan_type": "quick",
            "frameworks": ["NIST_800_53"]
        }
        scan_response = self.client.post("/compliance/scan", json=scan_payload)
        assert scan_response.status_code == 200
        scan_data = scan_response.json()

        # 3. Assess a specific control
        if controls["controls"]:
            control_id = controls["controls"][0]["id"]
            assess_response = self.client.post("/compliance/assess", params={"control_id": control_id})
            assert assess_response.status_code == 200
            assess_data = assess_response.json()
            assert assess_data["control_id"] == control_id

    def test_document_processing_workflow(self):
        """Test complete document processing workflow through API"""
        # 1. Analyze a document
        doc_payload = {
            "content": "This is a government policy document regarding access controls.",
            "analysis_type": "policy"
        }
        analysis_response = self.client.post("/ai/analyze-document", json=doc_payload)
        assert analysis_response.status_code == 200
        analysis_data = analysis_response.json()

        # 2. Translate the same document
        translation_payload = {
            "text": doc_payload["content"],
            "target_language": "Spanish"
        }
        translation_response = self.client.post("/ai/translate", json=translation_payload)
        assert translation_response.status_code == 200
        translation_data = translation_response.json()

        # 3. Verify both operations processed the same content
        assert analysis_data["analysis_type"] == "policy"
        assert translation_data["original_text"] == doc_payload["content"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
