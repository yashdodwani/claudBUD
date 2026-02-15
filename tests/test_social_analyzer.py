"""
Test analyze_social_context function

Tests the social and emotional signal extractor.
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from extractors import analyze_social_context
from dotenv import load_dotenv


def test_analyze_social_context():
    """Test social context analyzer with various scenarios"""

    # Load environment
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not found in environment")
        return

    print("=" * 70)
    print("Testing analyze_social_context()")
    print("=" * 70)
    print()

    # Test scenarios
    scenarios = [
        {
            "name": "Workplace Anger",
            "text": "My boss just yelled at me in front of everyone. I'm so pissed off."
        },
        {
            "name": "Bored Waiting",
            "text": "Stuck at the airport for 3 hours. Nothing to do. So bored."
        },
        {
            "name": "Need Advice",
            "text": "My team lead keeps giving me more work. How do I say no without sounding lazy?"
        },
        {
            "name": "Venting Frustration",
            "text": "Bhai everything went wrong today. First the train, then the meeting, now this. Can't catch a break."
        },
        {
            "name": "Anxious Decision",
            "text": "I have to choose between two job offers and I'm so stressed. What if I pick the wrong one?"
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"Test {i}: {scenario['name']}")
        print("-" * 70)
        print(f"Text: \"{scenario['text']}\"")
        print()

        try:
            analysis = analyze_social_context(scenario['text'])

            print("✅ Social Analysis:")
            print(f"   Primary Emotion:  {analysis.primary_emotion}")
            print(f"   Intensity:        {analysis.intensity}/10")
            print(f"   User Need:        {analysis.user_need}")
            print(f"   Relationship:     {analysis.relationship}")
            print(f"   Conflict Risk:    {analysis.conflict_risk}")
            print()

            # JSON output
            print(f"   JSON: {analysis.model_dump_json()}")
            print()

        except Exception as e:
            print(f"❌ Error: {e}")
            print()

        print()

    print("=" * 70)
    print("✅ All tests complete!")
    print("=" * 70)


if __name__ == "__main__":
    test_analyze_social_context()

