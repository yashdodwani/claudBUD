# Render Deployment Guide for Buddy AI

## Quick Deploy to Render

### Step 1: Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit - Buddy AI complete system"

# Create repo on GitHub and push
git remote add origin https://github.com/yourusername/buddy-ai.git
git branch -M main
git push -u origin main
```

### Step 2: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:

   **Name:** `buddy-ai`
   
   **Environment:** `Docker`
   
   **Region:** Choose closest to your users
   
   **Branch:** `main`
   
   **Build Command:** (Auto-detected from Dockerfile)
   
   **Start Command:** (Auto-detected from Dockerfile)

### Step 3: Set Environment Variables

In Render dashboard, add these environment variables:

**Required:**
```
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
```

**Optional (for learning features):**
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/buddy_ai
```

**System (auto-set by Render):**
```
PORT=10000
```

### Step 4: Deploy

Click **"Create Web Service"**

Render will:
1. Build Docker image
2. Deploy container
3. Assign public URL: `https://buddy-ai-xxxx.onrender.com`

---

## MongoDB Setup (Optional)

If you want learning features:

### Option 1: MongoDB Atlas (Recommended)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster
3. Create database user
4. Whitelist IP: `0.0.0.0/0` (allow from anywhere)
5. Get connection string
6. Add to Render environment variables as `MONGO_URI`

### Option 2: Skip MongoDB

System works without MongoDB:
- No user learning
- No trait adaptation
- No interaction history
- Still fully functional for basic chat!

---

## Verify Deployment

After deployment completes:

```bash
# Check health
curl https://buddy-ai-xxxx.onrender.com/health

# Test API
curl -X POST https://buddy-ai-xxxx.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "message": "Hello Buddy!",
    "meta": {"city": "Bangalore"}
  }'
```

---

## API Documentation

Once deployed, visit:
- **Swagger UI:** `https://buddy-ai-xxxx.onrender.com/docs`
- **ReDoc:** `https://buddy-ai-xxxx.onrender.com/redoc`

---

## Environment Variables Reference

### Required
| Variable | Description | Example |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Claude API key | `sk-ant-...` |

### Optional
| Variable | Description | Example |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB connection string | `mongodb+srv://...` |

### Auto-Set by Render
| Variable | Description |
|----------|-------------|
| `PORT` | Server port (usually 10000) |

---

## Free Tier Limits

Render Free Tier:
- ✅ 750 hours/month free
- ✅ Auto-sleep after 15 min inactivity
- ✅ Wake on request (cold start ~30s)
- ⚠️  Spins down when inactive

For production (paid plans):
- Always on
- No cold starts
- More CPU/RAM
- Custom domains

---

## Troubleshooting

### Build Fails

Check Render logs. Common issues:
1. Missing `requirements.txt` dependencies
2. Python version mismatch
3. Invalid Dockerfile syntax

**Fix:** Ensure all dependencies in `requirements.txt`

### App Crashes on Start

Check environment variables:
1. `ANTHROPIC_API_KEY` must be set
2. `MONGO_URI` format correct (if using MongoDB)

**Fix:** Add missing environment variables in Render dashboard

### Timeout/Slow Response

Render free tier spins down after inactivity:
- First request after sleep takes ~30s (cold start)
- Subsequent requests are fast

**Fix:** Upgrade to paid plan for always-on service

### MongoDB Connection Error

If MongoDB configured but not working:
1. Check `MONGO_URI` format
2. Whitelist Render IPs in MongoDB Atlas
3. Verify database user credentials

**Fix:** Can disable MongoDB - app still works without learning

---

## Custom Domain (Optional)

In Render dashboard:
1. Go to Settings
2. Custom Domains
3. Add domain: `api.yourbuddy.app`
4. Configure DNS (Render provides instructions)

---

## Monitoring

Render provides:
- ✅ Real-time logs
- ✅ Metrics dashboard
- ✅ Deploy history
- ✅ Health checks

Access via: Render Dashboard → Your Service → Logs/Metrics

---

## Scaling

### Vertical Scaling (More Resources)
Upgrade instance type in Render:
- Starter: $7/month
- Standard: $25/month
- Pro: $85/month

### Horizontal Scaling
Add more instances:
- Load balancer included
- Auto-scaling available on Team plans

---

## CI/CD

Auto-deploy on push:
1. Render watches `main` branch
2. Auto-builds on new commits
3. Auto-deploys if build succeeds

Manual deploy:
- Render Dashboard → Manual Deploy

---

## Costs Estimate

### Free Tier
- ✅ $0/month
- ✅ Perfect for hackathons/demos
- ⚠️  Spins down when inactive

### Production Setup
- Web Service (Starter): $7/month
- MongoDB Atlas (Free): $0/month
- **Total: $7/month**

### At Scale (1000+ users)
- Web Service (Standard): $25/month
- MongoDB Atlas (Shared): $9/month
- **Total: $34/month**

---

## Security Best Practices

1. ✅ Never commit `.env` file
2. ✅ Use environment variables in Render
3. ✅ Rotate API keys regularly
4. ✅ Enable HTTPS (auto on Render)
5. ✅ Set proper CORS origins (not `*` in production)

---

## Alternative Deployment Options

If not using Render:

### Railway
```bash
# Install Railway CLI
npm install -g railway

# Login and deploy
railway login
railway init
railway up
```

### Fly.io
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

### AWS/GCP/Azure
Use Dockerfile with:
- AWS ECS
- Google Cloud Run
- Azure Container Instances

---

## Support

Issues during deployment?

1. Check Render build logs
2. Verify environment variables
3. Test Docker locally:
   ```bash
   docker build -t buddy-ai .
   docker run -p 8000:8000 \
     -e ANTHROPIC_API_KEY=your_key \
     buddy-ai
   ```

---

**Status:** Ready to deploy! 🚀
**Time to deploy:** ~5 minutes
**Cost:** $0 (free tier) or $7/month (production)

