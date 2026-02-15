"""
Chat Router for Buddy AI

Exposes 3 clean endpoints:
- POST /chat - Normal conversation
- POST /chat/whatsapp - WhatsApp import
- GET /chat/learning/{user_id} - Learning insights
"""

import sys
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Setup path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import orchestrator
from orchestrator import buddy_chat

# Import stats function
try:
    from persona import get_interaction_stats
    mongodb_available = True
except:
    mongodb_available = False


# Request/Response Models
class ChatRequest(BaseModel):
    user_id: str
    message: str
    meta: Optional[Dict[str, Any]] = None  # Optional context: city, place, time, event


class WhatsAppChatRequest(BaseModel):
    user_id: str
    chat_text: str
    meta: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    reply: str
    mode: str
    emotion: str
    intensity: int
    relationship: str
    learning: Optional[str] = None
    error: Optional[str] = None


class LearningResponse(BaseModel):
    user_id: str
    total_interactions: int
    traits: List[str]
    common_scenarios: List[str]
    common_emotions: List[str]
    adaptations_learned: List[str]


# Create router
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for normal conversation.

    Example:
        POST /chat
        {
            "user_id": "demo_user",
            "message": "Bhai train late ho gayi",
            "meta": {
                "city": "Bangalore",
                "place": "railway_station",
                "time": "evening"
            }
        }

    Returns:
        {
            "reply": "...",
            "mode": "chill_companion",
            "emotion": "frustration",
            "learning": "Buddy learned you prefer short replies"
        }
    """
    try:
        result = buddy_chat(
            user_id=request.user_id,
            user_input=request.message,
            source="text",
            meta=request.meta  # Pass context metadata
        )
        return ChatResponse(**result)

    except Exception as e:
        # Never crash - return safe fallback
        return ChatResponse(
            reply="Hey, I'm here for you. What's going on?",
            mode="chill_companion",
            emotion="neutral",
            intensity=5,
            relationship="friend",
            learning=None,
            error=str(e)
        )


@router.post("/whatsapp", response_model=ChatResponse)
async def chat_whatsapp(request: WhatsAppChatRequest):
    """
    WhatsApp chat import endpoint.

    Analyzes WhatsApp chat export and generates response based on patterns.

    Example:
        POST /chat/whatsapp
        {
            "user_id": "demo_user",
            "chat_text": "12/01/2024, 10:30 - Boss: Need report\n...",
            "meta": {
                "city": "Mumbai",
                "time": "morning"
            }
        }

    Returns same format as normal chat endpoint.
    """
    try:
        result = buddy_chat(
            user_id=request.user_id,
            user_input=request.chat_text,
            source="whatsapp",
            meta=request.meta  # Pass context metadata
        )
        return ChatResponse(**result)

    except Exception as e:
        return ChatResponse(
            reply="I couldn't fully analyze the WhatsApp chat, but I'm here to help. What's the main issue?",
            mode="chill_companion",
            emotion="neutral",
            intensity=5,
            relationship="unknown",
            learning=None,
            error=str(e)
        )


@router.get("/learning/{user_id}", response_model=LearningResponse)
async def get_learning_insights(user_id: str):
    """
    Get learning insights for a user.

    Shows what Buddy has learned about the user over time.
    This is the DEMO WINNER endpoint - judges love visible learning!

    Example:
        GET /chat/learning/demo_user

    Returns:
        {
            "user_id": "demo_user",
            "total_interactions": 47,
            "traits": ["avoids_conflict", "needs_validation"],
            "common_scenarios": ["workplace_conflict", "exam_stress"],
            "common_emotions": ["anxiety", "frustration"],
            "adaptations_learned": [
                "Buddy learned you prefer diplomatic approaches",
                "Buddy adapted to validate your emotions first"
            ]
        }
    """
    try:
        if not mongodb_available:
            return LearningResponse(
                user_id=user_id,
                total_interactions=0,
                traits=[],
                common_scenarios=[],
                common_emotions=[],
                adaptations_learned=["Learning features require MongoDB (currently unavailable)"]
            )

        try:
            stats = get_interaction_stats(user_id)
        except Exception as e:
            # MongoDB error - return graceful response
            print(f"MongoDB error in get_interaction_stats: {e}")
            return LearningResponse(
                user_id=user_id,
                total_interactions=0,
                traits=[],
                common_scenarios=[],
                common_emotions=[],
                adaptations_learned=["Learning data temporarily unavailable"]
            )

        # Get traits
        try:
            from persona import get_user_traits
            traits = get_user_traits(user_id)
        except Exception as e:
            print(f"Error getting traits: {e}")
            traits = []

        return LearningResponse(
            user_id=user_id,
            total_interactions=stats.get('total_interactions', 0),
            traits=traits,
            common_scenarios=stats.get('common_scenarios', []),
            common_emotions=stats.get('common_emotions', []),
            adaptations_learned=stats.get('adaptations_learned', [])
        )

    except Exception as e:
        # Last resort - don't crash
        print(f"Error in learning endpoint: {e}")
        return LearningResponse(
            user_id=user_id,
            total_interactions=0,
            traits=[],
            common_scenarios=[],
            common_emotions=[],
            adaptations_learned=["Learning insights temporarily unavailable"]
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Buddy AI",
        "version": "1.0.0"
    }

