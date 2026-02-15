"""
Social Analysis Models

Pydantic models for emotion and relationship signal extraction.
"""

from pydantic import BaseModel, Field
from typing import Literal


class SocialAnalysis(BaseModel):
    """
    Structured analysis of emotional and social context from user message.

    This captures:
    - Primary emotion and intensity
    - What the user actually needs
    - Relationship dynamics
    - Conflict risk level
    """

    primary_emotion: Literal[
        "frustration",
        "anger",
        "sadness",
        "anxiety",
        "confusion",
        "boredom",
        "happy",
        "neutral"
    ] = Field(
        description="Main emotion detected in the message"
    )

    intensity: int = Field(
        ge=1,
        le=10,
        description="Emotional intensity on scale of 1-10"
    )

    user_need: Literal[
        "vent",              # Just wants to let it out
        "advice",            # Needs concrete solutions
        "reassurance",       # Needs validation/comfort
        "distraction",       # Wants to escape/lighten mood
        "decision_help",     # Stuck on a choice
        "validation"         # Needs to know they're right/justified
    ] = Field(
        description="What the user actually needs emotionally"
    )

    relationship: Literal[
        "friend",
        "stranger",
        "authority",         # Boss, manager, teacher, etc.
        "service_person",    # Customer service, waiter, etc.
        "family",
        "romantic",
        "unknown"
    ] = Field(
        description="Type of relationship being discussed"
    )

    conflict_risk: Literal["low", "medium", "high"] = Field(
        description="Risk level if direct confrontation happens"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "primary_emotion": "frustration",
                "intensity": 7,
                "user_need": "advice",
                "relationship": "authority",
                "conflict_risk": "high"
            }
        }

