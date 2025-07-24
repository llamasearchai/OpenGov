"""
Configuration management for GovSecure AI platform.
Handles all environment variables and application settings.

Author: Nik Jois
"""

import os
import secrets
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    """Environment enum for the application."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class ComplianceLevel(str, Enum):
    """Compliance level enum for the application."""
    FEDRAMP_MODERATE = "fedramp_moderate"
    FEDRAMP_HIGH = "fedramp_high"
    IL4 = "il4"
    IL5 = "il5"
    IL6 = "il6"
    CJIS = "cjis"
    HIPAA = "hipaa"


class LogLevel(str, Enum):
    """Log level enum."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseEngine(str, Enum):
    """Database engine enum."""
    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"


class CacheType(str, Enum):
    """Cache type enum."""
    REDIS = "redis"
    MEMORY = "memory"


class APIConfig(BaseSettings):
    """API configuration settings."""
    host: str = Field(default="0.0.0.0", env="GOVSECURE_API__HOST")
    port: int = Field(default=8000, env="GOVSECURE_API__PORT")
    workers: int = Field(default=4, env="GOVSECURE_API__WORKERS")
    reload: bool = Field(default=False, env="GOVSECURE_API__RELOAD")
    enable_docs: bool = Field(default=True, env="GOVSECURE_API__ENABLE_DOCS")
    api_version: str = Field(default="v1", env="GOVSECURE_API__API_VERSION")
    rate_limit: int = Field(default=100, env="GOVSECURE_API__RATE_LIMIT")
    timeout: int = Field(default=60, env="GOVSECURE_API__TIMEOUT")

    class Config:
        env_prefix = "GOVSECURE_API__"


class SecurityConfig(BaseSettings):
    """Security configuration settings."""
    secret_key: str = Field(default_factory=lambda: secrets.token_hex(32), env="GOVSECURE_SECURITY__SECRET_KEY")
    algorithm: str = Field(default="HS256", env="GOVSECURE_SECURITY__ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="GOVSECURE_SECURITY__ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="GOVSECURE_SECURITY__REFRESH_TOKEN_EXPIRE_DAYS")
    mfa_enabled: bool = Field(default=True, env="GOVSECURE_SECURITY__MFA_ENABLED")
    password_min_length: int = Field(default=12, env="GOVSECURE_SECURITY__PASSWORD_MIN_LENGTH")
    password_complexity: bool = Field(default=True, env="GOVSECURE_SECURITY__PASSWORD_COMPLEXITY")
    session_timeout_minutes: int = Field(default=15, env="GOVSECURE_SECURITY__SESSION_TIMEOUT_MINUTES")
    allowed_origins: List[str] = Field(default=["http://localhost:3000"], env="GOVSECURE_SECURITY__ALLOWED_ORIGINS")
    tls_min_version: str = Field(default="1.2", env="GOVSECURE_SECURITY__TLS_MIN_VERSION")

    class Config:
        env_prefix = "GOVSECURE_SECURITY__"


class DatabaseConfig(BaseSettings):
    """Database configuration settings."""
    engine: DatabaseEngine = Field(default=DatabaseEngine.POSTGRESQL, env="GOVSECURE_DATABASE__ENGINE")
    host: str = Field(default="localhost", env="GOVSECURE_DATABASE__HOST")
    port: int = Field(default=5432, env="GOVSECURE_DATABASE__PORT")
    username: str = Field(default="postgres", env="GOVSECURE_DATABASE__USERNAME")
    password: str = Field(default="", env="GOVSECURE_DATABASE__PASSWORD")
    database: str = Field(default="govsecure_ai", env="GOVSECURE_DATABASE__DATABASE")
    ssl_mode: str = Field(default="require", env="GOVSECURE_DATABASE__SSL_MODE")
    pool_size: int = Field(default=10, env="GOVSECURE_DATABASE__POOL_SIZE")
    max_overflow: int = Field(default=20, env="GOVSECURE_DATABASE__MAX_OVERFLOW")
    
    class Config:
        env_prefix = "GOVSECURE_DATABASE__"
    
    @property
    def connection_string(self) -> str:
        """Get database connection string."""
        if self.engine == DatabaseEngine.SQLITE:
            return f"sqlite:///{self.database}.db"
        
        auth = f"{self.username}:{self.password}" if self.username else ""
        host = f"{self.host}:{self.port}" if self.port else self.host
        
        if auth:
            return f"{self.engine.value}://{auth}@{host}/{self.database}"
        else:
            return f"{self.engine.value}://{host}/{self.database}"


