# Adaptive Learning System

**Complete Learning & Memory System**

## Overview

Buddy AI now features a complete adaptive learning system that:
1. **Learns** user traits from behavioral signals
2. **Remembers** patterns across interactions
3. **Adapts** responses based on learned preferences
4. **Logs** interactions for continuous improvement

## Complete Flow

```
User Message
    ↓
Extract Signals (analyze_social_context)
    ↓
Generate Policy (generate_behavior_policy)
    ↓
Learn Traits (update_user_traits) ← Stores signals, not message
    ↓
Load Memory (load_user_context) ← Gets learned traits
    ↓
Generate Response (generate_reply with memory) ← MEMORY INJECTED!
    ↓
Log Interaction (log_interaction) ← Track for adaptation
    ↓
Consistent, Personalized Response
```

## Step 1: Memory Injection in Responses

### Updated Function Signature

```python
from composer import generate_reply

response = generate_reply(
    user_input=message,
    analysis=analysis,
    policy=policy,
    rag_knowledge=knowledge,
    memory=memory  # NEW! Injects learned traits
)
```

### What Gets Injected

When `memory` contains learned traits, they're added to the Claude prompt:

```
=== USER PERSONALITY TRAITS ===
Based on past interactions, this user:
- Avoids confrontation, prefers diplomatic approach
- Needs emotional validation before advice
- Seeks reassurance and calm guidance
- Sensitive to workplace stress, be extra supportive

Adapt your tone and approach accordingly to maintain consistency.
```

### Memory Structure

```python
memory = {
    'learned_patterns': [
        'avoids_conflict',
        'needs_validation',
        'reassurance_seeking',
        'workplace_stress_prone'
    ],
    'interaction_count': 47
}
```

## Step 2: Interaction Logging

### log_interaction() Function

```python
from persona import log_interaction

# After sending response
log_interaction(
    user_id="user_123",
    scenario="workplace_conflict",
    emotion="anxiety",
    mode="diplomatic_advisor",
    metadata={
        'response_length': 'medium',
        'humor_level': 0
    }
)
```

### What's Logged

```json
{
  "user_id": "user_123",
  "timestamp": "2026-02-15T10:30:00Z",
  "scenario": "workplace_conflict",
  "emotion": "anxiety",
  "mode": "diplomatic_advisor",
  "metadata": {
    "response_length": "medium",
    "humor_level": 0
  },
  "type": "interaction_log"
}
```

**Privacy**: Only metadata, no message content!

## Step 3: Interaction Statistics

### get_interaction_stats() Function

```python
from persona import get_interaction_stats

stats = get_interaction_stats("user_123")
print(stats)
```

### Output Example

```python
{
    'total_interactions': 47,
    'common_scenarios': ['workplace_conflict', 'exam_stress', 'deadline_panic'],
    'common_emotions': ['anxiety', 'frustration', 'stress'],
    'preferred_modes': ['diplomatic_advisor', 'venting_listener', 'practical_helper'],
    'adaptations_learned': [
        "Buddy learned you prefer diplomatic approaches",
        "Buddy adapted to validate your emotions first",
        "Buddy is extra supportive for work-related stress",
        "Buddy learned you prefer concise replies"
    ]
}
```

## Complete Integration Example

```python
from extractors import analyze_social_context
from policy_engine import generate_behavior_policy
from rag import find_relevant_knowledge
from composer import generate_reply
from persona import (
    update_user_traits,
    load_user_context,
    log_interaction,
    get_interaction_stats
)

# User sends message
user_input = "My manager micromanages everything. So frustrating!"
user_id = "user_123"

# 1. Extract signals
analysis = analyze_social_context(user_input)

# 2. Generate policy
policy = generate_behavior_policy({
    "user_message": user_input,
    "emotion": analysis.primary_emotion,
    "relationship": analysis.relationship
})

# 3. Learn traits (NO message stored)
update_user_traits(user_id, analysis.model_dump(), policy.model_dump())

# 4. Load memory with learned traits
user_context = load_user_context(user_id)
memory = {
    'learned_patterns': user_context.get('learned_patterns', []),
    'interaction_count': user_context.get('interaction_count', 0)
}

# 5. Retrieve knowledge
knowledge = find_relevant_knowledge(user_input, analysis.model_dump())

# 6. Generate response WITH MEMORY INJECTION
response = generate_reply(
    user_input=user_input,
    analysis=analysis,
    policy=policy,
    rag_knowledge=knowledge,
    memory=memory  # ← Traits injected here!
)

# 7. Log interaction for future adaptation
log_interaction(
    user_id=user_id,
    scenario=knowledge.get('scenario', 'general') if knowledge else 'general',
    emotion=analysis.primary_emotion,
    mode=policy.mode,
    metadata={'response_length': policy.message_length}
)

# 8. Show what Buddy learned
stats = get_interaction_stats(user_id)
for adaptation in stats['adaptations_learned']:
    print(f"✅ {adaptation}")
```

