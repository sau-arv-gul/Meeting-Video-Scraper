# 🎥 Meeting Video Scraper
Meeting Video Scraper is a Python-based tool,  developed to scrape and download publicly available government meeting videos from various platforms such as CivicMedia, CivicClerk, YouTube and more.
These videos cover sessions like City Council meetings, Finance Committees, Planning Commissions, Zoning Boards, and other civic organizations.


## ✨ Features

- **Date-based filtering:** 
  filters and collects videos within a user-specified date range
- **Metadata extraction:** Captures video title, date, URL, and source type.
- **Direct video URL:** Extracts direct video URLs, which is downloaded by yt-dlp
- **Proxy:** Uses IP rotation and delays between requests to avoid getting blocked.


## 📟 Tech Stack

- **Requests:** 
  Sending lightweight HTTP requests.
- **BeautifulSoup:** Parsing and navigating HTML content.
- **Selenium:** Automating browser actions & handling dynamic websites.
- **Selenium-Wire:** Extends Selenium to capture requests and responses.
- **yt-dlp:** To download video from direct URL.



## 🧩 Modular Scraper Class Design

Since each website has a unique structure and layout, the scraper is built using dedicated Python classes, one for each base URL. This modular design makes it easy to maintain, debug, and extend.

### 🔹 Scraper Classes

Each base URL is handled by its own class:

- `CivicMediaScraper` : for Lansdale CivicMedia. [website link](https://www.lansdale.org/CivicMedia?CID=2024-Council-Meetings-26)
- `CivicClerkScraper` : for Charleston CivicClerk. [website link](https://charlestonwv.portal.civicclerk.com/)
- `YouTubeScraper` : for YouTube channels. [channel link](https://www.youtube.com/@SLCLiveMeetings/streams)
- `FredericksburgCityScraper` : for Fredericksburg RegionalWebTV. [website link](https://www.regionalwebtv.com/fredcc)
- `WinchesterVirginiaScraper` : for Winchester CivicWeb. [website link](https://winchesterva.civicweb.net/portal/)

### 🔧 Common Methods in Each Class

Each class contains the following methods:

- `get_all_url( )` : Extracts all video links from the base URL  
- `get_filtered_url( )` : Filters and returns only the videos between the specified date range  
- `save( )` : Saves the filtered results into `OUTPUT_1.json`  
- `get_direct_url( )` : for each filtered urls, it extract its direct url and save into `OUTPUT_2.json`.


## 🏛 Project Structure
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


## 🛠️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/sau-arv-gul/Meeting-Video-Scraper.git
cd Meeting-Video-Scraper
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Run the Scraper**
   - You don’t need to manually run individual scraper classes. Just execute Main.py — it automatically:
       - Reads your input from Input.json
       - Scrapes and filters meeting video metadata by date
       - Saves the filtered results to OUTPUT_1.json
       - for each filtered data, it extracts direct video URLs (for downloading with tools like yt-dlp)
       - saves extracted direct link to OUTPUT_2.json
 ```bash
python Main.py
```  

   


