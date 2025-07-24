# GovSecure AI Platform

[![CI/CD Pipeline](https://github.com/llamasearchai/OpenGov/actions/workflows/ci.yml/badge.svg)](https://github.com/llamasearchai/OpenGov/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/govsecure-ai-platform.svg)](https://badge.fury.io/py/govsecure-ai-platform)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Codecov](https://codecov.io/gh/llamasearchai/OpenGov/branch/main/graph/badge.svg)](https://codecov.io/gh/llamasearchai/OpenGov)

**Advanced AI-Powered Government Operations Platform with Latest OpenAI Models**

A comprehensive artificial intelligence platform designed specifically for US government agencies, providing secure, compliant, and efficient solutions for citizen services, document analysis, compliance management, and emergency response coordination. Now featuring complete support for all latest OpenAI models including GPT-4.1, o-series reasoning models, and DSPy integration for compound AI systems.

## Overview

The GovSecure AI Platform leverages cutting-edge OpenAI technology including the latest GPT-4.1, o3 reasoning models, and audio-capable models to deliver intelligent automation for government operations while maintaining the highest security standards required for federal environments. Built with FedRAMP compliance in mind and designed for IL5 compatibility.

## Latest AI Model Support

### Flagship Chat Models
- **GPT-4.1**: Latest flagship model for complex government tasks
- **GPT-4o**: Fast, intelligent, flexible model for general operations
- **GPT-4o Audio**: Audio-capable model for voice interfaces
- **ChatGPT-4o Latest**: Production-ready chat model

### Reasoning Models (o-series)
- **o3**: Most powerful reasoning model for complex analysis
- **o3-pro**: Enhanced compute version for critical decisions
- **o4-mini**: Faster, affordable reasoning model
- **o3-mini**: Small reasoning model for routine tasks
- **o1 Series**: Legacy reasoning models for established workflows

### Cost-Optimized Models
- **GPT-4.1 mini**: Balanced intelligence, speed, and cost
- **GPT-4.1 nano**: Fastest, most cost-effective model
- **GPT-4o mini**: Affordable model for focused tasks
- **GPT-4o mini Audio**: Cost-effective audio processing

### DSPy Compound AI System
- **Structured Reasoning**: Chain-of-thought processing for complex tasks
- **Multi-Step Analysis**: Advanced analytical workflows
- **Policy Analysis**: Comprehensive policy interpretation
- **Risk Assessment**: Multi-factor risk evaluation
- **Document Synthesis**: Information synthesis from multiple sources
- **Compliance Reasoning**: Advanced compliance analysis

## Key Features

### Core Capabilities
- **Intelligent Chat Assistant**: Multi-modal AI assistant with latest models
- **Document Analysis**: Advanced document processing with compliance checking
- **Multilingual Translation**: Real-time translation with audio support
- **Compliance Automation**: Automated NIST 800-53, FedRAMP, and FISMA compliance scanning
- **Emergency Response**: AI-powered incident coordination and response management
- **Citizen Service Portal**: Streamlined citizen request processing and service delivery
- **Audio Processing**: Voice interfaces and audio transcription capabilities
- **Reasoning Engine**: Complex multi-step reasoning with DSPy integration

### Advanced AI Features
- **Model Selection**: Automatic model selection based on task requirements
- **Reasoning Chains**: Structured reasoning with step-by-step analysis
- **Audio Capabilities**: Voice input/output with latest audio models
- **Cost Optimization**: Intelligent model routing for cost efficiency
- **Compound AI**: DSPy-powered multi-agent reasoning systems
- **Context Awareness**: Advanced context understanding across conversations

### Security & Compliance
- **FedRAMP High Baseline**: Designed for high-impact government systems
- **NIST 800-53 Controls**: Comprehensive security control implementation
- **FISMA Compliance**: Federal Information Security Management Act adherence
- **CJIS Security Policy**: Criminal Justice Information Services compliance
- **IL5 Compatible**: Information Level 5 security classification support
- **Zero Trust Architecture**: Modern security framework implementation

### Technical Excellence
- **Production Ready**: Enterprise-scale deployment capability
- **High Availability**: Redundant systems with 99.9% uptime SLA
- **Scalable Architecture**: Microservices-based design for horizontal scaling
- **API-First Design**: RESTful APIs with comprehensive documentation
- **Real-time Processing**: WebSocket support for live updates
- **Comprehensive Testing**: 100+ test cases with enhanced coverage

## Quick Start

### Prerequisites
- Python 3.9 or higher
- OpenAI API key with access to latest models
- PostgreSQL database (optional, SQLite for development)
- Redis for caching (optional)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/llamasearchai/OpenGov.git
   cd OpenGov
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   cp env.example .env
   # Edit .env with your OpenAI API key and configuration
   ```

4. **Initialize Database**
   ```bash
   python -m backend.core.database init
   ```

5. **Run the Application**
   ```bash
   # CLI Interface with latest models
   python cli.py start
   
   # Web API with full model support
   python cli.py web
   
   # Quick Compliance Scan with reasoning models
   python cli.py scan
   ```

## Model Configuration

### Environment Variables
```bash
# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here
OPENAI_ORGANIZATION=your-org-id

# Model Selection
OPENAI_DEFAULT_MODEL=gpt-4.1
OPENAI_REASONING_MODEL=o3
OPENAI_COST_OPTIMIZED_MODEL=gpt-4.1-mini
OPENAI_AUDIO_MODEL=gpt-4o-audio-preview
```

### Model Selection API
```python
from backend.core.config import get_config

config = get_config()

# Get reasoning models
reasoning_models = config.openai.get_reasoning_models()

# Get audio models
audio_models = config.openai.get_audio_models()

# Get model for specific use case
best_model = config.openai.get_model_for_use_case("compliance")
```

## Usage Examples

### DSPy Compound AI System

**Compliance Analysis with Reasoning**
```python
from backend.ai_agents.dspy_integration import get_dspy_orchestrator

orchestrator = get_dspy_orchestrator()

# Advanced compliance reasoning
result = await orchestrator.compliance_analysis(
    context="Government system with sensitive data",
    regulation="NIST 800-53 AC-2 requirements"
)

print(f"Analysis: {result.result}")
print(f"Reasoning Steps: {result.reasoning_steps}")
```

**Multi-Step Policy Analysis**
```python
# Complex policy analysis
result = await orchestrator.analyze_policy(
    policy_text="New data privacy regulation text...",
    context="Federal agency implementation"
)

print(f"Key Points: {result.result['key_points']}")
print(f"Implications: {result.result['implications']}")
```

**Document Synthesis**
```python
# Synthesize multiple documents
documents = [
    "Policy document 1 content...",
    "Regulation document 2 content...",
    "Guidelines document 3 content..."
]

result = await orchestrator.synthesize_documents(
    documents=documents,
    query="What are the key compliance requirements?"
)

print(f"Synthesis: {result.result['synthesis']}")
print(f"Conflicts: {result.result['conflicts']}")
```

### Command Line Interface

**Interactive Government Assistant with Latest Models**
```bash
python cli.py start
# Access to GPT-4.1, o3 reasoning, and audio models
```

**Model-Specific Chat**
```bash
# Use reasoning model for complex analysis
python cli.py chat "Analyze FISMA compliance requirements" --model o3

# Use audio model for voice processing
python cli.py chat "Process this audio input" --model gpt-4o-audio-preview

# Use cost-optimized model for routine tasks
python cli.py chat "Simple question" --model gpt-4.1-nano
```

### Web API Usage

**Model Selection Endpoint**
```bash
curl -X GET "http://localhost:8000/ai/models"
# Returns available models and capabilities
```

**Advanced Chat with Model Selection**
```bash
curl -X POST "http://localhost:8000/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze this complex policy document",
    "mode": "compliance",
    "model": "o3",
    "use_reasoning": true
  }'
```

**DSPy Reasoning Endpoint**
```bash
curl -X POST "http://localhost:8000/ai/dspy/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "compliance_reasoning",
    "input_data": {
      "context": "Government system",
      "regulation": "NIST 800-53"
    },
    "model": "o3-pro"
  }'
