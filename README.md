# 📽️ Meeting Video Scraper
Meeting Video Scraper is a Python-based tool,  developed to scrape and download publicly available government meeting videos from various platforms such as CivicMedia, CivicClerk, YouTube and more.
These videos cover sessions like City Council meetings, Finance Committees, Planning Commissions, Zoning Boards, and other civic organizations.


## ✨ Features

- **Date-based filtering:** 
  filters and collects videos within a user-specified date range
- **Metadata extraction:** Captures video title, date, URL, and source type.
- **Direct video URL:** Extracts direct video URLs, which is downloaded by yt-dlp
- **Proxy:** Uses IP rotation and delays between requests to avoid getting blocked.


## 🛠️ Tech Stack

- **Requests:** 
  Sending lightweight HTTP requests.
- **BeautifulSoup:** Parsing and navigating HTML content.
- **Selenium:** Automating browser actions & handling dynamic websites.
- **Selenium-Wire:** Extends Selenium to capture requests and responses.
- **yt-dlp:** To download video from direct URL.



## 🧱 Scraper Class Design

Since each website has a unique structure and layout, the scraper is built using dedicated Python classes — one for each base URL. This modular design makes it easy to maintain, debug, and extend.

### 🔹 Scraper Classes

Each base URL is handled by its own class:

- `CivicMediaScraper` — for Lansdale CivicMedia  
- `CivicClerkScraper` — for Charleston CivicClerk  
- `YouTubeScraper` — for YouTube Live Meeting streams  
- `FredericksburgCityScraper` — for RegionalWebTV (Fredericksburg)  
- `WinchesterVirginiaScraper` — for Winchester CivicWeb  

### 🔧 Common Methods in Each Class

Each class includes the following key methods:

- `get_all_url()` — Extracts all video links from the base URL  
- `get_filtered_url(start_date, end_date)` — Filters and returns only the videos between the specified date range  
- `save()` — Saves the filtered results into `OUTPUT_1.json`  
- `get_direct_url()` — Resolves embedded or indirect video pages into direct video file URLs that can be downloaded using tools like `yt-dlp`


## 📁 Project Structure
```text
Video Scraper/
│
├── crawlers/
│   ├── CivicClerk.py                # Scraper for CivicClerk websites
│   ├── CivicMedia.py                # Scraper for CivicMedia (Lansdale)
│   ├── Fredericksburg.py            # Scraper for RegionalWebTV (Fredericksburg)
│   ├── Winchester.py                # Scraper for Winchester, VA CivicWeb
│   ├── YouTube.py                   # Scraper for YouTube Live Streams
│
├── downloads/                       # Output video download directory
│
├── BONUS.py                         # Bonus problem code (optional task)
├── Input.json                       # input JSON for testing
├── Main.py                          # Main script to run metadata scraping
├── OUTPUT_1.json                    # Output of filtered metadata
├── OUTPUT_2.json                    # direct video URLs of filtered data 
├── Part2.ipynb                      # Jupyter Notebook for video URL resolution
├── requirements.txt                 # Required Python packages
```
