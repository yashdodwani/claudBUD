# Buddy - Culturally Intelligent AI Assistant

A context-aware AI that adapts to Indian communication patterns and individual user preferences.

## System Architecture

```
User Input → Signal Extractors → Behavior Knowledge RAG → Persona Memory → Behavior Policy Engine → Claude Response
```

## Key Features

- **Privacy-First**: Never stores raw conversations, only behavioral signals
- **Cultural Intelligence**: Indian communication patterns and social dynamics
- **Adaptive Learning**: Builds user-specific interaction preferences
- **WhatsApp Integration**: Import chats to understand relationship dynamics

## Project Structure

```
claudBUD/
├── behavior_library/          # Cultural intelligence database
├── src/
│   ├── extractors/           # Signal extraction modules
│   ├── policy_engine/        # Behavior policy decision engine
│   ├── rag/                  # Behavior knowledge retrieval
│   ├── persona/              # User memory management
│   └── whatsapp/             # WhatsApp import module
└── tests/
```

## Development Phases

- [x] Phase 1: Behavior Policy Engine schema + prompts ✅
  - [x] BehaviorPolicy Pydantic model
  - [x] Behavior decision prompt
  - [x] PolicyDecider class (Claude-powered)
  - [x] generate_behavior_policy() function
- [x] Phase 2: Emotion + Relationship extractor ✅
  - [x] SocialAnalysis Pydantic model
  - [x] Social analysis prompt
  - [x] analyze_social_context() function
  - [x] Integration with Phase 1
- [x] Phase 3: WhatsApp import parser ✅
  - [x] parse_whatsapp_chat() function
  - [x] Android + iOS format support
  - [x] Privacy-first (no storage, memory-only)
  - [x] Integration with Phase 1 + 2
- [x] Phase 4: RAG behavior retrieval ✅
  - [x] retrieve_behavior_knowledge() function
  - [x] Keyword-based matching
  - [x] 49 real scenarios from social media
  - [x] Indian cultural patterns
- [x] Phase 5: Response composer ✅
  - [x] generate_buddy_reply() function
  - [x] Natural Hinglish responses
  - [x] Context-aware tone matching
  - [x] Complete system integration

## 🎉 ALL PHASES COMPLETE!

## Optional: User Personalization (Persona Module)

Add user-specific context and memory:

```bash
# 1. Set up MongoDB (local or Atlas)
# 2. Add to .env:
MONGO_URI=mongodb://localhost:27017/buddy_ai

# 3. Use personalization
from persona import load_user_context
user_context = load_user_context(user_id="user_123")

# 4. Generate personalized response
response = generate_buddy_reply(
    user_input=message,
    analysis=analysis,
    policy=policy,
    rag_knowledge=knowledge,
    persona=user_context  # Adds personalization!
)
```

**Note**: System works perfectly without MongoDB. Persona module is optional.

See `docs/PERSONA_MODULE.md` for setup and usage.

## Quick Start

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 4. Run demos
python demo_policy.py                # Static policy examples (Phase 1)
python example_policy_decider.py     # Live Claude policy generation (Phase 1)
python example_social_analyzer.py    # Social signal extraction (Phase 2)
python example_integration.py        # Phase 1 + Phase 2 together
python example_full_pipeline.py      # Phase 1 + 2 + 3 together
python example_complete_system.py    # 🎉 ALL 5 PHASES TOGETHER!

# 5. Test components
python tests/test_behavior_policy.py        # Phase 1 tests
python tests/test_social_analyzer.py        # Phase 2 tests
python tests/test_whatsapp_parser.py        # Phase 3 tests
python tests/test_rag_retrieval.py          # Phase 4 tests
```

## Phase 1 Complete ✅

The Behavior Policy Engine is fully operational:
- **BehaviorPolicy Model**: Defines response behavior parameters
- **Decision Prompt**: Instructs Claude on policy selection rules
- **PolicyDecider**: Automatically generates policies from user context
- **generate_behavior_policy()**: Standalone function with automatic fallback

### Quick Usage - Phase 1

```python
from policy_engine import generate_behavior_policy

# Simple function call
policy = generate_behavior_policy({
    "user_message": "Boss yelled at me, need help replying",
    "emotion": "frustrated",
    "situation": "workplace_conflict"
})

print(policy.mode)  # diplomatic_advisor
print(policy.tone)  # calm_reassuring
```

## Phase 2 Complete ✅

The Social Signal Extractor is fully operational:
- **SocialAnalysis Model**: Structured emotional and relationship signals
- **Social Analysis Prompt**: Extracts practical context (not psychology)
- **analyze_social_context()**: Automatic signal extraction with fallback
- **Indian Context Awareness**: Authority power distance built-in

### Quick Usage - Phase 2

```python
from extractors import analyze_social_context

# Extract signals from message
analysis = analyze_social_context(
    "My boss just yelled at me in front of everyone"
)

