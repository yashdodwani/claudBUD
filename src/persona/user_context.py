"""
User Context Management

Loads and manages user profiles and memory for personalized responses.
"""

import os
from typing import Dict, Optional, Any
from datetime import datetime
from dotenv import load_dotenv
from .db import get_users_collection, get_memories_collection

# Load environment variables from .env
load_dotenv()


def load_user_context(user_id: str) -> dict:
    """
    Load user context from MongoDB.

    Fetches:
    - User profile (preferences, communication style)
    - Memory summary (recent interactions, learned patterns)

    If user doesn't exist, creates default profile.

    Args:
        user_id: Unique user identifier

    Returns:
        Compact dict usable in prompts with:
        - user_id
        - preferences (response style, humor level, etc.)
        - communication_style
        - memory_summary (recent learnings)
        - interaction_count
        - created_at
        - last_interaction

    Example:
        >>> context = load_user_context("user_123")
        >>> print(context['preferences']['humor_level'])  # 'medium'
        >>> print(context['memory_summary'])  # Recent patterns
    """

    users_collection = get_users_collection()
    memories_collection = get_memories_collection()

    # Try to fetch user profile
    user_profile = users_collection.find_one({"user_id": user_id})

    # If user doesn't exist, create default profile
    if not user_profile:
        user_profile = create_default_profile(user_id)
        users_collection.insert_one(user_profile)

    # Fetch memory summary
    memory_summary = get_memory_summary(user_id, memories_collection)

    # Build compact context for prompts
    context = {
        "user_id": user_id,
        "preferences": user_profile.get("preferences", {}),
        "communication_style": user_profile.get("communication_style", "casual"),
        "memory_summary": memory_summary,
        "interaction_count": user_profile.get("interaction_count", 0),
        "created_at": user_profile.get("created_at"),
        "last_interaction": user_profile.get("last_interaction")
    }

    # Update last interaction timestamp
    users_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {"last_interaction": datetime.utcnow()},
            "$inc": {"interaction_count": 1}
        }
    )

    return context


def create_default_profile(user_id: str) -> dict:
    """
    Create default user profile.

    Args:
        user_id: User identifier

    Returns:
        Default profile dict
    """
    now = datetime.utcnow()

    return {
        "user_id": user_id,
        "created_at": now,
        "last_interaction": now,
        "interaction_count": 0,
        "preferences": {
            "humor_level": "medium",  # low, medium, high
            "response_length": "medium",  # short, medium, long
            "formality": "casual",  # casual, balanced, formal
            "language_mix": "hinglish",  # hindi, hinglish, english
            "emoji_usage": "moderate"  # none, minimal, moderate, high
        },
        "communication_style": "casual",
        "learned_patterns": [],
        "topics_of_interest": [],
        "emotional_baseline": "neutral"
    }


def get_memory_summary(user_id: str, memories_collection) -> str:
    """
    Get compact memory summary for user.

    Retrieves recent memories and learned patterns.

    Args:
        user_id: User identifier
        memories_collection: MongoDB memories collection

    Returns:
        Compact string summary of recent learnings
    """

    # Fetch recent memories (last 5)
    recent_memories = list(
        memories_collection.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(5)
    )

    if not recent_memories:
        return "New user - no previous interactions"

    # Build compact summary
    summary_parts = []

    for memory in recent_memories:
        if "pattern" in memory:
            summary_parts.append(f"- {memory['pattern']}")
        elif "observation" in memory:
            summary_parts.append(f"- {memory['observation']}")

    if summary_parts:
        return "\n".join(summary_parts)
    else:
        return "Building understanding of user preferences"


def update_user_preferences(
    user_id: str,
    preferences: Dict[str, Any]
) -> bool:
    """
    Update user preferences.

    Args:
        user_id: User identifier
        preferences: Dict of preferences to update

    Returns:
        True if updated successfully
    """

    users_collection = get_users_collection()

    result = users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"preferences": preferences}}
    )

    return result.modified_count > 0


def save_memory(
    user_id: str,
    memory_type: str,
    content: str,
    metadata: Optional[Dict] = None
) -> bool:
    """
    Save a memory/learning about the user.

    Args:
        user_id: User identifier
        memory_type: Type of memory (pattern, preference, observation)
        content: Memory content
        metadata: Optional additional metadata

    Returns:
        True if saved successfully
    """

    memories_collection = get_memories_collection()

    memory = {
        "user_id": user_id,
        "type": memory_type,
        "content": content,
        "timestamp": datetime.utcnow(),
        "metadata": metadata or {}
    }

    if memory_type == "pattern":
        memory["pattern"] = content
    elif memory_type == "observation":
        memory["observation"] = content

    result = memories_collection.insert_one(memory)

    return result.acknowledged


def get_user_profile(user_id: str) -> Optional[Dict]:
    """
    Get full user profile.

    Args:
        user_id: User identifier

    Returns:
        User profile dict or None if not found
    """

    users_collection = get_users_collection()
    return users_collection.find_one({"user_id": user_id})

