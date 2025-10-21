"""Database connection management with pooling."""

from typing import Any, List, Tuple
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from db_query_agent.exceptions import ConnectionError, QueryExecutionError
from db_query_agent.config import DatabaseConfig
import logging
import asyncio

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages database connections with pooling."""
    
    def __init__(self, config: DatabaseConfig):
        """
        Initialize connection manager.
        
        Args:
            config: Database configuration
        """
        self.config = config
        self._engine: Engine = None
        self._create_engine()
    
    def _create_engine(self) -> None:
        """Create SQLAlchemy engine with connection pooling."""
        try:
            self._engine = create_engine(
                self.config.url,
                poolclass=QueuePool,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                pool_pre_ping=True,  # Verify connections before using
                echo=False
            )
            logger.info(f"Database engine created: {self._engine.dialect.name}")
        except Exception as e:
            logger.error(f"Failed to create database engine: {e}")
            raise ConnectionError(f"Failed to create database engine: {e}")
    
    @property
    def engine(self) -> Engine:
        """Get SQLAlchemy engine."""
        if self._engine is None:
            self._create_engine()
        return self._engine
    
    def execute_query(
        self,
        sql: str,
        timeout: int = 30
    ) -> List[Tuple[Any, ...]]:
        """
        Execute SQL query and return results.
        
        Args:
            sql: SQL query to execute
            timeout: Query timeout in seconds
            
        Returns:
            List of result tuples
        """
        try:
            with self.engine.connect() as conn:
                # Set query timeout
                result = conn.execute(
                    text(sql),
                    execution_options={"timeout": timeout}
                )
                
                # Fetch all results
                rows = result.fetchall()
                logger.debug(f"Query executed successfully: {len(rows)} rows returned")
                return rows
                
        except SQLAlchemyError as e:
            logger.error(f"Query execution failed: {e}")
            raise QueryExecutionError(f"Query execution failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {e}")
            raise QueryExecutionError(f"Unexpected error: {e}")
    
    async def execute_query_async(
        self,
        sql: str,
        timeout: int = 30
    ) -> List[Tuple[Any, ...]]:
        """
        Execute SQL query asynchronously.
        
        Args:
            sql: SQL query to execute
            timeout: Query timeout in seconds
            
        Returns:
            List of result tuples
        """
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.execute_query,
            sql,
            timeout
        )
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            True if connection successful
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def close(self) -> None:
        """Close all database connections."""
        if self._engine:
            self._engine.dispose()
            logger.info("Database connections closed")
    
    def get_pool_status(self) -> dict:
        """Get connection pool status."""
        if not self._engine:
            return {}
        
        pool = self._engine.pool
        return {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "total": pool.size() + pool.overflow()
        }
