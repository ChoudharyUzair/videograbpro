// Frontend Integration Code for Video Downloader
// Add this to your existing main.js file

// ============================================
// Configuration
// ============================================

// IMPORTANT: Update this URL after deploying backend to Railway/Render
const API_BASE_URL = 'http://localhost:5000';  // Change to your deployed URL
// Example: 'https://video-downloader-api.up.railway.app'

// ============================================
// API Functions
// ============================================

/**
 * Get video information without downloading
 * @param {string} url - Video URL
 * @returns {Promise<Object>} Video metadata
 */
async function getVideoInfo(url) {
  try {
    showLoading(true, 'Fetching video information...');
    
    const response = await fetch(`${API_BASE_URL}/api/info`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'Failed to fetch video info');
    }
    
    showLoading(false);
    return data;
    
  } catch (error) {
    showLoading(false);
    console.error('Error fetching video info:', error);
    showToast('Error: ' + error.message, 'error');
    return { success: false, error: error.message };
  }
}

/**
 * Download video with specified options
 * @param {string} url - Video URL
 * @param {string} quality - Video quality (4k, 1080p, 720p, 480p, 360p, best)
 * @param {string} format - Output format (mp4, webm)
 * @param {boolean} audioOnly - Download audio only (MP3)
 * @returns {Promise<void>}
 */
async function downloadVideo(url, quality = 'best', format = 'mp4', audioOnly = false) {
  try {
    showLoading(true, 'Preparing download...');
    
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
      const errorData = await response.json();
      throw new Error(errorData.error || 'Download failed');
    }
    
    // Get filename from Content-Disposition header if available
    const contentDisposition = response.headers.get('Content-Disposition');
    let filename = 'video.' + (audioOnly ? 'mp3' : format);
    
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
      if (filenameMatch) {
        filename = filenameMatch[1];
      }
    }
    
    // Create blob and trigger download
    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    // Cleanup
    window.URL.revokeObjectURL(downloadUrl);
    
    showLoading(false);
    showToast('Download started successfully!', 'success');
    
    // Add to download history
    addToHistory({
      url,
      filename,
      quality,
      format: audioOnly ? 'mp3' : format,
      timestamp: Date.now()
    });
    
  } catch (error) {
    showLoading(false);
    console.error('Download error:', error);
    showToast('Download failed: ' + error.message, 'error');
  }
}

/**
 * Get list of supported platforms
 * @returns {Promise<Array>} List of platforms
 */
async function getSupportedPlatforms() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/platforms`);
    const data = await response.json();
    return data.platforms || [];
  } catch (error) {
    console.error('Error fetching platforms:', error);
    return [];
  }
}

/**
 * Check if backend is healthy
 * @returns {Promise<boolean>}
 */
async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return response.ok;
  } catch (error) {
    console.error('Backend health check failed:', error);
    return false;
  }
}

// ============================================
// UI Helper Functions
// ============================================

/**
 * Show/hide loading indicator
 * @param {boolean} show - Show or hide
 * @param {string} message - Loading message
 */
function showLoading(show, message = 'Loading...') {
  const loader = document.getElementById('loader');
  const loaderText = document.getElementById('loader-text');
  
  if (loader) {
    loader.style.display = show ? 'flex' : 'none';
    if (loaderText && message) {
      loaderText.textContent = message;
    }
  }
}

/**
 * Show toast notification
 * @param {string} message - Toast message
 * @param {string} type - Toast type (success, error, info)
 */
function showToast(message, type = 'info') {
  // Check if toast container exists
  let toastContainer = document.getElementById('toast-container');
  
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 10000;
    `;
    document.body.appendChild(toastContainer);
  }
  
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.style.cssText = `
    background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
    color: white;
    padding: 16px 24px;
    border-radius: 8px;
    margin-bottom: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    animation: slideIn 0.3s ease;
  `;
  toast.textContent = message;
  
  toastContainer.appendChild(toast);
  
  // Auto remove after 3 seconds
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

/**
 * Display video information in UI
 * @param {Object} info - Video info object
 */
