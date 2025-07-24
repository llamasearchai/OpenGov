"""
Government AI Assistant
Comprehensive AI assistant for US government operations including citizen services,
document processing, compliance assistance, and emergency response coordination.

Author: Nik Jois
"""

import asyncio
import logging
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import json
import re

from pydantic import BaseModel, Field
import openai
from openai import AsyncOpenAI

from backend.core.config import get_config


class AssistantMode(Enum):
    """Operating modes for the government assistant"""
    GENERAL = "general"
    CITIZEN_SERVICE = "citizen_service"
    COMPLIANCE = "compliance"
    EMERGENCY_RESPONSE = "emergency_response"
    DOCUMENT_ANALYSIS = "document_analysis"
    TRANSLATION = "translation"


class DocumentAnalysisResult(BaseModel):
    """Result of document analysis"""
    analysis_type: str
    summary: str
    key_points: List[str] = Field(default_factory=list)
    entities: Dict[str, List[str]] = Field(default_factory=dict)
    sentiment: Optional[str] = None
    compliance_issues: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class TranslationResult(BaseModel):
    """Result of text translation"""
    source_language: str
    target_language: str
    original_text: str
    translated_text: str
    confidence_score: Optional[float] = None


class CitizenServiceQuery(BaseModel):
    """Structured citizen service query"""
    query_type: str
    category: str
    priority: str
    summary: str
    suggested_actions: List[str] = Field(default_factory=list)
    required_documents: List[str] = Field(default_factory=list)
    estimated_processing_time: Optional[str] = None


