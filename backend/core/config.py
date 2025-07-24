"""
Configuration Management for GovSecure AI Platform
Comprehensive configuration system supporting all OpenAI models and government compliance.

Author: Nik Jois
"""

import os
import logging
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OpenAIModelType(Enum):
    """OpenAI model types and categories"""
    # Flagship chat models
    GPT_4_1 = "gpt-4.1"
    GPT_4O = "gpt-4o"
    GPT_4O_AUDIO = "gpt-4o-audio-preview"
    CHATGPT_4O_LATEST = "chatgpt-4o-latest"
    
    # Reasoning models (o-series)
    O4_MINI = "o4-mini"
    O3 = "o3"
    O3_PRO = "o3-pro"
    O3_MINI = "o3-mini"
    O1 = "o1"
    O1_MINI = "o1-mini"
    O1_PRO = "o1-pro"
    
    # Cost-optimized models
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_4_1_NANO = "gpt-4.1-nano"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O_MINI_AUDIO = "gpt-4o-mini-audio-preview"
    
    # Legacy models (for backward compatibility)
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4 = "gpt-4"
    GPT_3_5_TURBO = "gpt-3.5-turbo"


class ModelCapability(Enum):
    """Model capability types"""
    TEXT = "text"
    AUDIO = "audio"
    REASONING = "reasoning"
    VISION = "vision"
    FUNCTION_CALLING = "function_calling"
    JSON_MODE = "json_mode"


@dataclass
class ModelConfig:
    """Configuration for individual OpenAI models"""
    name: str
    display_name: str
    description: str
    capabilities: List[ModelCapability] = field(default_factory=list)
    max_tokens: int = 4096
    context_window: int = 8192
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    reasoning_capable: bool = False
    audio_capable: bool = False
    recommended_use_cases: List[str] = field(default_factory=list)
    government_approved: bool = True
    compliance_level: str = "IL4"  # Information Level


