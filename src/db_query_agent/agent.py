"""Main DatabaseQueryAgent class - the primary interface for the package."""

import logging
import time
from typing import Dict, Any, Optional, AsyncIterator
from sqlalchemy import create_engine
from db_query_agent.config import AgentConfig, DatabaseConfig, CacheConfig, ModelConfig, SafetyConfig
from db_query_agent.schema_extractor import SchemaExtractor
from db_query_agent.cache_manager import CacheManager
from db_query_agent.connection_manager import ConnectionManager
from db_query_agent.query_validator import QueryValidator
from db_query_agent.agent_integration import DatabaseContext
from db_query_agent.session_manager import SessionManager, ChatSession
from db_query_agent.simple_multi_agent_system import SimpleMultiAgentSystem
from db_query_agent.exceptions import DatabaseQueryAgentError

logger = logging.getLogger(__name__)


class DatabaseQueryAgent:
    """
    Main interface for natural language database querying.
    
    Example:
        >>> agent = DatabaseQueryAgent(
        ...     database_url="postgresql://user:pass@localhost/db",
        ...     openai_api_key="sk-..."
        ... )
        >>> result = agent.query("How many users signed up last month?")
        >>> print(result["natural_response"])
    """
    
    def __init__(
        self,
        database_url: str,
        openai_api_key: str,
        # Model configuration
        model_strategy: str = "adaptive",
        fast_model: str = "gpt-4o-mini",
        balanced_model: str = "gpt-4.1-mini",
        complex_model: str = "gpt-4.1",
        # Cache configuration
        enable_cache: bool = True,
        cache_backend: str = "memory",
        schema_cache_ttl: int = 3600,
        query_cache_ttl: int = 300,
        llm_cache_ttl: int = 3600,
        # Safety configuration
        read_only: bool = True,
        allowed_tables: Optional[list[str]] = None,
        blocked_tables: Optional[list[str]] = None,
        max_query_timeout: int = 30,
        max_result_rows: int = 10000,
        # Connection configuration
        pool_size: int = 10,
        max_overflow: int = 20,
        # Performance configuration
        lazy_schema_loading: bool = True,
        max_tables_in_context: int = 5,
        enable_streaming: bool = True,
        warmup_on_init: bool = False,
    ):
        """
        Initialize DatabaseQueryAgent.
        
        Args:
            database_url: Database connection URL
            openai_api_key: OpenAI API key
            model_strategy: Model selection strategy ('fixed' or 'adaptive')
            fast_model: Fast model for simple queries
            balanced_model: Balanced model for medium queries
            complex_model: Complex model for hard queries
            enable_cache: Enable caching
            cache_backend: Cache backend ('memory', 'sqlite', 'redis')
            schema_cache_ttl: Schema cache TTL in seconds
            query_cache_ttl: Query result cache TTL in seconds
            llm_cache_ttl: LLM response cache TTL in seconds
            read_only: Only allow SELECT queries
            allowed_tables: List of allowed tables (None = all)
            blocked_tables: List of blocked tables
            max_query_timeout: Maximum query execution time
            max_result_rows: Maximum result rows
            pool_size: Connection pool size
            max_overflow: Maximum overflow connections
            lazy_schema_loading: Load only relevant tables
            max_tables_in_context: Maximum tables in LLM context
            enable_streaming: Enable streaming responses
            warmup_on_init: Warm up cache on initialization
        """
        logger.info("Initializing DatabaseQueryAgent")
        
        # Create configuration
        self.config = AgentConfig(
            openai_api_key=openai_api_key,
            database=DatabaseConfig(
                url=database_url,
                pool_size=pool_size,
                max_overflow=max_overflow
            ),
            cache=CacheConfig(
                enabled=enable_cache,
                backend=cache_backend,
                schema_ttl=schema_cache_ttl,
                query_ttl=query_cache_ttl,
                llm_ttl=llm_cache_ttl
            ),
            model=ModelConfig(
                strategy=model_strategy,
                fast_model=fast_model,
                balanced_model=balanced_model,
                complex_model=complex_model
            ),
            safety=SafetyConfig(
                read_only=read_only,
                allowed_tables=allowed_tables,
                blocked_tables=blocked_tables,
                max_query_timeout=max_query_timeout,
                max_result_rows=max_result_rows
            ),
            enable_streaming=enable_streaming,
            lazy_schema_loading=lazy_schema_loading,
            max_tables_in_context=max_tables_in_context,
            warmup_on_init=warmup_on_init
        )
        
        # Initialize query statistics
        self.stats = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "cache_hits": 0,
        }
        
        # Initialize components
        self._initialize_components()
        
        # Warmup if requested
        if warmup_on_init:
            self._warmup()
        
        logger.info("DatabaseQueryAgent initialized successfully")
    
    def _initialize_components(self) -> None:
        """Initialize all components."""
        # Connection manager
        self.connection_manager = ConnectionManager(self.config.database)
        
        # Test connection
        if not self.connection_manager.test_connection():
            raise DatabaseQueryAgentError("Failed to connect to database")
        
        # Schema extractor
        self.schema_extractor = SchemaExtractor(
            self.connection_manager.engine,
            cache_ttl=self.config.cache.schema_ttl
        )
        
        # Cache manager
        self.cache_manager = CacheManager(
            schema_ttl=self.config.cache.schema_ttl,
            query_ttl=self.config.cache.query_ttl,
            llm_ttl=self.config.cache.llm_ttl
        )
        
        # Query validator
        self.query_validator = QueryValidator(
            read_only=self.config.safety.read_only,
            allowed_tables=self.config.safety.allowed_tables,
            blocked_tables=self.config.safety.blocked_tables
        )
        
        # Database context
        self.db_context = DatabaseContext(
            connection_manager=self.connection_manager,
            schema_extractor=self.schema_extractor,
            validator=self.query_validator,
            safety_config=self.config.safety
        )
        
        # Session manager
        self.session_manager = SessionManager(
            backend=self.config.cache.backend
        )
        
        # Initialize multi-agent system (only system available)
        logger.info("Initializing multi-agent system (optimized for speed)...")
        self.multi_agent_system = SimpleMultiAgentSystem(
            database_context=self.db_context,
            model_config=self.config.model,
            openai_api_key=self.config.openai_api_key,
            cache_manager=self.cache_manager,
            cache_enabled=self.config.cache.enabled
        )
        logger.info("Multi-agent system initialized (1 LLM call per query)")
    
    def _warmup(self) -> None:
        """Warm up cache and connections."""
        logger.info("Warming up agent...")
        
        # Pre-load schema
        schema = self.schema_extractor.get_schema()
        logger.info(f"Schema loaded: {len(schema)} tables")
        
        # Test query
        try:
            self.connection_manager.execute_query("SELECT 1")
            logger.info("Connection pool warmed up")
        except Exception as e:
            logger.warning(f"Warmup query failed: {e}")
    
    async def query(
        self,
        question: str,
        return_sql: bool = True,
        return_results: bool = True,
        return_natural_response: bool = True,
        session: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Query database using natural language.
        
        Args:
            question: Natural language question
            return_sql: Include SQL in response
            return_results: Execute query and return results
            return_natural_response: Generate natural language response
            
        Returns:
            Dictionary with query results
        """
        start_time = time.time()
        logger.info(f"Processing query: {question}")
        
        try:
            # Use multi-agent system (only system available)
            logger.info("Using multi-agent system (conversational-first)")
            
            # Check if this will be a cache hit (for stats)
            was_cached = False
            if self.config.cache.enabled:
                schema_hash = str(hash(str(self.schema_extractor.get_schema())))
                cached = self.cache_manager.get_llm_response(question, schema_hash)
                was_cached = cached is not None
            
            result = await self.multi_agent_system.query(question, session=session)
            result["execution_time"] = time.time() - start_time
            
            # Update statistics
            if not result.get('is_casual', False):
                self.stats["total_queries"] += 1
                if was_cached:
                    self.stats["cache_hits"] += 1
                if result.get('error'):
                    self.stats["failed_queries"] += 1
                else:
                    self.stats["successful_queries"] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            # Update failure stats
            self.stats["failed_queries"] += 1
            return {
                "question": question,
                "error": str(e),
                "execution_time": time.time() - start_time
            }
    
    async def query_stream(self, question: str) -> AsyncIterator[str]:
        """
        Query database with streaming response.
        
        Note: Streaming is not currently supported in multi-agent mode.
        This method will be implemented in a future update.
        
        Args:
            question: Natural language question
            
        Yields:
            Response tokens as they are generated
        """
        logger.warning("Streaming is not yet supported in multi-agent mode")
        # For now, fall back to regular query and yield the complete response
        result = await self.query(question)
        yield result.get("natural_response", str(result.get("final_output", "")))
    
    def create_session(self, session_id: str) -> ChatSession:
        """
        Create a chat session for multi-turn conversations.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            ChatSession instance
        """
        session = self.session_manager.create_session(session_id)
        return ChatSession(session_id, self, session)
    
    def get_schema(self) -> Dict[str, Any]:
        """Get database schema."""
        return self.schema_extractor.get_schema()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            **self.stats,  # Include query statistics
            "cache": self.cache_manager.get_stats(),
            "pool": self.connection_manager.get_pool_status(),
            "sessions": self.session_manager.get_stats(),
            "schema_tables": len(self.schema_extractor.get_schema())
        }
    
    def close(self) -> None:
        """Close all connections and cleanup."""
        logger.info("Closing DatabaseQueryAgent")
        self.connection_manager.close()
