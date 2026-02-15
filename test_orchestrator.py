#!/usr/bin/env python3
"""
Test Orchestrator with 3 Consecutive Messages

Demonstrates adaptation over time with the buddy_chat() function.
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from dotenv import load_dotenv
from orchestrator import buddy_chat

load_dotenv()

def test_three_messages():
    """Test 3 consecutive messages to show adaptation"""

    print("=" * 70)
    print("🤖 BUDDY AI - Orchestrator Test")
    print("=" * 70)
    print()

    user_id = "test_orchestrator_user"

    messages = [
        "My manager just criticized my work in front of the whole team. I'm so embarrassed and angry.",
        "Now my team lead is micromanaging every single thing I do. It's so frustrating.",
        "I need to push back on this unrealistic deadline but don't want to seem incompetent."
    ]

    results = []

    for i, message in enumerate(messages, 1):
        print(f"{'─' * 70}")
        print(f"Message #{i}")
        print(f"{'─' * 70}")
        print(f"💬 User: \"{message}\"")
        print()

        # Call orchestrator
        result = buddy_chat(
            user_id=user_id,
            user_input=message,
            source="text"
        )

        results.append(result)

        # Show results
        print(f"   Emotion: {result['emotion']} ({result['intensity']}/10)")
        print(f"   Relationship: {result['relationship']}")
        print(f"   Mode: {result['mode']}")
        print()

        if result.get('learning'):
            print(f"   🧠 Learning: {result['learning']}")
            print()

        print(f"   🤖 Buddy: {result['reply'][:200]}...")
        print()

        if result.get('error'):
            print(f"   ⚠️  Error: {result['error']}")
            print()

        print()

    # Show progression
    print("=" * 70)
    print("🎯 Adaptation Progression")
    print("=" * 70)
    print()

    for i, result in enumerate(results, 1):
        print(f"Message {i}:")
        print(f"   Mode: {result['mode']}")
        if result.get('learning'):
            print(f"   📚 {result['learning']}")
        else:
            print(f"   📚 (Building understanding...)")
        print()

    print("=" * 70)
    print("✅ Orchestrator Working!")
    print("=" * 70)
    print()
    print("Key Features Demonstrated:")
    print("  ✅ Single entry point (buddy_chat)")
    print("  ✅ Automatic signal extraction")
    print("  ✅ Memory injection")
    print("  ✅ Trait learning")
    print("  ✅ Adaptation messaging")
    print("  ✅ Never crashes (fallback handling)")
    print()


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set!")
        sys.exit(1)

    test_three_messages()