```

## Architecture

### AI Model Management
- **Model Router**: Intelligent routing based on task complexity
- **Cost Optimizer**: Automatic selection of cost-effective models
- **Capability Matcher**: Match models to required capabilities
- **Performance Monitor**: Track model performance and costs

### DSPy Integration Layer
- **Reasoning Modules**: Structured reasoning components
- **Chain-of-Thought**: Multi-step analytical processes
- **Task Orchestrator**: Coordinate complex AI workflows
- **Result Synthesis**: Combine outputs from multiple models

### Audio Processing Pipeline
- **Speech Recognition**: Convert audio to text
- **Audio Generation**: Text-to-speech capabilities
- **Multi-language Support**: Audio processing in multiple languages
- **Real-time Processing**: Live audio stream processing

## Government Use Cases

### Enhanced with Latest Models

**Complex Policy Analysis (GPT-4.1 + o3)**
- Multi-document policy synthesis
- Regulatory impact assessment
- Stakeholder analysis with reasoning chains

**Emergency Response (o3 + Audio Models)**
- Real-time incident analysis with reasoning
- Voice-activated emergency protocols
- Multi-step crisis response planning

**Compliance Automation (o3-pro + DSPy)**
- Advanced compliance reasoning
- Gap analysis with structured thinking
- Automated remediation planning

**Citizen Services (GPT-4.1 + Audio)**
- Multilingual voice interfaces
- Complex benefit eligibility analysis
- Personalized service recommendations

## Testing and Quality Assurance

### Model Testing
```bash
# Test all model integrations
python -m pytest tests/test_models/ -v

# Test DSPy integration
python -m pytest tests/test_dspy/ -v

# Test audio capabilities
python -m pytest tests/test_audio/ -v
```

### Performance Testing
```bash
# Model performance benchmarks
python scripts/benchmark_models.py

# Cost analysis
python scripts/analyze_costs.py

# Reasoning quality tests
python scripts/test_reasoning.py
```

## Deployment

### Production Configuration
```yaml
# docker-compose.yml
version: '3.8'
services:
  govsecure-ai:
    image: govsecure-ai:latest
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_DEFAULT_MODEL=gpt-4.1
      - OPENAI_REASONING_MODEL=o3
      - ENABLE_DSPY=true
      - ENABLE_AUDIO=true
    ports:
      - "8000:8000"
```

### Model Access Requirements
- OpenAI API access with latest model availability
- Sufficient API rate limits for government usage
- Compliance with data residency requirements
- Security clearance for sensitive model usage

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenAI**: For providing the advanced AI capabilities including GPT-4.1, o-series reasoning models, and audio models
- **DSPy Team**: For the structured programming framework for language models
- **US Government**: For the security standards and compliance frameworks
- **Open Source Community**: For foundational technologies and libraries

---

**GovSecure AI Platform** - Advancing Government Operations Through Latest AI Technology

Built with precision for the public sector by Nik Jois and the open source community. 