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

- [x] Phase 1: Behavior Policy Engine schema + prompts
- [ ] Phase 2: Emotion + Relationship extractor
- [ ] Phase 3: WhatsApp import parser
- [ ] Phase 4: RAG behavior retrieval
- [ ] Phase 5: Response composer

