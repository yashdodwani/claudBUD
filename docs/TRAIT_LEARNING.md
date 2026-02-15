# User Trait Learning System

**Privacy-First Behavioral Pattern Learning**

## Overview

The trait learning system helps Buddy understand user preferences by analyzing **behavioral signals only** - never storing raw messages or conversation content.

## How It Works

### Signal → Trait Mapping

```python
from persona import update_user_traits

# After analyzing a message
update_user_traits(
    user_id="user_123",
    analysis={
        'primary_emotion': 'anxiety',
        'intensity': 8,
        'relationship': 'authority',
        'conflict_risk': 'high',
        'user_need': 'advice'
    },
    policy={
        'mode': 'diplomatic_advisor',
        'tone': 'calm_reassuring',
        'humor_level': 0
    }
)
```

### Trait Patterns

| Signal Pattern | Trait Learned | Impact |
|----------------|---------------|--------|
| `relationship='authority'` + `conflict_risk='high'` | `avoids_conflict` | Buddy uses more diplomatic approach |
| `mode='venting_listener'` or `user_need='vent'` | `needs_validation` | Buddy validates emotions before advice |
| `emotion='anxiety'` + `intensity >= 7` | `reassurance_seeking` | Buddy provides more reassurance |
| `emotion='anxiety'` + `intensity >= 8` | `high_anxiety_baseline` | Buddy uses consistently calm tone |
| `humor_level >= 2` + positive emotions | `humor_responsive` | Buddy can use more humor |
| `user_need='advice'` or `mode='practical_helper'` | `solution_oriented` | Buddy focuses on actionable steps |
| `user_need='reassurance'` or `'validation'` | `needs_emotional_support` | Empathy before solutions |
| `relationship='authority'` + negative emotions | `workplace_stress_prone` | Sensitive to work issues |

## What's Stored

### Memory Summaries Collection

```json
{
  "user_id": "user_123",
  "timestamp": "2026-02-15T10:30:00Z",
  "traits_identified": [
    "avoids_conflict",
    "reassurance_seeking",
    "workplace_stress_prone"
  ],
  "signals": {
    "emotion": "anxiety",
    "intensity": 8,
    "relationship": "authority",
    "conflict_risk": "high",
    "user_need": "advice",
    "mode": "diplomatic_advisor"
  },
  "type": "trait_update"
}
```

### User Profile (learned_patterns field)

```json
{
  "user_id": "user_123",
  "learned_patterns": [
    "avoids_conflict",
    "needs_validation",
    "reassurance_seeking",
    "workplace_stress_prone"
  ],
  "last_updated": "2026-02-15T10:30:00Z"
}
```

## What's NOT Stored

❌ **Raw message content**  
❌ **Conversation text**  
❌ **Personal details**  
❌ **Specific situations described**

✅ **Only behavioral signals and patterns**

## Usage

### Basic Trait Learning

```python
from extractors import analyze_social_context
from policy_engine import generate_behavior_policy
from persona import update_user_traits, get_user_traits

# User message arrives
user_message = "Boss criticized my work in meeting"
user_id = "user_123"

# Extract signals
analysis = analyze_social_context(user_message)

# Generate policy
policy = generate_behavior_policy({
    "user_message": user_message,
    "emotion": analysis.primary_emotion,
    "relationship": analysis.relationship
})

# Learn traits (NO message content stored!)
update_user_traits(
    user_id=user_id,
    analysis=analysis.model_dump(),
    policy=policy.model_dump()
)

# Get learned traits
traits = get_user_traits(user_id)
print(traits)  # ['avoids_conflict', 'workplace_stress_prone', ...]
```

### Integration with Complete System

```python
from extractors import analyze_social_context
from policy_engine import generate_behavior_policy
from rag import find_relevant_knowledge
from composer import generate_reply
from persona import update_user_traits, load_user_context

# 1. Analyze
analysis = analyze_social_context(user_message)

# 2. Generate policy
policy = generate_behavior_policy({...})

# 3. Learn traits
update_user_traits(user_id, analysis.model_dump(), policy.model_dump())

# 4. Load context (includes learned traits)
user_context = load_user_context(user_id)

# 5. Retrieve knowledge
knowledge = find_relevant_knowledge(user_message, analysis.model_dump())

# 6. Generate personalized response
response = generate_reply(
    user_input=user_message,
    analysis=analysis,
    policy=policy,
    rag_knowledge=knowledge,
    persona=user_context  # Includes learned traits!
)
```

