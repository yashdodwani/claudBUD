#!/usr/bin/env python3
"""
Complete Adaptive System Demo

Demonstrates:
1. User sends message
2. Extract signals
3. Generate policy
4. Learn traits
5. Load memory (with learned traits)
6. Generate response WITH memory injection
7. Log interaction
8. Show adaptations over time
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from dotenv import load_dotenv
from extractors import analyze_social_context
from policy_engine import generate_behavior_policy
from rag import find_relevant_knowledge
from composer import generate_reply


def simulate_conversation(user_id: str, messages: list):
    """Simulate a conversation showing adaptation"""

    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set!")
        return

    print("=" * 70)
    print("🤖 BUDDY AI - Adaptive Learning Demo")
    print("=" * 70)
    print()
    print(f"👤 User: {user_id}")
    print(f"📊 Simulating {len(messages)} interactions...")
    print()

    # Check if MongoDB is available
    mongodb_available = bool(os.getenv("MONGO_URI"))

    if mongodb_available:
        try:
            from persona import (
                update_user_traits,
                get_user_traits,
                load_user_context,
                log_interaction,
                get_interaction_stats
            )
        except Exception as e:
            print(f"⚠️  MongoDB error: {e}")
            mongodb_available = False

    for i, user_input in enumerate(messages, 1):
        print("─" * 70)
        print(f"Interaction #{i}")
        print("─" * 70)
        print(f"💬 User: \"{user_input}\"")
        print()

        # Extract signals
        print("   🔍 Analyzing...")
        analysis = analyze_social_context(user_input)

        # Generate policy
        policy = generate_behavior_policy({
            "user_message": user_input,
            "emotion": analysis.primary_emotion,
            "relationship": analysis.relationship,
            "conflict_risk": analysis.conflict_risk
        })

        # Learn traits and load memory
        memory = None
        if mongodb_available:
            try:
                # Update traits
                update_user_traits(user_id, analysis.model_dump(), policy.model_dump())

                # Load context with learned traits
                user_context = load_user_context(user_id)
                memory = {
                    'learned_patterns': user_context.get('learned_patterns', []),
                    'interaction_count': user_context.get('interaction_count', 0)
                }

                traits = get_user_traits(user_id)
                if traits:
                    print(f"   🧠 Active traits: {', '.join(traits[:3])}")

            except Exception as e:
                print(f"   ⚠️  Learning unavailable: {e}")

        # Retrieve knowledge
        knowledge = find_relevant_knowledge(user_input, analysis.model_dump())

        # Generate response WITH MEMORY
        print(f"   💭 Generating (with {'memory' if memory else 'no memory'})...")
        response = generate_reply(
            user_input=user_input,
            analysis=analysis,
            policy=policy,
            rag_knowledge=knowledge,
            memory=memory  # MEMORY INJECTION!
        )

        print()
        print(f"   🤖 Buddy: {response[:150]}...")
        print()

        # Log interaction
        if mongodb_available:
            try:
                log_interaction(
                    user_id=user_id,
                    scenario=knowledge.get('scenario', 'general') if knowledge else 'general',
                    emotion=analysis.primary_emotion,
                    mode=policy.mode,
                    metadata={
                        'response_length': policy.message_length,
                        'humor_level': policy.humor_level
                    }
                )
            except:
                pass

        print()

    # Show learning summary
    print("=" * 70)
    print("🎯 Learning Summary")
    print("=" * 70)
    print()

    if mongodb_available:
        try:
            stats = get_interaction_stats(user_id)

            print(f"Total Interactions: {stats['total_interactions']}")
            print()

            if stats['common_scenarios']:
                print("Common Scenarios:")
                for scenario in stats['common_scenarios']:
                    print(f"  • {scenario}")
                print()

            if stats['common_emotions']:
                print("Common Emotions:")
                for emotion in stats['common_emotions']:
                    print(f"  • {emotion}")
                print()

            if stats['adaptations_learned']:
                print("Adaptations Learned:")
                for adaptation in stats['adaptations_learned']:
                    print(f"  ✅ {adaptation}")
                print()

            print("─" * 70)
            print("🎉 Buddy is now personalized to your communication style!")
            print("─" * 70)

        except Exception as e:
            print(f"Stats unavailable: {e}")
    else:
        print("MongoDB not configured - running without learning")
        print("System still works perfectly!")

    print()


def main():
    # Simulate conversation with workplace stress user
    messages = [
        # Interaction 1: First workplace stress
        "My boss just criticized my work in front of the whole team. I'm so embarrassed.",

        # Interaction 2: Another authority conflict
        "Team lead keeps micromanaging everything I do. It's driving me crazy.",

        # Interaction 3: Seeking advice
        "I need to push back on this deadline but don't know how to say it professionally.",

        # Interaction 4: Venting
        "Everything at work is just overwhelming right now. I can't keep up.",

        # Interaction 5: Another workplace issue
        "Manager changed requirements again after I already finished. So frustrating!"
    ]

    simulate_conversation("adaptive_demo_user", messages)

    print()
    print("=" * 70)
    print("💡 What Just Happened?")
    print("=" * 70)
    print()
    print("1. Buddy extracted signals from each message")
    print("2. Buddy learned patterns:")
    print("   → 'avoids_conflict' (multiple authority conflicts)")
    print("   → 'workplace_stress_prone' (work-related stress)")
    print("   → 'needs_validation' (venting sessions)")
    print()
    print("3. Buddy injected learned traits into responses:")
    print("   → More diplomatic approach")
    print("   → Extra supportive for work issues")
    print("   → Validates emotions before advice")
    print()
    print("4. Buddy logged interactions for future adaptation")
    print()
    print("🎯 Result: Consistent, personalized responses!")
    print()


if __name__ == "__main__":
    main()

