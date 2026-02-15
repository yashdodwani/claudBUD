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


def update_user_traits(
    user_id: str,
    analysis: Dict[str, Any],
    policy: Dict[str, Any]
) -> bool:
    """
    Update user traits based on behavioral signals.

    Maps signals to personality traits and updates memory summaries.
    Does NOT store raw messages - only behavioral patterns.

    Signal → Trait Mapping:
    - Authority conflict often → avoids_conflict
    - Long venting sessions → needs_validation
    - High intensity anxiety → reassurance_seeking
    - Humor preference → humor_responsive
    - Frequent practical help → solution_oriented

    Args:
        user_id: User identifier
        analysis: Social analysis dict (emotion, relationship, intensity, etc.)
        policy: Behavior policy dict (mode, tone, etc.)

    Returns:
        True if traits updated successfully

    Example:
        >>> update_user_traits(
        ...     user_id="user_123",
        ...     analysis={'primary_emotion': 'anxiety', 'intensity': 8, 'relationship': 'authority'},
        ...     policy={'mode': 'venting_listener', 'humor_level': 0}
        ... )
        True
    """

    users_collection = get_users_collection()

    # Extract signals
    emotion = analysis.get('primary_emotion')
    intensity = analysis.get('intensity', 5)
    relationship = analysis.get('relationship')
    conflict_risk = analysis.get('conflict_risk')
    user_need = analysis.get('user_need')

    mode = policy.get('mode')
    humor_level = policy.get('humor_level', 1)

    # Determine traits from signals
    traits_to_add = []

    # Authority conflict patterns
    if relationship == 'authority' and conflict_risk == 'high':
        traits_to_add.append('avoids_conflict')

    # Venting patterns
    if mode == 'venting_listener' or user_need == 'vent':
        traits_to_add.append('needs_validation')

    # Anxiety patterns
    if emotion in ['anxiety', 'stressed'] and intensity >= 7:
        traits_to_add.append('reassurance_seeking')

    # High anxiety in general
    if emotion == 'anxiety' and intensity >= 8:
        traits_to_add.append('high_anxiety_baseline')

    # Humor responsiveness
    if humor_level >= 2 and emotion in ['boredom', 'neutral', 'happy']:
        traits_to_add.append('humor_responsive')

    # Solution-oriented
    if user_need in ['advice', 'decision_help'] or mode == 'practical_helper':
        traits_to_add.append('solution_oriented')

    # Emotional support needs
    if user_need in ['reassurance', 'validation']:
        traits_to_add.append('needs_emotional_support')

    # Workplace stress patterns
    if relationship == 'authority' and emotion in ['frustration', 'anger', 'anxiety']:
        traits_to_add.append('workplace_stress_prone')

    if not traits_to_add:
        return False

    # Get current profile
    profile = users_collection.find_one({"user_id": user_id})
    if not profile:
        # Create default profile first
        profile = create_default_profile(user_id)
        users_collection.insert_one(profile)

    # Get existing traits
    existing_traits = profile.get('learned_patterns', [])

    # Add new traits (avoid duplicates)
    for trait in traits_to_add:
        if trait not in existing_traits:
            existing_traits.append(trait)

    # Update profile
    users_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "learned_patterns": existing_traits,
                "last_updated": datetime.utcnow()
            }
        }
    )

    # Create memory summary entry (NOT storing raw message)
    memory_entry = {
        "user_id": user_id,
        "timestamp": datetime.utcnow(),
        "traits_identified": traits_to_add,
        "signals": {
            "emotion": emotion,
            "intensity": intensity,
            "relationship": relationship,
            "conflict_risk": conflict_risk,
            "user_need": user_need,
            "mode": mode
        },
        "type": "trait_update"
    }

    # Save to memory_summaries collection
    db = get_users_collection().database
    memory_summaries = db["memory_summaries"]
    memory_summaries.insert_one(memory_entry)

    return True


def get_user_traits(user_id: str) -> list:
    """
    Get learned traits for a user.

    Args:
        user_id: User identifier

    Returns:
        List of learned trait strings
    """

    profile = get_user_profile(user_id)
    if not profile:
        return []

    return profile.get('learned_patterns', [])


