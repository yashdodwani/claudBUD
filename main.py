"""
Buddy AI - Main FastAPI Application

Production-ready API server for Buddy AI chatbot.
"""

import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import router
from api.chat_router import router as chat_router

# Create FastAPI app
app = FastAPI(
    title="Buddy AI",
    description="Culturally intelligent AI companion with adaptive learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for all origins (for frontend development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "running",
        "service": "Buddy AI",
        "version": "1.0.0",
        "message": "Buddy AI is running! Visit /docs for API documentation.",
        "endpoints": {
            "chat": "POST /chat",
            "whatsapp": "POST /chat/whatsapp",
            "learning": "GET /chat/learning/{user_id}",
            "health": "GET /chat/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""

    # Check if API key is configured
    api_key_configured = bool(os.getenv("ANTHROPIC_API_KEY"))
    mongo_configured = bool(os.getenv("MONGO_URI"))

    return {
        "status": "healthy",
        "api_key_configured": api_key_configured,
        "mongodb_configured": mongo_configured,
        "learning_enabled": mongo_configured
    }


if __name__ == "__main__":
    import uvicorn

    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))

    print("=" * 70)
    print("🤖 Starting Buddy AI Server")
    print("=" * 70)
    print(f"   URL: http://localhost:{port}")
    print(f"   Docs: http://localhost:{port}/docs")
    print(f"   API Key: {'✅ Configured' if os.getenv('ANTHROPIC_API_KEY') else '❌ Not set'}")
    print(f"   MongoDB: {'✅ Configured' if os.getenv('MONGO_URI') else '⚠️  Not set (learning disabled)'}")
    print("=" * 70)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True  # Auto-reload on code changes
    )

