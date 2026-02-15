"""
Response Composer - Final Response Generation

Combines all signals, policy, and RAG knowledge to generate
the final Buddy response using Claude.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from anthropic import Anthropic


def generate_buddy_reply(
    user_input: str,
    analysis: Optional[Dict] = None,
    policy: Optional[Dict] = None,
    rag_knowledge: Optional[Dict] = None,
    persona: Optional[Dict] = None,
    memory: Optional[Dict] = None,
    meta: Optional[Dict] = None
) -> str:
    """
    Generate final Buddy response using Claude.

    Combines:
    - User input
    - Social analysis (emotion, relationship, conflict_risk)
    - Behavior policy (mode, tone, humor_level, etc.)
    - RAG knowledge (cultural patterns, do's and don'ts)
    - Persona memory (user preferences and context)
    - Memory (learned traits for consistency)
    - Meta (real-world context: city, place, time)

    Args:
        user_input: The user's message
        analysis: Social analysis dict from analyze_social_context()
        policy: Behavior policy dict from generate_behavior_policy()
        rag_knowledge: Retrieved behavior knowledge
        persona: User-specific preferences (optional)
        memory: User memory with learned traits (optional)
        meta: Real-world context (city, place, time, event)

    Returns:
        Generated response text

    Example:
        >>> reply = generate_buddy_reply(
        ...     user_input="Bhai train chut gayi",
        ...     analysis={'primary_emotion': 'frustration', 'relationship': 'friend'},
        ...     policy={'mode': 'chill_companion', 'tone': 'casual_supportive'},
        ...     rag_knowledge={'do': ['validate', 'suggest alternatives']},
        ...     memory={'learned_patterns': ['needs_validation']},
        ...     meta={'city': 'Bangalore', 'place': 'railway_station', 'time': 'evening'}
        ... )
        >>> print(reply)  # Context-aware response about Bangalore
    """

    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")

    # Initialize client
    client = Anthropic(api_key=api_key)

    # Load system prompt
    prompt_path = Path(__file__).parent / "response_prompt.txt"
    with open(prompt_path, 'r') as f:
        system_prompt = f.read()

    # Build context for Claude
    context_parts = [
        "=== USER MESSAGE ===",
        user_input,
        ""
    ]

    # Add user personality traits (MEMORY INJECTION)
    if memory and memory.get('learned_patterns'):
        context_parts.append("=== USER PERSONALITY TRAITS ===")
        context_parts.append("Based on past interactions, this user:")
        for trait in memory.get('learned_patterns', []):
            trait_description = {
                'avoids_conflict': '- Avoids confrontation, prefers diplomatic approach',
                'needs_validation': '- Needs emotional validation before advice',
                'reassurance_seeking': '- Seeks reassurance and calm guidance',
                'high_anxiety_baseline': '- Frequently anxious, needs steady calm tone',
                'humor_responsive': '- Responds well to appropriate humor',
                'solution_oriented': '- Prefers actionable, practical solutions',
                'needs_emotional_support': '- Needs empathy before problem-solving',
                'workplace_stress_prone': '- Sensitive to workplace stress, be extra supportive'
            }.get(trait, f'- {trait}')
            context_parts.append(trait_description)
        context_parts.append("")
        context_parts.append("Adapt your tone and approach accordingly to maintain consistency.")
        context_parts.append("")

    # Add real-world context (CRITICAL for grounding!)
    if meta:
        context_parts.append("=== REAL WORLD CONTEXT ===")
        city = meta.get('city', 'unknown')
        place = meta.get('place', 'unknown')
        time = meta.get('time', 'unknown')
        event = meta.get('event', None)

        context_parts.append(f"City: {city}")
        context_parts.append(f"Place: {place}")
        context_parts.append(f"Time: {time}")
        if event:
            context_parts.append(f"Event: {event}")
        context_parts.append("")
        context_parts.append("CRITICAL RULES:")
        context_parts.append("- NEVER assume a different city than stated")
        context_parts.append("- If city is unknown, speak generically")
        context_parts.append("- If city is known, ground suggestions locally (e.g., Bangalore metro, Mumbai local trains)")
        context_parts.append("- Use place context to make response realistic")
        context_parts.append("- Adapt advice to local infrastructure and culture")
        context_parts.append("")

    # Add social analysis
    if analysis:
        context_parts.append("=== SOCIAL ANALYSIS ===")
        context_parts.append(f"Emotion: {analysis.get('primary_emotion', 'unknown')}")
        context_parts.append(f"Intensity: {analysis.get('intensity', 5)}/10")
        context_parts.append(f"User Need: {analysis.get('user_need', 'unknown')}")
        context_parts.append(f"Relationship: {analysis.get('relationship', 'unknown')}")
        context_parts.append(f"Conflict Risk: {analysis.get('conflict_risk', 'low')}")
        context_parts.append("")

    # Add behavior policy
    if policy:
        context_parts.append("=== BEHAVIOR POLICY (FOLLOW STRICTLY) ===")
        context_parts.append(f"Mode: {policy.get('mode', 'chill_companion')}")
        context_parts.append(f"Tone: {policy.get('tone', 'casual_supportive')}")
        context_parts.append(f"Humor Level: {policy.get('humor_level', 1)}/3")
        context_parts.append(f"Message Length: {policy.get('message_length', 'medium')}")
        context_parts.append(f"Initiative: {policy.get('initiative', 'medium')}")
        context_parts.append(f"Give Action Steps: {policy.get('give_action_steps', False)}")
        context_parts.append(f"Ask Follow-up: {policy.get('ask_followup_question', False)}")
        context_parts.append("")

    # Add RAG knowledge
    if rag_knowledge:
        context_parts.append("=== CULTURAL CONTEXT (Indian Behavior Patterns) ===")

        if 'scenario' in rag_knowledge:
            context_parts.append(f"Scenario: {rag_knowledge['scenario']}")

        if 'typical_emotions' in rag_knowledge:
            context_parts.append(f"Typical Emotions: {', '.join(rag_knowledge['typical_emotions'])}")

        if 'do' in rag_knowledge:
            context_parts.append("\nDO:")
            for item in rag_knowledge['do'][:3]:  # Top 3
                context_parts.append(f"  - {item}")

        if 'dont' in rag_knowledge:
            context_parts.append("\nDON'T:")
            for item in rag_knowledge['dont'][:3]:  # Top 3
                context_parts.append(f"  - {item}")

        if 'tone' in rag_knowledge:
            context_parts.append(f"\nSuggested Tone: {rag_knowledge['tone']}")

        if 'humor_allowed' in rag_knowledge:
            context_parts.append(f"Humor Allowed: {rag_knowledge['humor_allowed']}")

        context_parts.append("")

    # Add persona (future use)
    if persona:
        context_parts.append("=== USER PREFERENCES ===")
        context_parts.append(json.dumps(persona, indent=2))
        context_parts.append("")

    context_parts.append("=== YOUR RESPONSE ===")
    context_parts.append("(Respond naturally as Buddy, following the policy and cultural context)")

    full_context = "\n".join(context_parts)

    try:
        # Call Claude
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": full_context
                }
            ]
        )

        # Extract response
        response_text = message.content[0].text.strip()
        return response_text

    except Exception as e:
        # Fallback response
        print(f"Warning: Failed to generate response ({e}). Using fallback.")
        return "Hey, I'm here for you. What's going on?"


def generate_reply(
    user_input: str,
    analysis: Optional[Any] = None,
    policy: Optional[Any] = None,
    rag_knowledge: Optional[Dict] = None,
    memory: Optional[Dict] = None,
    meta: Optional[Dict] = None
) -> str:
    """
    Simplified interface for generate_buddy_reply.

    Accepts Pydantic models or dicts and converts them automatically.

    Args:
        user_input: User's message
        analysis: SocialAnalysis object or dict
        policy: BehaviorPolicy object or dict
        rag_knowledge: Retrieved knowledge dict
        memory: User memory with learned traits (dict)
        meta: Real-world context (city, place, time)

    Returns:
        Generated response text
    """

    # Convert Pydantic models to dicts if needed
    analysis_dict = None
    if analysis:
        if hasattr(analysis, 'model_dump'):
            analysis_dict = analysis.model_dump()
        else:
            analysis_dict = analysis

    policy_dict = None
    if policy:
        if hasattr(policy, 'model_dump'):
            policy_dict = policy.model_dump()
        else:
            policy_dict = policy

    return generate_buddy_reply(
        user_input=user_input,
        analysis=analysis_dict,
        policy=policy_dict,
        rag_knowledge=rag_knowledge,
        memory=memory,
        meta=meta
    )

