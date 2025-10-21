"""
db-query-agent: AI-powered natural language database query system.

A Python package that enables natural language querying of databases using OpenAI Agents SDK.
"""

from db_query_agent.agent import DatabaseQueryAgent
from db_query_agent.exceptions import (
    DatabaseQueryAgentError,
    ValidationError,
    QueryExecutionError,
    SchemaExtractionError,
)

__version__ = "0.1.0"
__all__ = [
    "DatabaseQueryAgent",
    "DatabaseQueryAgentError",
    "ValidationError",
    "QueryExecutionError",
    "SchemaExtractionError",
]
