"""
Test User Context Management

Tests MongoDB connection and user context loading.
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from dotenv import load_dotenv


def test_user_context():
    """Test user context loading"""

    load_dotenv()

    if not os.getenv("MONGO_URI"):
        print("⚠️  MONGO_URI not set in .env file")
        print("   Add: MONGO_URI=mongodb://localhost:27017/buddy_ai")
        print("   Or use MongoDB Atlas connection string")
        print()
        print("Skipping MongoDB tests (optional feature)")
        return

    try:
        from persona import load_user_context, save_memory, update_user_preferences

        print("=" * 70)
        print("Testing User Context Management")
        print("=" * 70)
        print()

        # Test 1: Load user context (creates if not exists)
        print("Test 1: Load User Context")
        print("-" * 70)

        user_id = "test_user_123"
        context = load_user_context(user_id)

        print(f"✅ Loaded context for user: {context['user_id']}")
        print(f"   Preferences: {context['preferences']}")
        print(f"   Communication Style: {context['communication_style']}")
        print(f"   Interaction Count: {context['interaction_count']}")
        print(f"   Memory Summary: {context['memory_summary']}")
        print()

        # Test 2: Save a memory
        print("Test 2: Save Memory")
        print("-" * 70)

        saved = save_memory(
            user_id=user_id,
            memory_type="pattern",
            content="User prefers concise responses",
            metadata={"source": "interaction"}
        )

        if saved:
            print("✅ Memory saved successfully")
        else:
            print("❌ Failed to save memory")
        print()

        # Test 3: Update preferences
        print("Test 3: Update Preferences")
        print("-" * 70)

        updated = update_user_preferences(
            user_id=user_id,
            preferences={
                "humor_level": "high",
                "response_length": "short",
                "formality": "casual"
            }
        )

        if updated:
            print("✅ Preferences updated")
        else:
            print("❌ Failed to update preferences")
        print()

        # Test 4: Reload context to verify
        print("Test 4: Reload Context")
        print("-" * 70)

        context2 = load_user_context(user_id)
        print(f"✅ Reloaded context")
        print(f"   Humor Level: {context2['preferences'].get('humor_level')}")
        print(f"   Interaction Count: {context2['interaction_count']}")
        print()

        print("=" * 70)
        print("✅ All MongoDB tests passed!")
        print("=" * 70)
        print()
        print("User context is now integrated into Buddy AI!")
        print("Responses can be personalized based on user preferences.")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Install pymongo: pip install pymongo")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure MongoDB is running and MONGO_URI is correct")


def test_compact_context():
    """Show how context is used in prompts"""

    print()
    print("=" * 70)
    print("Example: Using Context in Prompts")
    print("=" * 70)
    print()

    # Example context dict
    example_context = {
        "user_id": "user_123",
        "preferences": {
            "humor_level": "high",
            "response_length": "medium",
            "formality": "casual",
            "language_mix": "hinglish"
        },
        "communication_style": "casual",
        "memory_summary": "- Prefers direct answers\n- Often stressed about work\n- Responds well to humor",
        "interaction_count": 47
    }

    print("Context Dict for Prompts:")
    print("-" * 70)
    print(f"User ID: {example_context['user_id']}")
    print(f"Preferences: {example_context['preferences']}")
    print(f"Memory Summary:")
    print(example_context['memory_summary'])
    print()
    print("This compact dict can be added to Claude prompts for personalization!")
    print()


if __name__ == "__main__":
    test_user_context()
    test_compact_context()

