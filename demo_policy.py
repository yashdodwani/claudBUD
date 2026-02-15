#!/usr/bin/env python3
"""
Quick demo of BehaviorPolicy model
Run: python demo_policy.py
"""

import sys
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from policy_engine.models import BehaviorPolicy


def demo():
    print("=" * 60)
    print("BUDDY - Behavior Policy Engine Demo")
    print("=" * 60)
    print()

    scenarios = [
        {
            "name": "🔥 Workplace Conflict",
            "description": "Boss sent angry email, user is stressed",
            "policy": BehaviorPolicy(
                mode="diplomatic_advisor",
                tone="calm_reassuring",
                humor_level=0,
                message_length="medium",
                initiative="medium",
                give_action_steps=True,
                ask_followup_question=False
            )
        },
        {
            "name": "😴 Bored & Waiting",
            "description": "Stuck in train, nothing to do",
            "policy": BehaviorPolicy(
                mode="chill_companion",
                tone="light_humor",
                humor_level=2,
                message_length="short",
                initiative="high",
                give_action_steps=False,
                ask_followup_question=True
            )
        },
        {
            "name": "😤 Need to Vent",
            "description": "Just had terrible day, needs to let it out",
            "policy": BehaviorPolicy(
                mode="venting_listener",
                tone="serious_care",
                humor_level=0,
                message_length="short",
                initiative="low",
                give_action_steps=False,
                ask_followup_question=False
            )
        },
        {
            "name": "💪 Exam Stress",
            "description": "Important exam tomorrow, feeling anxious",
            "policy": BehaviorPolicy(
                mode="motivational_push",
                tone="casual_supportive",
                humor_level=1,
                message_length="medium",
                initiative="high",
                give_action_steps=True,
                ask_followup_question=True
            )
        },
        {
            "name": "🤐 Overwhelmed",
            "description": "Too much happening, just needs presence",
            "policy": BehaviorPolicy(
                mode="silent_support",
                tone="calm_reassuring",
                humor_level=0,
                message_length="short",
                initiative="low",
                give_action_steps=False,
                ask_followup_question=False
            )
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['name']}")
        print(f"   Context: {scenario['description']}")
        print(f"   ───────────────────────────────────")
        p = scenario['policy']
        print(f"   Mode:           {p.mode}")
        print(f"   Tone:           {p.tone}")
        print(f"   Humor:          {'🎭' * p.humor_level if p.humor_level > 0 else '🚫'} ({p.humor_level}/3)")
        print(f"   Length:         {p.message_length}")
        print(f"   Initiative:     {p.initiative}")
        print(f"   Action steps:   {'✅' if p.give_action_steps else '❌'}")
        print(f"   Follow-up Q:    {'✅' if p.ask_followup_question else '❌'}")
        print()

    print("=" * 60)
    print("✅ Phase 1 Complete - BehaviorPolicy Model Ready!")
    print("=" * 60)


if __name__ == "__main__":
    demo()