print(analysis.primary_emotion)  # "anger"
print(analysis.relationship)     # "authority"
print(analysis.conflict_risk)    # "high"
print(analysis.user_need)        # "vent" or "advice"
```

## Phase 3 Complete ✅

The WhatsApp Parser is fully operational:
- **parse_whatsapp_chat()**: Privacy-first chat parsing
- **Android + iOS Support**: Both WhatsApp formats
- **No Storage**: Memory-only processing
- **Signal Extraction Ready**: Feeds into Phase 2

### Quick Usage - Phase 3

```python
from whatsapp import parse_whatsapp_chat

# Raw WhatsApp export
raw_chat = """
12/01/2024, 10:30 - Boss: Need that report now
12/01/2024, 10:31 - +91 98765 43210: Working on it sir
"""

# Clean it (privacy-first: no storage)
cleaned = parse_whatsapp_chat(raw_chat)
print(cleaned)
# Output:
# Need that report now
# Working on it sir

# ✅ Timestamps removed
# ✅ Phone numbers anonymized  
# ✅ No disk storage
```

### Integration - Phase 1 + Phase 2

```python
from extractors import analyze_social_context
from policy_engine import generate_behavior_policy

# Step 1: Extract social signals
analysis = analyze_social_context(user_message)

# Step 2: Generate behavior policy from signals
policy = generate_behavior_policy({
    "user_message": user_message,
    "emotion": analysis.primary_emotion,
    "relationship": analysis.relationship,
    "conflict_risk": analysis.conflict_risk
})

# Now you have: signals + policy → ready for response generation
```

### Full Pipeline - Phase 1 + 2 + 3

```python
from whatsapp import parse_whatsapp_chat
from extractors import analyze_social_context
from policy_engine import generate_behavior_policy

# Step 1: Parse WhatsApp (privacy-first)
cleaned_text = parse_whatsapp_chat(whatsapp_export)

# Step 2: Extract signals
analysis = analyze_social_context(cleaned_text)

# Step 3: Generate policy
policy = generate_behavior_policy({
    "user_message": "Help me handle this situation",
    "emotion": analysis.primary_emotion,
    "relationship": analysis.relationship,
    "conflict_risk": analysis.conflict_risk
})

# Complete context ready for response generation!
```

See `PHASE1_COMPLETE.md`, `PHASE2_COMPLETE.md`, and `PHASE3_COMPLETE.md` for detailed documentation.

## Phase 4 Complete ✅

The Behavior RAG system is fully operational:
- **retrieve_behavior_knowledge()**: Keyword-based pattern matching
- **49 Real Scenarios**: Extracted from Indian social media
- **Cultural Intelligence**: Do's, don'ts, and tone guidelines
- **find_relevant_knowledge()**: Smart context-aware retrieval

### Quick Usage - Phase 4

```python
from rag import retrieve_behavior_knowledge, find_relevant_knowledge

# Basic retrieval
knowledge = retrieve_behavior_knowledge("office stress work")
print(knowledge['scenario'])      # 'office_stress'
print(knowledge['do'])            # List of helpful patterns
print(knowledge['dont'])          # List of things to avoid

# Context-aware retrieval
knowledge = find_relevant_knowledge(
    user_message="Boss yelled at me",
    social_analysis={'primary_emotion': 'anger', 'relationship': 'authority'}
)
```

## Phase 5 Complete ✅

The Response Composer is fully operational:
- **generate_buddy_reply()**: Final response generation
- **Natural Hinglish**: Real friend vibes, not robotic
- **Cultural Context**: Indian communication patterns
- **Policy-Driven**: Follows behavior policy strictly

### Quick Usage - Phase 5

```python
from composer import generate_reply

# Generate final response
response = generate_reply(
    user_input="My manager humiliated me in meeting",
    analysis=social_analysis,     # From Phase 2
    policy=behavior_policy,        # From Phase 1
    rag_knowledge=retrieved_knowledge  # From Phase 4
)

print(response)  # Natural, context-aware Buddy response!
```

## Complete System - All 5 Phases

```python
from extractors import analyze_social_context
from policy_engine import generate_behavior_policy
from rag import find_relevant_knowledge
from composer import generate_reply

# User input
user_input = "My boss just yelled at me in front of everyone"

# Phase 2: Extract signals
analysis = analyze_social_context(user_input)

# Phase 1: Generate policy
policy = generate_behavior_policy({
    "user_message": user_input,
    "emotion": analysis.primary_emotion,
    "relationship": analysis.relationship,
    "conflict_risk": analysis.conflict_risk
})

# Phase 4: Retrieve knowledge
knowledge = find_relevant_knowledge(user_input, analysis.model_dump())

# Phase 5: Generate response
response = generate_reply(
    user_input=user_input,
    analysis=analysis,
    policy=policy,
    rag_knowledge=knowledge
)

print(response)  # Complete, culturally-aware Buddy response!
```

See `PHASE4_COMPLETE.md` and `PHASE5_COMPLETE.md` for detailed documentation.

