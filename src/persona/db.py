"""
PostgreSQL Connection Module

Handles database connections for user persona and memory storage.
Uses SQLAlchemy with Neon DB (PostgreSQL).
"""

import os
from typing import Optional
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()


def _clean_db_url(url: str) -> str:
    """
    Strip connection params unsupported by psycopg2 (e.g. channel_binding).
    Keeps sslmode and other valid params.
    """
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    params.pop("channel_binding", None)
    new_query = urlencode({k: v[0] for k, v in params.items()})
    return urlunparse(parsed._replace(query=new_query))


class PostgresDB:
    """PostgreSQL connection manager (singleton)"""

    _engine = None
    _SessionLocal = None

    @classmethod
    def connect(cls, db_url: Optional[str] = None):
        """
        Connect to PostgreSQL and set up session factory.

        Args:
            db_url: PostgreSQL connection URL (reads DATABASE_URL from env if None)
        """
        if cls._engine is not None:
            return cls._engine

        url = db_url or os.getenv("DATABASE_URL")
        if not url:
            raise ValueError("DATABASE_URL not found in environment")

        url = _clean_db_url(url)

        try:
            cls._engine = create_engine(
                url,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
            )
            # Test connection
            with cls._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("[PostgreSQL] Successfully connected to Neon DB!")
            cls._SessionLocal = sessionmaker(
                bind=cls._engine, autocommit=False, autoflush=False
            )
        except Exception as e:
            print(f"PostgreSQL connection error: {e}")
            cls._engine = None
            cls._SessionLocal = None
            return None

        return cls._engine

    @classmethod
    def get_session(cls) -> Optional[Session]:
        """Get a new database session (caller must close it)"""
        if cls._SessionLocal is None:
            cls.connect()
        if cls._SessionLocal is None:
            return None
        return cls._SessionLocal()

    @classmethod
    def close(cls):
        """Dispose engine and clear state"""
        if cls._engine:
            cls._engine.dispose()
            cls._engine = None
            cls._SessionLocal = None


def get_db_session() -> Optional[Session]:
    """Convenience function to get a database session"""
    return PostgresDB.get_session()
