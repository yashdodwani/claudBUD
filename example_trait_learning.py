#!/usr/bin/env python3
"""
Complete System with Trait Learning

Demonstrates:
1. User sends message
2. System analyzes signals
3. Generates policy
4. Learns traits from patterns
5. Generates personalized response
6. Updates user profile (NO raw message stored)
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from dotenv import load_dotenv
from extractors import analyze_social_context
from policy_engine import generate_behavior_policy
from rag import find_relevant_knowledge
from composer import generate_reply


def main():
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set!")
        return

    print("=" * 70)
    print("🤖 BUDDY AI - With Trait Learning")
    print("=" * 70)
    print()

    user_input = "Yaar my manager keeps micromanaging everything I do. It's so frustrating. I can't even make small decisions without approval."
    user_id = "learning_demo_user"

    print(f"👤 User: {user_id}")
    print(f"💬 Message: \"{user_input}\"")
    print()

    # Phase 2: Extract signals
    print("🔍 Phase 2: Extracting Signals...")
    analysis = analyze_social_context(user_input)

    print(f"   Emotion: {analysis.primary_emotion} ({analysis.intensity}/10)")
    print(f"   Relationship: {analysis.relationship}")
    print(f"   Conflict Risk: {analysis.conflict_risk}")
    print(f"   User Need: {analysis.user_need}")
    print()

    # Phase 1: Generate policy
    print("⚙️  Phase 1: Generating Policy...")
    policy = generate_behavior_policy({
        "user_message": user_input,
        "emotion": analysis.primary_emotion,
        "relationship": analysis.relationship,
        "conflict_risk": analysis.conflict_risk
    })

    print(f"   Mode: {policy.mode}")
    print(f"   Tone: {policy.tone}")
    print()

    # Learn traits (if MongoDB available)
    print("🧠 Learning User Traits...")
    if os.getenv("MONGO_URI"):
        try:
            from persona import update_user_traits, get_user_traits, load_user_context

            # Update traits based on signals
            updated = update_user_traits(
                user_id=user_id,
                analysis=analysis.model_dump(),
                policy=policy.model_dump()
            )

            if updated:
                traits = get_user_traits(user_id)
                print(f"   ✅ Traits learned: {', '.join(traits)}")
                print(f"   Privacy: NO raw message stored, only signals")
            else:
                print(f"   No new traits identified")

            # Load user context
            user_context = load_user_context(user_id)
            print(f"   Interaction #{user_context['interaction_count']}")

        except Exception as e:
            print(f"   ⚠️  Trait learning unavailable: {e}")
            user_context = None
    else:
        print(f"   ℹ️  MongoDB not configured (trait learning disabled)")
        user_context = None

    print()

    # Phase 4: Retrieve knowledge
    print("📚 Phase 4: Retrieving Knowledge...")
    knowledge = find_relevant_knowledge(user_input, analysis.model_dump())
    if knowledge:
        print(f"   Scenario: {knowledge.get('scenario', 'general')}")
    print()

    # Phase 5: Generate response
    print("💬 Phase 5: Generating Response...")
    print()

    response = generate_reply(
        user_input=user_input,
        analysis=analysis,
        policy=policy,
        rag_knowledge=knowledge
    )

    print("─" * 70)
    print("BUDDY'S RESPONSE:")
    print("─" * 70)
    print()
    print(response)
    print()
    print("─" * 70)
    print()

    # Show what was learned
    print("=" * 70)
    print("🎯 What Buddy Learned (Privacy-First)")
    print("=" * 70)
    print()

    if user_context:
        print("Traits Identified:")
        traits = get_user_traits(user_id)
        for trait in traits:
            print(f"  • {trait}")
        print()

        print("What's Stored:")
        print("  ✅ Behavioral signals (emotion, relationship, intensity)")
        print("  ✅ Trait patterns (avoids_conflict, needs_validation, etc.)")
        print("  ✅ Interaction count and timestamps")
        print()

        print("What's NOT Stored:")
        print("  ❌ Raw message content")
        print("  ❌ Conversation text")
        print("  ❌ Personal details")
    else:
        print("MongoDB not configured - no learning stored")
        print("System still works perfectly without it!")

    print()
    print("=" * 70)
    print("✅ Complete System with Trait Learning!")
    print("=" * 70)


def show_trait_examples():
    """Show what traits mean"""

    print()
    print("=" * 70)
    print("📚 Trait Meanings")
    print("=" * 70)
    print()

    traits = {
        "avoids_conflict": "User has authority conflicts → prefers diplomatic approach",
        "needs_validation": "User vents often → needs emotional validation first",
        "reassurance_seeking": "High anxiety → seeks reassurance and calm guidance",
        "humor_responsive": "Responds well to humor → can use light tone",
        "solution_oriented": "Seeks practical solutions → prefers actionable advice",
        "needs_emotional_support": "Needs empathy → emotions before solutions",
        "workplace_stress_prone": "Workplace stress → sensitive to work issues",
        "high_anxiety_baseline": "Frequently anxious → calm, steady responses"
    }

    for trait, meaning in traits.items():
        print(f"• {trait}")
        print(f"  → {meaning}")
        print()


if __name__ == "__main__":
    main()
    show_trait_examples()