class GovernmentAssistant:
    """
    Comprehensive AI Assistant for US Government Operations
    
    Provides intelligent assistance for:
    - Citizen service automation (311, benefits, permits)
    - Document analysis and processing
    - Multi-language translation services
    - Compliance validation and guidance
    - Emergency response coordination
    - Policy analysis and recommendation
    """
    
    def __init__(self, config=None):
        self.config = config or get_config()
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI clients
        self.openai_client = None
        self.async_openai_client = None
        
        try:
            if self.config.openai.api_key:
                self.openai_client = openai.OpenAI(
                    api_key=self.config.openai.api_key,
                    organization=self.config.openai.organization
                )
                self.async_openai_client = AsyncOpenAI(
                    api_key=self.config.openai.api_key,
                    organization=self.config.openai.organization
                )
                self.logger.info("OpenAI client initialized successfully")
            else:
                self.logger.warning("OpenAI API key not configured - using mock responses")
        except Exception as e:
            self.logger.warning(f"Failed to initialize OpenAI client: {e}")
        
        # Current assistant mode
        self.current_mode = AssistantMode.GENERAL
        
        # Knowledge bases for different domains
        self._load_knowledge_bases()
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        
    def _load_knowledge_bases(self):
        """Load domain-specific knowledge bases"""
        self.knowledge_bases = {
            "citizen_services": {
                "311_services": [
                    "Street light repair", "Pothole reporting", "Noise complaints",
                    "Parking violations", "Trash collection issues", "Water main breaks",
                    "Park maintenance", "Building permits", "Business licenses"
                ],
                "benefits": [
                    "SNAP benefits", "Medicaid enrollment", "Housing assistance",
                    "Unemployment benefits", "Social Security", "Veterans benefits",
                    "Child care assistance", "Energy assistance", "Senior services"
                ],
                "permits_licenses": [
                    "Business license", "Building permit", "Special event permit",
                    "Vendor permit", "Parking permit", "Construction permit",
                    "Liquor license", "Food service license", "Professional license"
                ]
            },
            "emergency_categories": [
                "Natural disasters", "Public health emergencies", "Security threats",
                "Infrastructure failures", "Environmental hazards", "Civil unrest",
                "Cybersecurity incidents", "Supply chain disruptions"
            ],
            "compliance_frameworks": [
                "NIST 800-53", "FedRAMP", "FISMA", "CMMC", "SOX", "HIPAA",
                "GDPR", "CCPA", "PCI DSS", "ISO 27001", "SOC 2"
            ],
            "government_agencies": {
                "federal": ["DHS", "DOD", "HHS", "DOE", "DOJ", "State", "Treasury"],
                "state": ["DMV", "Health Department", "Education", "Environmental"],
                "local": ["Police", "Fire", "Public Works", "Planning", "Parks"]
            }
        }
    
    async def set_mode(self, mode):
        """Set the operating mode of the assistant"""
        # Validate mode - accept both string and AssistantMode enum
        if isinstance(mode, str):
            try:
                mode = AssistantMode(mode)
            except ValueError:
                raise ValueError(f"Invalid assistant mode: {mode}")
        elif not isinstance(mode, AssistantMode):
            raise ValueError(f"Mode must be AssistantMode enum or string, got {type(mode)}")
        
        self.current_mode = mode
        self.logger.info(f"Assistant mode set to: {mode.value}")
        
        # Clear conversation history when switching modes
        self.conversation_history = []
    
    async def chat(self, message: str, context: Optional[Dict] = None) -> str:
        """
        Main chat interface with mode-aware responses
        
        Args:
            message: User input message
            context: Additional context for the conversation
            
        Returns:
            Assistant response as string
        """
        try:
            # Add message to conversation history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "role": "user",
                "content": message,
                "mode": self.current_mode.value
            })
            
            # Generate response based on current mode
            if self.current_mode == AssistantMode.CITIZEN_SERVICE:
                response = await self._handle_citizen_service(message, context)
            elif self.current_mode == AssistantMode.COMPLIANCE:
                response = await self._handle_compliance_query(message, context)
            elif self.current_mode == AssistantMode.EMERGENCY_RESPONSE:
                response = await self._handle_emergency_response(message, context)
            else:
                response = await self._handle_general_query(message, context)
            
            # Add response to conversation history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "role": "assistant",
                "content": response,
                "mode": self.current_mode.value
            })
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in chat: {e}")
            return f"I apologize, but I encountered an error processing your request. Please try again or contact technical support."
    
    async def _handle_citizen_service(self, message: str, context: Optional[Dict] = None) -> str:
        """Handle citizen service inquiries"""
        
        # Determine service category
        service_category = self._categorize_citizen_service(message)
        
        if not self.async_openai_client:
            # Mock response for when OpenAI is not available
            return self._generate_mock_citizen_response(message, service_category)
        
        try:
            system_prompt = f"""You are a helpful government customer service representative assisting citizens with {service_category} services. 

Key responsibilities:
- Provide accurate information about government services
- Guide citizens through processes step-by-step
- Identify required documents and forms
- Estimate processing times
- Offer alternative solutions when possible
- Maintain a professional, empathetic tone
- Reference relevant government websites and contact information

Available services in {service_category}:
{json.dumps(self.knowledge_bases['citizen_services'].get(service_category, []), indent=2)}

Current conversation context: {self.current_mode.value}
"""
            
            response = await self.async_openai_client.chat.completions.create(
                model=self.config.openai.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=self.config.openai.max_tokens,
                temperature=self.config.openai.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error in citizen service handler: {e}")
            return self._generate_mock_citizen_response(message, service_category)
    
    def _categorize_citizen_service(self, message: str) -> str:
        """Categorize citizen service inquiry"""
        message_lower = message.lower()
        
        # 311 services keywords
        if any(keyword in message_lower for keyword in ['street', 'pothole', 'noise', 'parking', 'trash', 'water', 'light']):
            return "311_services"
        
        # Benefits keywords
        if any(keyword in message_lower for keyword in ['snap', 'medicaid', 'housing', 'unemployment', 'benefits', 'assistance']):
            return "benefits"
        
        # Permits and licenses keywords
        if any(keyword in message_lower for keyword in ['permit', 'license', 'business', 'building', 'event']):
            return "permits_licenses"
        
        return "311_services"  # Default category
    
    def _generate_mock_citizen_response(self, message: str, category: str) -> str:
        """Generate mock response for citizen services when OpenAI is unavailable"""
        responses = {
            "311_services": f"Thank you for contacting 311 services. I understand you're inquiring about: {message[:50]}... For immediate assistance with street maintenance, utilities, or city services, please call 311 or visit your city's website. I can help you identify the specific department and required information for your request.",
            
            "benefits": f"I'm here to help you with government benefits and assistance programs. Based on your inquiry about: {message[:50]}... I can guide you through eligibility requirements, application processes, and required documentation. Would you like information about SNAP, Medicaid, housing assistance, or another specific program?",
            
            "permits_licenses": f"Thank you for your inquiry about permits and licenses: {message[:50]}... I can help you understand the application process, required documents, fees, and processing times. Please let me know the specific type of permit or license you need, and I'll provide detailed guidance."
        }
        
        return responses.get(category, "Thank you for contacting government services. I'm here to help you navigate government processes and find the information you need. Please provide more details about what service or assistance you're looking for.")
    
    async def _handle_compliance_query(self, message: str, context: Optional[Dict] = None) -> str:
        """Handle compliance-related queries"""
        
        if not self.async_openai_client:
            return self._generate_mock_compliance_response(message)
        
        try:
            system_prompt = f"""You are a compliance expert specializing in government and federal regulations. 

Your expertise covers:
- NIST 800-53 Security Controls
- FedRAMP compliance requirements
- FISMA implementation
- CMMC certification levels
- SOX financial controls
- Data protection regulations (GDPR, CCPA)
- Industry standards (ISO 27001, SOC 2)

Available frameworks: {', '.join(self.knowledge_bases['compliance_frameworks'])}

Provide specific, actionable guidance including:
- Relevant control requirements
- Implementation recommendations
- Risk assessment considerations
- Documentation requirements
- Audit preparation steps

Current context: Government compliance assistance
"""
            
            response = await self.async_openai_client.chat.completions.create(
                model=self.config.openai.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=self.config.openai.max_tokens,
                temperature=0.3  # Lower temperature for more precise compliance guidance
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error in compliance handler: {e}")
            return self._generate_mock_compliance_response(message)
    
    def _generate_mock_compliance_response(self, message: str) -> str:
        """Generate mock compliance response"""
        return f"""Based on your compliance inquiry: {message[:100]}...

I can provide guidance on government compliance frameworks including:

• NIST 800-53: Federal security controls and implementation guidance
• FedRAMP: Cloud security requirements for government systems  
• FISMA: Federal information security management requirements
• CMMC: Cybersecurity maturity model for defense contractors

For specific control implementations, I recommend:
1. Reviewing the applicable framework documentation
2. Conducting a gap analysis against current state
3. Developing implementation roadmap with timelines
4. Establishing continuous monitoring processes

Would you like detailed guidance on any specific compliance framework or control family?"""
    
    async def _handle_emergency_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Handle emergency response coordination queries"""
        
        if not self.async_openai_client:
            return self._generate_mock_emergency_response(message)
        
        try:
            system_prompt = f"""You are an emergency management coordinator assisting with emergency response planning and coordination.

Your responsibilities include:
- Emergency response planning and protocols
- Resource coordination and allocation
- Inter-agency communication
- Public safety coordination
- Disaster recovery planning
- Crisis communication strategies

Emergency categories: {', '.join(self.knowledge_bases['emergency_categories'])}

Government agencies coordination:
{json.dumps(self.knowledge_bases['government_agencies'], indent=2)}

Provide actionable emergency management guidance including:
- Response protocols and procedures
- Resource requirements and coordination
- Communication strategies
- Timeline considerations
- Recovery planning steps

Maintain urgency and clarity appropriate for emergency situations.
"""
            
            response = await self.async_openai_client.chat.completions.create(
                model=self.config.openai.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=self.config.openai.max_tokens,
                temperature=0.4  # Balanced creativity for emergency scenarios
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error in emergency response handler: {e}")
            return self._generate_mock_emergency_response(message)
    
    def _generate_mock_emergency_response(self, message: str) -> str:
        """Generate mock emergency response"""
        return f"""Emergency Response Coordination - {message[:50]}...

Immediate Actions Required:
1. Assess situation severity and scope
2. Activate appropriate response protocols  
3. Coordinate with relevant agencies (Police, Fire, EMS, Public Works)
4. Establish communication channels
5. Deploy resources as needed

Key Coordination Steps:
• Establish Incident Command System (ICS)
• Set up Emergency Operations Center (EOC) if needed
• Coordinate with state/federal agencies as appropriate
• Implement public communication strategy
• Document all actions for after-action review

For immediate emergency assistance, contact 911.
For emergency planning and coordination, please provide specific scenario details for targeted guidance."""
    
    async def _handle_general_query(self, message: str, context: Optional[Dict] = None) -> str:
        """Handle general government assistance queries"""
        
        if not self.async_openai_client:
            return self._generate_mock_general_response(message)
        
        try:
            system_prompt = """You are a knowledgeable government assistant helping with general inquiries about government services, processes, and information.

Your role includes:
- Providing accurate information about government services
- Explaining government processes and procedures
- Directing citizens to appropriate agencies and resources
- Offering guidance on civic engagement
- Clarifying government policies and regulations

Maintain a helpful, professional tone and provide specific, actionable information whenever possible.
Always suggest appropriate next steps or resources for follow-up."""
            
            response = await self.async_openai_client.chat.completions.create(
                model=self.config.openai.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=self.config.openai.max_tokens,
                temperature=self.config.openai.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error in general query handler: {e}")
            return self._generate_mock_general_response(message)
    
    def _generate_mock_general_response(self, message: str) -> str:
        """Generate mock response for general queries when OpenAI is unavailable"""
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in ['services', 'help', 'what', 'how']):
            return """Welcome to GovSecure AI Platform! I can assist you with:

• Citizen Services: 311 requests, benefits applications, permits and licenses
• Compliance Guidance: NIST 800-53, FedRAMP, FISMA, and other frameworks
• Document Analysis: Policy review, compliance checking, translation
• Emergency Response: Coordination, planning, and resource allocation

To get started, you can:
- Ask about specific government services
- Request compliance guidance for your organization
- Upload documents for analysis
- Get help with emergency response planning

How can I assist you today?"""
        
        elif any(keyword in message_lower for keyword in ['thank', 'bye', 'goodbye']):
            return "Thank you for using GovSecure AI Platform. Have a great day and stay safe!"
        
        else:
            return f"""I understand you're asking about: {message[:100]}...

While I don't have access to the full AI capabilities right now, I can still help you with government services information. I have extensive knowledge about:

• Federal compliance frameworks and requirements
• Government service processes and procedures  
• Emergency response protocols
• Document processing workflows

Please let me know what specific area you'd like assistance with, and I'll provide the best guidance I can using my built-in knowledge base."""
    
    async def analyze_document(self, content: str, analysis_type: str = "general") -> Dict[str, Any]:
        """
        Analyze document content with government-specific focus
        
        Args:
            content: Document text content
            analysis_type: Type of analysis (general, compliance, policy, legal, financial)
            
        Returns:
            Dictionary containing analysis results
        """
        if not content or not content.strip():
            raise ValueError("Document content cannot be empty")
            
        try:
            if not self.async_openai_client:
                return self._generate_mock_document_analysis(content, analysis_type)
            
            analysis_prompts = {
                "general": "Analyze this government document and provide a comprehensive summary including key points, important dates, stakeholders, and action items.",
                "compliance": "Analyze this document for compliance considerations including regulatory requirements, risk factors, control gaps, and remediation recommendations.",
                "policy": "Analyze this policy document including policy objectives, implementation requirements, affected stakeholders, and potential impacts.",
                "legal": "Analyze this legal document for key legal provisions, obligations, rights, deadlines, and compliance requirements.",
                "financial": "Analyze this financial document including budget items, expenditures, revenue sources, financial risks, and audit considerations."
            }
            
            prompt = analysis_prompts.get(analysis_type, analysis_prompts["general"])
            
            response = await self.async_openai_client.chat.completions.create(
                model=self.config.openai.model,
                messages=[
                    {"role": "system", "content": f"You are a government document analyst. {prompt}"},
                    {"role": "user", "content": f"Please analyze this document:\n\n{content[:4000]}"}  # Limit content length
                ],
                max_tokens=self.config.openai.max_tokens,
                temperature=0.3
            )
            
            analysis_result = response.choices[0].message.content
            
            return {
                "analysis_type": analysis_type,
                "summary": analysis_result,
                "timestamp": datetime.now().isoformat(),
                "content_length": len(content),
                "model_used": self.config.openai.model
            }
            
        except Exception as e:
            self.logger.error(f"Error in document analysis: {e}")
            return self._generate_mock_document_analysis(content, analysis_type)
    
    def _generate_mock_document_analysis(self, content: str, analysis_type: str) -> Dict[str, Any]:
        """Generate mock document analysis results"""
        mock_summaries = {
            "general": f"Document Summary: This appears to be a government document containing {len(content.split())} words. Key themes include policy implementation, stakeholder responsibilities, and procedural requirements. Important dates and deadlines should be reviewed for compliance.",
            
            "compliance": f"Compliance Analysis: Document reviewed for regulatory compliance. Identified {len(content.split()) // 100} potential compliance points requiring attention. Recommend detailed review of control requirements and implementation timelines.",
            
            "policy": f"Policy Analysis: Policy document outlines objectives and implementation framework. Contains {len(content.split())} words with focus on operational procedures and stakeholder requirements. Implementation timeline and resource allocation should be clarified.",
            
            "legal": f"Legal Analysis: Legal document contains contractual obligations and regulatory requirements. Key provisions identified for compliance monitoring. Recommend legal review of all obligations and deadlines.",
            
            "financial": f"Financial Analysis: Financial document contains budget allocations and expenditure requirements totaling references to monetary values. Audit trail and approval processes should be documented per government financial regulations."
        }
        
        return {
            "analysis_type": analysis_type,
            "summary": mock_summaries.get(analysis_type, mock_summaries["general"]),
            "timestamp": datetime.now().isoformat(),
            "content_length": len(content),
            "model_used": "mock_analysis"
        }
    
    async def translate_text(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Translate text to target language with government context awareness
        
        Args:
            text: Text to translate
            target_language: Target language for translation
            
        Returns:
            Dictionary containing translation results
        """
        try:
            if not self.async_openai_client:
                return self._generate_mock_translation(text, target_language)
            
            system_prompt = f"""You are a professional government translator specializing in official document translation. 

Translate the following text to {target_language} while:
- Maintaining official government terminology
- Preserving legal and regulatory language precision
- Keeping proper nouns and official titles
- Maintaining formal tone appropriate for government communications
- Indicating any terms that may need cultural adaptation

Provide only the translation without additional commentary."""
            
            response = await self.async_openai_client.chat.completions.create(
                model=self.config.openai.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Translate this text to {target_language}:\n\n{text[:3000]}"}
                ],
                max_tokens=self.config.openai.max_tokens,
                temperature=0.2  # Low temperature for accurate translation
            )
            
            translated_text = response.choices[0].message.content
            
            return {
                "source_language": "auto-detected",
                "target_language": target_language,
                "original_text": text,
                "translated_text": translated_text,
                "timestamp": datetime.now().isoformat(),
                "model_used": self.config.openai.model
            }
            
        except Exception as e:
            self.logger.error(f"Error in text translation: {e}")
            return self._generate_mock_translation(text, target_language)
    
    def _generate_mock_translation(self, text: str, target_language: str) -> Dict[str, Any]:
        """Generate mock translation results"""
        mock_translation = f"[MOCK TRANSLATION TO {target_language.upper()}] {text[:200]}... (Translation service unavailable - please configure OpenAI API key for full translation capabilities)"
        
        return {
            "source_language": "English",
            "target_language": target_language,
            "original_text": text,
            "translated_text": mock_translation,
            "timestamp": datetime.now().isoformat(),
            "model_used": "mock_translator"
        }
    
    async def process_citizen_query(self, query: str) -> CitizenServiceQuery:
        """
        Process and structure citizen service queries
        
        Args:
            query: Raw citizen query
            
        Returns:
            Structured CitizenServiceQuery object
        """
        try:
            category = self._categorize_citizen_service(query)
            priority = self._assess_query_priority(query)
            
            # Generate structured response
            if not self.async_openai_client:
                return self._generate_mock_citizen_query(query, category, priority)
            
            system_prompt = f"""Analyze this citizen service query and provide structured information:

Query Category: {category}
Priority Level: {priority}

Provide:
1. Brief summary of the request
2. Suggested actions for resolution
3. Required documents or information
4. Estimated processing time
5. Alternative solutions if applicable

Format response as structured data."""
            
            response = await self.async_openai_client.chat.completions.create(
                model=self.config.openai.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=800,
                temperature=0.4
            )
            
            # Parse response into structured format
            response_text = response.choices[0].message.content
            
            return CitizenServiceQuery(
                query_type=category,
                category=category,
                priority=priority,
                summary=response_text[:200] + "...",
                suggested_actions=["Contact appropriate department", "Provide required documentation"],
                required_documents=["Government ID", "Proof of address"],
                estimated_processing_time="3-5 business days"
            )
            
        except Exception as e:
            self.logger.error(f"Error processing citizen query: {e}")
            return self._generate_mock_citizen_query(query, "general", "normal")
    
    def _assess_query_priority(self, query: str) -> str:
        """Assess priority level of citizen query"""
        query_lower = query.lower()
        
        high_priority_keywords = ['emergency', 'urgent', 'immediate', 'safety', 'health', 'danger']
        if any(keyword in query_lower for keyword in high_priority_keywords):
            return "high"
        
        medium_priority_keywords = ['deadline', 'expires', 'time-sensitive', 'soon']
        if any(keyword in query_lower for keyword in medium_priority_keywords):
            return "medium"
        
        return "normal"
    
    def _generate_mock_citizen_query(self, query: str, category: str, priority: str) -> CitizenServiceQuery:
        """Generate mock structured citizen query"""
        return CitizenServiceQuery(
            query_type=category,
            category=category,
            priority=priority,
            summary=f"Citizen inquiry regarding {category}: {query[:100]}...",
            suggested_actions=[
                "Review inquiry details",
                "Contact appropriate department",
                "Provide status update to citizen"
            ],
            required_documents=["Government ID", "Supporting documentation"],
            estimated_processing_time="5-7 business days"
        )
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history"""
        return self.conversation_history.copy()
    
    async def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        self.logger.info("Conversation history cleared")
    
    async def get_available_modes(self) -> List[str]:
        """Get list of available assistant modes"""
        return [mode.value for mode in AssistantMode]
    
    def get_current_mode(self) -> str:
        """Get current assistant mode as string"""
        return self.current_mode.value if self.current_mode else "general"
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get system status information"""
        return {
            "assistant_ready": True,
            "current_mode": self.get_current_mode(),
            "openai_available": self.async_openai_client is not None,
            "conversation_length": len(self.conversation_history),
            "model": self.config.openai.model if self.async_openai_client else "mock",
            "last_interaction": datetime.now().isoformat()
        } 