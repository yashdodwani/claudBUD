"""
MongoDB Connection Module

Handles database connections for user persona and memory storage.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

# Load environment variables from .env
load_dotenv()


class MongoDB:
    """MongoDB connection manager"""

    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None

    @classmethod
    def connect(cls, mongo_uri: Optional[str] = None) -> Database:
        """
        Connect to MongoDB and return database instance.

        Args:
            mongo_uri: MongoDB connection string (if None, reads from MONGO_URI env var)

        Returns:
            MongoDB database instance

        Raises:
            ValueError: If MONGO_URI not found
        """
        if cls._db is not None:
            return cls._db

        # Get MongoDB URI
        uri = mongo_uri or os.getenv("MONGO_URI")
        if not uri:
            raise ValueError("MONGO_URI not found in environment")

        # Connect
        cls._client = MongoClient(uri)

        # Try to get database from URI, otherwise use default name
        try:
            cls._db = cls._client.get_database()  # Uses default database from URI
        except:
            # If no database in URI, use default name
            cls._db = cls._client["buddy_ai"]

        return cls._db

    @classmethod
    def get_db(cls) -> Database:
        """Get database instance (connects if not already connected)"""
        if cls._db is None:
            cls.connect()
        return cls._db

    @classmethod
    def get_collection(cls, collection_name: str) -> Collection:
        """Get a specific collection"""
        db = cls.get_db()
        return db[collection_name]

    @classmethod
    def close(cls):
        """Close MongoDB connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None


def get_users_collection() -> Collection:
    """Get users collection"""
    return MongoDB.get_collection("users")


def get_memories_collection() -> Collection:
    """Get memories collection"""
    return MongoDB.get_collection("memories")


def get_conversations_collection() -> Collection:
    """Get conversations collection"""
    return MongoDB.get_collection("conversations")

