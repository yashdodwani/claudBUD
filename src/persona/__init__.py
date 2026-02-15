"""Persona module for user context and memory management"""

from .db import MongoDB, get_users_collection, get_memories_collection, get_conversations_collection
from .user_context import (
    load_user_context,
    create_default_profile,
    get_memory_summary,
    update_user_preferences,
    save_memory,
    get_user_profile
)

__all__ = [
    "MongoDB",
    "get_users_collection",
    "get_memories_collection",
    "get_conversations_collection",
    "load_user_context",
    "create_default_profile",
    "update_user_preferences",
    "save_memory",
    "get_user_profile"
]

