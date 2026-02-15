"""
Test RAG Retrieval

Tests the behavior knowledge retrieval system.
"""

import sys
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from rag import retrieve_behavior_knowledge, get_all_scenarios, find_relevant_knowledge


def test_basic_retrieval():
    """Test basic knowledge retrieval"""

    print("=" * 70)
    print("Test 1: Basic Retrieval")
    print("=" * 70)
    print()

    # Test office stress scenario
    knowledge = retrieve_behavior_knowledge("office stress work")

    if knowledge:
        print("✅ Retrieved knowledge for 'office stress work':")
        print(f"   Scenario: {knowledge.get('scenario', 'N/A')}")
        print(f"   Emotions: {knowledge.get('typical_emotions', [])}")
        print(f"   Do's: {knowledge.get('do', [])[:3]}")
        print(f"   Don'ts: {knowledge.get('dont', [])[:3]}")
        print(f"   Humor Allowed: {knowledge.get('humor_allowed', False)}")
    else:
        print("❌ No knowledge retrieved")

    print()


def test_exam_stress():
    """Test exam stress retrieval"""

    print("=" * 70)
    print("Test 2: Exam Stress")
    print("=" * 70)
    print()

    knowledge = retrieve_behavior_knowledge("exam stress anxiety")

    if knowledge:
        print("✅ Retrieved knowledge for 'exam stress':")
        print(f"   Scenario: {knowledge.get('scenario', 'N/A')}")
        print(f"   Typical Emotions: {', '.join(knowledge.get('typical_emotions', []))}")
        print(f"   Tone: {knowledge.get('tone', 'N/A')}")
        print()
        print("   DO:")
        for item in knowledge.get('do', [])[:3]:
            print(f"      - {item}")
        print()
        print("   DON'T:")
        for item in knowledge.get('dont', [])[:3]:
            print(f"      - {item}")
    else:
        print("❌ No knowledge retrieved")

    print()


def test_list_scenarios():
    """Test listing all available scenarios"""

    print("=" * 70)
    print("Test 3: Available Scenarios")
    print("=" * 70)
    print()

    scenarios = get_all_scenarios()

    print(f"Found {len(scenarios)} scenarios:")
    print()

    # Show first 10
    for i, scenario in enumerate(scenarios[:10], 1):
        print(f"   {i}. {scenario}")

    if len(scenarios) > 10:
        print(f"   ... and {len(scenarios) - 10} more")

    print()


def test_with_social_analysis():
    """Test retrieval with social analysis"""

    print("=" * 70)
    print("Test 4: Retrieval with Social Analysis")
    print("=" * 70)
    print()

    # Simulate social analysis
    social_analysis = {
        'primary_emotion': 'frustrated',
        'relationship': 'authority',
        'user_need': 'advice'
    }

    user_message = "My boss keeps giving me impossible deadlines"

    knowledge = find_relevant_knowledge(user_message, social_analysis)

    if knowledge:
        print(f"✅ Retrieved knowledge for workplace scenario:")
        print(f"   Message: \"{user_message}\"")
        print(f"   Analysis: {social_analysis}")
        print()
        print(f"   Matched Scenario: {knowledge.get('scenario', 'N/A')}")
        print(f"   Action Suggestions: {knowledge.get('action_suggestions', [])[:3]}")
    else:
        print("❌ No knowledge retrieved")

    print()


def test_fallback():
    """Test fallback for unknown scenario"""

    print("=" * 70)
    print("Test 5: Fallback for Unknown Scenario")
    print("=" * 70)
    print()

    knowledge = retrieve_behavior_knowledge("totally unknown scenario xyz")

    if not knowledge:
        print("✅ Correctly returned empty dict for unknown scenario")
    else:
        print(f"⚠️  Got some match: {knowledge.get('scenario', 'N/A')}")

    print()


if __name__ == "__main__":
    test_basic_retrieval()
    test_exam_stress()
    test_list_scenarios()
    test_with_social_analysis()
    test_fallback()

    print("=" * 70)
    print("✅ All RAG tests complete!")
    print("=" * 70)

