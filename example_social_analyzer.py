#!/usr/bin/env python3
"""
Example: Using analyze_social_context() function

Demonstrates social and emotional signal extraction.
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from extractors import analyze_social_context
from dotenv import load_dotenv


def main():
    # Load API key
    load_dotenv()

    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️  OPENROUTER_API_KEY not set!")
        return

    print("=" * 70)
    print("🔍 Social Context Analyzer - Example")
    print("=" * 70)
    print()

    # Example message
    message = "Bhai my manager just gave me negative feedback in front of the whole team. I know I messed up but doing it publicly was so humiliating. I don't know how to face everyone tomorrow."

    print("📝 User Message:")
    print(f'   "{message}"')
    print()
    print("🔄 Analyzing social context...")
    print()

    # Analyze
    analysis = analyze_social_context(message)

    print("✅ Social Analysis Results:")
    print()
    print(f"   Emotion:         {analysis.primary_emotion} (intensity: {analysis.intensity}/10)")
    print(f"   User Need:       {analysis.user_need}")
    print(f"   Relationship:    {analysis.relationship}")
    print(f"   Conflict Risk:   {analysis.conflict_risk}")
    print()

    print("📋 JSON Output:")
    print(analysis.model_dump_json(indent=2))
    print()

    print("=" * 70)
    print("💡 Interpretation:")
    print("=" * 70)

    if analysis.primary_emotion in ["anger", "frustration"]:
        print("😤 User is upset - needs validation first")
    elif analysis.primary_emotion == "anxiety":
        print("😰 User is stressed - needs reassurance")
    elif analysis.primary_emotion == "sadness":
        print("😢 User is hurt - needs empathy")

    if analysis.relationship == "authority":
        print("👔 Authority relationship - be diplomatic")

    if analysis.conflict_risk == "high":
        print("⚠️  High conflict risk - suggest careful approach")

    if analysis.user_need == "vent":
        print("🗣️  Let them vent - don't jump to solutions")
    elif analysis.user_need == "advice":
        print("💡 They want concrete solutions")
    elif analysis.user_need == "reassurance":
        print("🤗 They need validation and comfort")

    print()


if __name__ == "__main__":
    main()

