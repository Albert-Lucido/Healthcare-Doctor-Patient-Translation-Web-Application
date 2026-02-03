# Deployment Guide

## Quick Start Deployment (12-Hour Timeline)

### Phase 1: Get API Keys (30 minutes)

1. **Azure Translator** (5 min)
   - Visit: https://azure.microsoft.com/free/
   - Create free account
   - Navigate to "Cognitive Services" → "Translator"
   - Create resource → Copy key, endpoint, region

2. **AssemblyAI** (5 min)
   - Visit: https://www.assemblyai.com/
   - Sign up for free account
   - Dashboard → Copy API key

3. **Cloudinary** (5 min)
   - Visit: https://cloudinary.com/users/register/free
   - Sign up for free account
   - Dashboard → Copy cloud name, API key, API secret

4. **MongoDB** (15 min)
   - Option A: Render MongoDB
     - Visit: https://render.com/
     - Create account → New → PostgreSQL (has MongoDB option)
   - Option B: MongoDB Atlas (Recommended)
     - Visit: https://www.mongodb.com/cloud/atlas/register
     - Create free cluster (M0)
     - Database Access → Create user
     - Network Access → Add IP (0.0.0.0/0 for testing)
     - Connect → Get connection string

### Phase 2: Backend Deployment on Render (45 minutes)

1. **Prepare Repository** (15 min)
   ```bash
   # Initialize git if not already done
   git init
   git add .
   git commit -m "Initial commit"
   
   # Push to GitHub
   # Create new repo on github.com
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Render** (30 min)
   - Go to https://render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: healthcare-translation-api
     - **Region**: Choose closest to you
     - **Branch**: main
     - **Root Directory**: backend
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: Free
   
   - Add Environment Variables:
     ```
     MONGODB_URI=<your-mongodb-connection-string>
     AZURE_TRANSLATOR_KEY=<your-key>
     AZURE_TRANSLATOR_ENDPOINT=https://api.cognitive.microsofttranslator.com/
     AZURE_TRANSLATOR_REGION=<your-region>
     ASSEMBLYAI_API_KEY=<your-key>
     CLOUDINARY_CLOUD_NAME=<your-name>
     CLOUDINARY_API_KEY=<your-key>
     CLOUDINARY_API_SECRET=<your-secret>
     ALLOWED_ORIGINS=*
     ```
   
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy your backend URL (e.g., https://healthcare-translation-api.onrender.com)

3. **Verify Backend** (5 min)
   - Visit: `https://your-backend-url.onrender.com/docs`
   - Check API documentation loads
   - Test: `https://your-backend-url.onrender.com/api/health`

### Phase 3: Frontend Deployment on Vercel (30 minutes)

1. **Update Frontend Config** (10 min)
   ```bash
   # Create .env.production file in project root
   echo "VITE_API_BASE_URL=https://your-backend-url.onrender.com" > .env.production
   
   # Update for local development
   echo "VITE_API_BASE_URL=http://localhost:8000" > .env.local
   ```