function displayVideoInfo(info) {
  const container = document.getElementById('video-info-container');
  
  if (!container) return;
  
  container.innerHTML = `
    <div class="video-info-card">
      ${info.thumbnail ? `<img src="${info.thumbnail}" alt="Thumbnail" class="video-thumbnail">` : ''}
      <h3>${info.title || 'Unknown Title'}</h3>
      <p><strong>Platform:</strong> ${info.platform || 'Unknown'}</p>
      <p><strong>Duration:</strong> ${formatDuration(info.duration || 0)}</p>
      <p><strong>Uploader:</strong> ${info.uploader || 'Unknown'}</p>
      ${info.view_count ? `<p><strong>Views:</strong> ${formatNumber(info.view_count)}</p>` : ''}
      
      <div class="quality-options">
        <h4>Available Qualities:</h4>
        <select id="quality-select" class="quality-selector">
          <option value="best">Best Quality</option>
          <option value="4k">4K (2160p)</option>
          <option value="1080p">1080p (Full HD)</option>
          <option value="720p" selected>720p (HD)</option>
          <option value="480p">480p (SD)</option>
          <option value="360p">360p</option>
        </select>
        
        <select id="format-select" class="format-selector">
          <option value="mp4" selected>MP4 (Video)</option>
          <option value="webm">WebM (Video)</option>
          <option value="mp3">MP3 (Audio Only)</option>
        </select>
      </div>
    </div>
  `;
  
  container.style.display = 'block';
}

/**
 * Add download to history
 * @param {Object} download - Download info
 */
function addToHistory(download) {
  let history = JSON.parse(localStorage.getItem('downloadHistory') || '[]');
  history.unshift(download);
  history = history.slice(0, 10); // Keep last 10
  localStorage.setItem('downloadHistory', JSON.stringify(history));
  updateHistoryDisplay();
}

/**
 * Update history display
 */
function updateHistoryDisplay() {
  const historyContainer = document.getElementById('download-history');
  if (!historyContainer) return;
  
  const history = JSON.parse(localStorage.getItem('downloadHistory') || '[]');
  
  if (history.length === 0) {
    historyContainer.innerHTML = '<p>No download history yet</p>';
    return;
  }
  
  historyContainer.innerHTML = history.map(item => `
    <div class="history-item">
      <span class="history-filename">${item.filename}</span>
      <span class="history-quality">${item.quality} - ${item.format}</span>
      <span class="history-time">${formatTimestamp(item.timestamp)}</span>
    </div>
  `).join('');
}

// ============================================
// Utility Functions
// ============================================

/**
 * Format duration in seconds to HH:MM:SS
 * @param {number} seconds
 * @returns {string}
 */
function formatDuration(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Format number with commas
 * @param {number} num
 * @returns {string}
 */
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Format timestamp to readable date
 * @param {number} timestamp
 * @returns {string}
 */
function formatTimestamp(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;
  
  // Less than 1 hour
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000);
    return `${minutes} min ago`;
  }
  
  // Less than 24 hours
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000);
    return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  }
  
  // More than 24 hours
  return date.toLocaleDateString();
}

/**
 * Validate video URL
 * @param {string} url
 * @returns {boolean}
 */
function validateURL(url) {
  try {
    const urlObj = new URL(url);
    return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
  } catch {
    return false;
  }
}

// ============================================
// Event Handlers (Example Implementation)
// ============================================

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
  // Check backend health
  const isHealthy = await checkBackendHealth();
  
  if (!isHealthy) {
    showToast('Backend is not responding. Please check your API URL.', 'error');
  }
  
  // Load download history
  updateHistoryDisplay();
  
  // Setup download form handler
  const downloadForm = document.getElementById('download-form');
  if (downloadForm) {
    downloadForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const urlInput = document.getElementById('video-url');
      const url = urlInput?.value.trim();
      
      if (!url) {
        showToast('Please enter a video URL', 'error');
        return;
      }
      
      if (!validateURL(url)) {
        showToast('Please enter a valid URL', 'error');
        return;
      }
      
      // Get video info first
      const info = await getVideoInfo(url);
      
      if (info.success) {
        displayVideoInfo(info);
        
        // Setup download button
        const downloadBtn = document.getElementById('start-download');
        if (downloadBtn) {
          downloadBtn.onclick = () => {
            const quality = document.getElementById('quality-select')?.value || '720p';
            const format = document.getElementById('format-select')?.value || 'mp4';
            const audioOnly = format === 'mp3';
            
            downloadVideo(url, quality, audioOnly ? 'mp4' : format, audioOnly);
          };
        }
      }
    });
  }
});

// ============================================
// Export functions (if using modules)
// ============================================

// Uncomment if using ES6 modules
// export { getVideoInfo, downloadVideo, getSupportedPlatforms, checkBackendHealth };

console.log('✅ Video Downloader Frontend Integration Loaded');
console.log('📡 API URL:', API_BASE_URL);
