from flask import Flask, request, jsonify, send_file, render_template
import os
import json
import threading
import time
from datetime import datetime
from chat_downloader import ChatDownloader
import tempfile

app = Flask(__name__)

# Configuration from environment variables
MAX_CONCURRENT_DOWNLOADS = int(os.environ.get('MAX_CONCURRENT_DOWNLOADS', 10))
DEFAULT_TIMEOUT = int(os.environ.get('DEFAULT_TIMEOUT', 7200))  # 2 hours
MAX_MESSAGES_LIMIT = int(os.environ.get('MAX_MESSAGES_LIMIT', 50000))
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# Store active downloads
active_downloads = {}

class ChatDownloadManager:
    def __init__(self):
        self.downloads = {}
        self.stop_flags = {}  # Control flags to stop downloads
    
    def start_download(self, url, output_format='jsonl', max_messages=None, timeout=None):
        download_id = f"download_{int(time.time())}"
        
        # Create temp file
        temp_dir = tempfile.gettempdir()
        filename = f"{download_id}.{output_format}"
        filepath = os.path.join(temp_dir, filename)
        
        # Initialize stop flag
        self.stop_flags[download_id] = False
        
        # Store download info
        self.downloads[download_id] = {
            'url': url,
            'filepath': filepath,
            'status': 'starting',
            'messages_count': 0,
            'start_time': datetime.now().isoformat(),
            'format': output_format,
            'can_stop': True
        }
        
        # Start download in background thread
        thread = threading.Thread(
            target=self._download_chat,
            args=(download_id, url, filepath, output_format, max_messages, timeout)
        )
        thread.daemon = True
        thread.start()
        
        return download_id
    
    def _download_chat(self, download_id, url, filepath, output_format, max_messages, timeout):
        try:
            self.downloads[download_id]['status'] = 'downloading'
            
            downloader = ChatDownloader()
            chat = downloader.get_chat(
                url=url,
                output=filepath,
                max_messages=max_messages,
                timeout=timeout,
                overwrite=True
            )
            
            message_count = 0
            for message in chat:
                # Check if stop was requested
                if self.stop_flags.get(download_id, False):
                    self.downloads[download_id]['status'] = 'stopped'
                    self.downloads[download_id]['end_time'] = datetime.now().isoformat()
                    self.downloads[download_id]['can_stop'] = False
                    break
                
                message_count += 1
                self.downloads[download_id]['messages_count'] = message_count
                
                # Update status every 10 messages
                if message_count % 10 == 0:
                    self.downloads[download_id]['last_update'] = datetime.now().isoformat()
            
            # Only mark as completed if not stopped
            if not self.stop_flags.get(download_id, False):
                self.downloads[download_id]['status'] = 'completed'
                self.downloads[download_id]['end_time'] = datetime.now().isoformat()
            
            self.downloads[download_id]['can_stop'] = False
            
        except Exception as e:
            self.downloads[download_id]['status'] = 'error'
            self.downloads[download_id]['error'] = str(e)
            self.downloads[download_id]['can_stop'] = False
    
    def stop_download(self, download_id):
        """Stop a download and mark it as stopped"""
        if download_id in self.downloads:
            if self.downloads[download_id]['status'] in ['starting', 'downloading']:
                self.stop_flags[download_id] = True
                return True
        return False
    
    def get_status(self, download_id):
        return self.downloads.get(download_id, {'status': 'not_found'})
    
    def get_file(self, download_id):
        if download_id in self.downloads:
            return self.downloads[download_id].get('filepath')
        return None

# Global download manager
download_manager = ChatDownloadManager()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api')
def api_info():
    return jsonify({
        'service': 'Chat Downloader API',
        'version': '1.0.0',
        'endpoints': {
            'POST /download': 'Start chat download',
            'GET /status/<download_id>': 'Check download status',
            'GET /download/<download_id>': 'Download file',
            'GET /health': 'Health check',
            'GET /active': 'List active downloads'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/download', methods=['POST'])
def start_download():
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        # Check concurrent downloads limit
        active_count = len([d for d in download_manager.downloads.values() 
                           if d['status'] in ['starting', 'downloading']])
        if active_count >= MAX_CONCURRENT_DOWNLOADS:
            return jsonify({'error': f'Maximum concurrent downloads ({MAX_CONCURRENT_DOWNLOADS}) reached'}), 429
        
        url = data['url']
        output_format = data.get('format', 'jsonl')
        max_messages = data.get('max_messages')
        timeout = data.get('timeout', DEFAULT_TIMEOUT)
        
        # Validate format
        if output_format not in ['json', 'jsonl', 'csv', 'txt']:
            return jsonify({'error': 'Invalid format. Use: json, jsonl, csv, txt'}), 400
        
        # Validate URL
        if not any(platform in url.lower() for platform in ['twitch.tv', 'youtube.com', 'facebook.com', 'zoom.us']):
            return jsonify({'error': 'Unsupported platform. Use Twitch, YouTube, Facebook, or Zoom URLs'}), 400
        
        # Apply limits
        if max_messages and max_messages > MAX_MESSAGES_LIMIT:
            max_messages = MAX_MESSAGES_LIMIT
        
        if timeout > DEFAULT_TIMEOUT:
            timeout = DEFAULT_TIMEOUT
        
        # Start download
        download_id = download_manager.start_download(
            url=url,
            output_format=output_format,
            max_messages=max_messages,
            timeout=timeout
        )
        
        return jsonify({
            'download_id': download_id,
            'status': 'started',
            'message': 'Download started successfully',
            'config': {
                'url': url,
                'format': output_format,
                'max_messages': max_messages,
                'timeout': timeout
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<download_id>')
def get_status(download_id):
    status = download_manager.get_status(download_id)
    return jsonify(status)

@app.route('/stop/<download_id>', methods=['POST'])
def stop_download(download_id):
    try:
        success = download_manager.stop_download(download_id)
        
        if success:
            return jsonify({
                'message': 'Download stopped successfully',
                'download_id': download_id,
                'status': 'stopping'
            })
        else:
            return jsonify({'error': 'Download not found or cannot be stopped'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<download_id>')
def download_file(download_id):
    try:
        filepath = download_manager.get_file(download_id)
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        status = download_manager.get_status(download_id)
        # Allow download for completed OR stopped downloads
        if status['status'] not in ['completed', 'stopped']:
            return jsonify({'error': 'Download not ready yet. Status: ' + status['status']}), 400
        
        # Check if file has content
        if os.path.getsize(filepath) == 0:
            return jsonify({'error': 'No messages captured yet'}), 400
        
        filename_suffix = "_partial" if status['status'] == 'stopped' else ""
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f"chat_{download_id}{filename_suffix}.{status['format']}"
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/active')
def list_active():
    return jsonify({
        'active_downloads': len(download_manager.downloads),
        'downloads': {k: {
            'status': v['status'],
            'messages_count': v['messages_count'],
            'start_time': v['start_time']
        } for k, v in download_manager.downloads.items()}
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)