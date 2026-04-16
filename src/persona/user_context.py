"""
User Context Management

Loads and manages user profiles and memory for personalized responses.
Uses PostgreSQL via SQLAlchemy (Neon DB).
"""

from typing import Dict, Optional, Any
from datetime import datetime
from .db import get_db_session
from .models import User, Memory, Interaction, MemorySummary


def load_user_context(user_id: str) -> dict:
    """
    Load user context from PostgreSQL.

    Fetches user profile and recent memory summary.
    Creates a default profile if the user doesn't exist.

    Args:
        user_id: Unique user identifier

    Returns:
        Compact dict usable in prompts with preferences, memory_summary, etc.
    """
    session = get_db_session()
    if session is None:
        return create_default_profile(user_id)

    try:
        user = session.query(User).filter_by(user_id=user_id).first()

        if not user:
            profile = create_default_profile(user_id)
            user = User(
                user_id=user_id,
                created_at=profile["created_at"],
                last_interaction=profile["last_interaction"],
                interaction_count=0,
                humor_level=profile["preferences"]["humor_level"],
                response_length=profile["preferences"]["response_length"],
                formality=profile["preferences"]["formality"],
                language_mix=profile["preferences"]["language_mix"],
                emoji_usage=profile["preferences"]["emoji_usage"],
                communication_style=profile["communication_style"],
                learned_patterns=profile["learned_patterns"],
                topics_of_interest=profile["topics_of_interest"],
                emotional_baseline=profile["emotional_baseline"],
            )
            session.add(user)
            session.commit()
            session.refresh(user)

        memory_summary = _get_memory_summary(user_id, session)

        context = {
            "user_id": user_id,
            "preferences": {
                "humor_level": user.humor_level,
                "response_length": user.response_length,
                "formality": user.formality,
                "language_mix": user.language_mix,
                "emoji_usage": user.emoji_usage,
            },
            "communication_style": user.communication_style,
            "memory_summary": memory_summary,
            "interaction_count": user.interaction_count,
            "created_at": user.created_at,
            "last_interaction": user.last_interaction,
        }

        # Update last interaction timestamp
        user.last_interaction = datetime.utcnow()
        user.interaction_count = (user.interaction_count or 0) + 1
        session.commit()

        return context

    except Exception as e:
        print(f"Warning: Could not load user context: {e}")
        session.rollback()
        return create_default_profile(user_id)
    finally:
        session.close()


