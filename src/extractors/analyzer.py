"""
Social Context Analyzer

Extracts emotional and relationship signals from user text.
"""

import os
import json
from pathlib import Path
from anthropic import Anthropic
from .models import SocialAnalysis


def analyze_social_context(text: str) -> SocialAnalysis:
    """
    Analyze emotional and social context of a message.

    Extracts:
    - Primary emotion and intensity
    - What the user actually needs (vent, advice, reassurance, etc.)
    - Relationship type (friend, authority, family, etc.)
    - Conflict risk level

    Args:
        text: User's message to analyze

    Returns:
        SocialAnalysis object with structured signals

    Raises:
        ValueError: If ANTHROPIC_API_KEY is not set

    Example:
        >>> analysis = analyze_social_context(
        ...     "My boss just yelled at me in front of everyone. So pissed off."
        ... )
        >>> print(analysis.primary_emotion)  # "anger"
        >>> print(analysis.relationship)     # "authority"
        >>> print(analysis.conflict_risk)    # "high"
    """
    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")

    # Initialize client
    client = Anthropic(api_key=api_key)

    # Load system prompt
    prompt_path = Path(__file__).parent / "social_analysis_prompt.txt"
    with open(prompt_path, "r") as f:
        system_prompt = f.read()

    try:
        # Call Claude API
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        # Parse response
        response_text = message.content[0].text.strip()

        # Handle markdown code blocks
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            # Remove first line (```json or ```) and last line (```)
            response_text = "\n".join(lines[1:-1])

        # Parse JSON
        analysis_dict = json.loads(response_text)

        # Create and validate SocialAnalysis
        return SocialAnalysis(**analysis_dict)

    except Exception as e:
        # Fallback to neutral safe default
        print(f"Warning: Failed to analyze social context ({e}). Using neutral fallback.")
        return SocialAnalysis(
            primary_emotion="neutral",
            intensity=5,
            user_need="advice",
            relationship="unknown",
            conflict_risk="low"
        )

