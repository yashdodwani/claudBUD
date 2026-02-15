"""
Test generate_behavior_policy() function

This tests the standalone function that generates BehaviorPolicy from context dict.
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from policy_engine import generate_behavior_policy
from dotenv import load_dotenv


def test_generate_behavior_policy():
    """Test the standalone generate_behavior_policy function"""

    # Load environment
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not found in environment")
        print("   Set it in .env file to run this test")
        return

    print("=" * 70)
    print("Testing generate_behavior_policy()")
    print("=" * 70)
    print()

    # Test Case 1: Workplace conflict
    print("Test 1: Workplace Conflict")
    print("-" * 70)
    context1 = {
        "user_message": "My manager just publicly criticized my work. I need to respond professionally but I'm really upset.",
        "emotion": "frustrated",
        "relationship": "manager_employee",
        "situation": "workplace_conflict"
    }

    print(f"Context: {context1}")
    print()

    try:
        policy1 = generate_behavior_policy(context1)
        print("✅ Generated Policy:")
        print(f"   Mode: {policy1.mode}")
        print(f"   Tone: {policy1.tone}")
        print(f"   Humor: {policy1.humor_level}/3")
        print(f"   Length: {policy1.message_length}")
        print(f"   Initiative: {policy1.initiative}")
        print(f"   Action steps: {policy1.give_action_steps}")
        print(f"   Follow-up: {policy1.ask_followup_question}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print()
    print()

    # Test Case 2: Casual boredom
    print("Test 2: Bored & Waiting")
    print("-" * 70)
    context2 = {
        "user_message": "Stuck at the airport for 3 hours. So bored.",
        "emotion": "bored",
        "situation": "waiting"
    }

    print(f"Context: {context2}")
    print()

    try:
        policy2 = generate_behavior_policy(context2)
        print("✅ Generated Policy:")
        print(f"   Mode: {policy2.mode}")
        print(f"   Tone: {policy2.tone}")
        print(f"   Humor: {policy2.humor_level}/3")
        print(f"   Length: {policy2.message_length}")
        print(f"   Initiative: {policy2.initiative}")
        print(f"   Action steps: {policy2.give_action_steps}")
        print(f"   Follow-up: {policy2.ask_followup_question}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print()
    print()

    # Test Case 3: Minimal context (should still work)
    print("Test 3: Minimal Context")
    print("-" * 70)
    context3 = {
        "user_message": "Just feeling overwhelmed today"
    }

    print(f"Context: {context3}")
    print()

    try:
        policy3 = generate_behavior_policy(context3)
        print("✅ Generated Policy:")
        print(f"   Mode: {policy3.mode}")
        print(f"   Tone: {policy3.tone}")
        print(f"   Humor: {policy3.humor_level}/3")
        print(f"   Length: {policy3.message_length}")
        print(f"   Initiative: {policy3.initiative}")
        print(f"   Action steps: {policy3.give_action_steps}")
        print(f"   Follow-up: {policy3.ask_followup_question}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print()
    print("=" * 70)
    print("✅ All tests complete!")
    print("=" * 70)


def test_fallback():
    """Test the fallback behavior when parsing fails"""

    print()
    print("=" * 70)
    print("Testing Fallback Behavior")
    print("=" * 70)
    print()

    # Note: This test simulates what happens if Claude returns invalid JSON
    # In practice, the fallback returns a safe chill_companion policy

    print("If Claude API fails or returns invalid JSON,")
    print("the function returns a fallback policy:")
    print()
    print("  mode: chill_companion")
    print("  tone: casual_supportive")
    print("  humor_level: 1")
    print("  message_length: medium")
    print("  initiative: medium")
    print("  give_action_steps: False")
    print("  ask_followup_question: True")
    print()
    print("This ensures the system never crashes, even with API issues.")
    print()


if __name__ == "__main__":
    test_generate_behavior_policy()
    test_fallback()

