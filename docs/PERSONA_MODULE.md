# User Context & Persona Module

**Optional Feature**: Enables user personalization and memory

## Overview

The persona module adds user-specific context and memory to Buddy AI:
- **User Profiles**: Stores preferences and communication style
- **Memory System**: Learns from interactions
- **Personalization**: Adapts responses to individual users

## Setup

### 1. Install MongoDB

**Option A: Local MongoDB**
```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# macOS
brew install mongodb-community

# Start MongoDB
sudo systemctl start mongodb  # Linux
brew services start mongodb-community  # macOS
```

**Option B: MongoDB Atlas (Cloud - Recommended)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string

### 2. Configure .env

```bash
# Add to .env file
MONGO_URI=mongodb://localhost:27017/buddy_ai

# Or for MongoDB Atlas:
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/buddy_ai
```

## Usage

### Load User Context

```python
from persona import load_user_context

# Load user profile and memory
context = load_user_context(user_id="user_123")

print(context)
# {
#   'user_id': 'user_123',
#   'preferences': {
#     'humor_level': 'medium',
#     'response_length': 'medium',
#     'formality': 'casual',
#     'language_mix': 'hinglish'
#   },
#   'communication_style': 'casual',
#   'memory_summary': '- Prefers direct answers\n- Often stressed about work',
#   'interaction_count': 5,
#   'created_at': datetime(...),
#   'last_interaction': datetime(...)
# }
```

### Save Memories

```python
from persona import save_memory

# Save a learning about the user
save_memory(
    user_id="user_123",
    memory_type="pattern",
    content="User prefers concise responses",
    metadata={"source": "interaction"}
)
```

### Update Preferences

```python
from persona import update_user_preferences

# Update user preferences
update_user_preferences(
    user_id="user_123",
    preferences={
        "humor_level": "high",
        "response_length": "short"
    }
)
```

## Integration with Response Generation

```python
from persona import load_user_context
from composer import generate_buddy_reply

# Load user context
user_context = load_user_context(user_id)

# Generate personalized response
response = generate_buddy_reply(
    user_input=user_message,
    analysis=social_analysis,
    policy=behavior_policy,
    rag_knowledge=knowledge,
    persona=user_context  # Adds personalization!
)
```

## User Profile Structure

### Default Profile

```json
{
  "user_id": "user_123",
  "created_at": "2026-02-15T...",
  "last_interaction": "2026-02-15T...",
  "interaction_count": 0,
  "preferences": {
    "humor_level": "medium",
    "response_length": "medium",
    "formality": "casual",
    "language_mix": "hinglish",
    "emoji_usage": "moderate"
  },
  "communication_style": "casual",
  "learned_patterns": [],
  "topics_of_interest": [],
  "emotional_baseline": "neutral"
}
```

### Memory Document

```json
{
  "user_id": "user_123",
  "type": "pattern",
  "content": "User prefers concise responses",
  "timestamp": "2026-02-15T...",
  "metadata": {
    "source": "interaction"
  }
}
```

## Collections

The module uses 3 MongoDB collections:

1. **users**: User profiles and preferences
2. **memories**: Learned patterns and observations
3. **conversations**: Interaction history (optional)

## Features

### Automatic Profile Creation

If user doesn't exist, default profile is created automatically:

```python
context = load_user_context("new_user_456")
# Creates profile with defaults if not exists
```

### Memory Summary

Recent memories are summarized for prompt context:

```python
# From last 5 interactions:
memory_summary = """
- Prefers direct answers
- Often stressed about work
- Responds well to humor
- Mentions deadlines frequently
- Authority figure issues
"""
```

### Interaction Tracking

Every `load_user_context()` call:
- Updates `last_interaction` timestamp
- Increments `interaction_count`
- Builds learning over time

## Privacy & Storage

**What's Stored:**
- ✅ User preferences
- ✅ Communication patterns
- ✅ Learned behaviors
- ✅ Interaction counts

**What's NOT Stored:**
- ❌ Raw conversation text (unless explicitly saved)
- ❌ Sensitive personal data
- ❌ Message content

**Privacy Note**: Only behavioral signals and preferences are stored, maintaining Buddy's privacy-first architecture.

## Optional Feature

**The system works perfectly without MongoDB!**

If `MONGO_URI` is not set:
- User context functions gracefully degrade
- System returns None for persona
- Responses still work (just not personalized)

Example graceful degradation:

```python
try:
    user_context = load_user_context(user_id)
except:
    user_context = None  # System still works!

response = generate_reply(
    user_input=message,
    analysis=analysis,
    policy=policy,
    rag_knowledge=knowledge,
    persona=user_context  # Can be None
)
```

## Testing

```bash
# Test user context (requires MongoDB)
python tests/test_user_context.py

# Test with personalization
python example_with_persona.py
```

## API Reference

### load_user_context(user_id: str) -> dict
Load user profile and memory. Creates default if not exists.

### create_default_profile(user_id: str) -> dict
Create default user profile.

### get_memory_summary(user_id: str, memories_collection) -> str
Get compact memory summary.

### update_user_preferences(user_id: str, preferences: dict) -> bool
Update user preferences.

### save_memory(user_id: str, memory_type: str, content: str, metadata: dict) -> bool
Save a learning/memory about user.

### get_user_profile(user_id: str) -> dict
Get full user profile.

## Benefits

With persona module:
- ✅ **Personalized** responses based on user preferences
- ✅ **Learning** from past interactions
- ✅ **Consistency** in communication style
- ✅ **Adaptation** to user needs over time
- ✅ **Context** from previous conversations

Without persona module:
- ✅ System still works perfectly
- ✅ Uses general Buddy personality
- ✅ No dependency on database

---

**Status**: Optional enhancement module  
**Dependencies**: pymongo, MongoDB  
**Integration**: Works with all 5 phases  
**Privacy**: Stores preferences only, not conversations

