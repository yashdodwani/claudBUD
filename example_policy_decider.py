#!/usr/bin/env python3
"""
Example: Using PolicyDecider to automatically decide response behavior

This demonstrates Phase 1 complete implementation:
- User provides a message
- PolicyDecider uses Claude to analyze context
- Returns a BehaviorPolicy object
- This policy will control how Claude responds

Usage:
1. Set ANTHROPIC_API_KEY in .env file
2. Run: python example_policy_decider.py
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from policy_engine.decider import PolicyDecider
from dotenv import load_dotenv


def main():
    # Load API key from .env
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set!")
        print("   Create a .env file with: ANTHROPIC_API_KEY=your_key_here")
        return

    print("=" * 70)
    print("🤖 Buddy - PolicyDecider Example")
    print("=" * 70)
    print()

    # Initialize the decider
    decider = PolicyDecider()

    # Example user message
    user_message = "Bhai my manager just yelled at me in front of everyone. I'm so pissed off but I need to reply professionally. Help?"

    print(f"📝 User Message:")
    print(f'   "{user_message}"')
    print()
    print("🔍 Analyzing context with Claude...")
    print()

    # Decide policy
    policy = decider.decide_policy(
        user_message=user_message,
        emotion="frustrated",
        relationship="manager_employee",
        situation="workplace_conflict"
    )

    print("✅ Generated BehaviorPolicy:")
    print()
    print(f"   Mode:              {policy.mode}")
    print(f"   Tone:              {policy.tone}")
    print(f"   Humor Level:       {policy.humor_level}/3")
    print(f"   Message Length:    {policy.message_length}")
    print(f"   Initiative:        {policy.initiative}")
    print(f"   Give Action Steps: {policy.give_action_steps}")
    print(f"   Ask Follow-up:     {policy.ask_followup_question}")
    print()

    print("📋 JSON Output (for Claude system prompt):")
    print(policy.model_dump_json(indent=2))
    print()

    print("=" * 70)
    print("💡 Next: This policy will control how Claude generates the response")
    print("=" * 70)


if __name__ == "__main__":
    main()

