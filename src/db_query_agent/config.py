"""Configuration management for db-query-agent."""

from typing import Optional, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class DatabaseConfig(BaseModel):
    """Database configuration."""
    
    url: str = Field(..., description="Database connection URL")
    pool_size: int = Field(default=10, description="Connection pool size")
    max_overflow: int = Field(default=20, description="Maximum overflow connections")
    pool_timeout: int = Field(default=30, description="Pool timeout in seconds")
    pool_recycle: int = Field(default=3600, description="Connection recycle time in seconds")


class CacheConfig(BaseModel):
    """Cache configuration."""
    
    enabled: bool = Field(default=True, description="Enable caching")
    backend: str = Field(default="memory", description="Cache backend: memory, sqlite, redis")
    schema_ttl: int = Field(default=3600, description="Schema cache TTL in seconds")
    query_ttl: int = Field(default=300, description="Query result cache TTL in seconds")
    llm_ttl: int = Field(default=3600, description="LLM response cache TTL in seconds")
    redis_url: Optional[str] = Field(default=None, description="Redis URL if using redis backend")


class ModelConfig(BaseModel):
    """LLM model configuration."""
    
    strategy: str = Field(default="adaptive", description="Model selection strategy: fixed, adaptive")
    fast_model: str = Field(default="gpt-4o-mini", description="Fast model for simple queries")
    balanced_model: str = Field(default="gpt-4.1-mini", description="Balanced model")
    complex_model: str = Field(default="gpt-4.1", description="Complex model for hard queries")
    temperature: float = Field(default=0.0, description="Model temperature")
    max_tokens: int = Field(default=1000, description="Maximum tokens for response")


class SafetyConfig(BaseModel):
    """Safety and validation configuration."""
    
    read_only: bool = Field(default=True, description="Allow only SELECT queries")
    allowed_tables: Optional[List[str]] = Field(default=None, description="Allowed tables (None = all)")
    blocked_tables: Optional[List[str]] = Field(default=None, description="Blocked tables")
    max_query_timeout: int = Field(default=30, description="Maximum query execution time in seconds")
    max_result_rows: int = Field(default=10000, description="Maximum result rows")
    enable_guardrails: bool = Field(default=True, description="Enable input/output guardrails")


class AgentConfig(BaseModel):
    """Complete agent configuration."""
    
    openai_api_key: str = Field(..., description="OpenAI API key")
    database: DatabaseConfig
    cache: CacheConfig = Field(default_factory=CacheConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    safety: SafetyConfig = Field(default_factory=SafetyConfig)
    
    enable_streaming: bool = Field(default=True, description="Enable streaming responses")
    lazy_schema_loading: bool = Field(default=True, description="Load only relevant tables")
    max_tables_in_context: int = Field(default=5, description="Max tables to include in context")
    use_embeddings: bool = Field(default=False, description="Use embeddings for table selection")
    warmup_on_init: bool = Field(default=False, description="Warm up cache on initialization")
    
    @classmethod
    def from_env(cls, database_url: Optional[str] = None) -> "AgentConfig":
        """Create configuration from environment variables."""
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        db_url = database_url or os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL must be provided or set in environment")
        
        return cls(
            openai_api_key=openai_api_key,
            database=DatabaseConfig(url=db_url),
            cache=CacheConfig(
                backend=os.getenv("CACHE_BACKEND", "memory"),
                redis_url=os.getenv("REDIS_URL"),
            ),
            model=ModelConfig(
                fast_model=os.getenv("FAST_MODEL", "gpt-4o-mini"),
                balanced_model=os.getenv("BALANCED_MODEL", "gpt-4.1-mini"),
            ),
            safety=SafetyConfig(
                read_only=os.getenv("READ_ONLY", "true").lower() == "true",
                max_query_timeout=int(os.getenv("QUERY_TIMEOUT", "30")),
            ),
        )
