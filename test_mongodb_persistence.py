#!/usr/bin/env python3
"""
Test MongoDB Data Persistence

Verifies that data is actually being saved to MongoDB
"""

import sys
sys.path.insert(0, 'src')

from dotenv import load_dotenv
load_dotenv()

from persona import load_user_context, update_user_traits, get_user_traits
from persona.db import MongoDB

print("=" * 70)
print("Testing MongoDB Data Persistence")
print("=" * 70)
print()

# Test 1: Connection
print("Test 1: MongoDB Connection")
print("-" * 70)
db = MongoDB.connect()
if db is not None:
    print(f"✅ Connected to database: {db.name}")
else:
    print("❌ MongoDB connection failed!")
    sys.exit(1)
print()

# Test 2: Create User Profile
print("Test 2: Create User Profile")
print("-" * 70)
test_user_id = "test_persistence_user"

try:
    context = load_user_context(test_user_id)
    print(f"✅ User profile created/loaded")
    print(f"   User ID: {context['user_id']}")
    print(f"   Interaction count: {context['interaction_count']}")
except Exception as e:
    print(f"❌ Failed to create user profile: {e}")
    sys.exit(1)
print()

# Test 3: Update Traits
print("Test 3: Update User Traits")
print("-" * 70)

analysis = {
    'primary_emotion': 'anxiety',
    'intensity': 8,
    'relationship': 'authority',
    'conflict_risk': 'high',
    'user_need': 'advice'
}

policy = {
    'mode': 'diplomatic_advisor',
    'tone': 'calm_reassuring',
    'humor_level': 0
}

try:
    result = update_user_traits(test_user_id, analysis, policy)
    if result:
        print("✅ Traits updated successfully")
    else:
        print("⚠️  No traits identified (might be normal)")
except Exception as e:
    print(f"❌ Failed to update traits: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# Test 4: Verify Traits Saved
print("Test 4: Verify Traits Were Saved")
print("-" * 70)

try:
    traits = get_user_traits(test_user_id)
    if traits:
        print(f"✅ Traits saved and retrieved: {traits}")
    else:
        print("⚠️  No traits found (check if any were identified)")
except Exception as e:
    print(f"❌ Failed to retrieve traits: {e}")
    sys.exit(1)
print()

# Test 5: Direct MongoDB Check
print("Test 5: Direct MongoDB Verification")
print("-" * 70)

try:
    from persona.db import get_users_collection
    users = get_users_collection()

    if users is None:
        print("❌ Users collection is None!")
        sys.exit(1)

    user_doc = users.find_one({"user_id": test_user_id})

    if user_doc:
        print("✅ User document found in MongoDB:")
        print(f"   User ID: {user_doc.get('user_id')}")
        print(f"   Learned patterns: {user_doc.get('learned_patterns', [])}")
        print(f"   Interaction count: {user_doc.get('interaction_count', 0)}")
        print(f"   Last updated: {user_doc.get('last_updated')}")
    else:
        print("❌ User document NOT found in MongoDB!")
        print("   Data is NOT being saved!")
        sys.exit(1)

except Exception as e:
    print(f"❌ Direct MongoDB check failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
print()

# Test 6: Multiple Updates
print("Test 6: Multiple Trait Updates")
print("-" * 70)

for i in range(3):
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

    update_user_traits(test_user_id, analysis2, policy2)

print("✅ Multiple updates completed")

final_traits = get_user_traits(test_user_id)
print(f"✅ Final traits: {final_traits}")
print()

# Final Verification
print("=" * 70)
print("FINAL VERIFICATION")
print("=" * 70)

user_doc = users.find_one({"user_id": test_user_id})
if user_doc and user_doc.get('learned_patterns'):
    print("✅ SUCCESS! Data is being saved to MongoDB!")
    print()
    print("Saved data:")
    print(f"  - User ID: {user_doc['user_id']}")
    print(f"  - Traits: {user_doc.get('learned_patterns', [])}")
    print(f"  - Interactions: {user_doc.get('interaction_count', 0)}")
    print()
    print("MongoDB persistence is working correctly! 🎉")
else:
    print("❌ FAILED! Data is NOT being saved!")
    print()
    print("Possible issues:")
    print("  - MongoDB connection not persistent")
    print("  - Write operations failing silently")
    print("  - Database permissions issue")

print("=" * 70)

