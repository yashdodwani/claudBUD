# generate_behavior_policy() Function

## Overview

A standalone function that generates a `BehaviorPolicy` object from a context dictionary using Claude API.

## Signature

```python
def generate_behavior_policy(context: dict) -> BehaviorPolicy
```

## What It Does

1. ✅ Takes a context dictionary with user information
2. ✅ Calls Claude API with the behavior policy system prompt
3. ✅ Passes context as formatted JSON
4. ✅ Parses Claude's JSON response
5. ✅ Returns validated BehaviorPolicy object
6. ✅ **Automatically falls back to `chill_companion` if parsing fails**

## Parameters

**context** (dict): Dictionary containing user context

### Supported Context Keys:

- `user_message` (str) - The user's message
- `emotion` (str) - Detected emotion (e.g., "frustrated", "anxious")
- `relationship` (str) - Relationship context (e.g., "manager_employee")
- `situation` (str) - Situation type (e.g., "workplace_conflict", "boredom")
- Any other custom context fields

## Returns

`BehaviorPolicy` object with these fields:
- `mode`: Interaction mode
- `tone`: Response tone
- `humor_level`: 0-3 scale
- `message_length`: short/medium/long
- `initiative`: low/medium/high
- `give_action_steps`: boolean
- `ask_followup_question`: boolean

## Fallback Behavior

If Claude API fails or returns invalid JSON, the function **automatically returns a safe default**:

```python
BehaviorPolicy(
    mode="chill_companion",
    tone="casual_supportive",
    humor_level=1,
    message_length="medium",
    initiative="medium",
    give_action_steps=False,
    ask_followup_question=True
)
```

This ensures your application never crashes due to API issues.

## Requirements

- `ANTHROPIC_API_KEY` must be set in environment variables
- Claude API access

## Usage Examples

### Example 1: Basic Usage

```python
from policy_engine import generate_behavior_policy

context = {
    "user_message": "My boss yelled at me. Need to reply professionally.",
    "emotion": "frustrated",
    "situation": "workplace_conflict"
}

policy = generate_behavior_policy(context)
print(policy.mode)  # diplomatic_advisor
print(policy.tone)  # calm_reassuring
```

### Example 2: Minimal Context

```python
# Works even with minimal information
context = {
    "user_message": "I'm bored"
}

policy = generate_behavior_policy(context)
print(policy.mode)  # chill_companion
```

### Example 3: Rich Context

```python
context = {
    "user_message": "Team lead assigned 5 tasks when I'm drowning",
    "emotion": "stressed",
    "relationship": "team_lead_member",
    "situation": "work_overload",
    "time_of_day": "late_evening",
    "urgency": "high"
}

policy = generate_behavior_policy(context)
# Claude will consider all context to make the best decision
```

### Example 4: Error Handling

```python
try:
    policy = generate_behavior_policy(context)
    # Policy is guaranteed to be valid
    # Either from Claude or from fallback
except ValueError as e:
    # Only raises if ANTHROPIC_API_KEY is missing
    print(f"API key error: {e}")
```

## Comparison with PolicyDecider Class

| Feature | `generate_behavior_policy()` | `PolicyDecider` class |
|---------|----------------------------|---------------------|
| API calls | One-shot function | Reusable instance |
| State | Stateless | Maintains client |
| Usage | Simple, direct | Object-oriented |
| Best for | Quick generation | Multiple calls |
| Fallback | Automatic | Manual handling |

### When to Use Each

**Use `generate_behavior_policy()`:**
- One-off policy generation
- Simple scripts
- Maximum convenience
- Automatic error handling

**Use `PolicyDecider` class:**
- Making many policy decisions
- Need more control
- Custom error handling
- Class-based architecture

## Testing

Run the test suite:

```bash
source venv/bin/activate

# Run tests
python tests/test_generate_behavior_policy.py

# Run example
python example_generate_policy.py
```

## Code Location

- **Function**: `src/policy_engine/decider.py`
- **Export**: `src/policy_engine/__init__.py`
- **Import**: `from policy_engine import generate_behavior_policy`

## Error Messages

**ValueError**: "ANTHROPIC_API_KEY not found in environment"
- **Solution**: Set the API key in your `.env` file

**Warning**: "Failed to generate policy (error). Using fallback."
- **Meaning**: Claude API call failed, using safe default
- **Action**: No action needed, fallback is safe

## Performance

- **Typical latency**: 1-3 seconds (depends on Claude API)
- **Fallback latency**: Instant (no API call)
- **Max tokens**: 500 (sufficient for policy JSON)

## Privacy & Security

✅ **No data storage**: Function is stateless, nothing persisted
✅ **API key safety**: Read from environment, never hardcoded
✅ **Context privacy**: Only sent to Claude API for analysis

## Integration Example

```python
# In your main application
from policy_engine import generate_behavior_policy
from anthropic import Anthropic
import os

def respond_to_user(user_message: str, user_context: dict):
    """Generate a contextually appropriate response"""
    
    # Step 1: Generate policy
    context = {
        "user_message": user_message,
        **user_context  # Include emotion, situation, etc.
    }
    
    policy = generate_behavior_policy(context)
    
    # Step 2: Use policy to generate response
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        system=f"""You are Buddy, a friendly Indian AI companion.
        
Response behavior:
- Mode: {policy.mode}
- Tone: {policy.tone}
- Humor level: {policy.humor_level}/3
- Length: {policy.message_length}
- Give action steps: {policy.give_action_steps}
- Ask follow-up: {policy.ask_followup_question}

Respond accordingly.""",
        messages=[{"role": "user", "content": user_message}]
    )
    
    return response.content[0].text

# Usage
response = respond_to_user(
    "My manager criticized me publicly",
    {"emotion": "frustrated", "situation": "workplace_conflict"}
)
```

---

**Status**: ✅ Function complete and tested
**Location**: `src/policy_engine/decider.py`
**Exported**: Yes, via `__init__.py`

