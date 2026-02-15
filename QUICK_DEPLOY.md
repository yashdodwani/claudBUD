# 🚀 Quick Deploy to Render

## Prerequisites

1. GitHub account
2. Render account (free): https://render.com
3. Anthropic API key: https://console.anthropic.com

## Step-by-Step Deployment

### 1. Push to GitHub

```bash
# If not already initialized
git init
git add .
git commit -m "Buddy AI - Ready for deployment"

# Create repo on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/buddy-ai.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the `buddy-ai` repository

### 3. Configure Service

**Settings:**
- **Name:** `buddy-ai` (or your choice)
- **Environment:** `Docker`
- **Region:** Choose closest to your users
- **Branch:** `main`
- **Plan:** Free (or paid for production)

### 4. Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

**Required:**
```
ANTHROPIC_API_KEY = sk-ant-api03-...your-key...
```

**Optional (for learning features):**
```
MONGO_URI = mongodb+srv://username:password@cluster.mongodb.net/buddy_ai
```

### 5. Deploy!

Click **"Create Web Service"**

Render will:
- ✅ Build Docker image (2-3 minutes)
- ✅ Deploy container
- ✅ Assign URL: `https://buddy-ai-xxxx.onrender.com`

### 6. Test Your Deployment

```bash
# Check health
curl https://your-app.onrender.com/health

# Test chat
curl -X POST https://your-app.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "demo",
    "message": "Hello!",
    "meta": {"city": "Bangalore"}
  }'
```

## View API Documentation

Visit your deployed URL + `/docs`:
```
https://your-app.onrender.com/docs
```

## Need MongoDB? (Optional)

For learning features, set up MongoDB Atlas:

1. Go to https://www.mongodb.com/cloud/atlas
2. Create free cluster (M0)
3. Create database user
4. Whitelist IP: `0.0.0.0/0`
5. Get connection string
6. Add as `MONGO_URI` in Render

**Note:** App works fine without MongoDB!

## Local Docker Testing

Before deploying:

```bash
# Test Docker build
./test_docker.sh

# Or manually:
docker build -t buddy-ai .
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key \
  buddy-ai
```

## Troubleshooting

### Build fails
- Check Render build logs
- Ensure `requirements.txt` is complete
- Verify Dockerfile syntax

### App crashes
- Verify `ANTHROPIC_API_KEY` is set in Render
- Check application logs in Render dashboard

### MongoDB errors
- Double-check `MONGO_URI` format
- Verify IP whitelist in MongoDB Atlas
- Can skip MongoDB - app still works!

## Cost

- **Free Tier:** $0/month (spins down after 15 min inactivity)
- **Starter:** $7/month (always on)
- **Standard:** $25/month (better performance)

## Next Steps

1. ✅ Deploy to Render
2. ✅ Get your API URL
3. ✅ Build frontend
4. ✅ Connect frontend to API
5. 🎉 Launch!

---

**Complete deployment guide:** See `DEPLOYMENT.md`

