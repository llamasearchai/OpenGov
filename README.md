![OpenGov Logo](assets/opengov_logo.svg)

# GovSecure AI Platform

[![CI/CD Pipeline](https://github.com/nikjois/PublicGovPlatform/actions/workflows/ci.yml/badge.svg)](https://github.com/nikjois/PublicGovPlatform/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/govsecure-ai-platform.svg)](https://badge.fury.io/py/govsecure-ai-platform)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Codecov](https://codecov.io/gh/nikjois/PublicGovPlatform/branch/main/graph/badge.svg)](https://codecov.io/gh/nikjois/PublicGovPlatform)

**Advanced AI-Powered Government Operations Platform with Latest OpenAI Models**

A comprehensive artificial intelligence platform designed specifically for US government agencies, providing secure, compliant, and efficient solutions for citizen services, document analysis, compliance management, and emergency response coordination. Built with complete support for all latest OpenAI models including GPT-4.1, o-series reasoning models, and DSPy integration for compound AI systems.

## Table of Contents

- [Overview](#overview)
- [Latest AI Model Support](#latest-ai-model-support)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)
- [Government Use Cases](#government-use-cases)
- [Security & Compliance](#security--compliance)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)
- [Acknowledgments](#acknowledgments)

## Overview

The GovSecure AI Platform leverages cutting-edge OpenAI technology including the latest GPT-4.1, o3 reasoning models, and audio-capable models to deliver intelligent automation for government operations while maintaining the highest security standards required for federal environments. Built with FedRAMP compliance in mind and designed for IL5 compatibility.

**Author:** Nik Jois (nikjois@llamasearch.ai)  
**Organization:** LlamaSearch AI  
**Version:** 2.0.0  
**License:** MIT  

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

#### From PyPI (Recommended)
```bash
pip install govsecure-ai-platform
```

#### From Source
```bash
git clone https://github.com/nikjois/PublicGovPlatform.git
cd PublicGovPlatform
pip install -r requirements.txt
pip install -e .
```

### Environment Configuration
```bash
cp env.example .env
# Edit .env with your OpenAI API key and configuration
```

### Initialize Database
```bash
govsecure init-db
```

### Run the Application
```bash
# CLI Interface with latest models
govsecure start

# Web API with full model support
govsecure web

# Quick Compliance Scan with reasoning models
govsecure scan
```

## Configuration

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

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/govsecure
REDIS_URL=redis://localhost:6379

# Security Configuration
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Compliance Configuration
FEDRAMP_MODE=true
AUDIT_LOGGING=true
ENCRYPTION_AT_REST=true
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

#### Compliance Analysis with Reasoning
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
print(f"Confidence Score: {result.confidence}")
```

#### Multi-Step Policy Analysis
```python
# Complex policy analysis
result = await orchestrator.analyze_policy(
    policy_text="New data privacy regulation text...",
    context="Federal agency implementation"
)

print(f"Key Points: {result.result['key_points']}")
print(f"Implications: {result.result['implications']}")
print(f"Risk Assessment: {result.result['risks']}")
```

#### Document Synthesis
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
print(f"Recommendations: {result.result['recommendations']}")
```

### Command Line Interface

#### Interactive Government Assistant
```bash
# Start interactive session with latest models
govsecure start

# Use reasoning model for complex analysis
govsecure chat "Analyze FISMA compliance requirements" --model o3

# Use audio model for voice processing
govsecure chat "Process this audio input" --model gpt-4o-audio-preview

# Use cost-optimized model for routine tasks
govsecure chat "Simple question" --model gpt-4.1-nano
```

#### Batch Processing
```bash
# Process multiple documents
govsecure process-batch --input-dir ./documents --output-dir ./results

# Compliance scan
govsecure compliance-scan --target ./system-configs --framework nist-800-53

# Generate compliance report
govsecure generate-report --type compliance --output ./compliance-report.pdf
```

### Web API Usage

#### Model Selection Endpoint
```bash
curl -X GET "http://localhost:8000/api/v1/models"
# Returns available models and capabilities
```

#### Advanced Chat with Model Selection
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "message": "Analyze this complex policy document",
    "mode": "compliance",
    "model": "o3",
    "use_reasoning": true,
    "context": {
      "agency": "GSA",
      "classification": "UNCLASSIFIED"
    }
  }'
```

#### DSPy Reasoning Endpoint
```bash
curl -X POST "http://localhost:8000/api/v1/ai/dspy/analyze" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "task_type": "compliance_reasoning",
    "input_data": {
      "context": "Government system",
      "regulation": "NIST 800-53"
    },
    "model": "o3-pro"
  }'
```

## API Documentation

### Core Endpoints

#### Authentication
```
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
GET  /api/v1/auth/user
```

#### AI Services
```
POST /api/v1/ai/chat
POST /api/v1/ai/analyze
POST /api/v1/ai/translate
POST /api/v1/ai/summarize
GET  /api/v1/ai/models
```

#### Compliance
```
POST /api/v1/compliance/scan
GET  /api/v1/compliance/frameworks
GET  /api/v1/compliance/reports
POST /api/v1/compliance/validate
```

#### Document Processing
```
POST /api/v1/documents/upload
POST /api/v1/documents/analyze
GET  /api/v1/documents/{id}
DELETE /api/v1/documents/{id}
```

### Interactive API Documentation
Access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Architecture

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │   CLI Client    │    │  Mobile App     │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      API Gateway        │
                    │     (FastAPI)           │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   AI Agent Manager      │
                    │   (DSPy Integration)    │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                       │                        │
┌───────▼────────┐    ┌─────────▼─────────┐    ┌────────▼────────┐
│ Compliance     │    │   OpenAI Models   │    │   Document      │
│ Engine         │    │   (GPT-4.1, o3)   │    │   Processor     │
└────────────────┘    └───────────────────┘    └─────────────────┘
```

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

#### Complex Policy Analysis (GPT-4.1 + o3)
- Multi-document policy synthesis
- Regulatory impact assessment
- Stakeholder analysis with reasoning chains
- Cross-reference validation
- Risk impact modeling

#### Emergency Response (o3 + Audio Models)
- Real-time incident analysis with reasoning
- Voice-activated emergency protocols
- Multi-step crisis response planning
- Resource allocation optimization
- Stakeholder communication automation

#### Compliance Automation (o3-pro + DSPy)
- Advanced compliance reasoning
- Gap analysis with structured thinking
- Automated remediation planning
- Control effectiveness assessment
- Audit trail generation

#### Citizen Services (GPT-4.1 + Audio)
- Multilingual voice interfaces
- Complex benefit eligibility analysis
- Personalized service recommendations
- Case management automation
- Service delivery optimization

## Security & Compliance

### Federal Compliance Standards
- **FedRAMP High**: Authority to Operate (ATO) ready
- **NIST 800-53**: Comprehensive control implementation
- **FISMA**: Federal security management compliance
- **CJIS**: Criminal justice information security
- **IL5**: Information Level 5 compatibility

### Security Features
- **End-to-End Encryption**: Data protection in transit and at rest
- **Zero Trust Architecture**: Continuous verification model
- **Multi-Factor Authentication**: Enhanced access controls
- **Audit Logging**: Comprehensive activity tracking
- **Access Controls**: Role-based permission system

### Privacy Protection
- **Data Minimization**: Collect only necessary information
- **Retention Policies**: Automated data lifecycle management
- **Anonymization**: PII protection techniques
- **Consent Management**: User privacy controls

## Testing and Quality Assurance

### Automated Testing
```bash
# Run full test suite
pytest tests/ -v --cov=backend --cov-report=html

# Test specific components
pytest tests/test_ai_agents/ -v
pytest tests/test_compliance/ -v
pytest tests/test_api/ -v

# Security testing
bandit -r backend/
safety check

# Performance testing
pytest tests/test_performance/ -v --benchmark-only
```

### Model Testing
```bash
# Test all model integrations
pytest tests/test_models/ -v

# Test DSPy integration
pytest tests/test_dspy/ -v

# Test audio capabilities
pytest tests/test_audio/ -v

# Reasoning quality tests
python scripts/test_reasoning.py
```

### Quality Metrics
- **Code Coverage**: > 85%
- **Security Score**: A+ (Bandit)
- **Performance**: < 200ms API response time
- **Reliability**: 99.9% uptime
- **Compliance**: 100% control implementation

## Deployment

### Production Deployment

#### Docker Deployment
```yaml
# docker-compose.yml
version: '3.8'
services:
  govsecure-ai:
    image: ghcr.io/nikjois/publicgovplatform:latest
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_DEFAULT_MODEL=gpt-4.1
      - OPENAI_REASONING_MODEL=o3
      - ENABLE_DSPY=true
      - ENABLE_AUDIO=true
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: govsecure
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

#### Kubernetes Deployment
```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Scale deployment
kubectl scale deployment govsecure-ai --replicas=5
```

### Cloud Deployment Options

#### AWS GovCloud
- **ECS/Fargate**: Container orchestration
- **RDS**: Managed database service
- **ElastiCache**: Redis caching
- **ALB**: Load balancing
- **WAF**: Web application firewall

#### Azure Government
- **Container Instances**: Serverless containers
- **Azure Database**: PostgreSQL service
- **Redis Cache**: Managed caching
- **Application Gateway**: Load balancing
- **Key Vault**: Secret management

### Model Access Requirements
- OpenAI API access with latest model availability
- Sufficient API rate limits for government usage
- Compliance with data residency requirements
- Security clearance for sensitive model usage

## Contributing

We welcome contributions from the community! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/nikjois/PublicGovPlatform.git
cd PublicGovPlatform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

### Code Style
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **bandit**: Security analysis

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

### Getting Help
- **Documentation**: [Full documentation](https://github.com/nikjois/PublicGovPlatform#readme)
- **Issues**: [GitHub Issues](https://github.com/nikjois/PublicGovPlatform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nikjois/PublicGovPlatform/discussions)
- **Email**: nikjois@llamasearch.ai

### Enterprise Support
For enterprise deployments and dedicated support:
- **Email**: nikjois@llamasearch.ai
- **Custom Training**: Available for government teams
- **Consulting**: Implementation and optimization services
- **Priority Support**: 24/7 support for critical deployments

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## Acknowledgments

- **OpenAI**: For providing the advanced AI capabilities including GPT-4.1, o-series reasoning models, and audio models
- **DSPy Team**: For the structured programming framework for language models
- **US Government**: For the security standards and compliance frameworks that guide this platform
- **Open Source Community**: For foundational technologies and libraries that make this platform possible
- **Federal Technology Community**: For feedback and requirements that shape government AI solutions

---

**GovSecure AI Platform** - Advancing Government Operations Through Latest AI Technology

**Built with precision for the public sector by [Nik Jois](mailto:nikjois@llamasearch.ai) and the open source community.**

Copyright (c) 2024 Nik Jois. All rights reserved. 