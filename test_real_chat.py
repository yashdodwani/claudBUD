#!/usr/bin/env python3
"""Test a real chat interaction to see MongoDB saves"""

import sys
sys.path.insert(0, 'src')

from dotenv import load_dotenv
load_dotenv()

from orchestrator import buddy_chat
from persona import get_user_traits
from persona.db import get_users_collection

print("=" * 70)
print("Testing Real Chat with MongoDB Persistence")
print("=" * 70)
print()

user_id = "test_real_chat_user"
message = "bhai abhi to tera bhai flat ho gya hai"

print(f"User ID: {user_id}")
print(f"Message: {message}")
print()

# Before chat - check existing data
print("BEFORE CHAT:")
print("-" * 70)
users = get_users_collection()
if users is not None:
    existing = users.find_one({"user_id": user_id})
    if existing:
        print(f"  Traits: {existing.get('learned_patterns', [])}")
        print(f"  Interactions: {existing.get('interaction_count', 0)}")
    else:
        print("  No existing data")
else:
    print("  MongoDB not available")
print()

# Send chat
print("SENDING CHAT:")
print("-" * 70)
result = buddy_chat(
    user_id=user_id,
    user_input=message,
    source="text",
    meta={
        "city": "",
        "place": "unknown",
        "time": "06:47 PM"
    }
)

print(f"  Reply: {result['reply'][:100]}...")
print(f"  Mode: {result['mode']}")
print(f"  Emotion: {result['emotion']}")
print(f"  Learning: {result.get('learning', 'None')}")
print()

# After chat - check saved data
print("AFTER CHAT:")
print("-" * 70)
if users is not None:
    after = users.find_one({"user_id": user_id})
    if after:
        print(f"  Traits: {after.get('learned_patterns', [])}")
        print(f"  Interactions: {after.get('interaction_count', 0)}")
        print(f"  Last updated: {after.get('last_updated')}")

        # Check if data actually changed
        if existing and after:
            if after.get('interaction_count', 0) > existing.get('interaction_count', 0):
                print()
                print("  ✅ Interaction count INCREASED!")
            else:
                print()
                print("  ❌ Interaction count DID NOT INCREASE!")

            existing_traits = set(existing.get('learned_patterns', []))
            new_traits = set(after.get('learned_patterns', []))
            added_traits = new_traits - existing_traits

            if added_traits:
                print(f"  ✅ New traits added: {list(added_traits)}")
            else:
                print("  ⚠️  No new traits added (might be normal)")
    else:
        print("  ❌ No data found after chat!")
else:
    print("  MongoDB not available")

print()
print("=" * 70)

