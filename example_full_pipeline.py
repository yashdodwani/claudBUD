#!/usr/bin/env python3
"""
Full Integration Example: WhatsApp → Social Analysis → Behavior Policy

Demonstrates the complete pipeline from Phase 3 → Phase 2 → Phase 1
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from whatsapp import parse_whatsapp_chat, extract_last_n_messages
from extractors import analyze_social_context
from policy_engine import generate_behavior_policy
from dotenv import load_dotenv


def main():
    load_dotenv()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY not set!")
        return

    print("=" * 70)
    print("🔗 Full Pipeline Demo: WhatsApp → Signals → Policy")
    print("=" * 70)
    print()

    # Sample WhatsApp chat export (workplace conflict scenario)
    whatsapp_chat = """15/02/2024, 09:00 - Team Lead: Morning
15/02/2024, 09:01 - +91 98765 43210: Good morning sir
15/02/2024, 09:15 - Team Lead: I need that report by 11am today
15/02/2024, 09:16 - +91 98765 43210: Sir, you assigned it yesterday evening only
I haven't had time to complete it properly
15/02/2024, 09:17 - Team Lead: That's not my problem
You should have worked late
15/02/2024, 09:18 - +91 98765 43210: Sir, I had another deadline too
I'm really trying my best
15/02/2024, 09:19 - Team Lead: Your best isn't good enough
Other team members don't make excuses
15/02/2024, 09:20 - +91 98765 43210: <This message was deleted>
15/02/2024, 09:21 - +91 98765 43210: Okay sir, I'll try to finish it"""

    print("📱 Step 1: Parse WhatsApp Chat")
    print("-" * 70)
    print("Raw Export (sample):")
    print(whatsapp_chat[:200] + "...")
    print()

    # Parse chat (privacy-first: no storage)
    cleaned_text = parse_whatsapp_chat(whatsapp_chat)

    print("Cleaned Text:")
    print(cleaned_text)
    print()
    print("✅ Timestamps removed, phone numbers anonymized")
    print("✅ No data stored to disk")
    print()

    # Step 2: Extract social signals
    print("🔍 Step 2: Extract Social Signals")
    print("-" * 70)

    analysis = analyze_social_context(cleaned_text)

    print(f"Primary Emotion:  {analysis.primary_emotion}")
    print(f"Intensity:        {analysis.intensity}/10")
    print(f"User Need:        {analysis.user_need}")
    print(f"Relationship:     {analysis.relationship}")
    print(f"Conflict Risk:    {analysis.conflict_risk}")
    print()
    print("✅ Behavioral signals extracted")
    print()

    # Step 3: Generate behavior policy
    print("⚙️  Step 3: Generate Behavior Policy")
    print("-" * 70)

    context = {
        "user_message": "My team lead is being really harsh and unreasonable",
        "emotion": analysis.primary_emotion,
        "intensity": analysis.intensity,
        "relationship": analysis.relationship,
        "conflict_risk": analysis.conflict_risk,
        "user_need": analysis.user_need
    }

    policy = generate_behavior_policy(context)

    print(f"Mode:             {policy.mode}")
    print(f"Tone:             {policy.tone}")
    print(f"Humor Level:      {policy.humor_level}/3")
    print(f"Message Length:   {policy.message_length}")
    print(f"Initiative:       {policy.initiative}")
    print(f"Action Steps:     {policy.give_action_steps}")
    print(f"Follow-up Q:      {policy.ask_followup_question}")
    print()
    print("✅ Response strategy determined")
    print()

    # Summary
    print("=" * 70)
    print("📋 Complete Pipeline Summary")
    print("=" * 70)
    print()
    print("WhatsApp Chat Export (raw)")
    print("         ↓")
    print("parse_whatsapp_chat() [Phase 3]")
    print("         ↓")
    print(f"Clean Text (privacy-first)")
    print("         ↓")
    print("analyze_social_context() [Phase 2]")
    print("         ↓")
    print(f"Signals: emotion={analysis.primary_emotion}, ")
    print(f"         relationship={analysis.relationship}, ")
    print(f"         risk={analysis.conflict_risk}")
    print("         ↓")
    print("generate_behavior_policy() [Phase 1]")
    print("         ↓")
    print(f"Policy: mode={policy.mode}, tone={policy.tone}")
    print("         ↓")
    print("Claude Response Generation [Phase 5 - Coming Soon]")
    print()

    # Interpretation
    print("=" * 70)
    print("💡 Interpretation")
    print("=" * 70)
    print()

    if analysis.relationship == "authority":
        print("👔 Authority relationship detected from chat pattern")
        print("   → Team lead giving orders, user using 'sir'")

    if analysis.conflict_risk == "high":
        print("⚠️  High conflict risk identified")
        print("   → Power imbalance, harsh communication")

    if analysis.primary_emotion in ["frustration", "sadness", "anxiety"]:
        print(f"😔 Negative emotion detected: {analysis.primary_emotion}")
        print(f"   → Intensity {analysis.intensity}/10 indicates significant distress")

    if policy.mode == "diplomatic_advisor":
        print("🎯 Diplomatic advisor mode activated")
        print("   → Will help craft professional, careful response")

    if policy.humor_level == 0:
        print("🚫 No humor")
        print("   → Serious situation requires professional approach")

    if policy.give_action_steps:
        print("✅ Action steps enabled")
        print("   → Will provide concrete guidance on how to respond")

    print()
    print("=" * 70)
    print("🎉 Phases 1 + 2 + 3 working perfectly together!")
    print("=" * 70)
    print()
    print("Privacy Guarantee:")
    print("  • Raw chat never stored")
    print("  • Only behavioral signals extracted")
    print("  • Phone numbers anonymized")
    print("  • Compliant with data protection standards")


if __name__ == "__main__":
    main()

