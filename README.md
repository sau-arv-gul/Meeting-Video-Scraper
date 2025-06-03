# 📽️ Meeting Video Scraper
Meeting Video Scraper is a Python-based tool,  developed to scrape and download publicly available government meeting videos from various platforms such as CivicMedia, CivicClerk, YouTube and more.
These videos cover sessions like City Council meetings, Finance Committees, Planning Commissions, Zoning Boards, and other civic organizations.
## 🛠️ Tech Stack
This project uses the following tools and libraries:

- **Selenium** – For automating browser actions and handling dynamic websites.
- **Selenium-Wire** – Extends Selenium to capture requests and responses.
- **Requests** – For sending lightweight HTTP requests.
- **BeautifulSoup** – For parsing and navigating HTML content.
- **yt-dlp** – For downloading videos from supported platforms using direct URLs.


Each website has a different layout and structure, so the project uses dedicated scraper classes tailored to each platform.
Since each website has a different layout and structure, the project includes a separate scraper class customized for each platform.

## ✨ Features

- **Date-based filtering:** 
  filters and collects videos within a user-specified date range
- **Metadata extraction:** Captures video title, date, URL, and source type.
- **Direct video URL:** Extracts direct video URLs, which is downloaded by yt-dlp
- **Proxy:** Uses IP rotation and delays between requests to avoid getting blocked.
 
