# Contributing to GovSecure AI Platform

Thank you for your interest in contributing to the GovSecure AI Platform! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Testing Guidelines](#testing-guidelines)
- [Security Considerations](#security-considerations)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a code of conduct that ensures a welcoming environment for all contributors. By participating, you agree to uphold professional standards and treat all participants with respect.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry for dependency management
- Git for version control
- OpenAI API key (for full functionality)
- Docker (optional, for containerized development)

### Setting up Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/nikjois/PublicGovPlatform.git
   cd PublicGovPlatform
   ```

2. **Set up Python environment:**
   ```bash
   # Using Poetry (recommended)
   poetry install
   poetry shell
   
   # Or using pip
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment configuration:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run tests to ensure setup is correct:**
   ```bash
   pytest tests/ -v
   ```

5. **Run the CLI to verify installation:**
   ```bash
   python cli.py
   ```

## Development Process

### Branch Naming Convention

- `feature/description-of-feature` - New features
- `bugfix/description-of-bug` - Bug fixes
- `docs/description-of-change` - Documentation updates
- `refactor/description-of-refactor` - Code refactoring
- `security/description-of-fix` - Security-related changes

### Commit Message Format

Follow conventional commit format:

```
type(scope): brief description

Detailed description of the change.

- Additional bullet points if needed
- Reference issues: Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `security`: Security improvements

### Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clean, documented code
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes:**
   ```bash
   # Run all tests
   pytest tests/ -v --cov=backend

   # Run specific test files
   pytest tests/test_cli.py -v
   pytest tests/test_api.py -v

   # Run security tests
   pytest tests/security/ -v

   # Check code quality
   black --check .
   isort --check-only .
   flake8 .
   mypy backend/
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat(cli): add new compliance scanning feature

   - Implement CMMC framework support
   - Add comprehensive test coverage
   - Update CLI interface with new commands

   Fixes #456"
   ```

5. **Push and create pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Testing Guidelines

### Test Structure

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **Security Tests**: Test security controls and compliance
- **Performance Tests**: Test system performance under load

### Writing Tests

1. **Test file naming:**
   ```
   tests/test_module_name.py
   tests/integration/test_integration_scenario.py
   tests/security/test_security_controls.py
   ```

2. **Test function naming:**
   ```python
   def test_function_should_do_something_when_condition():
       """Test that function does something when condition is met."""
       pass
   ```

3. **Test structure:**
   ```python
   def test_example():
       # Arrange
       setup_data = create_test_data()
       
       # Act
       result = perform_action(setup_data)
       
       # Assert
       assert result.is_successful
       assert result.data == expected_data
   ```

### Mock Data and API Keys

- Always use mock data for testing
- Never commit real API keys or credentials
- Use pytest fixtures for common test data
- Mock external API calls

Example:
```python
@pytest.fixture
def mock_openai_client():
    with patch('backend.ai_agents.government_assistant.AsyncOpenAI') as mock:
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content="Mock response"))]
        )
        mock.return_value = mock_client
        yield mock_client
```

### Test Coverage

- Maintain minimum 90% test coverage
- All new features must include tests
- Critical security functions require 100% coverage

## Security Considerations

### Security-First Development

1. **Never commit sensitive data:**
   - API keys, passwords, certificates
   - Real user data or PII
   - Internal system configurations

2. **Follow secure coding practices:**
   - Input validation and sanitization
   - Proper authentication and authorization
   - Secure error handling (no information leakage)
   - Use parameterized queries for database operations

3. **Government compliance requirements:**
   - All code must be compliant with FedRAMP High standards
   - Follow NIST 800-53 security controls
   - Implement proper audit logging
   - Ensure data encryption at rest and in transit

### Security Testing

```bash
# Run security scans
bandit -r backend/
safety check
semgrep --config=auto .

