"""
Setup script for GovSecure AI Platform
Author: Nik Jois
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="govsecure-ai-platform",
    version="2.0.0",
    author="Nik Jois",
    description="Advanced AI-Powered Government Operations Platform with Latest OpenAI Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llamasearchai/OpenGov",
    project_urls={
        "Bug Tracker": "https://github.com/llamasearchai/OpenGov/issues",
        "Documentation": "https://github.com/llamasearchai/OpenGov#readme",
        "Source Code": "https://github.com/llamasearchai/OpenGov",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Government",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Financial :: Accounting",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Framework :: FastAPI",
        "Natural Language :: English",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "isort>=5.12.0",
            "mypy>=1.7.1",
            "bandit>=1.7.5",
            "safety>=2.3.5",
        ],
        "audio": [
            "librosa>=0.10.1",
            "soundfile>=0.12.1",
            "speech-recognition>=3.10.0",
        ],
        "dspy": [
            "dspy-ai>=2.4.0",
        ],
        "full": [
            "librosa>=0.10.1",
            "soundfile>=0.12.1",
            "speech-recognition>=3.10.0",
            "dspy-ai>=2.4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "govsecure=cli:cli",
            "govsecure-ai=cli:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "backend": ["*.json", "*.yaml", "*.yml"],
        "": ["*.md", "*.txt", "*.cfg", "*.ini"],
    },
    keywords=[
        "government", "ai", "openai", "gpt-4", "compliance", "fedramp", "nist", 
        "security", "automation", "dspy", "reasoning", "audio", "translation",
        "policy", "analysis", "risk", "assessment", "citizen", "services"
    ],
    zip_safe=False,
) 