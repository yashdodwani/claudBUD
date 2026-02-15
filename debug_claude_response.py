#!/usr/bin/env python3
"""
Debug script to see what Claude Sonnet 4.5 actually returns
"""

import sys
import os
sys.path.insert(0, '/home/voyager4/projects/claudBUD/src')

from anthropic import Anthropic
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv()

# Load prompt
prompt_path = Path('src/policy_engine/behavior_policy_prompt.txt')
with open(prompt_path, 'r') as f:
    system_prompt = f.read()

# Test context
context = {
    "user_message": "Boss yelled at me in meeting",
    "emotion": "frustrated",
    "situation": "workplace_conflict"
}

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("=" * 70)
print("Testing Claude Sonnet 4.5 Response")
print("=" * 70)
print()
print("System Prompt:")
print(system_prompt)
print()
print("=" * 70)
print("User Context:")
print(json.dumps(context, indent=2))
print()
print("=" * 70)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=500,
    system=system_prompt,
    messages=[
        {
            "role": "user",
            "content": f"Context:\n{json.dumps(context, indent=2)}"
        }
    ]
)

response_text = message.content[0].text.strip()

print("Raw Response:")
print(response_text)
print()
print("=" * 70)

# Try to parse it
if response_text.startswith("```"):
    lines = response_text.split("\n")
    response_text = "\n".join(lines[1:-1])

try:
    parsed = json.loads(response_text)
    print("Parsed JSON:")
    print(json.dumps(parsed, indent=2))
except Exception as e:
    print(f"Failed to parse: {e}")