## Benefits Over Time

### After 5 Interactions

```python
traits = get_user_traits("user_123")
# ['avoids_conflict', 'needs_validation']
```

Buddy learns:
- User prefers diplomatic approach
- Needs emotional validation

### After 20 Interactions

```python
traits = get_user_traits("user_123")
# ['avoids_conflict', 'needs_validation', 'workplace_stress_prone', 
#  'reassurance_seeking', 'solution_oriented']
```

Buddy now knows:
- User's core communication style
- Common stress patterns
- Preferred support type
- Response style preferences

### Result

Responses become more personalized without storing any conversation content!

## Privacy Guarantees

### GDPR Compliant

- ✅ Only behavioral metadata stored
- ✅ No PII in trait data
- ✅ User can be deleted (right to be forgotten)
- ✅ Transparent data collection

### Data Minimization

```python
# What we could store (but DON'T):
{
  "message": "Boss criticized my work...",  # ❌ NOT STORED
  "full_conversation": [...],  # ❌ NOT STORED
  "personal_details": {...}  # ❌ NOT STORED
}

# What we actually store:
{
  "traits_identified": ["avoids_conflict"],  # ✅ Behavioral pattern only
  "signals": {
    "emotion": "anxiety",  # ✅ Signal only
    "relationship": "authority"  # ✅ Context only
  }
}
```

## API Reference

### update_user_traits(user_id, analysis, policy) → bool

Updates user traits based on behavioral signals.

**Parameters:**
- `user_id` (str): User identifier
- `analysis` (dict): Social analysis from `analyze_social_context()`
- `policy` (dict): Behavior policy from `generate_behavior_policy()`

**Returns:** `True` if traits were updated

**Side Effects:**
- Updates `learned_patterns` in user profile
- Creates entry in `memory_summaries` collection
- Does NOT store raw message content

### get_user_traits(user_id) → list

Gets learned traits for a user.

**Parameters:**
- `user_id` (str): User identifier

**Returns:** List of trait strings

**Example:**
```python
traits = get_user_traits("user_123")
# ['avoids_conflict', 'needs_validation', 'reassurance_seeking']
```

## Collections Used

### users
Stores user profiles with `learned_patterns` field

### memory_summaries
Stores trait learning events (signals only, no messages)

## Testing

```bash
# Test trait learning
python tests/test_trait_learning.py

# Example with full system
python example_trait_learning.py
```

## Performance

- **Learning Time**: Instant (single DB write)
- **Trait Matching**: O(n) where n = number of signal rules
- **Storage**: Minimal (~200 bytes per trait update)
- **Privacy**: Maximum (zero message content)

## Future Enhancements

Potential additions:
- Trait confidence scores
- Trait decay over time (old patterns fade)
- Multi-trait combinations
- Automatic trait-based policy adjustments

## Example Scenario

```
User: "My team lead keeps giving me more work when I'm already overloaded"

Signals Extracted:
  emotion: frustration
  intensity: 6
  relationship: authority
  conflict_risk: high
  user_need: advice

Traits Learned:
  ✅ avoids_conflict (authority + conflict_risk)
  ✅ workplace_stress_prone (authority + frustration)
  ✅ solution_oriented (user_need: advice)

Stored:
  ✅ Traits: ['avoids_conflict', 'workplace_stress_prone', 'solution_oriented']
  ✅ Signals: {emotion: 'frustration', relationship: 'authority', ...}
  ❌ Message: NOT STORED

Result:
  Next time user has workplace stress, Buddy will:
  - Use diplomatic approach (avoids_conflict)
  - Be sensitive to work issues (workplace_stress_prone)
  - Provide actionable solutions (solution_oriented)
```

---

**Status**: Fully implemented  
**Privacy**: First-class  
**Storage**: Signals only, no messages  
**Learning**: Automatic and continuous

