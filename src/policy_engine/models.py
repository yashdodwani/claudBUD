"""
Behavior Policy Engine - Core Models

Defines how Buddy should respond based on context, emotion, and user preferences.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BehaviorPolicy(BaseModel):
    """
    The decision object that controls Claude's response behavior.

    This merges:
    - Emotion signals
    - Relationship dynamics
    - Scenario context
    - Persona memory
    - Behavior RAG knowledge
    """

    mode: Literal[
        "venting_listener",      # User needs to vent, just listen and validate
        "chill_companion",       # Casual hanging out, light conversation
        "practical_helper",      # User needs concrete solutions/action
        "diplomatic_advisor",    # Sensitive situation, need careful wording
        "motivational_push",     # User needs encouragement/motivation
        "silent_support"         # Just acknowledge, don't push conversation
    ] = Field(
        description="Primary interaction mode based on user's emotional state and needs"
    )

    tone: Literal[
        "casual_supportive",     # Friendly, relaxed but caring
        "calm_reassuring",       # Soothing, grounding presence
        "light_humor",           # Playful, using humor to lighten mood
        "serious_care",          # Empathetic, focused attention
        "respectful_formal"      # Professional, careful language
    ] = Field(
        description="Tone of voice to use in response"
    )

    humor_level: int = Field(
        ge=0,
        le=3,
        description="0=none, 1=subtle, 2=moderate, 3=full banter"
    )

    message_length: Literal["short", "medium", "long"] = Field(
        description="How much to say - short=1-2 lines, medium=paragraph, long=detailed"
    )

    initiative: Literal["low", "medium", "high"] = Field(
        description="How proactive to be - low=reactive only, high=suggest next steps"
    )

    give_action_steps: bool = Field(
        description="Whether to provide concrete action items"
    )

    ask_followup_question: bool = Field(
        description="Whether to ask a question to continue conversation"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "mode": "diplomatic_advisor",
                "tone": "calm_reassuring",
                "humor_level": 0,
                "message_length": "medium",
                "initiative": "medium",
                "give_action_steps": True,
                "ask_followup_question": False
            }
        }

