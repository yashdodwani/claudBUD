"""
Test BehaviorPolicy Pydantic model
"""

import sys
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from policy_engine.models import BehaviorPolicy


def test_behavior_policy_creation():
    """Test creating a BehaviorPolicy instance"""

    # Example: Workplace conflict scenario
    policy = BehaviorPolicy(
        mode="diplomatic_advisor",
        tone="calm_reassuring",
        humor_level=0,
        message_length="medium",
        initiative="medium",
        give_action_steps=True,
        ask_followup_question=False
    )

    print("✓ Workplace Conflict Policy:")
    print(f"  Mode: {policy.mode}")
    print(f"  Tone: {policy.tone}")
    print(f"  Humor: {policy.humor_level}/3")
    print(f"  Length: {policy.message_length}")
    print(f"  Initiative: {policy.initiative}")
    print(f"  Action steps: {policy.give_action_steps}")
    print(f"  Follow-up Q: {policy.ask_followup_question}")
    print()

    # Example: Casual boredom
    policy2 = BehaviorPolicy(
        mode="chill_companion",
        tone="light_humor",
        humor_level=2,
        message_length="short",
        initiative="high",
        give_action_steps=False,
        ask_followup_question=True
    )

    print("✓ Casual Boredom Policy:")
    print(f"  Mode: {policy2.mode}")
    print(f"  Tone: {policy2.tone}")
    print(f"  Humor: {policy2.humor_level}/3")
    print(f"  Length: {policy2.message_length}")
    print(f"  Initiative: {policy2.initiative}")
    print(f"  Action steps: {policy2.give_action_steps}")
    print(f"  Follow-up Q: {policy2.ask_followup_question}")
    print()

    # Example: Venting after bad day
    policy3 = BehaviorPolicy(
        mode="venting_listener",
        tone="serious_care",
        humor_level=0,
        message_length="short",
        initiative="low",
        give_action_steps=False,
        ask_followup_question=False
    )

    print("✓ Venting Support Policy:")
    print(f"  Mode: {policy3.mode}")
    print(f"  Tone: {policy3.tone}")
    print(f"  Humor: {policy3.humor_level}/3")
    print(f"  Length: {policy3.message_length}")
    print(f"  Initiative: {policy3.initiative}")
    print(f"  Action steps: {policy3.give_action_steps}")
    print(f"  Follow-up Q: {policy3.ask_followup_question}")
    print()

    # Test JSON serialization
    print("✓ JSON Export:")
    print(policy.model_dump_json(indent=2))
    print()

    print("✅ All tests passed!")


if __name__ == "__main__":
    test_behavior_policy_creation()

