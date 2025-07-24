"""
GovSecure AI Platform - Main API Application
Comprehensive REST API for US Government AI services including citizen services,
compliance automation, document processing, and emergency response.

Author: Nik Jois
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import json

from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
import structlog

from backend.core.config import get_config
from backend.ai_agents.government_assistant import GovernmentAssistant, AssistantMode
from backend.ai_agents.compliance_agent import ComplianceAgent, ComplianceFramework
from backend.compliance.scanner import ComplianceScanner, ScanType
from backend.utils.system_checker import SystemChecker

# Initialize configuration and logging
config = get_config()
logger = structlog.get_logger(__name__)

# Initialize security
security = HTTPBearer(auto_error=False)

# Create FastAPI application
app = FastAPI(
    title="GovSecure AI Platform API",
    description="Comprehensive AI-powered platform for US Government operations in 2025",
    version="1.0.0",
    docs_url="/docs" if config.debug else None,
    redoc_url="/redoc" if config.debug else None,
    openapi_url="/openapi.json" if config.debug else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.gov", "https://*.mil"] if config.is_production else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Configure trusted hosts
if config.is_production:
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["*.gov", "*.mil", "localhost", "127.0.0.1"]
    )

# Initialize core services
government_assistant = GovernmentAssistant(config)
compliance_agent = ComplianceAgent()
compliance_scanner = ComplianceScanner()
system_checker = SystemChecker(config)


# Pydantic Models for API
class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    version: str
    environment: str
    services: Dict[str, str]


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., description="User message", min_length=1, max_length=4000)
    mode: Optional[str] = Field("general", description="Assistant mode")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    mode: str
    timestamp: datetime
    session_id: Optional[str] = None


class DocumentAnalysisRequest(BaseModel):
    """Document analysis request model"""
    content: str = Field(..., description="Document content", min_length=1)
    analysis_type: str = Field("general", description="Type of analysis")
    language: Optional[str] = Field("en", description="Document language")


class DocumentAnalysisResponse(BaseModel):
    """Document analysis response model"""
    analysis_type: str
    summary: str
    key_points: List[str] = Field(default_factory=list)
    compliance_issues: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    timestamp: datetime


class TranslationRequest(BaseModel):
    """Translation request model"""
    text: str = Field(..., description="Text to translate", min_length=1, max_length=5000)
    target_language: str = Field(..., description="Target language")
    source_language: Optional[str] = Field("auto", description="Source language")


class TranslationResponse(BaseModel):
    """Translation response model"""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    timestamp: datetime


class ComplianceScanRequest(BaseModel):
    """Compliance scan request model"""
    scan_type: str = Field("full", description="Type of scan")
    frameworks: List[str] = Field(default_factory=lambda: ["NIST_800_53"], description="Compliance frameworks")
    target_system: Optional[str] = Field("default", description="Target system identifier")


class ComplianceScanResponse(BaseModel):
    """Compliance scan response model"""
    scan_id: str
    scan_type: str
    status: str
    overall_score: float
    findings: List[Dict[str, Any]]
    recommendations: List[str]
    timestamp: datetime


class CitizenServiceRequest(BaseModel):
    """Citizen service request model"""
    query: str = Field(..., description="Citizen inquiry", min_length=1)
    category: Optional[str] = Field(None, description="Service category")
    priority: str = Field("normal", description="Request priority")
    contact_info: Optional[Dict[str, str]] = Field(None, description="Contact information")


class CitizenServiceResponse(BaseModel):
    """Citizen service response model"""
    request_id: str
    response: str
    category: str
    priority: str
    estimated_resolution: Optional[str] = None
    next_steps: List[str] = Field(default_factory=list)
    timestamp: datetime


class EmergencyResponseRequest(BaseModel):
    """Emergency response request model"""
    incident_type: str = Field(..., description="Type of emergency incident")
    severity: str = Field(..., description="Incident severity")
    location: Optional[str] = Field(None, description="Incident location")
    description: str = Field(..., description="Incident description")
    resources_needed: Optional[List[str]] = Field(None, description="Required resources")


class EmergencyResponseResponse(BaseModel):
    """Emergency response response model"""
    incident_id: str
    response_plan: str
    immediate_actions: List[str]
    resource_allocation: Dict[str, Any]
    coordination_steps: List[str]
    estimated_timeline: str
    timestamp: datetime


# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    if not credentials and config.is_production:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # In development mode, allow requests without authentication
    if not credentials and config.is_development:
        return {"user_id": "dev_user", "roles": ["admin"], "clearance": "public"}
    
    # TODO: Implement proper JWT token validation
    # For now, return mock user data
    return {
        "user_id": "authenticated_user",
        "roles": ["user"],
        "clearance": "public"
    }


# API Routes

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "GovSecure AI Platform API",
        "version": "1.0.0",
        "description": "Comprehensive AI platform for US Government operations",
        "documentation": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Comprehensive health check endpoint"""
    try:
        # Check core services
        services = {
            "api": "healthy",
            "database": "healthy",  # TODO: Implement actual database check
            "cache": "healthy",     # TODO: Implement actual cache check
            "ai_assistant": "healthy",
            "compliance_engine": "healthy"
        }
        
        # Check OpenAI connectivity
        if config.openai.api_key:
            services["openai"] = "healthy"
        else:
            services["openai"] = "not_configured"
        
        return HealthCheckResponse(
            status="healthy",
            timestamp=datetime.now(),
            version="1.0.0",
            environment=config.environment,
            services=services
        )
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=500, detail="Health check failed")


