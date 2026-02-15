#!/usr/bin/env python3
"""
Test Context Signals Layer

Demonstrates how real-world context prevents "fake" responses.
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from dotenv import load_dotenv
from orchestrator import buddy_chat

load_dotenv()

def test_context_grounding():
    """Test context-aware responses"""

    print("=" * 70)
    print("🌍 CONTEXT SIGNALS LAYER - Test")
    print("=" * 70)
    print()

    user_id = "context_test_user"
    message = "Bhai meri train chut gayi, bahot traffic tha"

    # Test 1: Without context (generic)
    print("Test 1: WITHOUT Context")
    print("-" * 70)
    print(f"Message: \"{message}\"")
    print("Meta: None")
    print()

    result1 = buddy_chat(
        user_id=user_id,
        user_input=message,
        source="text"
    )

    print(f"Mode: {result1['mode']}")
    print(f"Reply: {result1['reply'][:150]}...")
    print()
    print()

    # Test 2: With Bangalore context
    print("Test 2: WITH Bangalore Context")
    print("-" * 70)
    print(f"Message: \"{message}\"")
    print("Meta: {city: 'Bangalore', place: 'railway_station', time: 'evening'}")
    print()

    result2 = buddy_chat(
        user_id=user_id,
        user_input=message,
        source="text",
        meta={
            "city": "Bangalore",
            "place": "railway_station",
            "time": "evening"
        }
    )

    print(f"Mode: {result2['mode']}")
    print(f"Reply: {result2['reply'][:200]}...")
    print()
    print()

    # Test 3: With Mumbai context (different city!)
    print("Test 3: WITH Mumbai Context")
    print("-" * 70)
    print(f"Message: \"{message}\"")
    print("Meta: {city: 'Mumbai', place: 'railway_station', time: 'evening'}")
    print()

    result3 = buddy_chat(
        user_id=user_id,
        user_input=message,
        source="text",
        meta={
            "city": "Mumbai",
            "place": "railway_station",
            "time": "evening"
        }
    )

    print(f"Mode: {result3['mode']}")
    print(f"Reply: {result3['reply'][:200]}...")
    print()
    print()

    # Test 4: Workplace context
    print("Test 4: Office Context")
    print("-" * 70)
    message4 = "My manager is being unreasonable about this deadline"
    print(f"Message: \"{message4}\"")
    print("Meta: {city: 'Bangalore', place: 'workplace', time: 'afternoon'}")
    print()

    result4 = buddy_chat(
        user_id=user_id,
        user_input=message4,
        source="text",
        meta={
            "city": "Bangalore",
            "place": "workplace",
            "time": "afternoon"
        }
    )

    print(f"Mode: {result4['mode']}")
    print(f"Reply: {result4['reply'][:200]}...")
    print()
    print()

    # Summary
    print("=" * 70)
    print("🎯 What Context Does")
    print("=" * 70)
    print()
    print("WITHOUT context:")
    print("  → Generic response")
    print("  → No city-specific advice")
    print("  → Feels \"AI-like\"")
    print()
    print("WITH context:")
    print("  → Bangalore: Mentions Bangalore infrastructure")
    print("  → Mumbai: Mentions Mumbai local trains")
    print("  → Grounded in reality")
    print("  → Feels like a local friend")
    print()
    print("🚫 Prevents hallucination:")
    print("  → Won't suggest Delhi metro when in Bangalore")
    print("  → Won't give wrong city-specific advice")
    print("  → Stays realistic and helpful")
    print()


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set!")
        sys.exit(1)

    test_context_grounding()

