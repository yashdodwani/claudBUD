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
- [ ] Phase 2: Emotion + Relationship extractor
- [ ] Phase 3: WhatsApp import parser
- [ ] Phase 4: RAG behavior retrieval
- [ ] Phase 5: Response composer

## Quick Start

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 4. Run demo
python demo_policy.py              # Static policy examples
python example_policy_decider.py   # Live Claude policy generation
```

## Phase 1 Complete ✅

The Behavior Policy Engine is fully operational:
- **BehaviorPolicy Model**: Defines response behavior parameters
- **Decision Prompt**: Instructs Claude on policy selection rules
- **PolicyDecider**: Automatically generates policies from user context
- **generate_behavior_policy()**: Standalone function with automatic fallback

### Quick Usage

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

See `docs/PHASE1_COMPLETE.md` and `docs/GENERATE_BEHAVIOR_POLICY.md` for detailed documentation.

