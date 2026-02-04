# 🧪 Local Testing Guide

## **Local Machine Pe Backend Test Karo**

Deploy karne se pehle local pe test karna zaroori hai!

---

## 📋 **Requirements:**

- ✅ Python 3.8+ installed
- ✅ pip package manager
- ✅ Terminal/Command Prompt

---

## 🚀 **Quick Start (Windows):**

### **Step 1: Python Check Karo**

```cmd
python --version
```

Agar Python nahi hai toh: https://python.org se download karo

---

### **Step 2: Project Folder Mein Jao**

```cmd
cd path\to\video-downloader-backend
```

---

### **Step 3: Virtual Environment Banao**

```cmd
python -m venv venv
```

---

### **Step 4: Virtual Environment Activate Karo**

**Windows:**
```cmd
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

Screen pe `(venv)` dikhna chahiye.

---

### **Step 5: Dependencies Install Karo**

```cmd
pip install -r requirements.txt
```

Wait karo 2-3 minutes...

---

### **Step 6: Server Start Karo**

```cmd
python app.py
```

Output:
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

✅ **Server ready hai!**

---

## 🧪 **Testing:**

### **Method 1: Browser Test**

Browser mein open karo:
```
http://localhost:5000
```

Response:
```json
{
  "status": "running",
  "message": "Video Downloader Backend API",
  "version": "1.0.0"
}
```

---

### **Method 2: Postman/Insomnia**

Download: [Postman](https://postman.com/downloads)

**Test 1: Get Video Info**

```
Method: POST
URL: http://localhost:5000/api/info
Headers: Content-Type: application/json
Body (JSON):
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Test 2: Download Video**

```
Method: POST
URL: http://localhost:5000/api/download
Headers: Content-Type: application/json
Body (JSON):
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "quality": "720p",
  "format": "mp4",
  "audio_only": false
}
```

---

### **Method 3: cURL (Command Line)**

**Health Check:**
```bash
curl http://localhost:5000/
```

**Get Video Info:**
```bash
curl -X POST http://localhost:5000/api/info ^
  -H "Content-Type: application/json" ^
  -d "{\"url\":\"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"}"
```

**Download Test:**
```bash
curl -X POST http://localhost:5000/api/download ^
  -H "Content-Type: application/json" ^
  -d "{\"url\":\"https://www.youtube.com/watch?v=dQw4w9WgXcQ\",\"quality\":\"720p\"}" ^
  --output video.mp4
```

---

### **Method 4: Python Script**

Create `test.py`:

```python
import requests
import json

API_URL = "http://localhost:5000"

# Test 1: Health check
response = requests.get(f"{API_URL}/")
print("Health Check:", response.json())

# Test 2: Get video info
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
response = requests.post(
    f"{API_URL}/api/info",
    json={"url": video_url}
)
print("\nVideo Info:", json.dumps(response.json(), indent=2))

# Test 3: Download video
response = requests.post(
    f"{API_URL}/api/download",
    json={
        "url": video_url,
        "quality": "720p",
        "format": "mp4",
        "audio_only": False
    }
)

if response.status_code == 200:
    with open("test_video.mp4", "wb") as f:
        f.write(response.content)
    print("\n✅ Video downloaded: test_video.mp4")
else:
    print("\n❌ Download failed:", response.text)
```

Run:
```bash
python test.py
```

---

## 🌐 **Test Frontend Integration:**

### **Option 1: Simple HTML Test Page**

Create `test_frontend.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Backend Test</title>
</head>
<body>
    <h1>Video Downloader Test</h1>
    
    <input type="text" id="videoUrl" placeholder="Enter video URL" style="width:400px">
    <button onclick="testInfo()">Get Info</button>
    <button onclick="testDownload()">Download</button>
    
    <pre id="result"></pre>

    <script>
        const API_URL = 'http://localhost:5000';

        async function testInfo() {
            const url = document.getElementById('videoUrl').value;
            const response = await fetch(`${API_URL}/api/info`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url})
            });
            const data = await response.json();
            document.getElementById('result').textContent = JSON.stringify(data, null, 2);
        }

        async function testDownload() {
            const url = document.getElementById('videoUrl').value;
            const response = await fetch(`${API_URL}/api/download`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    url,
                    quality: '720p',
                    format: 'mp4',
                    audio_only: false
                })
            });
            
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = 'video.mp4';
            a.click();
        }
    </script>
</body>
</html>
```

Browser mein open karo: `test_frontend.html`

---

## 🐛 **Common Issues:**

### **Port Already in Use:**

```
Error: Address already in use
```

**Solution:**
```cmd
# Kill process on port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Or change port in app.py
port = int(os.environ.get('PORT', 8000))  # Change to 8000
```

---

### **Module Not Found:**

```
Error: No module named 'flask'
```

**Solution:**
```cmd
# Make sure venv is activated
pip install -r requirements.txt
```

---

### **yt-dlp Download Error:**

```
Error: Unable to extract video data
```

**Possible Reasons:**
- Video URL invalid
- Geo-restricted content
- Age-restricted video
- Private video

**Test with public video:**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

---

### **CORS Error (from browser):**

```
Access to fetch blocked by CORS policy
```

**Already fixed in code!** `flask-cors` installed hai.

---

## 📊 **Performance Test:**

### **Test Different Platforms:**

```python
test_urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # YouTube
    "https://www.tiktok.com/@username/video/1234567890",  # TikTok
    "https://www.instagram.com/reel/ABC123/",  # Instagram
    "https://twitter.com/user/status/1234567890",  # Twitter
]

for url in test_urls:
    print(f"\nTesting: {url}")
    # Your test code
```

---

## 🔍 **Debug Mode:**

App.py mein last line change karo:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # debug=True
```

**Debug mode features:**
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

**⚠️ Production mein `debug=False` rakho!**

---

## 📝 **Test Checklist:**

- ✅ Python installed
- ✅ Virtual environment created
- ✅ Dependencies installed
- ✅ Server starts without errors
- ✅ Health endpoint works
- ✅ Info endpoint works
- ✅ Download endpoint works
- ✅ Multiple platforms tested
- ✅ Different qualities tested
- ✅ Audio-only tested
- ✅ Error handling tested
- ✅ Frontend integration tested

---

## 🚀 **Ready for Deployment:**

Agar sab tests pass ho gaye:

1. ✅ Git commit karo
2. ✅ GitHub pe push karo
3. ✅ Railway/Render pe deploy karo
4. ✅ Production test karo

---

## 💡 **Development Tips:**

1. **Hot Reload:** Debug mode mein code save karo, server auto-reload hoga
2. **Logs:** Terminal mein request logs dikhenge
3. **Testing:** Pehle local test karo, phir deploy karo
4. **Git:** Regular commits karo

---

**Local testing complete! Deploy karne ke liye ready! 🎉**
