# 🚀 Quick Start Guide - Video Downloader Backend

## **5 Minutes Mein Backend Live Karo!**

---

## ✅ **What You'll Get:**

- ✅ 100% Free Python Backend
- ✅ No Paid APIs
- ✅ Multi-platform video downloads
- ✅ Ready to deploy

---

## 📦 **Files Included:**

```
video-downloader-backend/
├── app.py                        # Main backend code
├── requirements.txt              # Dependencies
├── Procfile                      # Deployment config
├── runtime.txt                   # Python version
├── README.md                     # Complete documentation
├── RAILWAY_DEPLOY.md            # Railway deployment guide
├── RENDER_DEPLOY.md             # Render deployment guide
├── LOCAL_TEST.md                # Local testing guide
├── frontend_integration.js      # Frontend code
└── QUICK_START.md               # This file
```

---

## ⚡ **Fast Track - Railway Deploy (Easiest)**

### **Step 1: GitHub Setup (2 minutes)**

1. **GitHub.com** pe jao, login karo
2. **New repository** banao: `video-downloader-backend`
3. **Upload files** karo (all files from this folder)
4. Done!

---

### **Step 2: Railway Deploy (3 minutes)**

1. **[Railway.app](https://railway.app)** pe jao
2. **Sign up** with GitHub
3. **New Project** → **Deploy from GitHub**
4. **Select your repository**
5. Wait 2-3 minutes...
6. **Done!** ✅

---

### **Step 3: Get Your API URL**

1. Railway dashboard mein **Settings** → **Networking**
2. **Generate Domain** click karo
3. Copy your URL:
   ```
   https://your-app.up.railway.app
   ```

---

### **Step 4: Connect to Frontend**

Apni website ki `main.js` mein yeh change karo:

```javascript
// Line 1 pe add karo
const API_BASE_URL = 'https://your-app.up.railway.app';
```

**Replace** karo:
- `your-app.up.railway.app` with your actual Railway URL

---

### **Step 5: Test Karo**

Browser mein test karo:
```
https://your-app.up.railway.app/
```

Response dikhna chahiye:
```json
{
  "status": "running",
  "message": "Video Downloader Backend API"
}
```

✅ **Working!** Your backend is live! 🎉

---

## 🎯 **Alternative: Render.com Deploy**

Agar Railway nahi, toh Render use karo:

1. **[Render.com](https://render.com)** pe jao
2. **Sign up** with GitHub
3. **New** → **Web Service**
4. **Connect repository**
5. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. **Create Web Service**
7. Wait 5-10 minutes
8. **Done!** Get your `.onrender.com` URL

---

## 🧪 **Want to Test Locally First?**

### **Quick Local Test:**

```bash
# 1. Open terminal in project folder
cd video-downloader-backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run server
python app.py

# 4. Open browser
# Go to: http://localhost:5000
```

**Full local testing guide:** See `LOCAL_TEST.md`

---

## 📱 **Frontend Integration:**

### **Method 1: Direct Code (Easiest)**

Apni website ki `main.js` mein:

```javascript
const API_BASE_URL = 'https://your-deployed-backend-url.com';

async function downloadVideo(url, quality, format) {
  const response = await fetch(`${API_BASE_URL}/api/download`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, quality, format, audio_only: false })
  });
  
  const blob = await response.blob();
  const downloadUrl = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = downloadUrl;
  a.download = `video.${format}`;
  a.click();
}
```

### **Method 2: Use Provided Integration File**

Copy paste karo `frontend_integration.js` ka code apni `main.js` mein!

---

## 🎯 **API Endpoints:**

### **1. Health Check**
```
GET /
Response: {"status": "running"}
```

### **2. Get Video Info**
```
POST /api/info
Body: {"url": "https://youtube.com/watch?v=..."}
Response: Video metadata
```

### **3. Download Video**
```
POST /api/download
Body: {
  "url": "https://...",
  "quality": "720p",
  "format": "mp4",
  "audio_only": false
}
Response: Video file
```

---

## ✅ **Success Checklist:**

- [ ] Files uploaded to GitHub
- [ ] Railway/Render account created
- [ ] Backend deployed successfully
- [ ] Got backend URL
- [ ] Updated frontend with URL
- [ ] Tested `/` endpoint
- [ ] Tested `/api/info` endpoint
- [ ] Tested `/api/download` endpoint
- [ ] Frontend connects successfully
- [ ] Download works end-to-end
- [ ] **DONE!** 🎉

---

## 💰 **Cost:**

| Item | Cost |
|------|------|
| Python code | FREE |
| yt-dlp library | FREE |
| Railway.app hosting | FREE (500 hrs/month) |
| Render.com hosting | FREE (with sleep) |
| Domain (optional) | You already have! |
| **TOTAL** | **₹0** 💰 |

---

## 🐛 **Quick Troubleshooting:**

### **Deploy Failed?**
- Check if all files uploaded
- Verify `requirements.txt` exists
- See Railway/Render logs

### **Backend Not Responding?**
- Wait 2-3 minutes for first deploy
- Check if URL is correct
- Try `/api/health` endpoint

### **CORS Error?**
- Backend already has CORS enabled
- Check if API_BASE_URL is correct in frontend

### **Download Fails?**
- Test with YouTube public video first
- Check if URL is valid
- See backend logs for errors

---

## 📚 **More Help:**

- **Railway Deploy:** See `RAILWAY_DEPLOY.md`
- **Render Deploy:** See `RENDER_DEPLOY.md`
- **Local Testing:** See `LOCAL_TEST.md`
- **Full Docs:** See `README.md`

---

## 🎊 **Summary:**

1. ✅ Upload to GitHub (2 min)
2. ✅ Deploy to Railway (3 min)
3. ✅ Get URL and update frontend (1 min)
4. ✅ **Total: 6 minutes!** ⏱️

---

**Backend ready hai! Jao aur deploy karo! 🚀**

**Questions?** Check other .md files for detailed guides!