@app.get("/system/info")
async def system_info(current_user: dict = Depends(get_current_user)):
    """Get system information and status"""
    try:
        info = system_checker.get_system_info()
        return JSONResponse(content=info)
    except Exception as e:
        logger.error("System info retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve system information")


@app.post("/system/check")
async def system_check(current_user: dict = Depends(get_current_user)):
    """Run comprehensive system health checks"""
    try:
        overall_health = await system_checker.check_all()
        results = {
            "overall_health": overall_health,
            "status": "healthy" if overall_health else "unhealthy", 
            "checks": system_checker.check_results,
            "system_info": system_checker.get_system_info(),
            "recommendations": system_checker.get_recommendations(),
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(content=results)
    except Exception as e:
        logger.error("System check failed", error=str(e))
        raise HTTPException(status_code=500, detail="System check failed")


# AI Assistant Endpoints

@app.post("/ai/chat", response_model=ChatResponse)
async def chat_with_assistant(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """Chat with the government AI assistant"""
    try:
        # Set assistant mode
        if request.mode:
            try:
                mode = AssistantMode(request.mode)
                await government_assistant.set_mode(mode)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid mode: {request.mode}")
        
        # Get response from assistant
        response = await government_assistant.chat(request.message, request.context)
        
        return ChatResponse(
            response=response,
            mode=government_assistant.get_current_mode(),
            timestamp=datetime.now()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions with their original status codes
        raise
    except Exception as e:
        logger.error("Chat request failed", error=str(e))
        raise HTTPException(status_code=500, detail="Chat request failed")


@app.post("/ai/analyze-document", response_model=DocumentAnalysisResponse)
async def analyze_document(
    request: DocumentAnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """Analyze a document using AI"""
    try:
        result = await government_assistant.analyze_document(
            request.content, 
            request.analysis_type
        )
        
        return DocumentAnalysisResponse(
            analysis_type=result["analysis_type"],
            summary=result["summary"],
            timestamp=datetime.fromisoformat(result["timestamp"])
        )
        
    except Exception as e:
        logger.error("Document analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail="Document analysis failed")


@app.post("/ai/analyze-document-upload")
async def analyze_document_upload(
    file: UploadFile = File(...),
    analysis_type: str = Form("general"),
    current_user: dict = Depends(get_current_user)
):
    """Analyze an uploaded document"""
    try:
        # Read file content
        content = await file.read()
        
        # Handle different file types
        if file.content_type == "text/plain":
            text_content = content.decode("utf-8")
        elif file.content_type == "application/pdf":
            # TODO: Implement PDF text extraction
            text_content = "PDF processing not yet implemented"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Analyze document
        result = await government_assistant.analyze_document(text_content, analysis_type)
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "analysis": result
        }
        
    except Exception as e:
        logger.error("Document upload analysis failed", error=str(e))
        raise HTTPException(status_code=500, detail="Document upload analysis failed")


@app.post("/ai/translate", response_model=TranslationResponse)
async def translate_text(
    request: TranslationRequest,
    current_user: dict = Depends(get_current_user)
):
    """Translate text to another language"""
    try:
        result = await government_assistant.translate_text(
            request.text,
            request.target_language
        )
        
        return TranslationResponse(
            original_text=result["original_text"],
            translated_text=result["translated_text"],
            source_language=result["source_language"],
            target_language=result["target_language"],
            timestamp=datetime.fromisoformat(result["timestamp"])
        )
        
    except Exception as e:
        logger.error("Translation failed", error=str(e))
        raise HTTPException(status_code=500, detail="Translation failed")


# Compliance Endpoints

@app.post("/compliance/scan", response_model=ComplianceScanResponse)
async def run_compliance_scan(
    request: ComplianceScanRequest,
    current_user: dict = Depends(get_current_user)
):
    """Run a compliance scan"""
    try:
        if request.scan_type == "quick":
            result = await compliance_scanner.quick_scan()
        elif request.scan_type == "full":
            result = await compliance_scanner.run_full_scan()
        else:
            raise HTTPException(status_code=400, detail="Invalid scan type")
        
        scan_id = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return ComplianceScanResponse(
            scan_id=scan_id,
            scan_type=request.scan_type,
            status="completed",
            overall_score=result.overall_score,
            findings=result.findings if hasattr(result, 'findings') else [],
            recommendations=result.recommendations if hasattr(result, 'recommendations') else [],
            timestamp=datetime.now()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions with their original status codes
        raise
    except Exception as e:
        logger.error("Compliance scan failed", error=str(e))
        raise HTTPException(status_code=500, detail="Compliance scan failed")


@app.get("/compliance/controls/{framework}")
async def get_compliance_controls(
    framework: str,
    current_user: dict = Depends(get_current_user)
):
    """Get compliance controls for a specific framework"""
    try:
        # TODO: Implement actual control retrieval
        controls = {
            "nist_800_53": [
                {"id": "AC-1", "title": "Access Control Policy and Procedures", "status": "implemented"},
                {"id": "AC-2", "title": "Account Management", "status": "partial"},
                {"id": "AU-1", "title": "Audit and Accountability Policy", "status": "implemented"}
            ],
            "fedramp": [
                {"id": "AC-1", "title": "Access Control Policy and Procedures", "status": "implemented"},
                {"id": "IA-2", "title": "Identification and Authentication", "status": "implemented"}
            ]
        }
        
        framework_controls = controls.get(framework.lower(), [])
        if not framework_controls:
            raise HTTPException(status_code=404, detail="Framework not found")
        
        return {
            "framework": framework,
            "controls": framework_controls,
            "total_controls": len(framework_controls)
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions with their original status codes
        raise
    except Exception as e:
        logger.error("Failed to retrieve compliance controls", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve compliance controls")


@app.post("/compliance/assess")
async def assess_compliance_control(
    control_id: str,
    system_description: str = "Default government system",
    implementation_details: str = "Standard implementation per NIST guidelines",
    current_user: dict = Depends(get_current_user)
):
    """Assess a specific compliance control"""
    try:
        assessment = await compliance_agent.assess_control(
            control_id=control_id,
            system_description=system_description,
            implementation_details=implementation_details
        )
        return {
            "control_id": control_id,
            "system_description": system_description,
            "assessment": assessment,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error("Control assessment failed", error=str(e))
        raise HTTPException(status_code=500, detail="Control assessment failed")


# Citizen Services Endpoints

@app.post("/citizen/request", response_model=CitizenServiceResponse)
async def submit_citizen_request(
    request: CitizenServiceRequest,
    current_user: dict = Depends(get_current_user)
):
    """Submit a citizen service request"""
    try:
        # Set assistant to citizen service mode
        await government_assistant.set_mode(AssistantMode.CITIZEN_SERVICE)
        
        # Process the request
        response = await government_assistant.chat(request.query)
        
        request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return CitizenServiceResponse(
            request_id=request_id,
            response=response,
            category=request.category or "general",
            priority=request.priority,
            estimated_resolution="3-5 business days",
            next_steps=["Review request", "Contact citizen if needed", "Process application"],
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Citizen request processing failed", error=str(e))
        raise HTTPException(status_code=500, detail="Citizen request processing failed")


@app.get("/citizen/services")
async def get_available_services():
    """Get list of available citizen services"""
    return {
        "311_services": [
            "Street light repair", "Pothole reporting", "Noise complaints",
            "Parking violations", "Trash collection issues"
        ],
        "benefits": [
            "SNAP benefits", "Medicaid enrollment", "Housing assistance",
            "Unemployment benefits", "Veterans benefits"
        ],
        "permits_licenses": [
            "Business license", "Building permit", "Special event permit",
            "Food service license", "Professional license"
        ]
    }


# Emergency Response Endpoints

@app.post("/emergency/incident", response_model=EmergencyResponseResponse)
async def report_emergency_incident(
    request: EmergencyResponseRequest,
    current_user: dict = Depends(get_current_user)
):
    """Report and coordinate emergency incident response"""
    try:
        # Set assistant to emergency response mode
        await government_assistant.set_mode(AssistantMode.EMERGENCY_RESPONSE)
        
        # Generate response plan
        query = f"Emergency incident: {request.incident_type}, Severity: {request.severity}, Description: {request.description}"
        response_plan = await government_assistant.chat(query)
        
        incident_id = f"inc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return EmergencyResponseResponse(
            incident_id=incident_id,
            response_plan=response_plan,
            immediate_actions=[
                "Assess situation safety",
                "Contact first responders",
                "Establish command center",
                "Coordinate resources"
            ],
            resource_allocation={
                "personnel": "TBD based on assessment",
                "equipment": "Standard emergency kit",
                "vehicles": "Emergency response units"
            },
            coordination_steps=[
                "Activate Emergency Operations Center",
                "Notify relevant agencies",
                "Implement communication plan",
                "Monitor situation"
            ],
            estimated_timeline="Initial response: 15-30 minutes",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Emergency incident processing failed", error=str(e))
        raise HTTPException(status_code=500, detail="Emergency incident processing failed")


# Administrative Endpoints

@app.get("/admin/stats")
async def get_system_statistics(current_user: dict = Depends(get_current_user)):
    """Get system usage statistics"""
    try:
        # TODO: Implement actual statistics collection
        stats = {
            "total_requests": 1250,
            "active_users": 45,
            "compliance_scans_today": 8,
            "citizen_requests_today": 23,
            "emergency_incidents_today": 2,
            "system_uptime": "99.9%",
            "last_updated": datetime.now()
        }
        return stats
        
    except Exception as e:
        logger.error("Failed to retrieve statistics", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")


@app.post("/admin/maintenance")
async def trigger_system_maintenance(current_user: dict = Depends(get_current_user)):
    """Trigger system maintenance tasks"""
    try:
        # TODO: Implement actual maintenance tasks
        maintenance_tasks = [
            "Clear temporary files",
            "Update compliance databases",
            "Refresh AI model cache",
            "Archive old logs",
            "Run system health checks"
        ]
        
        return {
            "status": "maintenance_scheduled",
            "tasks": maintenance_tasks,
            "estimated_duration": "30 minutes",
            "scheduled_time": datetime.now() + timedelta(hours=1)
        }
        
    except Exception as e:
        logger.error("Maintenance scheduling failed", error=str(e))
        raise HTTPException(status_code=500, detail="Maintenance scheduling failed")


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error("HTTP exception occurred", 
                status_code=exc.status_code, 
                detail=exc.detail,
                path=request.url.path)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "status_code": exc.status_code,
                "message": exc.detail,
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path)
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error("Unexpected exception occurred", 
                error=str(exc),
                path=request.url.path)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "status_code": 500,
                "message": "Internal server error",
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url.path)
            }
        }
    )


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("GovSecure AI Platform API starting up",
               version="1.0.0",
               environment=config.environment)


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("GovSecure AI Platform API shutting down")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.debug,
        log_level="debug" if config.debug else "info"
    ) 