2. **Deploy on Vercel** (20 min)
   - Visit: https://vercel.com/signup
   - Sign up with GitHub
   - Click "New Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: Vite
     - **Root Directory**: ./
     - **Build Command**: `npm run build`
     - **Output Directory**: dist
   
   - Add Environment Variable:
     - `VITE_API_BASE_URL` = `https://your-backend-url.onrender.com`
   
   - Click "Deploy"
   - Wait 2-3 minutes
   - Get your URL (e.g., https://healthcare-translation.vercel.app)

3. **Update Backend CORS** (5 min)
   - Go back to Render dashboard
   - Open your web service
   - Environment → Edit
   - Update `ALLOWED_ORIGINS`:
     ```
     ALLOWED_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:5173
     ```
   - Save and redeploy

### Phase 4: Testing (15 minutes)

1. **Frontend Connectivity**
   - Open your Vercel URL
   - Open browser DevTools (F12)
   - Select role and languages
   - Check console for errors

2. **Text Translation**
   - Type a message
   - Verify translation appears
   - Check message history loads

3. **Audio Recording** (Note: Requires HTTPS)
   - Click microphone button
   - Allow microphone permission
   - Record a test message
   - Verify transcription and translation

4. **Search & Summary**
   - Search for keywords
   - Generate summary of conversation

### Troubleshooting Common Issues

#### Backend Issues

**Error: MongoDB connection failed**
```python
# Check MongoDB URI format:
mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority

# Ensure IP whitelist includes 0.0.0.0/0 or Render IPs
```

**Error: Module not found**
```bash
# Check requirements.txt includes all dependencies
# Re-deploy on Render
```

**Error: Port binding failed**
```python
# Ensure start command uses $PORT:
uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### Frontend Issues

**Error: CORS policy blocked**
```javascript
// Backend .env must include frontend URL in ALLOWED_ORIGINS
ALLOWED_ORIGINS=https://your-app.vercel.app
```

**Error: API calls return 404**
```javascript
// Check .env.production has correct backend URL
VITE_API_BASE_URL=https://your-backend.onrender.com
// NO trailing slash!
```

**Error: Audio recording doesn't work**
```
// MediaRecorder requires HTTPS
// Vercel provides HTTPS automatically
// For localhost, use: chrome://flags/#unsafely-treat-insecure-origin-as-secure
```

### Free Tier Limits

Monitor usage to stay within free tiers:

- **Render**: 750 hours/month (instance sleeps after 15min inactivity)
- **Vercel**: Unlimited deployments, 100GB bandwidth/month
- **MongoDB Atlas**: 512MB storage
- **Azure Translator**: 2M characters/month
- **AssemblyAI**: 5 hours transcription/month
- **Cloudinary**: 25GB storage, 25GB bandwidth

### Performance Optimization

1. **Reduce Render Cold Starts**
   ```python
   # Add to main.py startup event
   @app.on_event("startup")
   async def startup():
       await Database.connect_db()
   ```

2. **Enable Caching on Vercel**
   ```javascript
   // vite.config.js
   export default {
     build: {
       rollupOptions: {
         output: {
           manualChunks: {
             vendor: ['react', 'react-dom']
           }
         }
       }
     }
   }
   ```

3. **Compress Audio Files**
   ```javascript
   // In AudioRecorder.jsx, use opus codec
   const mediaRecorder = new MediaRecorder(stream, {
     mimeType: 'audio/webm;codecs=opus'
   });
   ```

### Monitoring & Logs

**Render Logs:**
- Dashboard → Your Service → Logs tab
- Real-time streaming logs

**Vercel Logs:**
- Dashboard → Your Project → Deployments → View logs

**MongoDB Metrics:**
- Atlas Dashboard → Metrics tab
- Monitor connections, operations, storage

### Next Steps

1. **Custom Domain** (Optional)
   - Vercel: Settings → Domains → Add
   - Render: Settings → Custom Domain

2. **Authentication** (Future Enhancement)
   - Add JWT tokens
   - User registration/login
   - Role-based access control

3. **Analytics** (Optional)
   - Add Google Analytics
   - Track usage patterns
   - Monitor error rates

### Estimated Timeline Recap

- API Keys Setup: 30 minutes
- Backend Deployment: 45 minutes
- Frontend Deployment: 30 minutes
- Testing & Debugging: 15 minutes
- **Total: ~2 hours for deployment**

This leaves 10 hours for development, testing, and refinements!

### Emergency Contacts

- Render Status: https://status.render.com/
- Vercel Status: https://www.vercel-status.com/
- MongoDB Status: https://status.mongodb.com/

### Success Checklist

- [ ] All API keys obtained
- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Text messages translate correctly
- [ ] Audio recording works
- [ ] Search functionality works
- [ ] Summary generation works
- [ ] Mobile responsive design verified
- [ ] CORS configured correctly
- [ ] Environment variables secured

Congratulations! Your Healthcare Translation App is now live! 🎉
