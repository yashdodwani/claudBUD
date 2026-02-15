#!/usr/bin/env python3
"""
Complete System with User Context (Persona)

Demonstrates the full Buddy AI system WITH personalization:
- User profile loading
- Memory integration
- Personalized responses
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from dotenv import load_dotenv
from extractors import analyze_social_context
from policy_engine import generate_behavior_policy
from rag import find_relevant_knowledge
from composer import generate_buddy_reply


def main():
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set!")
        return

    print("=" * 70)
    print("🤖 BUDDY AI - With User Personalization")
    print("=" * 70)
    print()

    # User input
    user_input = "Yaar I'm so stressed about this project deadline. Boss keeps changing requirements."
    user_id = "demo_user_456"

    print(f"📝 User: {user_id}")
    print(f"💬 Message: \"{user_input}\"")
    print()

    # Try to load user context (optional - gracefully degrades)
    user_context = None
    try:
        if os.getenv("MONGO_URI"):
            from persona import load_user_context
            user_context = load_user_context(user_id)
            print("👤 User Context Loaded:")
            print(f"   Preferences: {user_context['preferences']}")
            print(f"   Interaction Count: {user_context['interaction_count']}")
            print(f"   Memory: {user_context['memory_summary'][:60]}...")
            print()
    except Exception as e:
        print("ℹ️  User context not available (MongoDB not configured)")
        print("   System will work without personalization")
        print()

    # Phase 2: Extract signals
    print("🔍 Extracting Social Signals...")
    analysis = analyze_social_context(user_input)
    print(f"   Emotion: {analysis.primary_emotion} ({analysis.intensity}/10)")
    print(f"   Relationship: {analysis.relationship}")
    print(f"   User Need: {analysis.user_need}")
    print()

    # Phase 1: Generate policy
    print("⚙️  Generating Behavior Policy...")
    policy = generate_behavior_policy({
        "user_message": user_input,
        "emotion": analysis.primary_emotion,
        "relationship": analysis.relationship,
        "conflict_risk": analysis.conflict_risk
    })
    print(f"   Mode: {policy.mode}")
    print(f"   Tone: {policy.tone}")
    print()

    # Phase 4: Retrieve knowledge
    print("📚 Retrieving Behavior Knowledge...")
    knowledge = find_relevant_knowledge(user_input, analysis.model_dump())
    if knowledge:
        print(f"   Scenario: {knowledge.get('scenario', 'general')}")
    print()

    # Phase 5: Generate response (with persona if available)
    print("💬 Generating Personalized Response...")
    print()

    response = generate_buddy_reply(
        user_input=user_input,
        analysis=analysis.model_dump(),
        policy=policy.model_dump(),
        rag_knowledge=knowledge,
        persona=user_context  # Adds personalization if available
    )

    print("─" * 70)
    print("BUDDY'S RESPONSE:")
    print("─" * 70)
    print()
    print(response)
    print()
    print("─" * 70)
    print()

    # Save interaction memory (if MongoDB available)
    if user_context and os.getenv("MONGO_URI"):
        try:
            from persona import save_memory
            save_memory(
                user_id=user_id,
                memory_type="observation",
                content=f"Stressed about work deadline, boss changing requirements",
                metadata={
                    "emotion": analysis.primary_emotion,
                    "intensity": analysis.intensity
                }
            )
            print("💾 Interaction saved to memory")
            print()
        except:
            pass

    print("=" * 70)
    print("✅ Complete System Working!")
    print("=" * 70)
    print()

    if user_context:
        print("🎯 Personalization Active:")
        print("   • User preferences applied")
        print("   • Memory context included")
        print("   • Learning from interactions")
    else:
        print("ℹ️  Running without personalization")
        print("   • To enable: Set MONGO_URI in .env")
        print("   • System still works perfectly without it!")
    print()


if __name__ == "__main__":
    main()

