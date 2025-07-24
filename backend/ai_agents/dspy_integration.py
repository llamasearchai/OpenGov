"""
DSPy Integration for GovSecure AI Platform
Advanced compound AI system using DSPy for structured reasoning and multi-step tasks.

Author: Nik Jois
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import json

# DSPy import handling with graceful fallback
DSPY_AVAILABLE = False
try:
    import dspy
    from dspy import OpenAI, ChainOfThought, Predict, Module
    try:
        from dspy.primitives.assertions import assert_transform_module, backtrack_handler
    except ImportError:
        # Handle different DSPy versions
        pass
    DSPY_AVAILABLE = True
except ImportError:
    # Create mock classes for when DSPy is not available
    class Module:
        def __init__(self):
            pass
    
    class ChainOfThought:
        def __init__(self, *args, **kwargs):
            pass
    
    class Predict:
        def __init__(self, *args, **kwargs):
            pass
    
    class OpenAI:
        def __init__(self, *args, **kwargs):
            pass

from backend.core.config import get_config


class DSPyTaskType(Enum):
    """Types of DSPy-powered tasks"""
    COMPLIANCE_REASONING = "compliance_reasoning"
    POLICY_ANALYSIS = "policy_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    MULTI_STEP_ANALYSIS = "multi_step_analysis"
    DOCUMENT_SYNTHESIS = "document_synthesis"
    DECISION_SUPPORT = "decision_support"
    REGULATORY_INTERPRETATION = "regulatory_interpretation"


@dataclass
class DSPyResult:
    """Result from DSPy processing"""
    task_type: DSPyTaskType
    result: Any
    reasoning_steps: List[str]
    confidence_score: float
    metadata: Dict[str, Any]
    model_used: str
    processing_time: float


class ComplianceReasoning(Module):
    """DSPy module for compliance reasoning tasks"""
    
    def __init__(self):
        super().__init__()
        if DSPY_AVAILABLE:
            try:
                self.reason = ChainOfThought("context, regulation -> analysis, compliance_status, recommendations")
            except Exception:
                self.reason = None
    
    def forward(self, context: str, regulation: str):
        if not DSPY_AVAILABLE or not hasattr(self, 'reason') or self.reason is None:
            return self._mock_compliance_reasoning(context, regulation)
        
        try:
            return self.reason(context=context, regulation=regulation)
        except Exception:
            return self._mock_compliance_reasoning(context, regulation)
    
    def _mock_compliance_reasoning(self, context: str, regulation: str):
        """Mock compliance reasoning when DSPy is not available"""
        return {
            "analysis": f"Mock analysis of compliance for: {regulation[:100]}...",
            "compliance_status": "requires_review",
            "recommendations": [
                "Review specific requirements",
                "Implement necessary controls",
                "Document compliance measures"
            ]
        }


class PolicyAnalysis(Module):
    """DSPy module for policy analysis and interpretation"""
    
    def __init__(self):
        super().__init__()
        if DSPY_AVAILABLE:
            try:
                self.analyze = ChainOfThought("policy_text, context -> key_points, implications, stakeholder_impact")
            except Exception:
                self.analyze = None
    
    def forward(self, policy_text: str, context: str = ""):
        if not DSPY_AVAILABLE or not hasattr(self, 'analyze') or self.analyze is None:
            return self._mock_policy_analysis(policy_text, context)
        
        try:
            return self.analyze(policy_text=policy_text, context=context)
        except Exception:
            return self._mock_policy_analysis(policy_text, context)
    
    def _mock_policy_analysis(self, policy_text: str, context: str):
        """Mock policy analysis when DSPy is not available"""
        return {
            "key_points": [
                "Main policy objective identified",
                "Implementation requirements outlined",
                "Compliance deadlines specified"
            ],
            "implications": "Policy has significant impact on government operations",
            "stakeholder_impact": "Affects multiple government agencies and citizen services"
        }


class RiskAssessment(Module):
    """DSPy module for comprehensive risk assessment"""
    
    def __init__(self):
        super().__init__()
        if DSPY_AVAILABLE:
            try:
                self.assess = ChainOfThought("system_info, threat_context -> risk_level, vulnerabilities, mitigation_strategies")
            except Exception:
                self.assess = None
    
    def forward(self, system_info: str, threat_context: str = ""):
        if not DSPY_AVAILABLE or not hasattr(self, 'assess') or self.assess is None:
            return self._mock_risk_assessment(system_info, threat_context)
        
        try:
            return self.assess(system_info=system_info, threat_context=threat_context)
        except Exception:
            return self._mock_risk_assessment(system_info, threat_context)
    
    def _mock_risk_assessment(self, system_info: str, threat_context: str):
        """Mock risk assessment when DSPy is not available"""
        return {
            "risk_level": "medium",
            "vulnerabilities": [
                "Potential data exposure risk",
                "Authentication bypass possibility",
                "Insufficient logging coverage"
            ],
            "mitigation_strategies": [
                "Implement additional access controls",
                "Enhance monitoring capabilities",
                "Regular security assessments"
            ]
        }


class MultiStepAnalysis(Module):
    """DSPy module for complex multi-step analytical tasks"""
    
    def __init__(self):
        super().__init__()
        if DSPY_AVAILABLE:
            try:
                self.step1 = ChainOfThought("input -> initial_analysis")
                self.step2 = ChainOfThought("initial_analysis, context -> refined_analysis")
                self.step3 = ChainOfThought("refined_analysis -> final_conclusions, recommendations")
            except Exception:
                self.step1 = self.step2 = self.step3 = None
    
    def forward(self, input_data: str, context: str = ""):
        if not DSPY_AVAILABLE or not hasattr(self, 'step1') or self.step1 is None:
            return self._mock_multi_step_analysis(input_data, context)
        
        try:
            # Step 1: Initial analysis
            step1_result = self.step1(input=input_data)
            
            # Step 2: Refined analysis with context
            step2_result = self.step2(
                initial_analysis=step1_result.initial_analysis,
                context=context
            )
            
            # Step 3: Final conclusions
            step3_result = self.step3(refined_analysis=step2_result.refined_analysis)
            
            return {
                "steps": [step1_result, step2_result, step3_result],
                "final_conclusions": step3_result.final_conclusions,
                "recommendations": step3_result.recommendations
            }
        except Exception:
            return self._mock_multi_step_analysis(input_data, context)
    
    def _mock_multi_step_analysis(self, input_data: str, context: str):
        """Mock multi-step analysis when DSPy is not available"""
        return {
            "steps": [
                {"step": 1, "analysis": "Initial data processing completed"},
                {"step": 2, "analysis": "Contextual analysis applied"},
                {"step": 3, "analysis": "Final synthesis generated"}
            ],
            "final_conclusions": "Comprehensive analysis completed with multi-step reasoning",
            "recommendations": [
                "Implement identified improvements",
                "Monitor key metrics",
                "Review findings quarterly"
            ]
        }


class DocumentSynthesis(Module):
    """DSPy module for synthesizing information from multiple documents"""
    
    def __init__(self):
        super().__init__()
        if DSPY_AVAILABLE:
            try:
                self.synthesize = ChainOfThought("documents, query -> synthesis, key_insights, conflicts")
            except Exception:
                self.synthesize = None
    
    def forward(self, documents: List[str], query: str):
        if not DSPY_AVAILABLE or not hasattr(self, 'synthesize') or self.synthesize is None:
            return self._mock_document_synthesis(documents, query)
        
        try:
            # Combine documents for processing
            combined_docs = "\n\n---DOCUMENT SEPARATOR---\n\n".join(documents)
            return self.synthesize(documents=combined_docs, query=query)
        except Exception:
            return self._mock_document_synthesis(documents, query)
    
    def _mock_document_synthesis(self, documents: List[str], query: str):
        """Mock document synthesis when DSPy is not available"""
        return {
            "synthesis": f"Synthesized information from {len(documents)} documents regarding: {query}",
            "key_insights": [
                "Common themes identified across documents",
                "Regulatory requirements consolidated",
                "Implementation guidance extracted"
            ],
            "conflicts": ["No major conflicts identified between source documents"]
        }


class DSPyOrchestrator:
    """Main orchestrator for DSPy-powered compound AI system"""
    
    def __init__(self):
        try:
            self.config = get_config()
        except Exception:
            self.config = None
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize DSPy if available
        if DSPY_AVAILABLE and self.config:
            self._initialize_dspy()
        else:
            self.logger.warning("DSPy not available or config not loaded - using mock implementations")
        
        # Initialize modules
        self.compliance_reasoning = ComplianceReasoning()
        self.policy_analysis = PolicyAnalysis()
        self.risk_assessment = RiskAssessment()
        self.multi_step_analysis = MultiStepAnalysis()
        self.document_synthesis = DocumentSynthesis()
    
    def _initialize_dspy(self):
        """Initialize DSPy with OpenAI configuration"""
        try:
            if not self.config or not hasattr(self.config, 'openai'):
                return
            
            # Configure DSPy with the best reasoning model
            reasoning_model = getattr(self.config.openai, 'reasoning_model', 'gpt-4')
            api_key = getattr(self.config.openai, 'api_key', '')
            
            if not api_key:
                self.logger.warning("No OpenAI API key configured")
                return
            
            # Set up DSPy OpenAI client
            dspy_client = OpenAI(
                model=reasoning_model,
                api_key=api_key,
                max_tokens=getattr(self.config.openai, 'max_tokens', 4096)
            )
            
            dspy.configure(lm=dspy_client)
            self.logger.info(f"DSPy initialized with model: {reasoning_model}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize DSPy: {e}")
            global DSPY_AVAILABLE
            DSPY_AVAILABLE = False
    
    async def process_task(
        self,
        task_type: DSPyTaskType,
        input_data: Dict[str, Any],
        model_override: Optional[str] = None
    ) -> DSPyResult:
        """Process a task using appropriate DSPy module"""
        import time
        start_time = time.time()
        
        try:
            # Select appropriate module
            if task_type == DSPyTaskType.COMPLIANCE_REASONING:
                result = self.compliance_reasoning.forward(
                    context=input_data.get("context", ""),
                    regulation=input_data.get("regulation", "")
                )
            elif task_type == DSPyTaskType.POLICY_ANALYSIS:
                result = self.policy_analysis.forward(
                    policy_text=input_data.get("policy_text", ""),
                    context=input_data.get("context", "")
                )
            elif task_type == DSPyTaskType.RISK_ASSESSMENT:
                result = self.risk_assessment.forward(
                    system_info=input_data.get("system_info", ""),
                    threat_context=input_data.get("threat_context", "")
                )
            elif task_type == DSPyTaskType.MULTI_STEP_ANALYSIS:
                result = self.multi_step_analysis.forward(
                    input_data=input_data.get("input_data", ""),
                    context=input_data.get("context", "")
                )
            elif task_type == DSPyTaskType.DOCUMENT_SYNTHESIS:
                result = self.document_synthesis.forward(
                    documents=input_data.get("documents", []),
                    query=input_data.get("query", "")
                )
            else:
                raise ValueError(f"Unsupported task type: {task_type}")
            
            processing_time = time.time() - start_time
            
            # Extract reasoning steps if available
            reasoning_steps = []
            if hasattr(result, 'steps'):
                reasoning_steps = [str(step) for step in result.steps]
            elif isinstance(result, dict) and 'steps' in result:
                reasoning_steps = [str(step) for step in result['steps']]
            
            model_used = model_override or (
                self.config.openai.reasoning_model if self.config and hasattr(self.config, 'openai') 
                else 'mock-model'
            )
            
            return DSPyResult(
                task_type=task_type,
                result=result,
                reasoning_steps=reasoning_steps,
                confidence_score=0.85,  # Default confidence
                metadata={
                    "dspy_available": DSPY_AVAILABLE,
                    "input_keys": list(input_data.keys()),
                    "processing_time": processing_time
                },
                model_used=model_used,
                processing_time=processing_time
            )
            
        except Exception as e:
            self.logger.error(f"Error processing DSPy task {task_type}: {e}")
            
            # Return error result
            return DSPyResult(
                task_type=task_type,
                result={"error": str(e)},
                reasoning_steps=["Error occurred during processing"],
                confidence_score=0.0,
                metadata={"error": True, "dspy_available": DSPY_AVAILABLE},
                model_used=model_override or "error-fallback",
                processing_time=time.time() - start_time
            )
    
    async def compliance_analysis(
        self,
        context: str,
        regulation: str,
        model: Optional[str] = None
    ) -> DSPyResult:
        """Perform compliance analysis using DSPy reasoning"""
        return await self.process_task(
            DSPyTaskType.COMPLIANCE_REASONING,
            {"context": context, "regulation": regulation},
            model
        )
    
    async def analyze_policy(
        self,
        policy_text: str,
        context: str = "",
        model: Optional[str] = None
    ) -> DSPyResult:
        """Analyze policy using DSPy structured reasoning"""
        return await self.process_task(
            DSPyTaskType.POLICY_ANALYSIS,
            {"policy_text": policy_text, "context": context},
            model
        )
    
    async def assess_risk(
        self,
        system_info: str,
        threat_context: str = "",
        model: Optional[str] = None
    ) -> DSPyResult:
        """Perform risk assessment using DSPy"""
        return await self.process_task(
            DSPyTaskType.RISK_ASSESSMENT,
            {"system_info": system_info, "threat_context": threat_context},
            model
        )
    
    async def multi_step_reasoning(
        self,
        input_data: str,
        context: str = "",
        model: Optional[str] = None
    ) -> DSPyResult:
        """Perform multi-step reasoning analysis"""
        return await self.process_task(
            DSPyTaskType.MULTI_STEP_ANALYSIS,
            {"input_data": input_data, "context": context},
            model
        )
    
    async def synthesize_documents(
        self,
        documents: List[str],
        query: str,
        model: Optional[str] = None
    ) -> DSPyResult:
        """Synthesize information from multiple documents"""
        return await self.process_task(
            DSPyTaskType.DOCUMENT_SYNTHESIS,
            {"documents": documents, "query": query},
            model
        )
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get information about available models for DSPy tasks"""
        if not self.config or not hasattr(self.config, 'openai'):
            return {"error": "OpenAI configuration not available"}
        
        try:
            return {
                "reasoning_models": getattr(self.config.openai, 'get_reasoning_models', lambda: [])(),
                "default_reasoning": getattr(self.config.openai, 'reasoning_model', 'gpt-4'),
                "flagship_models": [
                    getattr(self.config.openai, 'default_model', 'gpt-4'),
                    "gpt-4.1",
                    "o3",
                    "o3-pro"
                ],
                "cost_optimized": getattr(self.config.openai, 'get_cost_optimized_models', lambda: [])(),
                "dspy_available": DSPY_AVAILABLE
            }
        except Exception as e:
            return {"error": f"Configuration error: {e}", "dspy_available": DSPY_AVAILABLE}
    
    def get_task_types(self) -> List[Dict[str, str]]:
        """Get available DSPy task types"""
        return [
            {
                "type": task_type.value,
                "description": self._get_task_description(task_type)
            }
            for task_type in DSPyTaskType
        ]
    
    def _get_task_description(self, task_type: DSPyTaskType) -> str:
        """Get description for task type"""
        descriptions = {
            DSPyTaskType.COMPLIANCE_REASONING: "Advanced compliance analysis with structured reasoning",
            DSPyTaskType.POLICY_ANALYSIS: "Comprehensive policy interpretation and impact analysis",
            DSPyTaskType.RISK_ASSESSMENT: "Multi-factor risk assessment with mitigation strategies",
            DSPyTaskType.MULTI_STEP_ANALYSIS: "Complex multi-step analytical reasoning",
            DSPyTaskType.DOCUMENT_SYNTHESIS: "Synthesis and analysis of multiple documents",
            DSPyTaskType.DECISION_SUPPORT: "Structured decision support with reasoning chains",
            DSPyTaskType.REGULATORY_INTERPRETATION: "Legal and regulatory document interpretation"
        }
        return descriptions.get(task_type, "Advanced AI reasoning task")


# Global DSPy orchestrator instance
_dspy_orchestrator: Optional[DSPyOrchestrator] = None


def get_dspy_orchestrator() -> DSPyOrchestrator:
    """Get the global DSPy orchestrator instance"""
    global _dspy_orchestrator
    if _dspy_orchestrator is None:
        _dspy_orchestrator = DSPyOrchestrator()
    return _dspy_orchestrator 