class CacheConfig(BaseSettings):
    """Cache configuration settings."""
    type: CacheType = Field(default=CacheType.REDIS, env="GOVSECURE_CACHE__TYPE")
    host: str = Field(default="localhost", env="GOVSECURE_CACHE__HOST")
    port: int = Field(default=6379, env="GOVSECURE_CACHE__PORT")
    db: int = Field(default=0, env="GOVSECURE_CACHE__DB")
    password: Optional[str] = Field(default=None, env="GOVSECURE_CACHE__PASSWORD")
    ssl: bool = Field(default=False, env="GOVSECURE_CACHE__SSL")
    default_ttl: int = Field(default=300, env="GOVSECURE_CACHE__DEFAULT_TTL")
    
    class Config:
        env_prefix = "GOVSECURE_CACHE__"


class AuthConfig(BaseSettings):
    """Authentication configuration settings."""
    auth_providers: List[str] = Field(default=["local"], env="GOVSECURE_AUTH__AUTH_PROVIDERS")
    rbac_enabled: bool = Field(default=True, env="GOVSECURE_AUTH__RBAC_ENABLED")
    jwt_enabled: bool = Field(default=True, env="GOVSECURE_AUTH__JWT_ENABLED")
    saml_enabled: bool = Field(default=False, env="GOVSECURE_AUTH__SAML_ENABLED")
    oidc_enabled: bool = Field(default=False, env="GOVSECURE_AUTH__OIDC_ENABLED")
    max_sessions_per_user: int = Field(default=5, env="GOVSECURE_AUTH__MAX_SESSIONS_PER_USER")
    max_failed_logins: int = Field(default=5, env="GOVSECURE_AUTH__MAX_FAILED_LOGINS")
    lockout_duration_minutes: int = Field(default=30, env="GOVSECURE_AUTH__LOCKOUT_DURATION_MINUTES")
    
    class Config:
        env_prefix = "GOVSECURE_AUTH__"


class ComplianceConfig(BaseSettings):
    """Compliance configuration settings."""
    compliance_level: ComplianceLevel = Field(default=ComplianceLevel.FEDRAMP_HIGH, env="GOVSECURE_COMPLIANCE__COMPLIANCE_LEVEL")
    auto_remediation_enabled: bool = Field(default=True, env="GOVSECURE_COMPLIANCE__AUTO_REMEDIATION_ENABLED")
    scans_schedule: str = Field(default="0 0 * * *", env="GOVSECURE_COMPLIANCE__SCANS_SCHEDULE")
    report_generation_enabled: bool = Field(default=True, env="GOVSECURE_COMPLIANCE__REPORT_GENERATION_ENABLED")
    continuous_monitoring_enabled: bool = Field(default=True, env="GOVSECURE_COMPLIANCE__CONTINUOUS_MONITORING_ENABLED")
    vulnerability_scan_enabled: bool = Field(default=True, env="GOVSECURE_COMPLIANCE__VULNERABILITY_SCAN_ENABLED")
    stig_compliance_enabled: bool = Field(default=True, env="GOVSECURE_COMPLIANCE__STIG_COMPLIANCE_ENABLED")
    
    class Config:
        env_prefix = "GOVSECURE_COMPLIANCE__"


class LoggingConfig(BaseSettings):
    """Logging configuration settings."""
    level: LogLevel = Field(default=LogLevel.INFO, env="GOVSECURE_LOGGING__LEVEL")
    format: str = Field(default="json", env="GOVSECURE_LOGGING__FORMAT")
    log_to_file: bool = Field(default=True, env="GOVSECURE_LOGGING__LOG_TO_FILE")
    log_file: str = Field(default="logs/govsecure-ai.log", env="GOVSECURE_LOGGING__LOG_FILE")
    enable_audit_logs: bool = Field(default=True, env="GOVSECURE_LOGGING__ENABLE_AUDIT_LOGS")
    audit_log_file: str = Field(default="logs/audit.log", env="GOVSECURE_LOGGING__AUDIT_LOG_FILE")
    opentelemetry_enabled: bool = Field(default=True, env="GOVSECURE_LOGGING__OPENTELEMETRY_ENABLED")
    opentelemetry_endpoint: Optional[str] = Field(default=None, env="GOVSECURE_LOGGING__OPENTELEMETRY_ENDPOINT")
    
    class Config:
        env_prefix = "GOVSECURE_LOGGING__"


class AIConfig(BaseSettings):
    """AI model configuration settings."""
    model_registry_path: str = Field(default="models", env="GOVSECURE_AI__MODEL_REGISTRY_PATH")
    enable_gpu: bool = Field(default=False, env="GOVSECURE_AI__ENABLE_GPU")
    max_batch_size: int = Field(default=16, env="GOVSECURE_AI__MAX_BATCH_SIZE")
    default_inference_timeout: int = Field(default=60, env="GOVSECURE_AI__DEFAULT_INFERENCE_TIMEOUT")
    enable_stream_responses: bool = Field(default=True, env="GOVSECURE_AI__ENABLE_STREAM_RESPONSES")
    model_validation_required: bool = Field(default=True, env="GOVSECURE_AI__MODEL_VALIDATION_REQUIRED")
    model_monitoring_enabled: bool = Field(default=True, env="GOVSECURE_AI__MODEL_MONITORING_ENABLED")
    explainability_required: bool = Field(default=True, env="GOVSECURE_AI__EXPLAINABILITY_REQUIRED")
    
    class Config:
        env_prefix = "GOVSECURE_AI__"


