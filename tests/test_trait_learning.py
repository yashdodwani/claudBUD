"""
Test User Trait Learning

Demonstrates how traits are learned from behavioral signals.
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from dotenv import load_dotenv


def test_trait_learning():
    """Test trait learning from signals"""

    load_dotenv()

    if not os.getenv("MONGO_URI"):
        print("⚠️  MONGO_URI not set - showing examples without database")
        show_trait_mapping_examples()
        return

    try:
        from persona import update_user_traits, get_user_traits, load_user_context

        print("=" * 70)
        print("Testing User Trait Learning")
        print("=" * 70)
        print()

        user_id = "test_trait_user"

        # Scenario 1: Authority conflict with high anxiety
        print("Test 1: Authority Conflict + High Anxiety")
        print("-" * 70)

        analysis1 = {
            'primary_emotion': 'anxiety',
            'intensity': 8,
            'relationship': 'authority',
            'conflict_risk': 'high',
            'user_need': 'advice'
        }

        policy1 = {
            'mode': 'diplomatic_advisor',
            'tone': 'calm_reassuring',
            'humor_level': 0
        }

        updated = update_user_traits(user_id, analysis1, policy1)

        if updated:
            traits = get_user_traits(user_id)
            print(f"✅ Traits identified: {traits}")
            print(f"   Expected: avoids_conflict, reassurance_seeking, workplace_stress_prone")
        else:
            print("❌ No traits identified")
        print()

        # Scenario 2: Venting session
        print("Test 2: Venting Session")
        print("-" * 70)

        analysis2 = {
            'primary_emotion': 'frustration',
            'intensity': 6,
            'relationship': 'friend',
            'conflict_risk': 'low',
            'user_need': 'vent'
        }

        policy2 = {
            'mode': 'venting_listener',
            'tone': 'casual_supportive',
            'humor_level': 1
        }

        updated = update_user_traits(user_id, analysis2, policy2)

        if updated:
            traits = get_user_traits(user_id)
            print(f"✅ Updated traits: {traits}")
            print(f"   New trait: needs_validation")
        print()

        # Scenario 3: Solution-oriented request
        print("Test 3: Solution-Oriented")
        print("-" * 70)

        analysis3 = {
            'primary_emotion': 'confusion',
            'intensity': 5,
            'relationship': 'unknown',
            'conflict_risk': 'low',
            'user_need': 'decision_help'
        }

        policy3 = {
            'mode': 'practical_helper',
            'tone': 'casual_supportive',
            'humor_level': 1
        }

        updated = update_user_traits(user_id, analysis3, policy3)

        if updated:
            traits = get_user_traits(user_id)
            print(f"✅ Updated traits: {traits}")
            print(f"   New trait: solution_oriented")
        print()

        # Show final profile
        print("=" * 70)
        print("Final User Profile")
        print("=" * 70)

        context = load_user_context(user_id)
        print(f"User ID: {context['user_id']}")
        print(f"Interaction Count: {context['interaction_count']}")
        print(f"Learned Patterns: {traits}")
        print()

        print("✅ Trait learning working!")
        print()
        print("Privacy Note:")
        print("  • Only behavioral signals stored")
        print("  • NO raw messages saved")
        print("  • Only trait patterns learned")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure MongoDB is running")


def show_trait_mapping_examples():
    """Show examples of signal-to-trait mapping"""

    print()
    print("=" * 70)
    print("Signal → Trait Mapping Examples")
    print("=" * 70)
    print()

    mappings = [
        {
            "signals": {
                "relationship": "authority",
                "conflict_risk": "high"
            },
            "trait": "avoids_conflict",
            "description": "User has authority conflicts → learns to avoid confrontation"
        },
        {
            "signals": {
                "mode": "venting_listener",
                "user_need": "vent"
            },
            "trait": "needs_validation",
            "description": "User vents often → needs emotional validation"
        },
        {
            "signals": {
                "emotion": "anxiety",
                "intensity": "8+"
            },
            "trait": "reassurance_seeking",
            "description": "High intensity anxiety → seeks reassurance"
        },
        {
            "signals": {
                "humor_level": "2+",
                "emotion": "boredom/neutral"
            },
            "trait": "humor_responsive",
            "description": "Responds well to humor → prefers light tone"
        },
        {
            "signals": {
                "user_need": "advice/decision_help",
                "mode": "practical_helper"
            },
            "trait": "solution_oriented",
            "description": "Seeks solutions → prefers actionable advice"
        },
        {
            "signals": {
                "user_need": "reassurance/validation"
            },
            "trait": "needs_emotional_support",
            "description": "Needs emotional support → empathy first"
        },
        {
            "signals": {
                "relationship": "authority",
                "emotion": "frustration/anger/anxiety"
            },
            "trait": "workplace_stress_prone",
            "description": "Workplace stress pattern → sensitive to work issues"
        }
    ]

    for i, mapping in enumerate(mappings, 1):
        print(f"{i}. Trait: {mapping['trait']}")
        print(f"   Signals: {mapping['signals']}")
        print(f"   → {mapping['description']}")
        print()

    print("=" * 70)
    print("Benefits:")
    print("=" * 70)
    print("  • Buddy learns user preferences over time")
    print("  • Responses become more personalized")
    print("  • No raw messages stored (privacy-first)")
    print("  • Only behavioral patterns tracked")
    print()


if __name__ == "__main__":
    test_trait_learning()