def log_interaction(
    user_id: str,
    scenario: str,
    emotion: str,
    mode: str,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Log interaction outcome for adaptive learning.

    Stores interaction patterns to help Buddy learn preferences over time.
    Does NOT store message content - only behavioral metadata.

    Args:
        user_id: User identifier
        scenario: Scenario type (e.g., 'workplace_conflict', 'exam_stress')
        emotion: Detected emotion
        mode: Response mode used (e.g., 'diplomatic_advisor', 'venting_listener')
        metadata: Optional additional data (response_length, humor_used, etc.)

    Returns:
        True if logged successfully

    Example:
        >>> log_interaction(
        ...     user_id="user_123",
        ...     scenario="workplace_conflict",
        ...     emotion="anxiety",
        ...     mode="diplomatic_advisor",
        ...     metadata={'response_length': 'medium', 'humor_level': 0}
        ... )
        True
    """

    users_collection = get_users_collection()

    # Get interactions collection
    db = users_collection.database
    interactions = db["interactions"]

    # Create interaction log entry
    interaction = {
        "user_id": user_id,
        "timestamp": datetime.utcnow(),
        "scenario": scenario,
        "emotion": emotion,
        "mode": mode,
        "metadata": metadata or {},
        "type": "interaction_log"
    }

    # Insert interaction log
    result = interactions.insert_one(interaction)

    # Update user's interaction count (already done in load_user_context, but ensure consistency)
    users_collection.update_one(
        {"user_id": user_id},
        {
            "$inc": {"total_interactions": 1},
            "$set": {"last_interaction": datetime.utcnow()}
        },
        upsert=True
    )

    return result.acknowledged


def get_interaction_stats(user_id: str) -> Dict[str, Any]:
    """
    Get interaction statistics for a user.

    Analyzes past interactions to show learning and adaptation.

    Args:
        user_id: User identifier

    Returns:
        Dict with interaction statistics

    Example:
        >>> stats = get_interaction_stats("user_123")
        >>> print(stats)
        {
            'total_interactions': 47,
            'common_scenarios': ['workplace_conflict', 'exam_stress'],
            'common_emotions': ['anxiety', 'frustration'],
            'preferred_modes': ['diplomatic_advisor', 'venting_listener'],
            'adaptations_learned': [
                'Buddy learned you prefer short replies',
                'Buddy adapted to your workplace stress patterns'
            ]
        }
    """

    users_collection = get_users_collection()
    db = users_collection.database
    interactions = db["interactions"]

    # Get all interactions for user
    user_interactions = list(interactions.find({"user_id": user_id}))

    if not user_interactions:
        return {
            'total_interactions': 0,
            'common_scenarios': [],
            'common_emotions': [],
            'preferred_modes': [],
            'adaptations_learned': []
        }

    # Analyze patterns
    scenarios = {}
    emotions = {}
    modes = {}

    for interaction in user_interactions:
        scenario = interaction.get('scenario', 'unknown')
        emotion = interaction.get('emotion', 'unknown')
        mode = interaction.get('mode', 'unknown')

        scenarios[scenario] = scenarios.get(scenario, 0) + 1
        emotions[emotion] = emotions.get(emotion, 0) + 1
        modes[mode] = modes.get(mode, 0) + 1

    # Get top 3 of each
    common_scenarios = sorted(scenarios.items(), key=lambda x: x[1], reverse=True)[:3]
    common_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
    preferred_modes = sorted(modes.items(), key=lambda x: x[1], reverse=True)[:3]

    # Generate adaptation messages
    adaptations = []

    # Get learned traits
    traits = get_user_traits(user_id)

    if 'avoids_conflict' in traits:
        adaptations.append("Buddy learned you prefer diplomatic approaches")
    if 'needs_validation' in traits:
        adaptations.append("Buddy adapted to validate your emotions first")
    if 'solution_oriented' in traits:
        adaptations.append("Buddy learned you prefer actionable solutions")
    if 'reassurance_seeking' in traits:
        adaptations.append("Buddy provides more reassurance based on your patterns")
    if 'humor_responsive' in traits:
        adaptations.append("Buddy uses appropriate humor when suitable")
    if 'workplace_stress_prone' in traits:
        adaptations.append("Buddy is extra supportive for work-related stress")

    # Check metadata for preferences
    recent_interactions = user_interactions[-10:] if len(user_interactions) > 10 else user_interactions
    response_lengths = [i.get('metadata', {}).get('response_length') for i in recent_interactions if i.get('metadata', {}).get('response_length')]

    if response_lengths:
        from collections import Counter
        most_common_length = Counter(response_lengths).most_common(1)[0][0]
        if most_common_length == 'short':
            adaptations.append("Buddy learned you prefer concise replies")
        elif most_common_length == 'long':
            adaptations.append("Buddy learned you appreciate detailed responses")

    return {
        'total_interactions': len(user_interactions),
        'common_scenarios': [s[0] for s in common_scenarios],
        'common_emotions': [e[0] for e in common_emotions],
        'preferred_modes': [m[0] for m in preferred_modes],
        'adaptations_learned': adaptations
    }


