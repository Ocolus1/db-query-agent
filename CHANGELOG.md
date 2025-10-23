# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup with package structure
- Core configuration management with Pydantic models
- Schema extraction using SQLAlchemy reflection
  - Automatic table, column, and relationship detection
  - Schema caching with TTL
  - Relevant table selection using keyword matching
- Multi-layer caching system
  - In-memory cache (L1) with TTL support
  - Schema, query result, and LLM response caching
- Query validation and safety checks
  - SQL parsing with sqlparse
  - Read-only mode enforcement
  - Table allowlist/blocklist support
  - Dangerous keyword detection
- Database connection management
  - Connection pooling with SQLAlchemy
  - Async query execution support
  - Connection health checks
- Custom exception hierarchy
- Comprehensive logging throughout

### Added (Phase 2)
- OpenAI Agents SDK integration with streaming support
  - Agent creation with dynamic instructions
  - Function tools for query execution and validation
  - Adaptive model selection based on query complexity
  - Streaming response support
- Session management for conversation history
  - SQLite-backed session storage
  - Chat session wrapper for multi-turn conversations
  - Session cleanup and statistics
- Main DatabaseQueryAgent class
  - Simple query() method interface
  - Async query execution
  - Streaming support with query_stream()
  - Session creation for chat-like interactions
  - Comprehensive statistics and monitoring
- Comprehensive test suite
  - Unit tests for all Phase 1 components
  - Unit tests for all Phase 2 components
  - Test fixtures and utilities
  - 90%+ code coverage
- **SSL/TLS support for database connections**
  - Automatic SSL detection from database URL
  - Certificate-based authentication support
  - Database-specific SSL configuration (PostgreSQL, MySQL, SQL Server)
  - Environment variable configuration
  - SSL verification control
  - Comprehensive SSL documentation
- **Test suite fixes and improvements**
  - Fixed connection_manager fixture to use test data
  - Fixed get_pool_status to handle different pool types
  - All 75 tests passing ✅

### Added (Phase 3)
- **Streamlit Demo Application** 🎉
  - Interactive web UI for testing and demonstration
  - Natural language query interface
  - Schema browser with table/column visualization
  - Query history tracking
  - Results visualization (charts)
  - CSV export functionality
  - Session support for conversational queries
  - Statistics dashboard
  - Demo database creation script
  - Comprehensive documentation
  - **Secure credential handling** - Reads from .env file, not UI input
  - Fixed Streamlit deprecation warnings (use_container_width → width)
  - **Instagram-style chat interface** - Chat bubbles, natural responses, collapsible details
  - **Conversational AI layer in core agent** - Handles greetings, help, time/date, casual chat
  - **Smart natural responses in core agent** - Shows actual values for COUNT/single-value queries
  - **Refactored conversational logic** - Moved from UI to agent core for universal access
  - **Fixed session support** - ChatSession now uses conversational layer
  - **Proper memory implementation** - Integrated OpenAI Agents SDK session memory for conversation history
  - **🤖 Simple Multi-Agent System** - 2 agents (Conversational + SQL as tool) for speed
  - **Conversational-first architecture** - All interactions through friendly conversational agent
  - **No SQL jargon** - Users never see SQL queries, only natural language responses
  - **Speed optimized** - 1 LLM call per query (50-60% faster than handoff architecture)
  - **SQL Agent as tool** - Backend worker called by conversational agent when needed
  - **Dynamic tools** - No hardcoded data, all fetched from database
  - **Codebase cleanup** - Removed old complex multi-agent files (10 files deleted)
  - **Fixed Streamlit connection** - Added use_multi_agent=True parameter
  - **Fixed agent initialization** - Store use_multi_agent before _initialize_components()
  - **Fixed SQL Agent schema** - Changed results type from Any to str for OpenAI API compatibility
  - **Pure conversational interface** - Removed View Details section, SQL stays hidden (conversational-first design)
  - **Fixed statistics tracking** - Query stats now update correctly (total, successful, failed, cache hits)
  - **Fixed caching in multi-agent system** - Multi-agent system now uses cache for faster repeated queries
  - **Removed single-agent fallback** - Multi-agent is now the only system (simplified architecture)
  - **Cleaned up unused imports** - Removed AgentIntegration and ConversationalLayer from agent.py
  - **Updated query_stream** - No longer depends on single-agent AgentIntegration