@dataclass
class OpenAIConfig:
    """OpenAI API configuration with all model support"""
    api_key: str = ""
    organization: Optional[str] = None
    base_url: str = "https://api.openai.com/v1"
    
    # Default models for different use cases
    default_model: str = "gpt-4.1"
    reasoning_model: str = "o3"
    cost_optimized_model: str = "gpt-4.1-mini"
    audio_model: str = "gpt-4o-audio-preview"
    
    # Model configurations
    models: Dict[str, ModelConfig] = field(default_factory=dict)
    
    # API settings
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 60
    max_retries: int = 3
    
    def __post_init__(self):
        """Initialize model configurations"""
        if not self.models:
            self.models = self._get_default_model_configs()
    
    def _get_default_model_configs(self) -> Dict[str, ModelConfig]:
        """Get default configurations for all supported models"""
        return {
            # Flagship chat models
            "gpt-4.1": ModelConfig(
                name="gpt-4.1",
                display_name="GPT-4.1",
                description="Flagship GPT model for complex tasks",
                capabilities=[ModelCapability.TEXT, ModelCapability.VISION, ModelCapability.FUNCTION_CALLING, ModelCapability.JSON_MODE],
                max_tokens=8192,
                context_window=32768,
                cost_per_1k_input=0.03,
                cost_per_1k_output=0.06,
                recommended_use_cases=["Complex analysis", "Policy review", "Legal documents", "Strategic planning"],
                compliance_level="IL5"
            ),
            "gpt-4o": ModelConfig(
                name="gpt-4o",
                display_name="GPT-4o",
                description="Fast, intelligent, flexible GPT model",
                capabilities=[ModelCapability.TEXT, ModelCapability.VISION, ModelCapability.FUNCTION_CALLING],
                max_tokens=4096,
                context_window=16384,
                cost_per_1k_input=0.025,
                cost_per_1k_output=0.05,
                recommended_use_cases=["General chat", "Document analysis", "Citizen services"],
                compliance_level="IL4"
            ),
            "gpt-4o-audio-preview": ModelConfig(
                name="gpt-4o-audio-preview",
                display_name="GPT-4o Audio",
                description="GPT-4o models capable of audio inputs and outputs",
                capabilities=[ModelCapability.TEXT, ModelCapability.AUDIO, ModelCapability.FUNCTION_CALLING],
                max_tokens=4096,
                context_window=16384,
                audio_capable=True,
                cost_per_1k_input=0.025,
                cost_per_1k_output=0.05,
                recommended_use_cases=["Voice interfaces", "Audio transcription", "Multilingual support"],
                compliance_level="IL3"
            ),
            "chatgpt-4o-latest": ModelConfig(
                name="chatgpt-4o-latest",
                display_name="ChatGPT-4o",
                description="GPT-4o model used in ChatGPT",
                capabilities=[ModelCapability.TEXT, ModelCapability.FUNCTION_CALLING],
                max_tokens=4096,
                context_window=16384,
                cost_per_1k_input=0.025,
                cost_per_1k_output=0.05,
                recommended_use_cases=["Interactive chat", "Q&A systems", "Help desk automation"]
            ),
            
            # Reasoning models (o-series)
            "o4-mini": ModelConfig(
                name="o4-mini",
                display_name="o4-mini",
                description="Faster, more affordable reasoning model",
                capabilities=[ModelCapability.TEXT, ModelCapability.REASONING, ModelCapability.JSON_MODE],
                max_tokens=2048,
                context_window=8192,
                reasoning_capable=True,
                cost_per_1k_input=0.015,
                cost_per_1k_output=0.03,
                recommended_use_cases=["Quick analysis", "Compliance checks", "Decision support"],
                compliance_level="IL4"
            ),
            "o3": ModelConfig(
                name="o3",
                display_name="o3",
                description="Our most powerful reasoning model",
                capabilities=[ModelCapability.TEXT, ModelCapability.REASONING, ModelCapability.JSON_MODE],
                max_tokens=8192,
                context_window=32768,
                reasoning_capable=True,
                cost_per_1k_input=0.05,
                cost_per_1k_output=0.10,
                recommended_use_cases=["Complex reasoning", "Multi-step analysis", "Strategic planning", "Risk assessment"],
                compliance_level="IL5"
            ),
            "o3-pro": ModelConfig(
                name="o3-pro",
                display_name="o3-pro",
                description="Version of o3 with more compute for better responses",
                capabilities=[ModelCapability.TEXT, ModelCapability.REASONING, ModelCapability.JSON_MODE],
                max_tokens=8192,
                context_window=32768,
                reasoning_capable=True,
                cost_per_1k_input=0.08,
                cost_per_1k_output=0.16,
                recommended_use_cases=["Critical analysis", "High-stakes decisions", "Complex policy review"],
                compliance_level="IL5"
            ),
            "o3-mini": ModelConfig(
                name="o3-mini",
                display_name="o3-mini",
                description="A small model alternative to o3",
                capabilities=[ModelCapability.TEXT, ModelCapability.REASONING],
                max_tokens=2048,
                context_window=8192,
                reasoning_capable=True,
                cost_per_1k_input=0.02,
                cost_per_1k_output=0.04,
                recommended_use_cases=["Basic reasoning", "Routine analysis", "Quick decisions"]
            ),
            "o1": ModelConfig(
                name="o1",
                display_name="o1",
                description="Previous full o-series reasoning model",
                capabilities=[ModelCapability.TEXT, ModelCapability.REASONING],
                max_tokens=4096,
                context_window=16384,
                reasoning_capable=True,
                cost_per_1k_input=0.04,
                cost_per_1k_output=0.08,
                recommended_use_cases=["Legacy reasoning tasks", "Established workflows"]
            ),
            "o1-mini": ModelConfig(
                name="o1-mini",
                display_name="o1-mini",
                description="A small model alternative to o1 (Deprecated)",
                capabilities=[ModelCapability.TEXT, ModelCapability.REASONING],
                max_tokens=2048,
                context_window=8192,
                reasoning_capable=True,
                cost_per_1k_input=0.015,
                cost_per_1k_output=0.03,
                recommended_use_cases=["Legacy applications", "Migration scenarios"],
                government_approved=False  # Deprecated
            ),
            "o1-pro": ModelConfig(
                name="o1-pro",
                display_name="o1-pro",
                description="Version of o1 with more compute for better responses",
                capabilities=[ModelCapability.TEXT, ModelCapability.REASONING],
                max_tokens=4096,
                context_window=16384,
                reasoning_capable=True,
                cost_per_1k_input=0.06,
                cost_per_1k_output=0.12,
                recommended_use_cases=["Legacy high-performance tasks"]
            ),
            
            # Cost-optimized models
            "gpt-4.1-mini": ModelConfig(
                name="gpt-4.1-mini",
                display_name="GPT-4.1 mini",
                description="Balanced for intelligence, speed, and cost",
                capabilities=[ModelCapability.TEXT, ModelCapability.FUNCTION_CALLING, ModelCapability.JSON_MODE],
                max_tokens=4096,
                context_window=16384,
                cost_per_1k_input=0.015,
                cost_per_1k_output=0.03,
                recommended_use_cases=["High-volume processing", "Routine tasks", "Citizen services"],
                compliance_level="IL4"
            ),
            "gpt-4.1-nano": ModelConfig(
                name="gpt-4.1-nano",
                display_name="GPT-4.1 nano",
                description="Fastest, most cost-effective GPT-4.1 model",
                capabilities=[ModelCapability.TEXT, ModelCapability.JSON_MODE],
                max_tokens=2048,
                context_window=8192,
                cost_per_1k_input=0.005,
                cost_per_1k_output=0.01,
                recommended_use_cases=["Simple tasks", "High-frequency requests", "Basic automation"],
                compliance_level="IL3"
            ),
            "gpt-4o-mini": ModelConfig(
                name="gpt-4o-mini",
                display_name="GPT-4o mini",
                description="Fast, affordable small model for focused tasks",
                capabilities=[ModelCapability.TEXT, ModelCapability.FUNCTION_CALLING],
                max_tokens=2048,
                context_window=8192,
                cost_per_1k_input=0.01,
                cost_per_1k_output=0.02,
                recommended_use_cases=["Quick responses", "Simple analysis", "Routine operations"]
            ),
            "gpt-4o-mini-audio-preview": ModelConfig(
                name="gpt-4o-mini-audio-preview",
                display_name="GPT-4o mini Audio",
                description="Smaller model capable of audio inputs and outputs",
                capabilities=[ModelCapability.TEXT, ModelCapability.AUDIO],
                max_tokens=2048,
                context_window=8192,
                audio_capable=True,
                cost_per_1k_input=0.01,
                cost_per_1k_output=0.02,
                recommended_use_cases=["Voice interfaces", "Audio processing", "Cost-effective speech"]
            )
        }
    
    def get_model_by_capability(self, capability: ModelCapability) -> List[str]:
        """Get models that support a specific capability"""
        return [
            model_name for model_name, config in self.models.items()
            if capability in config.capabilities and config.government_approved
        ]
    
    def get_reasoning_models(self) -> List[str]:
        """Get all reasoning-capable models"""
        return [
            model_name for model_name, config in self.models.items()
            if config.reasoning_capable and config.government_approved
        ]
    
    def get_audio_models(self) -> List[str]:
        """Get all audio-capable models"""
        return [
            model_name for model_name, config in self.models.items()
            if config.audio_capable and config.government_approved
        ]
    
    def get_cost_optimized_models(self) -> List[str]:
        """Get cost-optimized models sorted by cost"""
        cost_models = [
            (model_name, config) for model_name, config in self.models.items()
            if config.cost_per_1k_input <= 0.02 and config.government_approved
        ]
        return [model[0] for model in sorted(cost_models, key=lambda x: x[1].cost_per_1k_input)]
    
    def get_model_for_use_case(self, use_case: str) -> Optional[str]:
        """Get recommended model for specific use case"""
        use_case_lower = use_case.lower()
        
        # Use case to model mapping
        use_case_mappings = {
            "reasoning": self.reasoning_model,
            "analysis": "gpt-4.1",
            "chat": "gpt-4o",
            "audio": self.audio_model,
            "cost": self.cost_optimized_model,
            "compliance": "o3",
            "emergency": "gpt-4.1",
            "translation": "gpt-4o",
            "documents": "gpt-4.1"
        }
        
        for key, model in use_case_mappings.items():
            if key in use_case_lower:
                return model
        
        return self.default_model


