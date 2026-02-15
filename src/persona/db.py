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

        # Connect with proper configuration for MongoDB Atlas
        # Use certifi for SSL certificates to avoid handshake issues
        try:
            import certifi

            cls._client = MongoClient(
                uri,
                tlsCAFile=certifi.where(),  # Use certifi certificates
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )

            # Test connection
            cls._client.admin.command('ping')
            print("[MongoDB] Successfully connected to MongoDB Atlas!")

        except Exception as e:
            print(f"MongoDB connection error: {e}")
            # Don't raise - let app work without MongoDB
            cls._client = None
            cls._db = None
            return None

        # Try to get database from URI, otherwise use default name
        if cls._client:
            try:
                cls._db = cls._client.get_database()  # Uses default database from URI
            except Exception as e:
                print(f"Database selection error: {e}")
                # If no database in URI, use default name
                try:
                    cls._db = cls._client["buddy_ai"]
                except Exception as e:
                    print(f"Failed to create default database: {e}")
                    cls._client = None
                    cls._db = None
                    return None

        return cls._db

    @classmethod
    def get_db(cls) -> Database:
        """Get database instance (connects if not already connected)"""
        if cls._db is None:
            cls.connect()
        return cls._db

    @classmethod
    def get_collection(cls, collection_name: str) -> Optional[Collection]:
        """Get a specific collection"""
        db = cls.get_db()
        if db is None:
            return None
        return db[collection_name]

    @classmethod
    def close(cls):
        """Close MongoDB connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None


def get_users_collection() -> Optional[Collection]:
    """Get users collection"""
    return MongoDB.get_collection("users")


def get_memories_collection() -> Optional[Collection]:
    """Get memories collection"""
    return MongoDB.get_collection("memories")


def get_conversations_collection() -> Optional[Collection]:
    """Get conversations collection"""
    return MongoDB.get_collection("conversations")

