"""
Video Downloader Backend - 100% Free, No Paid APIs
Supports: YouTube, TikTok, Instagram, Twitter, Facebook, Sora
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import json
import time
from datetime import datetime
import tempfile
import threading
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configuration
DOWNLOAD_DIR = tempfile.gettempdir()
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB limit
CACHE_EXPIRE_HOURS = 2

# Platform detection patterns
PLATFORM_PATTERNS = {
    'youtube': r'(youtube\.com|youtu\.be)',
    'tiktok': r'tiktok\.com',
    'instagram': r'instagram\.com',
    'twitter': r'(twitter\.com|x\.com)',
    'facebook': r'facebook\.com',
    'sora': r'(openai\.com.*sora|sora\.openai\.com)'
}


def detect_platform(url):
    """Detect video platform from URL"""
    for platform, pattern in PLATFORM_PATTERNS.items():
        if re.search(pattern, url, re.IGNORECASE):
            return platform
    return 'unknown'


def clean_old_files():
    """Clean up old downloaded files"""
    try:
        now = time.time()
        for filename in os.listdir(DOWNLOAD_DIR):
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            if os.path.isfile(filepath):
                # Delete files older than CACHE_EXPIRE_HOURS
                if now - os.path.getmtime(filepath) > CACHE_EXPIRE_HOURS * 3600:
                    os.remove(filepath)
    except Exception as e:
        print(f"Cleanup error: {str(e)}")


def get_video_info(url):
    """Extract video metadata without downloading"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'skip_download': True,
        # YouTube bot protection bypass
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['dash', 'hls']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Get available formats
            formats = []
            if 'formats' in info:
                for f in info['formats']:
                    if f.get('vcodec') != 'none':  # Has video
                        format_info = {
                            'format_id': f.get('format_id'),
                            'quality': f.get('format_note', 'Unknown'),
                            'ext': f.get('ext', 'mp4'),
                            'filesize': f.get('filesize', 0),
                            'resolution': f"{f.get('width', '?')}x{f.get('height', '?')}",
                            'fps': f.get('fps', 30),
                            'vcodec': f.get('vcodec', 'unknown'),
                            'acodec': f.get('acodec', 'unknown'),
                        }
                        formats.append(format_info)
            
            # Sort formats by quality
            formats = sorted(formats, key=lambda x: x.get('filesize', 0), reverse=True)
            
            return {
                'success': True,
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'description': info.get('description', '')[:200],
                'upload_date': info.get('upload_date', ''),
                'platform': detect_platform(url),
                'formats': formats[:10],  # Return top 10 formats
                'url': url
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Failed to extract video information'
        }


def download_video(url, quality='best', format_type='mp4', audio_only=False):
    """Download video with specified quality - Multi-platform support"""
    
    # Clean old files before downloading
    threading.Thread(target=clean_old_files).start()
    
    output_template = os.path.join(DOWNLOAD_DIR, '%(title)s_%(id)s.%(ext)s')
    
    # Detect platform for platform-specific settings
    platform = detect_platform(url)
    
    if audio_only:
        # Audio only download (MP3)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['dash', 'hls']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        }
    else:
        # Video download with quality selection
        format_selector = 'best'
        
        if quality == '4k':
            format_selector = 'bestvideo[height<=2160]+bestaudio/best[height<=2160]'
        elif quality == '1080p':
            format_selector = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif quality == '720p':
            format_selector = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif quality == '480p':
            format_selector = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
        elif quality == '360p':
            format_selector = 'bestvideo[height<=360]+bestaudio/best[height<=360]'
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': output_template,
            'merge_output_format': format_type,
            'quiet': False,
            'no_warnings': False,
            # Multi-platform support with bot protection
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['dash', 'hls']
                },
                'tiktok': {
                    'api_hostname': 'api22-normal-c-useast2a.tiktokv.com'
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            # Platform-specific options
            'nocheckcertificate': True,
            'geo_bypass': True,
            'age_limit': None,
        }
        
        # TikTok specific settings
        if platform == 'tiktok':
            ydl_opts['format'] = 'best'
            ydl_opts['http_headers']['Referer'] = 'https://www.tiktok.com/'
        
        # Instagram specific settings
        elif platform == 'instagram':
            ydl_opts['format'] = 'best'
            ydl_opts['http_headers']['Referer'] = 'https://www.instagram.com/'
        
        # Twitter/X specific settings
        elif platform == 'twitter':
            ydl_opts['format'] = 'best'
            ydl_opts['http_headers']['Referer'] = 'https://twitter.com/'
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Get the downloaded file path
            if audio_only:
                filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
            else:
                filename = ydl.prepare_filename(info)
            
            if not os.path.exists(filename):
                # Try without extension and add format_type
                base_name = ydl.prepare_filename(info).rsplit('.', 1)[0]
                filename = f"{base_name}.{format_type}"
            
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                
                return {
                    'success': True,
                    'filepath': filename,
                    'filename': os.path.basename(filename),
                    'title': info.get('title', 'video'),
                    'filesize': file_size,
                    'duration': info.get('duration', 0),
                    'format': format_type if not audio_only else 'mp3',
                    'platform': platform
                }
            else:
                return {
                    'success': False,
                    'error': 'File not found after download'
                }
                
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f'Download failed for {platform}: {str(e)}'
        }