# Run security-specific tests
pytest tests/security/ -v
```

## Pull Request Process

### Before Submitting

1. **Code quality checks:**
   ```bash
   # Format code
   black .
   isort .
   
   # Check for issues
   flake8 .
   mypy backend/
   
   # Run full test suite
   pytest tests/ -v --cov=backend --cov-fail-under=90
   
   # Security checks
   bandit -r backend/
   ```

2. **Documentation updates:**
   - Update README.md if needed
   - Add/update docstrings
   - Update API documentation
   - Add changelog entry

3. **Self-review checklist:**
   - [ ] Code follows project style guidelines
   - [ ] All tests pass
   - [ ] Security considerations addressed
   - [ ] Documentation updated
   - [ ] No sensitive data committed
   - [ ] Backward compatibility maintained
   - [ ] Performance impact considered

### Pull Request Template

When creating a PR, include:

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Security improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] Security testing completed

## Compliance
- [ ] Code follows government security standards
- [ ] No sensitive data exposed
- [ ] Audit logging implemented where required
- [ ] FedRAMP controls considered

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### Review Process

1. **Automated checks:** All CI/CD checks must pass
2. **Code review:** At least one maintainer review required
3. **Security review:** Security-related changes require additional review
4. **Documentation review:** Documentation changes reviewed for accuracy

## Coding Standards

### Python Code Style

- **PEP 8 compliance:** Use `black` for automatic formatting
- **Import organization:** Use `isort` for import sorting
- **Type hints:** Use type hints for all function signatures
- **Docstrings:** Use Google-style docstrings

Example:
```python
from typing import Dict, List, Optional

async def process_compliance_data(
    data: Dict[str, Any], 
    framework: str = "NIST_800_53"
) -> Optional[List[Dict[str, Any]]]:
    """
    Process compliance data for the specified framework.
    
    Args:
        data: Raw compliance data to process
        framework: Compliance framework to use for processing
        
    Returns:
        Processed compliance data or None if processing fails
        
    Raises:
        ValueError: If framework is not supported
        ProcessingError: If data processing fails
    """
    if framework not in SUPPORTED_FRAMEWORKS:
        raise ValueError(f"Unsupported framework: {framework}")
    
    try:
        # Processing logic here
        return processed_data
    except Exception as e:
        logger.error(f"Failed to process compliance data: {e}")
        raise ProcessingError(f"Processing failed: {e}") from e
```

### File Organization

```
backend/
├── __init__.py
├── api/            # REST API endpoints
├── ai_agents/      # AI agent implementations
├── auth/           # Authentication and authorization
├── compliance/     # Compliance scanning and validation
├── core/           # Core configuration and utilities
└── utils/          # Utility functions and helpers

tests/
├── __init__.py
├── integration/    # Integration tests
├── security/       # Security tests
├── unit/           # Unit tests
└── fixtures/       # Test fixtures and data
```

## Documentation

### Code Documentation

- **Docstrings:** All public functions and classes
- **Comments:** Complex logic and business rules
- **Type hints:** All function parameters and returns
- **README updates:** For significant changes

### API Documentation

- **OpenAPI/Swagger:** REST API documentation
- **Examples:** Include usage examples
- **Error codes:** Document all error responses
- **Authentication:** Document auth requirements

### User Documentation

- **Installation guide:** Step-by-step setup
- **Usage examples:** Common use cases
- **Configuration guide:** All configuration options
- **Troubleshooting:** Common issues and solutions

## Getting Help

### Communication Channels

- **GitHub Issues:** Bug reports and feature requests
- **GitHub Discussions:** General questions and discussions
- **Email:** nikjois@llamasearch.ai for sensitive issues

### Resources

- **Architecture Documentation:** [docs/architecture.md](docs/architecture.md)
- **Security Guide:** [docs/security.md](docs/security.md)
- **API Reference:** [docs/api/](docs/api/)
- **Development Guide:** [docs/development.md](docs/development.md)

## Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` file
- GitHub contributors page
- Release notes for significant contributions

Thank you for contributing to the GovSecure AI Platform! Your efforts help improve government technology and public service delivery. 