class StorageConfig(BaseSettings):
    """Storage configuration settings."""
    provider: str = Field(default="local", env="GOVSECURE_STORAGE__PROVIDER")
    local_path: str = Field(default="data", env="GOVSECURE_STORAGE__LOCAL_PATH")
    encryption_enabled: bool = Field(default=True, env="GOVSECURE_STORAGE__ENCRYPTION_ENABLED")
    encryption_key_management: str = Field(default="application", env="GOVSECURE_STORAGE__ENCRYPTION_KEY_MANAGEMENT")
    file_size_limit_mb: int = Field(default=100, env="GOVSECURE_STORAGE__FILE_SIZE_LIMIT_MB")
    bucket_name: Optional[str] = Field(default=None, env="GOVSECURE_STORAGE__BUCKET_NAME")
    
    class Config:
        env_prefix = "GOVSECURE_STORAGE__"


class FeatureFlags(BaseSettings):
    """Feature flags configuration."""
    demo_mode: bool = Field(default=False, env="GOVSECURE_FEATURES__DEMO_MODE")
    mock_ai_responses: bool = Field(default=False, env="GOVSECURE_FEATURES__MOCK_AI_RESPONSES")
    bypass_auth: bool = Field(default=False, env="GOVSECURE_FEATURES__BYPASS_AUTH")
    enable_debug_endpoints: bool = Field(default=False, env="GOVSECURE_FEATURES__ENABLE_DEBUG_ENDPOINTS")
    
    class Config:
        env_prefix = "GOVSECURE_FEATURES__"


class OpenAIConfig(BaseSettings):
    """OpenAI configuration settings."""
    api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    organization: Optional[str] = Field(default=None, env="OPENAI_ORGANIZATION")
    model: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    max_tokens: int = Field(default=4096, env="OPENAI_MAX_TOKENS")
    temperature: float = Field(default=0.1, env="OPENAI_TEMPERATURE")
    
    class Config:
        env_prefix = "OPENAI_"


class Config(BaseSettings):
    """Main configuration class that combines all settings."""
    
    # Core settings
    app_name: str = Field(default="GovSecure AI", env="GOVSECURE_APP_NAME")
    environment: Environment = Field(default=Environment.DEVELOPMENT, env="GOVSECURE_ENVIRONMENT")
    deployment_id: str = Field(default="local-dev", env="GOVSECURE_DEPLOYMENT_ID")
    base_dir: str = Field(default=".", env="GOVSECURE_BASE_DIR")
    debug: bool = Field(default=False, env="GOVSECURE_DEBUG")
    version: str = Field(default="1.0.0", env="GOVSECURE_VERSION")
    
    # Sub-configurations
    api: APIConfig = Field(default_factory=APIConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)
    compliance: ComplianceConfig = Field(default_factory=ComplianceConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    ai: AIConfig = Field(default_factory=AIConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    features: FeatureFlags = Field(default_factory=FeatureFlags)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"
    
    @validator("base_dir")
    def validate_base_dir(cls, v):
        """Validate base directory exists."""
        path = Path(v)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return str(path.absolute())
    
    def __init__(self, **kwargs):
        """Initialize configuration with nested models."""
        super().__init__(**kwargs)
        
        # Initialize nested configurations
        self.api = APIConfig()
        self.security = SecurityConfig()
        self.database = DatabaseConfig()
        self.cache = CacheConfig()
        self.auth = AuthConfig()
        self.compliance = ComplianceConfig()
        self.logging = LoggingConfig()
        self.ai = AIConfig()
        self.storage = StorageConfig()
        self.features = FeatureFlags()
        
        # Try to initialize OpenAI config (may fail if no API key)
        try:
            self.openai = OpenAIConfig()
        except Exception:
            # Create default OpenAI config for cases where no key is set
            self.openai = OpenAIConfig(api_key="not-set")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == Environment.PRODUCTION
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""  
        return self.environment == Environment.DEVELOPMENT
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing."""
        return self.environment == Environment.TESTING
    
    def get_log_level(self) -> str:
        """Get the appropriate log level."""
        if self.debug:
            return "DEBUG"
        return self.logging.level.value


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config() -> Config:
    """Reload the configuration from environment."""
    global _config
    _config = Config()
    return _config 