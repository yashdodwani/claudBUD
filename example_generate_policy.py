#!/usr/bin/env python3
"""
Example: Using generate_behavior_policy() function

The simplest way to generate a BehaviorPolicy from context.
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from policy_engine import generate_behavior_policy
from dotenv import load_dotenv


def main():
    # Load API key
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set!")
        print("   Create a .env file with: ANTHROPIC_API_KEY=your_key_here")
        return

    print("=" * 70)
    print("🤖 generate_behavior_policy() - Simple Example")
    print("=" * 70)
    print()

    # Define context
    context = {
        "user_message": "Bhai my team lead just assigned me 5 new tasks when I'm already drowning. I don't know how to say no without sounding lazy.",
        "emotion": "stressed",
        "relationship": "team_lead_member",
        "situation": "work_overload"
    }

    print("📝 Context:")
    for key, value in context.items():
        print(f"   {key}: {value}")
    print()

    print("🔄 Calling generate_behavior_policy()...")
    print()

    # Generate policy (with automatic fallback on error)
    policy = generate_behavior_policy(context)

    print("✅ Generated BehaviorPolicy:")
    print()
    print(f"   mode              → {policy.mode}")
    print(f"   tone              → {policy.tone}")
    print(f"   humor_level       → {policy.humor_level}/3")
    print(f"   message_length    → {policy.message_length}")
    print(f"   initiative        → {policy.initiative}")
    print(f"   give_action_steps → {policy.give_action_steps}")
    print(f"   ask_followup      → {policy.ask_followup_question}")
    print()

    print("📋 As JSON:")
    print(policy.model_dump_json(indent=2))
    print()

    print("=" * 70)
    print("💡 This policy will now control how Buddy responds!")
    print("=" * 70)


if __name__ == "__main__":
    main()

