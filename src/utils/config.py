"""
Application Configuration
Menggunakan pydantic-settings untuk type-safe configuration management
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings dengan validasi tipe"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # API Keys
    deepseek_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    deepseek_base_url: str = "https://api.deepseek.com"
    
    # LangSmith
    langchain_tracing_v2: bool = False
    langchain_api_key: Optional[str] = None
    langchain_project: str = "xyz-ai-nexus"
    
    # Application
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"
    
    # Agent Configuration
    default_llm_model: str = "deepseek-chat"
    orchestrator_model: str = "deepseek-chat"
    max_iterations: int = 10
    agent_timeout: int = 300
    
    # Database
    chroma_persist_directory: str = "./data/chroma"
    redis_url: str = "redis://localhost:6379"
    
    # Security
    api_key_header: str = "X-API-Key"
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"
    
    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse allowed origins as list"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Global settings instance
settings = Settings()
