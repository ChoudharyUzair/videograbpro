# Video Downloader Backend API

## 🚀 **100% Free Backend - No Paid APIs**

Complete Python backend for multi-platform video downloader using `yt-dlp` library.

### ✅ **Supported Platforms:**
- YouTube (Videos, Shorts)
- TikTok
- Instagram (Reels, Posts, IGTV)
- Twitter/X
- Facebook
- Sora (OpenAI)
- And 1000+ more sites!

### 🎯 **Features:**
- ✅ No paid APIs required
- ✅ Multiple quality options (4K, 1080p, 720p, 480p, 360p)
- ✅ Format selection (MP4, WebM)
- ✅ Audio extraction (MP3)
- ✅ Video metadata extraction
- ✅ Automatic cleanup of old files
- ✅ CORS enabled for frontend
- ✅ RESTful API design
- ✅ 100% FREE to host

---

## 📋 **API Endpoints:**

### 1. **Health Check**
```
GET /
GET /api/health
```

### 2. **Get Supported Platforms**
```
GET /api/platforms
```

### 3. **Get Video Info**
```
POST /api/info
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}

Response:
{
  "success": true,
  "title": "Video Title",
  "thumbnail": "https://...",
  "duration": 180,
  "platform": "youtube",
  "formats": [...]
}
```

### 4. **Download Video**
```
POST /api/download
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "quality": "1080p",  // Options: 4k, 1080p, 720p, 480p, 360p, best
  "format": "mp4",     // Options: mp4, webm
  "audio_only": false  // true for MP3 audio only
}

Response:
Binary file download (video/audio file)
```

---

## 🏗️ **Project Structure:**

```
video-downloader-backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # For Railway/Render deployment
├── runtime.txt           # Python version
├── README.md             # This file
├── .gitignore            # Git ignore rules
└── deployment/
    ├── RAILWAY_DEPLOY.md    # Railway deployment guide
    ├── RENDER_DEPLOY.md     # Render deployment guide
    └── VERCEL_DEPLOY.md     # Vercel deployment guide
```

---

## 🚀 **Local Development:**

### **1. Clone/Download Files**
```bash
# Create project directory
mkdir video-downloader-backend
cd video-downloader-backend

# Copy all files from this package
```

### **2. Install Dependencies**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### **3. Run Server**
```bash
python app.py

# Server will start at: http://localhost:5000
```

### **4. Test API**
```bash
# Health check
curl http://localhost:5000/

# Get video info
curl -X POST http://localhost:5000/api/info \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

---

## ☁️ **Free Deployment Options:**

### **Option 1: Railway.app** (⭐ Recommended)
- ✅ 500 hours/month free
- ✅ Easy deployment
- ✅ Auto SSL
- ✅ Custom domain support

**Steps:**
1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Connect your repository
4. Railway auto-detects and deploys!

### **Option 2: Render.com**
- ✅ Free tier available
- ✅ Auto-deploy from Git
- ✅ SSL included

**Steps:**
1. Create account at [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`

### **Option 3: Vercel (Serverless)**
- ✅ Completely free
- ✅ Serverless functions
- ✅ Global CDN

**Note:** Requires minor code changes for serverless (see VERCEL_DEPLOY.md)

---

## 🔌 **Frontend Integration:**

### **Update Your Frontend (index.html / main.js)**

```javascript
// Replace this in your main.js
const API_BASE_URL = 'https://your-backend.railway.app';  // Your deployed backend URL

// Get video info
async function getVideoInfo(url) {
  const response = await fetch(`${API_BASE_URL}/api/info`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url })
  });
  
  const data = await response.json();
  return data;
}

// Download video
async function downloadVideo(url, quality, format, audioOnly) {
  const response = await fetch(`${API_BASE_URL}/api/download`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url,
      quality,
      format,
      audio_only: audioOnly
    })
  });
  
  // Create download link
  const blob = await response.blob();
  const downloadUrl = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = downloadUrl;
  a.download = 'video.mp4';  // Filename
  a.click();
}
```

---

## 🛠️ **Environment Variables:**

For production deployment:

```bash
PORT=5000                    # Server port (auto-set by hosting)
FLASK_ENV=production         # Production mode
MAX_FILE_SIZE=524288000     # 500MB in bytes
CACHE_EXPIRE_HOURS=2        # Auto-cleanup time
```

---

## 📊 **Cost Analysis:**

| Service | Free Tier | Cost |
|---------|-----------|------|
| Railway.app | 500 hrs/month | ₹0 |
| Render.com | 750 hrs/month | ₹0 |
| Vercel | Unlimited | ₹0 |
| yt-dlp Library | Open source | ₹0 |
| **Total** | - | **₹0** 💰 |

---

## ⚡ **Performance:**

- Video info extraction: ~2-5 seconds
- Download speed: Based on internet connection
- File cleanup: Automatic after 2 hours
- Concurrent requests: Supports multiple users

---

## 🔒 **Security Notes:**

1. ✅ CORS enabled for your frontend domain
2. ✅ Input validation on all endpoints
3. ✅ Automatic file cleanup
4. ✅ Error handling
5. ⚠️ For production: Add rate limiting
6. ⚠️ For production: Add authentication (optional)

---

## 🐛 **Troubleshooting:**

### **"Module not found" error:**
```bash
pip install -r requirements.txt
```

### **Download fails:**
- Check if URL is valid
- Some videos may be geo-restricted
- Try different quality/format

### **Large file timeout:**
- Increase hosting timeout limits
- Use quality selector for smaller files

---

## 📝 **License:**

MIT License - Free to use and modify

---

## 🤝 **Support:**

For issues:
1. Check error logs
2. Verify URL is supported
3. Test locally first
4. Check hosting service logs

---

## 🚀 **Next Steps:**

1. ✅ Test locally
2. ✅ Deploy to Railway/Render
3. ✅ Get backend URL
4. ✅ Update frontend with backend URL
5. ✅ Test end-to-end
6. ✅ Launch! 🎉

---

**Backend ready! Deploy karo aur enjoy karo! 🚀**
