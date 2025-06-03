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





## Class
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
├── Input.json                       # Sample input JSON for testing
├── Main.py                          # Main script to run metadata scraping
├── OUTPUT_1.json                    # Output of Problem 1 (metadata)
├── OUTPUT_2.json                    # Output of Problem 2 (direct video URLs)
├── Part2.ipynb                      # Jupyter Notebook for video URL resolution
├── requirements.txt                 # Required Python packages
```
