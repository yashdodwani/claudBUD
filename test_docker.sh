#!/bin/bash
# Test Docker build locally before deploying to Render

set -e  # Exit on error

echo "═══════════════════════════════════════════════════════════════════════"
echo "🐳 Testing Docker Build for Buddy AI"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "   Create .env with:"
    echo "   ANTHROPIC_API_KEY=your_key_here"
    echo ""
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo "1️⃣  Building Docker image..."
docker build -t buddy-ai:test .

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed!"
    exit 1
fi

echo ""
echo "2️⃣  Starting container..."
docker run -d \
    --name buddy-ai-test \
    -p 8000:8000 \
    -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    -e MONGO_URI=${MONGO_URI:-} \
    buddy-ai:test

echo "✅ Container started!"
echo ""

# Wait for container to be ready
echo "3️⃣  Waiting for server to be ready..."
sleep 5

# Test health endpoint
echo "4️⃣  Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)

if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✅ Health check passed!"
    echo "   Response: $HEALTH_RESPONSE"
else
    echo "❌ Health check failed!"
    echo "   Response: $HEALTH_RESPONSE"
    docker logs buddy-ai-test
    docker stop buddy-ai-test
    docker rm buddy-ai-test
    exit 1
fi

echo ""
echo "5️⃣  Testing chat endpoint..."
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{
        "user_id": "test_user",
        "message": "Hello Buddy!",
        "meta": {"city": "Bangalore"}
    }')

if echo "$CHAT_RESPONSE" | grep -q "reply"; then
    echo "✅ Chat endpoint working!"
    echo "   Reply: $(echo $CHAT_RESPONSE | jq -r '.reply' | head -c 100)..."
else
    echo "❌ Chat endpoint failed!"
    echo "   Response: $CHAT_RESPONSE"
    docker logs buddy-ai-test
    docker stop buddy-ai-test
    docker rm buddy-ai-test
    exit 1
fi

echo ""
echo "6️⃣  Cleaning up..."
docker stop buddy-ai-test
docker rm buddy-ai-test

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ ALL TESTS PASSED!"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "🚀 Docker image is ready for deployment!"
echo ""
echo "Next steps:"
echo "  1. Push to GitHub"
echo "  2. Connect to Render"
echo "  3. Set ANTHROPIC_API_KEY in Render dashboard"
echo "  4. Deploy!"
echo ""
echo "View docs: cat DEPLOYMENT.md"
echo "═══════════════════════════════════════════════════════════════════════"

