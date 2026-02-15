"""
Policy Decider - Uses Claude to determine BehaviorPolicy from context

This module uses Claude to analyze user context and decide the appropriate
behavior policy (mode, tone, humor level, etc.)
"""

import os
import json
from pathlib import Path
from typing import Optional
from anthropic import Anthropic
from .models import BehaviorPolicy


def generate_behavior_policy(context: dict) -> BehaviorPolicy:
    """
    Generate a BehaviorPolicy from context using Claude API.

    This is a standalone function that:
    - Calls Claude API with behavior_policy_prompt.txt
    - Passes context as JSON
    - Parses response into BehaviorPolicy
    - Falls back to safe default if parsing fails

    Args:
        context: Dictionary containing user context. Can include:
            - user_message (str): The user's message
            - emotion (str): Detected emotion
            - relationship (str): Relationship context
            - situation (str): Situation type
            - Any other contextual information

    Returns:
        BehaviorPolicy object

    Raises:
        ValueError: If ANTHROPIC_API_KEY is not set

    Example:
        >>> policy = generate_behavior_policy({
        ...     "user_message": "Boss yelled at me, need help",
        ...     "emotion": "frustrated",
        ...     "situation": "workplace_conflict"
        ... })
        >>> print(policy.mode)  # diplomatic_advisor
    """
    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")

    # Initialize client
    client = Anthropic(api_key=api_key)

    # Load system prompt
    prompt_path = Path(__file__).parent / "behavior_policy_prompt.txt"
    with open(prompt_path, "r") as f:
        system_prompt = f.read()

    # Convert context dict to readable format for Claude
    context_str = json.dumps(context, indent=2)

    try:
        # Call Claude API
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Context:\n{context_str}"
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
        policy_dict = json.loads(response_text)

        # Create and validate BehaviorPolicy
        return BehaviorPolicy(**policy_dict)

    except Exception as e:
        # Fallback to safe default: chill_companion
        print(f"Warning: Failed to generate policy ({e}). Using fallback.")
        return BehaviorPolicy(
            mode="chill_companion",
            tone="casual_supportive",
            humor_level=1,
            message_length="medium",
            initiative="medium",
            give_action_steps=False,
            ask_followup_question=True
        )


class PolicyDecider:
    """
    Decides BehaviorPolicy using Claude based on user context.

    Takes in:
    - User message
    - Emotion signals (optional)
    - Relationship context (optional)
    - Situation type (optional)

    Returns: BehaviorPolicy object
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize PolicyDecider with Anthropic API key.

        Args:
            api_key: Anthropic API key. If None, reads from ANTHROPIC_API_KEY env var
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment or constructor")

        self.client = Anthropic(api_key=self.api_key)

        # Load the behavior policy prompt
        prompt_path = Path(__file__).parent / "behavior_policy_prompt.txt"
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()

    def decide_policy(
        self,
        user_message: str,
        emotion: Optional[str] = None,
        relationship: Optional[str] = None,
        situation: Optional[str] = None
    ) -> BehaviorPolicy:
        """
        Analyze context and decide appropriate BehaviorPolicy.

        Args:
            user_message: The user's current message
            emotion: Detected emotion (e.g., "frustrated", "anxious")
            relationship: Relationship context (e.g., "manager_employee", "friend")
            situation: Situation type (e.g., "workplace_conflict", "boredom")

        Returns:
            BehaviorPolicy object with decided parameters
        """

        # Build context for Claude
        context_parts = [f"User message: {user_message}"]

        if emotion:
            context_parts.append(f"Detected emotion: {emotion}")
        if relationship:
            context_parts.append(f"Relationship: {relationship}")
        if situation:
            context_parts.append(f"Situation: {situation}")

        user_context = "\n".join(context_parts)

        # Call Claude to decide policy
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_context
                }
            ]
        )

        # Parse JSON response
        response_text = message.content[0].text.strip()

        # Handle potential markdown code blocks
        if response_text.startswith("```"):
            # Extract JSON from code block
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])  # Remove first and last lines

        policy_dict = json.loads(response_text)

        # Create and return BehaviorPolicy
        return BehaviorPolicy(**policy_dict)

    def decide_policy_with_signals(
        self,
        user_message: str,
        emotion_signal: Optional[dict] = None,
        relationship_signal: Optional[dict] = None,
        situation_signal: Optional[dict] = None
    ) -> BehaviorPolicy:
        """
        Decide policy using full signal objects (for Phase 2+ integration).

        Args:
            user_message: The user's message
            emotion_signal: Dict with emotion, intensity, needs
            relationship_signal: Dict with relationship type, formality, power dynamic
            situation_signal: Dict with scenario, environment, decision_required

        Returns:
            BehaviorPolicy object
        """

        # Extract simple values from signals
        emotion = emotion_signal.get("emotion") if emotion_signal else None
        relationship = relationship_signal.get("relationship") if relationship_signal else None
        situation = situation_signal.get("scenario") if situation_signal else None

        return self.decide_policy(
            user_message=user_message,
            emotion=emotion,
            relationship=relationship,
            situation=situation
        )