## Adaptation Over Time

### After 5 Interactions

```python
stats = get_interaction_stats("user_123")
# {
#     'total_interactions': 5,
#     'adaptations_learned': [
#         "Buddy learned you prefer diplomatic approaches"
#     ]
# }
```

Buddy starts learning basic patterns.

### After 20 Interactions

```python
stats = get_interaction_stats("user_123")
# {
#     'total_interactions': 20,
#     'common_scenarios': ['workplace_conflict', 'exam_stress'],
#     'adaptations_learned': [
#         "Buddy learned you prefer diplomatic approaches",
#         "Buddy adapted to validate your emotions first",
#         "Buddy is extra supportive for work-related stress"
#     ]
# }
```

Buddy understands your communication style and stress patterns.

### After 50 Interactions

```python
stats = get_interaction_stats("user_123")
# {
#     'total_interactions': 50,
#     'common_scenarios': ['workplace_conflict', 'exam_stress', 'deadline_panic'],
#     'common_emotions': ['anxiety', 'frustration'],
#     'preferred_modes': ['diplomatic_advisor', 'venting_listener'],
#     'adaptations_learned': [
#         "Buddy learned you prefer diplomatic approaches",
#         "Buddy adapted to validate your emotions first",
#         "Buddy learned you prefer actionable solutions",
#         "Buddy provides more reassurance based on your patterns",
#         "Buddy is extra supportive for work-related stress",
#         "Buddy learned you prefer concise replies"
#     ]
# }
```

Fully personalized responses!

## Collections Used

### interactions
Stores interaction logs (scenario, emotion, mode)

```json
{
  "user_id": "user_123",
  "timestamp": "2026-02-15T10:30:00Z",
  "scenario": "workplace_conflict",
  "emotion": "anxiety",
  "mode": "diplomatic_advisor",
  "metadata": {...}
}
```

### users
Updated with interaction counts

```json
{
  "user_id": "user_123",
  "learned_patterns": [...],
  "total_interactions": 47,
  "last_interaction": "2026-02-15T10:30:00Z"
}
```

### memory_summaries
Trait learning events

```json
{
  "user_id": "user_123",
  "traits_identified": ["avoids_conflict", ...],
  "signals": {...}
}
```

## Privacy Guarantees

### What's Stored
- ✅ Behavioral signals (emotion, relationship, intensity)
- ✅ Learned traits (avoids_conflict, needs_validation, etc.)
- ✅ Interaction metadata (scenario, mode, timestamp)
- ✅ Statistics (counts, common patterns)

### What's NOT Stored
- ❌ Raw message content
- ❌ Conversation text
- ❌ Personal details
- ❌ Sensitive information

**100% Privacy-First Design**

## API Reference

### generate_reply() - Updated

```python
generate_reply(
    user_input: str,
    analysis: Optional[Any] = None,
    policy: Optional[Any] = None,
    rag_knowledge: Optional[Dict] = None,
    memory: Optional[Dict] = None  # NEW!
) -> str
```

### log_interaction()

```python
log_interaction(
    user_id: str,
    scenario: str,
    emotion: str,
    mode: str,
    metadata: Optional[Dict] = None
) -> bool
```

### get_interaction_stats()

```python
get_interaction_stats(user_id: str) -> Dict[str, Any]
```

Returns:
- `total_interactions`: Count
- `common_scenarios`: Top 3 scenarios
- `common_emotions`: Top 3 emotions
- `preferred_modes`: Top 3 response modes
- `adaptations_learned`: List of learned adaptations

## Testing

```bash
# Test adaptive system
python example_adaptive_system.py
```

## Benefits

### Consistency
- Same user gets consistent tone across interactions
- Buddy remembers preferred communication style

### Personalization
- Responses adapt to individual preferences
- No two users get exactly the same experience

### Privacy
- No message content stored
- Only behavioral patterns tracked

### Learning
- Continuous improvement over time
- Automatic adaptation without manual configuration

## Example Output

```
Interaction #1:
💬 User: "Boss criticized me in meeting"
🧠 Active traits: (none yet, first interaction)
🤖 Buddy: [Standard supportive response]

Interaction #3:
💬 User: "Manager micromanages everything"
🧠 Active traits: avoids_conflict, workplace_stress_prone
🤖 Buddy: [More diplomatic, extra supportive for work stress]

Interaction #10:
💬 User: "Team lead changed requirements again"
🧠 Active traits: avoids_conflict, workplace_stress_prone, needs_validation
🤖 Buddy: [Validates emotions, diplomatic advice, work-stress aware]

Adaptations Learned:
✅ Buddy learned you prefer diplomatic approaches
✅ Buddy is extra supportive for work-related stress
✅ Buddy adapted to validate your emotions first
```

---

**Status**: Fully implemented  
**Privacy**: Maximum (no message storage)  
**Learning**: Automatic and continuous  
**Adaptation**: Real-time based on patterns

