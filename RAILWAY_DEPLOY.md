# 🚀 Railway.app Deployment Guide

## **Railway.app pe Backend Deploy Karo (FREE)**

Railway.app sabse easy aur reliable free hosting hai Python backend ke liye.

---

## 📋 **Prerequisites:**

- ✅ GitHub account
- ✅ Railway.app account
- ✅ Your backend code ready

---

## 🎯 **Step-by-Step Deployment:**

### **Step 1: GitHub Repository Banao**

1. **GitHub.com pe jao** aur login karo
2. **New Repository** create karo:
   - Name: `video-downloader-backend`
   - Public ya Private (kuch bhi)
   - Click "Create repository"

3. **Local files upload karo:**
   ```bash
   # Git initialize (optional - local pe)
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/video-downloader-backend.git
   git push -u origin main
   ```
   
   **Ya simply GitHub web interface se files upload karo:**
   - Upload files button click karo
   - Saari files select karo (app.py, requirements.txt, etc.)
   - Commit changes

---

### **Step 2: Railway.app Account Setup**

1. **Railway.app pe jao:** https://railway.app
2. **"Login"** pe click karo
3. **GitHub se sign up** karo (recommended)
4. Permissions allow karo

---

### **Step 3: Project Deploy Karo**

1. **Dashboard mein "New Project"** click karo

2. **"Deploy from GitHub repo"** select karo

3. **Configure GitHub App:**
   - "Configure GitHub App" pe click karo
   - Apni repository select karo (`video-downloader-backend`)
   - Save karo

4. **Repository Select Karo:**
   - Apni repository list mein dikhegi
   - Click karo us pe

5. **Railway Auto-Deploy Karega:**
   - Railway automatically detect karega `requirements.txt`
   - Build process start hoga
   - Logs dikhenge (2-3 minutes lagenge)

---

### **Step 4: Environment Variables (Optional)**

Agar chahiye toh add karo:

1. Project settings mein jao
2. **Variables** tab pe click karo
3. Add karo:
   ```
   PORT = 5000
   FLASK_ENV = production
   ```

---

### **Step 5: Domain/URL Nikalo**

1. **Settings** → **Networking**
2. **"Generate Domain"** pe click karo
3. Railway aapko URL dega:
   ```
   https://video-downloader-backend-production.up.railway.app
   ```
   Ya custom domain add kar sakte ho

4. **Copy karo yeh URL** - yeh aapka backend API URL hai!

---

### **Step 6: Test Karo**

Browser mein ya Postman mein test karo:

```bash
# Health check
https://your-app.up.railway.app/

# Get video info
curl -X POST https://your-app.up.railway.app/api/info \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

---

## 🔄 **Auto-Deployment Setup:**

Railway automatically deploy karta hai jab bhi aap GitHub pe code push karte ho!

1. Code change karo local pe
2. Git commit aur push karo
3. Railway automatically detect karega
4. New version deploy ho jayega (2-3 minutes)

---

## 📊 **Free Tier Limits:**

| Feature | Free Tier |
|---------|-----------|
| Execution Time | 500 hours/month |
| RAM | 512MB - 8GB |
| Bandwidth | Fair use |
| Projects | Unlimited |
| Deployments | Unlimited |

**500 hours = 20+ days of uptime monthly!**

---

## ⚡ **Railway Dashboard Features:**

### **Logs Dekhna:**
- Project → Deployments → Logs
- Real-time logs stream
- Error debugging ke liye

### **Metrics:**
- CPU usage
- Memory usage
- Request count

### **Settings:**
- Environment variables
- Custom domains
- Auto-deployment settings

---

## 🎯 **Frontend Integration:**

Railway URL milne ke baad, apne frontend mein update karo:

### **Option 1: Direct JavaScript Update**

Agar aapne pehle wali website use ki hai, toh `main.js` mein yeh change karo:

```javascript
// main.js ke top pe add karo
const API_BASE_URL = 'https://your-app.up.railway.app';

// Example: Video info function
async function getVideoInfo(url) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/info`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url })
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch video info');
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    return { success: false, error: error.message };
  }
}

// Download function
async function downloadVideo(url, quality = 'best', format = 'mp4', audioOnly = false) {
  try {
    showLoading(true); // Your loading function
    
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
    
    if (!response.ok) {
      throw new Error('Download failed');
    }
    
    // Create blob and download
    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = `video.${audioOnly ? 'mp3' : format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(downloadUrl);
    
    showLoading(false);
    showSuccess('Download started!');
    
  } catch (error) {
    showLoading(false);
    showError(error.message);
  }
}
```

### **Option 2: Netlify Environment Variable**

Netlify pe environment variable set karo:

1. Netlify dashboard → Site settings
2. Build & deploy → Environment
3. Add variable:
   ```
   Key: VITE_API_URL (ya API_URL)
   Value: https://your-app.up.railway.app
   ```
4. Redeploy your site

---

## 🐛 **Troubleshooting:**

### **Build Failed:**
- Check `requirements.txt` spelling
- Verify Python version in `runtime.txt`
- Check Railway logs for errors

### **App Crashes:**
- Railway logs mein error dekho
- Verify `Procfile` syntax
- Check if port is correctly set

### **CORS Error:**
- Backend mein CORS already enabled hai
- Browser console mein exact error dekho
- Verify frontend URL

### **Deployment Stuck:**
- Railway dashboard reload karo
- Check GitHub connection
- Try manual redeploy

---

## 💰 **Cost Monitoring:**

Railway dashboard mein:
- Usage tab dekho
- Monthly hours tracking
- Set alerts (optional)

**Free tier:** 500 hours/month (20+ days)
**Agar zyada chahiye:** $5/month se upgrade karo

---

## 🔒 **Security Best Practices:**

1. ✅ `.env` file ko `.gitignore` mein rakho
2. ✅ Sensitive data environment variables mein rakho
3. ✅ Rate limiting add karo (production ke liye)
4. ✅ Input validation check karo

---

## 📱 **Mobile Testing:**

Backend deploy hone ke baad mobile pe test karo:
- Browser mein URL open karo
- Network tab check karo
- API responses verify karo

---

## 🎉 **Success Checklist:**

- ✅ Railway account created
- ✅ GitHub repo connected
- ✅ App deployed successfully
- ✅ Backend URL obtained
- ✅ API endpoints tested
- ✅ Frontend updated with backend URL
- ✅ End-to-end testing done
- ✅ Live on production! 🚀

---

## 📞 **Need Help?**

Railway Community:
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app
- Twitter: @Railway

---

**Railway.app pe deploy karo aur enjoy karo FREE backend! 🎊**
