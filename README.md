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

4. **Download videos**
```bash
python BOUNUS.py
```


## 🚀 Want to Run or Test Each Scraper Separately?

If you want to run, inspect, or test each scraper class individually — no problem!  
Check out this [Google Colab notebook](https://colab.research.google.com/drive/1x5roTvC3zV75O14UmLH1mdDUejFMNOTj?usp=sharing) where you can:

- Run individual scraper classes
- Apply custom date ranges
- Explore filtered results in isolation

Perfect for debugging, experimenting, or scraping from specific platforms as needed.


## 🔍 Testing Data Part 2
- The testing url of part 2 was done in this [Google Colab notebook](https://colab.research.google.com/drive/1W5bPFRhP1id0fE0y1CZgN3CjcPfaTjkk?usp=sharing)
- One of the bonus challenge URLs was also successfully resolved — see the final section of the notebook for details.
   


## ⚠️ Challenges Faced During Extraction

While building this scraper, I encountered several complex scenarios that made extraction non-trivial. Here are some key technical challenges:

- **🔐 Blocked Access to Direct Video Links**  
  - Some `.m3u8` HLS stream URLs returned **403 Forbidden** errors when accessed outside the site. These were often protected by referrer policies or temporary session tokens tied to an authenticated browser session.

- **📦 Blob URLs Cannot Be Downloaded**  
  - Platforms like IBM Cloud Video or Viebit use `blob:` URLs (e.g., `blob:https://...`) in their `<video>` tags. These URLs are temporary, in-memory browser references and do **not** point to actual downloadable video files like `.mp4` or `.m3u8`.

- **⚙️ Dynamic JavaScript Rendering**  
  - The video players and metadata are often rendered dynamically using JavaScript. This makes standard tools like `requests` or `BeautifulSoup` ineffective, since they can't execute JavaScript. Tools like `selenium-wire` were necessary to capture underlying network requests.

- **🔄 JavaScript-Based Pagination**  
  - Some websites used ASP.NET-style pagination (`__doPostBack(...)`), which triggers JavaScript-based POST requests instead of changing page URLs. Scraping these required simulating those POST actions manually.

- **🎥 HLS Streaming Instead of Direct `.mp4` Files**  
  - Many sites used HTTP Live Streaming (HLS), which splits videos into `.ts` segments served via `.m3u8` playlists. Extracting usable download links required identifying and interpreting those manifests.

---

These issues gave me deeper insights into how streaming platforms work under the hood — particularly regarding **referrer policies**, **authenticated sessions**, and **dynamic video delivery mechanisms**. Each challenge improved the robustness of the scraper and broadened my technical understanding.



### 📚 Disclaimer
This project is for **educational purposes only**.
It demonstrates how public video links can be extracted using basic scraping techniques, while respecting site limits and structure.

🔒 No login-restricted or private content was accessed.

Please use responsibly and respect each website’s terms of service.
