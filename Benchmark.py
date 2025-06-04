from yt_dlp import YoutubeDL
import time
# Define options for yt-dlp


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
    'outtmpl': 'aria2c_%(title)s.%(ext)s',  # Output file template
}


ydl_simple= {
    'format': 'best',  # Download the best quality video
    'outtmpl': 'simple_%(title)s.%(ext)s',  # Output file template
}

# URL of the video to download
video_url = [
    "https://cpmedia.azureedge.net/charlestonwv/12e5cc84d9.mp4",
    "https://wms.civplus.tikiliveapi.com/vodhttporigin_civplustest/155443/smil:civplustest/encoded_streams/1/1370/155443.smil/playlist.m3u8?p=vodcdn&chid=93139&ts_chunk_length=6&op_id=1&userId=0&videoId=155443&stime=1748963258&etime=1749049658&token=0cca1d845e7bef34c86b2&ip=157.37.168.111&ua=Mozilla%252F5.0%2B%2528Windows%2BNT%2B10.0%253B%2BWin64%253B%2Bx64%2529%2BAppleWebKit%252F537.36%2B%2528KHTML%252C%2Blike%2BGecko%2529%2BHeadlessChrome%252F137.0.0.0%2BSafari%252F537.36&live=0&avod=1&app_bundle=tikilive.webDevice&domain=civplus.tikiliveapi.com&app_id=0&app_name=TikiLIVE%2BHTML5%2BWeb%2BDevice&cb=1748963233&ccpa=1---&consent=0&device_type=&did=&gdpr=0&h=1080&w=720&livestream=0&min_ad_duration=5&max_ad_duration=30&site_domain=https%3A%2F%2Fcivplus.tikiliveapi.com%2F&site_name=Civic+Plus+-+Tikilive+API+10.0.0&hls_marker=1&debug=true&gender=&age=&content_genre=&content_id=155443&content_title=1267%2B-%2BWork%2BSession%2B12.4.2024&network_name=pa-lansdaleborough&content_owner=1370&viewing_user=guest&oid=1&bid=1370",
    "https://embed-ssl.wistia.com/deliveries/2180fae7f9ce028f07770c8f609632982cec6e3b.m3u8",
    "https://winchesterva.new.swagit.com/videos/294320/download"
]


# =============================== yt-dlp + aria2c =========================================
t1 = time.time()
for url in video_url:
    try:
        with YoutubeDL(aria2c_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"[ERROR] Failed to download {url} - {e}")

t2 = time.time()
ariac_time = (t2-t1)/60
print("yt-dl+ aria2c time: ",ariac_time,"Minutes")


# ================================== simple yt-dlp ========================================
t1 = time.time()
for url in video_url:
    try:
        with YoutubeDL(ydl_simple) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"[ERROR] Failed to download {url} - {e}")
t2 = time.time()
simple_time = (t2-t1)/60

print("yt-dl time: ",simple_time,"Minutes")



print("Total Time taken by ydl       :", simple_time, "minutes")
print("Total Time taken by ydl+aria2c:", ariac_time, "minutes")


