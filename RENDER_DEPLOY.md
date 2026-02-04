# 🚀 Render.com Deployment Guide

## **Render.com pe Backend Deploy Karo (FREE)**

Render.com bhi ek excellent free hosting option hai Python apps ke liye.

---

## 📋 **Prerequisites:**

- ✅ GitHub account
- ✅ Render.com account
- ✅ Your backend code in GitHub repository

---

## 🎯 **Step-by-Step Deployment:**

### **Step 1: GitHub Repository**

Pehle apna code GitHub pe push karo (agar nahi kiya):

1. GitHub pe new repository banao
2. Files upload karo
3. Repository URL note karo

---

### **Step 2: Render Account Setup**

1. **Render.com pe jao:** https://render.com
2. **Sign up** karo (GitHub se recommended)
3. GitHub permissions allow karo

---

### **Step 3: New Web Service Create Karo**

1. **Dashboard** mein **"New +"** button click karo
2. **"Web Service"** select karo

3. **Connect Repository:**
   - GitHub repository select karo
   - Ya manually Git URL provide karo
   - "Connect" click karo

---

### **Step 4: Configure Service**

**Basic Settings:**

```
Name: video-downloader-api
Region: Choose closest to you (Singapore for Asia)
Branch: main
Runtime: Python 3
```

**Build Settings:**

```
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

**Instance Type:**
```
Free (select free tier)
```

---

### **Step 5: Environment Variables (Optional)**

Add karo agar chahiye:

```
PORT = 10000 (Render auto-set karta hai)
PYTHON_VERSION = 3.11.0
```

---

### **Step 6: Deploy!**

1. **"Create Web Service"** button click karo
2. Render automatically deploy karega
3. Build logs dikhenge (5-10 minutes lag sakte hain first time)
4. Status: "Live" dikhne tak wait karo

---

### **Step 7: Get Your URL**

Deploy hone ke baad aapko URL milega:

```
https://video-downloader-api.onrender.com
```

Copy karo yeh URL!

---

## 🔄 **Auto-Deployment:**

Render automatically redeploy karta hai jab:
- GitHub pe code push karo
- Settings mein "Auto-Deploy" enabled ho (default enabled)

---

## 📊 **Free Tier Details:**

| Feature | Free Tier |
|---------|-----------|
| Services | Unlimited |
| Bandwidth | 100GB/month |
| Build Minutes | 500 minutes/month |
| RAM | 512MB |
| Sleep After | 15 mins inactivity |

**Important:** Free tier apps sleep after 15 minutes of inactivity!
- First request takes 30-60 seconds (cold start)
- Subsequent requests fast hain

---

## ⚡ **Keep App Awake (Optional):**

### **Method 1: Cron Job (Free)**

Create a free account at **cron-job.org**:

1. Add new cron job
2. URL: `https://your-app.onrender.com/api/health`
3. Schedule: Every 10 minutes
4. This keeps your app awake!

### **Method 2: UptimeRobot**

1. **UptimeRobot.com** pe account banao
2. New monitor add karo
3. URL: Your Render app URL
4. Interval: 5 minutes
5. Free!

---

## 🎯 **Frontend Integration:**

Render URL milne ke baad frontend update karo:

```javascript
// main.js
const API_BASE_URL = 'https://video-downloader-api.onrender.com';

// Get video info
async function fetchVideoInfo(url) {
  const response = await fetch(`${API_BASE_URL}/api/info`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });
  return await response.json();
}

// Download video
async function downloadVideo(url, quality, format, audioOnly) {
  const response = await fetch(`${API_BASE_URL}/api/download`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, quality, format, audio_only: audioOnly })
  });
  
  const blob = await response.blob();
  const downloadUrl = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = downloadUrl;
  a.download = `video.${format}`;
  a.click();
}
```

---

## 🐛 **Troubleshooting:**

### **Build Failed:**
```
Solution:
- Check requirements.txt
- Verify Python version
- See build logs in Render dashboard
```

### **App Not Responding:**
```
Reason: Free tier app sleeps after 15 mins
Solution: 
- First request takes time (cold start)
- Use UptimeRobot to keep awake
- Or upgrade to paid tier ($7/month)
```

### **CORS Error:**
```
Solution:
- Backend already has flask-cors enabled
- Check if frontend URL is correct
- Verify API endpoint spelling
```

### **Timeout Errors:**
```
Reason: Large file downloads
Solution:
- Select lower quality
- Increase timeout in Render settings
- Or use Railway (better for large files)
```

---

## 📈 **Monitoring:**

Render dashboard provides:
- ✅ CPU usage graphs
- ✅ Memory usage
- ✅ Request metrics
- ✅ Response times
- ✅ Error logs

Access: Dashboard → Your Service → Metrics tab

---

## 🔒 **Custom Domain (Optional):**

Agar apna domain use karna hai:

1. Render dashboard → Settings
2. Custom Domain section
3. Add domain: `api.yourdomain.com`
4. Render will give you CNAME record
5. Add CNAME in Hostinger DNS:
   ```
   Type: CNAME
   Name: api
   Value: your-app.onrender.com
   ```

---

## 💰 **Upgrade Options:**

Agar free tier limits cross ho jayein:

| Plan | Price | Features |
|------|-------|----------|
| Starter | $7/month | No sleep, 1GB RAM |
| Standard | $25/month | 2GB RAM, faster |

---

## 🆚 **Render vs Railway:**

| Feature | Render | Railway |
|---------|--------|---------|
| Free Hours | Always on* | 500 hrs/month |
| Cold Start | Yes (15min sleep) | No |
| Build Time | 5-10 mins | 2-3 mins |
| Bandwidth | 100GB | Fair use |
| Best For | Low-traffic | High-traffic |

*With 15-min sleep period

---

## 🎉 **Success Checklist:**

- ✅ Render account created
- ✅ GitHub repo connected
- ✅ Service configured
- ✅ Deployed successfully
- ✅ URL obtained
- ✅ API tested
- ✅ Frontend updated
- ✅ (Optional) Keep-alive setup
- ✅ Live! 🚀

---

## 📞 **Support:**

Render Resources:
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

---

## 💡 **Pro Tips:**

1. **Environment Secrets:** Use Render's secret files for sensitive data
2. **Health Checks:** Enable health check path: `/api/health`
3. **Notifications:** Setup Slack/Discord alerts for deployments
4. **Logs:** Use Render's log streams for debugging

---

## 🚀 **Quick Deploy Command:**

Agar Git se deploy kar rahe ho:

```bash
# Push to GitHub
git add .
git commit -m "Backend ready"
git push origin main

# Render will auto-deploy!
```

---

**Render.com pe deploy karo aur backend live karo! 🎊**

**Note:** Railway agar fast startup chahiye, Render agar always-on chahiye (with cold starts)!
