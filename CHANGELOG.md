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