### Added (Phase 4 - Dynamic Configuration & Extensibility) 🚀
- **🎛️ Fully Dynamic Configuration System**
  - All parameters optional - load from `.env` or pass directly
  - `from_env()` class method for easy .env loading with overrides
  - Parameter priority: Direct parameter > .env > Default
  - No hardcoded values - fully customizable
  - Support for 20+ configuration parameters

- **📋 Model Configuration**
  - Configure fast_model, balanced_model, complex_model
  - Set model_strategy (adaptive/fixed)
  - Load from .env: `FAST_MODEL`, `BALANCED_MODEL`, `COMPLEX_MODEL`, `MODEL_STRATEGY`
  - Override in code: `agent = DatabaseQueryAgent.from_env(fast_model="gpt-4.1")`

- **💾 Cache Configuration**
  - Enable/disable caching dynamically
  - Configure cache backend (memory/sqlite/redis)
  - Set TTL for schema, query, and LLM caches
  - Load from .env: `CACHE_ENABLED`, `CACHE_BACKEND`, `CACHE_*_TTL`
  
- **🔒 Safety Configuration**
  - Configure read_only mode
  - Set query timeout and max result rows
  - Load from .env: `READ_ONLY`, `QUERY_TIMEOUT`, `MAX_RESULT_ROWS`

- **🔌 Connection Configuration**
  - Configure pool size and max overflow
  - Load from .env: `DB_POOL_SIZE`, `DB_MAX_OVERFLOW`

- **⚡ Performance Configuration**
  - Configure lazy schema loading, streaming, warmup
  - Load from .env: `LAZY_SCHEMA_LOADING`, `ENABLE_STREAMING`, `WARMUP_ON_INIT`

- **📊 Statistics Configuration**
  - Enable/disable statistics tracking with `enable_statistics` parameter
  - Optional query statistics (no overhead when disabled)
  - Track total queries, success/failure rate, cache hits

- **💬 Session Configuration**
  - Configure session backend (sqlite/memory)
  - Set custom session database path
  - `session_backend` and `session_db_path` parameters

- **🔧 New Utility Methods**
  - `get_session_history(session_id)` - Get conversation history for a session
  - `list_sessions()` - List all active session IDs
  - `get_schema_info(include_foreign_keys=True)` - Detailed schema with relationships
  - `clear_session(session_id)` - Clear session history
  - `delete_session(session_id)` - Delete a session
  - `get_stats()` - Enhanced statistics with optional query stats

- **📦 Enhanced Package Exports**
  - Exposed `ChatSession` in package exports
  - Exposed all config classes: `AgentConfig`, `DatabaseConfig`, `CacheConfig`, `ModelConfig`, `SafetyConfig`
  - Better IDE autocomplete and type hints

- **📚 Comprehensive Documentation**
  - New `USAGE_EXAMPLES.md` with 20+ examples
  - All configuration options documented
  - Flask/FastAPI integration examples
  - Session management examples
  - Statistics and monitoring examples
  - Schema exploration examples

- **🎨 Updated Demo Application**
  - Uses new `from_env()` method
  - Cleaner configuration approach
  - Automatic credential loading from .env

- **✅ Backward Compatibility**
  - All existing code continues to work
  - New features are optional enhancements
  - No breaking changes

### Added (Streaming Support) ⚡
- **🌊 Token-by-Token Streaming** - Real-time response streaming using OpenAI Agents SDK
  - Implemented `query_stream()` method in multi-agent system
  - Uses `Runner.run_streamed()` with `ResponseTextDeltaEvent`
  - Reduces perceived wait time - users see responses as they're generated
  - Fully integrated with caching (cached responses returned instantly)
  - Works with sessions for conversational context
  - **Configurable via parameter, .env, or UI checkbox**
  - `enable_streaming` parameter (default: False - opt-in feature)
  - Load from .env: `ENABLE_STREAMING=true`
  - Streamlit UI: "⚡ Stream" checkbox in query interface
  - Example: `async for chunk in agent.query_stream("question"): print(chunk, end="")`

### Fixed
- **Query History display** - Shows natural response instead of SQL (consistent with conversational-first design)

### Planned
- Streamlit demo UI for testing
- Safety guardrails for input/output validation
- Example integration scripts (Django, Flask, FastAPI)
- Performance benchmarks
- Complete API documentation
- PyPI package release

## [0.1.0] - TBD

### Added
- Initial release
