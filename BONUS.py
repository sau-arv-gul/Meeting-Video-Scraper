import os
import json
import threading
from yt_dlp import YoutubeDL

# Load video URLs
with open('OUTPUT_2.json', 'r') as f:
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



t1 = time.time()

for url in urls:
    download_video(url)

t2= time.time()
total_time = (t2-t1)/60

print("✅ All downloads completed and saved in 'downloads/' folder.")
print("Total time to download videos: ",total_time,"Minutes" )