@dataclass
class Config:
    """Main configuration class combining all settings"""
    
    # Core application settings
    app_name: str = "GovSecure AI Platform"
    version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    
    # OpenAI configuration
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    
    # Security settings
    secret_key: str = "your-super-secret-key-change-in-production"
    
    # Database settings
    database_url: str = "sqlite:///./govsecure.db"
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Compliance settings
    compliance_level: str = "FEDRAMP_HIGH"
    
    def __post_init__(self):
        """Initialize configuration from environment variables"""
        # Load OpenAI configuration from environment
        api_key = os.getenv("OPENAI_API_KEY", "")
        organization = os.getenv("OPENAI_ORGANIZATION")
        
        if api_key:
            self.openai = OpenAIConfig(
                api_key=api_key,
                organization=organization
            )
        else:
            # Create default config for development/testing
            self.openai = OpenAIConfig()
        
        # Load other environment variables
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.database_url = os.getenv("DATABASE_URL", self.database_url)
        self.api_host = os.getenv("API_HOST", self.api_host)
        self.api_port = int(os.getenv("API_PORT", str(self.api_port)))
        self.secret_key = os.getenv("SECRET_KEY", self.secret_key)
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment.lower() == "production"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode"""
        return self.environment.lower() == "testing"


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config() -> Config:
    """Reload the configuration from environment"""
    global _config
    _config = Config()
    return _config 