def create_default_profile(user_id: str) -> dict:
    """
    Create default user profile dict (not persisted).

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
            "humor_level": "medium",
            "response_length": "medium",
            "formality": "casual",
            "language_mix": "hinglish",
            "emoji_usage": "moderate",
        },
        "communication_style": "casual",
        "learned_patterns": [],
        "topics_of_interest": [],
        "emotional_baseline": "neutral",
    }


def _get_memory_summary(user_id: str, session) -> str:
    """
    Build compact memory summary string from recent memories.

    Args:
        user_id: User identifier
        session: Active SQLAlchemy session

    Returns:
        Summary string of recent learnings
    """
    recent_memories = (
        session.query(Memory)
        .filter_by(user_id=user_id)
        .order_by(Memory.timestamp.desc())
        .limit(5)
        .all()
    )

    if not recent_memories:
        return "New user - no previous interactions"

    summary_parts = []
    for memory in recent_memories:
        if memory.pattern:
            summary_parts.append(f"- {memory.pattern}")
        elif memory.observation:
            summary_parts.append(f"- {memory.observation}")

    if summary_parts:
        return "\n".join(summary_parts)
    return "Building understanding of user preferences"


def get_memory_summary(user_id: str, _ignored=None) -> str:
    """
    Public wrapper for memory summary (session managed internally).

    Args:
        user_id: User identifier
        _ignored: Kept for API compatibility (was MongoDB collection)

    Returns:
        Summary string
    """
    session = get_db_session()
    if session is None:
        return "New user - no previous interactions"
    try:
        return _get_memory_summary(user_id, session)
    finally:
        session.close()


def update_user_preferences(user_id: str, preferences: Dict[str, Any]) -> bool:
    """
    Update user preferences.

    Args:
        user_id: User identifier
        preferences: Dict with keys matching preference columns

    Returns:
        True if updated successfully
    """
    session = get_db_session()
    if session is None:
        return False

    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            return False

        if "humor_level" in preferences:
            user.humor_level = preferences["humor_level"]
        if "response_length" in preferences:
            user.response_length = preferences["response_length"]
        if "formality" in preferences:
            user.formality = preferences["formality"]
        if "language_mix" in preferences:
            user.language_mix = preferences["language_mix"]
        if "emoji_usage" in preferences:
            user.emoji_usage = preferences["emoji_usage"]

        session.commit()
        return True
    except Exception as e:
        print(f"Error updating preferences: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def save_memory(
    user_id: str,
    memory_type: str,
    content: str,
    metadata: Optional[Dict] = None,
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
    session = get_db_session()
    if session is None:
        return False

    try:
        memory = Memory(
            user_id=user_id,
            type=memory_type,
            content=content,
            timestamp=datetime.utcnow(),
            extra_metadata=metadata or {},
        )
        if memory_type == "pattern":
            memory.pattern = content
        elif memory_type == "observation":
            memory.observation = content

        session.add(memory)
        session.commit()
        return True
    except Exception as e:
        print(f"Error saving memory: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def get_user_profile(user_id: str) -> Optional[Dict]:
    """
    Get full user profile as a dict.

    Args:
        user_id: User identifier

    Returns:
        User profile dict or None if not found
    """
    session = get_db_session()
    if session is None:
        return None

    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            return None
        return {
            "user_id": user.user_id,
            "created_at": user.created_at,
            "last_interaction": user.last_interaction,
            "interaction_count": user.interaction_count,
            "total_interactions": user.total_interactions,
            "preferences": {
                "humor_level": user.humor_level,
                "response_length": user.response_length,
                "formality": user.formality,
                "language_mix": user.language_mix,
                "emoji_usage": user.emoji_usage,
            },
            "communication_style": user.communication_style,
            "learned_patterns": user.learned_patterns or [],
            "topics_of_interest": user.topics_of_interest or [],
            "emotional_baseline": user.emotional_baseline,
        }
    finally:
        session.close()


def update_user_traits(
    user_id: str,
    analysis: Dict[str, Any],
    policy: Dict[str, Any],
) -> bool:
    """
    Update user traits based on behavioral signals.

    Maps signals to personality traits and stores memory summaries.
    Does NOT store raw messages - only behavioral patterns.

    Args:
        user_id: User identifier
        analysis: Social analysis dict (emotion, relationship, intensity, etc.)
        policy: Behavior policy dict (mode, tone, etc.)

    Returns:
        True if traits updated successfully
    """
    session = get_db_session()
    if session is None:
        print("Warning: PostgreSQL unavailable, cannot update traits")
        return False

    try:
        emotion = analysis.get("primary_emotion")
        intensity = analysis.get("intensity", 5)
        relationship = analysis.get("relationship")
        conflict_risk = analysis.get("conflict_risk")
        user_need = analysis.get("user_need")
        mode = policy.get("mode")
        humor_level = policy.get("humor_level", 1)

        traits_to_add = []

        if relationship == "authority" and conflict_risk == "high":
            traits_to_add.append("avoids_conflict")
        if mode == "venting_listener" or user_need == "vent":
            traits_to_add.append("needs_validation")
        if emotion in ["anxiety", "stressed"] and intensity >= 7:
            traits_to_add.append("reassurance_seeking")
        if emotion == "anxiety" and intensity >= 8:
            traits_to_add.append("high_anxiety_baseline")
        if humor_level >= 2 and emotion in ["boredom", "neutral", "happy"]:
            traits_to_add.append("humor_responsive")
        if user_need in ["advice", "decision_help"] or mode == "practical_helper":
            traits_to_add.append("solution_oriented")
        if user_need in ["reassurance", "validation"]:
            traits_to_add.append("needs_emotional_support")
        if relationship == "authority" and emotion in ["frustration", "anger", "anxiety"]:
            traits_to_add.append("workplace_stress_prone")

        if not traits_to_add:
            return False

        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            profile = create_default_profile(user_id)
            user = User(
                user_id=user_id,
                created_at=profile["created_at"],
                last_interaction=profile["last_interaction"],
            )
            session.add(user)
            session.flush()

        existing_traits = list(user.learned_patterns or [])
        for trait in traits_to_add:
            if trait not in existing_traits:
                existing_traits.append(trait)

        user.learned_patterns = existing_traits
        user.last_updated = datetime.utcnow()

        # Save memory summary
        summary = MemorySummary(
            user_id=user_id,
            timestamp=datetime.utcnow(),
            traits_identified=traits_to_add,
            signals={
                "emotion": emotion,
                "intensity": intensity,
                "relationship": relationship,
                "conflict_risk": conflict_risk,
                "user_need": user_need,
                "mode": mode,
            },
            type="trait_update",
        )
        session.add(summary)
        session.commit()
        return True

    except Exception as e:
        print(f"Error updating user traits: {e}")
        session.rollback()
        return False
    finally:
        session.close()


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
    return profile.get("learned_patterns", [])


def log_interaction(
    user_id: str,
    scenario: str,
    emotion: str,
    mode: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Log interaction outcome for adaptive learning.

    Stores interaction patterns (NOT message content) for adaptation.

    Args:
        user_id: User identifier
        scenario: Scenario type (e.g., 'workplace_conflict', 'exam_stress')
        emotion: Detected emotion
        mode: Response mode used
        metadata: Optional additional data

    Returns:
        True if logged successfully
    """
    session = get_db_session()
    if session is None:
        print("Warning: PostgreSQL unavailable, cannot log interaction")
        return False

    try:
        interaction = Interaction(
            user_id=user_id,
            timestamp=datetime.utcnow(),
            scenario=scenario,
            emotion=emotion,
            mode=mode,
            extra_metadata=metadata or {},
            type="interaction_log",
        )
        session.add(interaction)

        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.total_interactions = (user.total_interactions or 0) + 1
            user.last_interaction = datetime.utcnow()
        else:
            # upsert
            profile = create_default_profile(user_id)
            new_user = User(
                user_id=user_id,
                created_at=profile["created_at"],
                last_interaction=datetime.utcnow(),
                total_interactions=1,
            )
            session.add(new_user)

        session.commit()
        return True
    except Exception as e:
        print(f"Error logging interaction: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def get_interaction_stats(user_id: str) -> Dict[str, Any]:
    """
    Get interaction statistics for a user.

    Args:
        user_id: User identifier

    Returns:
        Dict with interaction statistics and adaptation messages
    """
    session = get_db_session()
    if session is None:
        return {
            "total_interactions": 0,
            "common_scenarios": [],
            "common_emotions": [],
            "preferred_modes": [],
            "adaptations_learned": [],
        }

    try:
        user_interactions = (
            session.query(Interaction).filter_by(user_id=user_id).all()
        )

        if not user_interactions:
            return {
                "total_interactions": 0,
                "common_scenarios": [],
                "common_emotions": [],
                "preferred_modes": [],
                "adaptations_learned": [],
            }

        scenarios: Dict[str, int] = {}
        emotions: Dict[str, int] = {}
        modes: Dict[str, int] = {}

        for interaction in user_interactions:
            s = interaction.scenario or "unknown"
            e = interaction.emotion or "unknown"
            m = interaction.mode or "unknown"
            scenarios[s] = scenarios.get(s, 0) + 1
            emotions[e] = emotions.get(e, 0) + 1
            modes[m] = modes.get(m, 0) + 1

        common_scenarios = sorted(scenarios.items(), key=lambda x: x[1], reverse=True)[:3]
        common_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
        preferred_modes = sorted(modes.items(), key=lambda x: x[1], reverse=True)[:3]

        adaptations = []
        traits = get_user_traits(user_id)

        if "avoids_conflict" in traits:
            adaptations.append("Buddy learned you prefer diplomatic approaches")
        if "needs_validation" in traits:
            adaptations.append("Buddy adapted to validate your emotions first")
        if "solution_oriented" in traits:
            adaptations.append("Buddy learned you prefer actionable solutions")
        if "reassurance_seeking" in traits:
            adaptations.append("Buddy provides more reassurance based on your patterns")
        if "humor_responsive" in traits:
            adaptations.append("Buddy uses appropriate humor when suitable")
        if "workplace_stress_prone" in traits:
            adaptations.append("Buddy is extra supportive for work-related stress")

        recent = user_interactions[-10:] if len(user_interactions) > 10 else user_interactions
        response_lengths = [
            i.extra_metadata.get("response_length")
            for i in recent
            if i.extra_metadata and i.extra_metadata.get("response_length")
        ]
        if response_lengths:
            from collections import Counter
            most_common = Counter(response_lengths).most_common(1)[0][0]
            if most_common == "short":
                adaptations.append("Buddy learned you prefer concise replies")
            elif most_common == "long":
                adaptations.append("Buddy learned you appreciate detailed responses")

        return {
            "total_interactions": len(user_interactions),
            "common_scenarios": [s[0] for s in common_scenarios],
            "common_emotions": [e[0] for e in common_emotions],
            "preferred_modes": [m[0] for m in preferred_modes],
            "adaptations_learned": adaptations,
        }
    finally:
        session.close()
