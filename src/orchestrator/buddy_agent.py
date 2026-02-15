"""
Buddy Agent Orchestrator

Main entry point that coordinates all modules.
This is what the frontend calls for every interaction.
"""

import os
import sys
from typing import Dict, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import all modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from extractors import analyze_social_context
from policy_engine import generate_behavior_policy
from rag import find_relevant_knowledge
from composer import generate_reply


def buddy_chat(
    user_id: str,
    user_input: str,
    source: str = "text",
    meta: Optional[Dict[str, Any]] = None
) -> dict:
    """
    Main orchestrator function for Buddy AI.

    This is the SINGLE entry point that coordinates all modules:
    1. Load user memory
    2. Preprocess input (WhatsApp if needed)
    3. Extract signals
    4. Decide behavior policy
    5. Retrieve cultural knowledge
    6. Generate response WITH memory AND context
    7. Update learned traits
    8. Log interaction
    9. Return response + adaptation message

    Args:
        user_id: Unique user identifier
        user_input: User's message (or WhatsApp chat export)
        source: "text" or "whatsapp"
        meta: Optional context metadata (city, place, time, event)
              Example: {"city": "Bangalore", "place": "railway_station", "time": "evening"}

    Returns:
        Dict with:
        - reply: Generated response text
        - mode: Response mode used
        - emotion: Detected emotion
        - learning: Latest adaptation learned (or None)
        - error: Error message if something failed (or None)

    Example:
        >>> result = buddy_chat(
        ...     user_id="user_123",
        ...     user_input="Bhai train chut gayi",
        ...     source="text",
        ...     meta={"city": "Bangalore", "place": "railway_station", "time": "evening"}
        ... )
        >>> print(result['reply'])  # Context-aware response about Bangalore trains
        >>> print(result['learning'])  # "Buddy learned you avoid confrontation"
    """

    try:
        # Initialize meta if not provided
        if meta is None:
            meta = {}

        # Step 4 (Optional): Smart context inference from message
        if not meta.get('place'):
            message_lower = user_input.lower()

            # Infer place type from keywords
            if any(word in message_lower for word in ['train', 'railway', 'platform', 'metro']):
                meta['place'] = 'transit'
            elif any(word in message_lower for word in ['office', 'boss', 'manager', 'meeting', 'work']):
                meta['place'] = 'workplace'
            elif any(word in message_lower for word in ['exam', 'test', 'college', 'university', 'class']):
                meta['place'] = 'educational'
            elif any(word in message_lower for word in ['airport', 'flight']):
                meta['place'] = 'airport'
            elif any(word in message_lower for word in ['hospital', 'doctor']):
                meta['place'] = 'hospital'

        # Step 1: Load user memory context
        context = None
        memory = None

        # Check if MongoDB is available
        if os.getenv("MONGO_URI"):
            try:
                from persona import (
                    load_user_context,
                    update_user_traits,
                    log_interaction,
                    get_interaction_stats
                )

                context = load_user_context(user_id)
                memory = {
                    'learned_patterns': context.get('learned_patterns', []),
                    'interaction_count': context.get('interaction_count', 0)
                }
                mongodb_available = True
            except Exception as e:
                print(f"Warning: MongoDB unavailable - {e}")
                mongodb_available = False
        else:
            mongodb_available = False

        # Step 2: Preprocess input (WhatsApp if needed)
        if source == "whatsapp":
            try:
                from whatsapp import parse_whatsapp_chat
                analysis_text = parse_whatsapp_chat(user_input)
                if not analysis_text:
                    analysis_text = user_input  # Fallback to raw
            except Exception as e:
                print(f"Warning: WhatsApp parsing failed - {e}")
                analysis_text = user_input
        else:
            analysis_text = user_input

        # Step 3: Extract signals
        analysis = analyze_social_context(analysis_text)

        # Step 4: Generate behavior policy
        policy = generate_behavior_policy({
            "user_message": user_input,
            "emotion": analysis.primary_emotion,
            "relationship": analysis.relationship,
            "conflict_risk": analysis.conflict_risk,
            "user_need": analysis.user_need,
            "intensity": analysis.intensity
        })

        # Step 5: Retrieve RAG knowledge
        knowledge = find_relevant_knowledge(user_input, analysis.model_dump())

        # Step 6: Generate response WITH memory AND context
        response = generate_reply(
            user_input=user_input,
            analysis=analysis,
            policy=policy,
            rag_knowledge=knowledge,
            memory=memory,  # Memory injection for consistency!
            meta=meta  # Real-world context injection!
        )

        # Step 7 & 8: Update traits and log interaction (if MongoDB available)
        learning_message = None

        if mongodb_available:
            try:
                # Update learned traits
                update_user_traits(
                    user_id=user_id,
                    analysis=analysis.model_dump(),
                    policy=policy.model_dump()
                )

                # Log interaction
                log_interaction(
                    user_id=user_id,
                    scenario=knowledge.get('scenario', 'unknown') if knowledge else 'unknown',
                    emotion=analysis.primary_emotion,
                    mode=policy.mode,
                    metadata={
                        'response_length': policy.message_length,
                        'humor_level': policy.humor_level,
                        'source': source
                    }
                )

                # Get adaptation message (Step C: Adaptation Reveal)
                stats = get_interaction_stats(user_id)
                if stats.get('adaptations_learned'):
                    learning_message = stats['adaptations_learned'][-1]

            except Exception as e:
                print(f"Warning: Learning/logging failed - {e}")

        # Step 9: Return complete response
        return {
            "reply": response,
            "mode": policy.mode,
            "emotion": analysis.primary_emotion,
            "intensity": analysis.intensity,
            "relationship": analysis.relationship,
            "learning": learning_message,
            "error": None
        }

    except Exception as e:
        # Step D: Stability Patch - NEVER crash during demo!
        print(f"ERROR in buddy_chat: {e}")
        import traceback
        traceback.print_exc()

        # Return safe fallback response
        return {
            "reply": "Hey, I'm here for you. What's going on?",
            "mode": "chill_companion",
            "emotion": "neutral",
            "intensity": 5,
            "relationship": "friend",
            "learning": None,
            "error": str(e)
        }


def buddy_chat_simple(user_id: str, user_input: str) -> str:
    """
    Simplified interface that just returns the reply text.

    Args:
        user_id: User identifier
        user_input: User's message

    Returns:
        Reply text
    """
    result = buddy_chat(user_id, user_input)
    return result['reply']