# API Routes

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'Video Downloader Backend API - Multi-Platform Support',
        'version': '2.0.0',
        'platforms': ['YouTube', 'TikTok', 'Instagram', 'Twitter/X', 'Facebook', 'Sora'],
        'endpoints': {
            '/api/info': 'POST - Get video information',
            '/api/download': 'POST - Download video',
            '/api/platforms': 'GET - Supported platforms',
            '/api/health': 'GET - Health check'
        }
    })


@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    """Return supported platforms"""
    return jsonify({
        'success': True,
        'platforms': [
            {'name': 'YouTube', 'id': 'youtube', 'supported': True, 'features': ['4K', 'Audio', 'Subtitles']},
            {'name': 'TikTok', 'id': 'tiktok', 'supported': True, 'features': ['No Watermark', 'HD']},
            {'name': 'Instagram', 'id': 'instagram', 'supported': True, 'features': ['Reels', 'IGTV', 'Posts']},
            {'name': 'Twitter/X', 'id': 'twitter', 'supported': True, 'features': ['HD', 'GIFs']},
            {'name': 'Facebook', 'id': 'facebook', 'supported': True, 'features': ['HD', 'Stories']},
            {'name': 'Sora (OpenAI)', 'id': 'sora', 'supported': True, 'features': ['AI Videos']},
        ]
    })


@app.route('/api/info', methods=['POST'])
def video_info():
    """Get video information and available formats"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            return jsonify({
                'success': False,
                'error': 'Invalid URL format'
            }), 400
        
        # Detect platform
        platform = detect_platform(url)
        if platform == 'unknown':
            return jsonify({
                'success': False,
                'error': 'Unsupported platform. Supported: YouTube, TikTok, Instagram, Twitter, Facebook, Sora'
            }), 400
        
        info = get_video_info(url)
        return jsonify(info)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download', methods=['POST'])
def download():
    """Download video with specified quality and format - Multi-platform"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        quality = data.get('quality', 'best')  # 4k, 1080p, 720p, 480p, 360p, best
        format_type = data.get('format', 'mp4')  # mp4, webm
        audio_only = data.get('audio_only', False)  # True for MP3
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'URL is required'
            }), 400
        
        # Detect and validate platform
        platform = detect_platform(url)
        if platform == 'unknown':
            return jsonify({
                'success': False,
                'error': 'Unsupported platform'
            }), 400
        
        # Start download
        result = download_video(url, quality, format_type, audio_only)
        
        if result['success']:
            # Return file for download
            try:
                return send_file(
                    result['filepath'],
                    as_attachment=True,
                    download_name=result['filename'],
                    mimetype='audio/mpeg' if audio_only else 'video/mp4'
                )
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'File send error: {str(e)}'
                }), 500
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': 'running',
        'platforms_supported': 6
    })


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

