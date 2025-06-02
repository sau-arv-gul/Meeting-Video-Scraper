import os
import json
import threading
from yt_dlp import YoutubeDL

# Load video URLs
with open('direct_urls.json', 'r') as f:
    urls = json.load(f)

# Create downloads directory if it doesn't exist
download_dir = 'downloads'
os.makedirs(download_dir, exist_ok=True)

# Configure aria2c + yt-dlp options
aria2c_opts = {
    'external_downloader': 'aria2c',
    'external_downloader_args': [
        '--max-connection-per-server=10',
        '--split=16',
        '--min-split-size=1M',
        '--retry-wait=6',
        '--timeout=30',
        '--allow-overwrite=true'
    ],
    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s')  # Save in downloads/
}

# Download function
def download_video(url):
    try:
        with YoutubeDL(aria2c_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"[ERROR] Failed to download {url} - {e}")

# Start threads
threads = []
for url in urls:
    t = threading.Thread(target=download_video, args=(url,))
    t.start()
    threads.append(t)

# Wait for all threads to complete
for t in threads:
    t.join()

print("✅ All downloads completed and saved in 'downloads/' folder.")
