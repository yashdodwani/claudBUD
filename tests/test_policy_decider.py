"""
Test PolicyDecider - demonstrates automatic policy generation

NOTE: Requires ANTHROPIC_API_KEY environment variable to be set
Run: python tests/test_policy_decider.py
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from policy_engine.decider import PolicyDecider
from dotenv import load_dotenv


def test_policy_decider():
    """Test the PolicyDecider with various scenarios"""

    # Load environment variables
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not found in environment")
        print("   Please create a .env file with your API key")
        print("   Example: echo 'ANTHROPIC_API_KEY=your_key_here' > .env")
        return

    print("=" * 70)
    print("PolicyDecider Test - Automatic BehaviorPolicy Generation")
    print("=" * 70)
    print()

    # Initialize decider
    decider = PolicyDecider()

    # Test scenarios
    scenarios = [
        {
            "name": "Workplace Conflict",
            "message": "My boss just sent me an angry email saying my work is not good enough. I'm so stressed.",
            "emotion": "frustrated",
            "situation": "workplace_conflict"
        },
        {
            "name": "Bored Waiting",
            "message": "Ugh sitting in this train for 2 more hours. So bored.",
            "emotion": "bored",
            "situation": "waiting"
        },
        {
            "name": "Need to Vent",
            "message": "Bhai I can't take this anymore. Everything is going wrong today. First the meeting, then the client call, now this.",
            "emotion": "overwhelmed",
            "situation": "venting"
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['name']}")
        print(f"   Message: \"{scenario['message']}\"")
        print(f"   Context: emotion={scenario.get('emotion')}, situation={scenario.get('situation')}")
        print()

        try:
            # Get policy from Claude
            policy = decider.decide_policy(
                user_message=scenario['message'],
                emotion=scenario.get('emotion'),
                situation=scenario.get('situation')
            )

            print(f"   ✅ Generated Policy:")
            print(f"      Mode:           {policy.mode}")
            print(f"      Tone:           {policy.tone}")
            print(f"      Humor:          {policy.humor_level}/3")
            print(f"      Length:         {policy.message_length}")
            print(f"      Initiative:     {policy.initiative}")
            print(f"      Action steps:   {policy.give_action_steps}")
            print(f"      Follow-up Q:    {policy.ask_followup_question}")
            print()

        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()

    print("=" * 70)
    print("✅ PolicyDecider test complete!")
    print("=" * 70)


if __name__ == "__main__":
    test_policy_decider()

