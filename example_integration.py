#!/usr/bin/env python3
"""
Integration Example: Phase 1 + Phase 2

Demonstrates how social analysis feeds into behavior policy generation.
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from extractors import analyze_social_context
from policy_engine import generate_behavior_policy
from dotenv import load_dotenv


def main():
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set!")
        return

    print("=" * 70)
    print("🤖 Buddy - Phase 1 + Phase 2 Integration")
    print("=" * 70)
    print()

    # Example user message
    message = "Yaar my boss just publicly criticized my work in the team meeting. Everyone was there. I'm so embarrassed and angry. I need to respond to his email but I don't know what to say."

    print("📝 User Message:")
    print(f'   "{message}"')
    print()

    # Step 1: Extract social signals
    print("🔍 Step 1: Extracting Social Signals...")
    print()

    analysis = analyze_social_context(message)

    print("   ✅ Social Analysis:")
    print(f"      Emotion:       {analysis.primary_emotion} ({analysis.intensity}/10)")
    print(f"      Need:          {analysis.user_need}")
    print(f"      Relationship:  {analysis.relationship}")
    print(f"      Conflict Risk: {analysis.conflict_risk}")
    print()

    # Step 2: Generate behavior policy
    print("⚙️  Step 2: Generating Behavior Policy...")
    print()

    # Build context from social analysis
    context = {
        "user_message": message,
        "emotion": analysis.primary_emotion,
        "intensity": analysis.intensity,
        "user_need": analysis.user_need,
        "relationship": analysis.relationship,
        "conflict_risk": analysis.conflict_risk
    }

    policy = generate_behavior_policy(context)

    print("   ✅ Behavior Policy:")
    print(f"      Mode:           {policy.mode}")
    print(f"      Tone:           {policy.tone}")
    print(f"      Humor Level:    {policy.humor_level}/3")
    print(f"      Message Length: {policy.message_length}")
    print(f"      Initiative:     {policy.initiative}")
    print(f"      Action Steps:   {policy.give_action_steps}")
    print(f"      Follow-up Q:    {policy.ask_followup_question}")
    print()

    # Step 3: Explain the decision
    print("=" * 70)
    print("💡 Why This Policy?")
    print("=" * 70)
    print()

    if analysis.relationship == "authority":
        print("👔 Authority relationship detected → diplomatic approach")

    if analysis.conflict_risk == "high":
        print("⚠️  High conflict risk → careful, professional tone")

    if analysis.primary_emotion in ["anger", "frustration"]:
        print("😤 Strong negative emotion → calm reassuring tone")

    if analysis.user_need == "vent":
        print("🗣️  Needs to vent → low initiative, let them talk")
    elif analysis.user_need == "advice":
        print("💡 Needs advice → provide action steps")

    if policy.humor_level == 0:
        print("🚫 No humor → serious situation requires professional response")

    print()
    print("=" * 70)
    print("📋 Complete Pipeline:")
    print("=" * 70)
    print()
    print("User Message")
    print("     ↓")
    print(f"Social Analysis (emotion={analysis.primary_emotion}, need={analysis.user_need})")
    print("     ↓")
    print(f"Behavior Policy (mode={policy.mode}, tone={policy.tone})")
    print("     ↓")
    print("Claude Response (coming in Phase 5)")
    print()
    print("=" * 70)
    print("✅ Phase 1 + Phase 2 working perfectly together!")
    print("=" * 70)


if __name__ == "__main__":
    main()

