import re
import os
import time
import json
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class WinchesterVirginiaScraper:
    def __init__(self,base_url,output_file,proxy_list):
        self.base_url = base_url
        self.proxy_list = proxy_list
        self.output_file = output_file
        self._ensure_output_file()
        self.HEADERS = {"User-Agent": "Mozilla/5.0"}
        self.archiev_url = "https://winchesterva.new.swagit.com/views/82/"
        
        

    def _ensure_output_file(self):
        """
        Checks if the output file exists. If not, creates a new file with an empty list.

        This method makes sure the file specified by `self.output_file` is present.
        If the file doesn't exist, it creates the file and writes an empty JSON array `[]` to it.
        This helps avoid errors when trying to save or read data later.
        """
        if not os.path.exists(self.output_file):
            with open(self.output_file, 'w') as f:
                json.dump([], f)
        
    

    def get_random_proxy(self,proxy_list):
        return random.choice(proxy_list)
    
    def parse_date(self, date_str):
        """
        Converts a date string like 'Sep 09, 2024' to a date object.

        Args:
            date_str (str): Date in the format '%b %d, %Y'.

        Returns:
            date or None: Parsed date object, or None if parsing fails.
        """
        try:
            
            date_obj = datetime.strptime(date_str.strip(), "%b %d, %Y").date()
            return date_obj
        except ValueError as ve:
            print(f"[ERROR] Failed to parse date: '{date_str}' — {ve}")
            return None

    
    def get_filtered_url(self, start_date, end_date):
        """
        Scrape all video metadata of Committee and Council meetings from the website within a given date range.

        The website is organized section-wise, where each section represents a different committee or council.
        Inside each section, videos are further organized by year. This function navigates through each
        section and each year tab to extract all available videos, filtering them based on the given date range.

        Steps:
            - Visit the main archive page.
            - Loop through each section (committee/council).
            - Within each section, loop through each year tab.
            - Scrape the videos listed under that year.
            - Extract title, date, and URL of each video.
            - Filter videos based on the `start_date` and `end_date`.

        Args:
            start_date (str): The start of the date range in 'YYYY-MM-DD' format.
            end_date (str): The end of the date range in 'YYYY-MM-DD' format.

        Returns:
            list: A list of dictionaries, each containing:
                - 'url' (str): Direct link to the video.
                - 'title' (str): Title of the video.
                - 'date' (str): Date of the video in 'YYYY-MM-DD' format.
                - 'source_type' (str): Type of content, always 'video' in this case.

        Notes:
            - Uses rotating proxies to avoid request blocking.
            - Retries the request up to 7 times if it fails due to network issues.
            - Skips any entries with invalid or missing data.

        """
        filtered_data = []

        base_domain = "https://winchesterva.new.swagit.com"
        
        max_retries = 7
        for _ in range(max_retries):
            proxy = self.get_random_proxy(self.proxy_list)
            try:
                response = requests.get(self.archiev_url, headers=self.HEADERS, proxies={"http": proxy, "https": proxy}, timeout=10)
                time.sleep(0.7)
                if response.status_code == 200:
                    print(f"[✓] Success: {self.archiev_url} via PROXY : {proxy}")
                    soup = BeautifulSoup(response.text, 'html.parser')

                    sections = soup.find_all("div", class_="panel panel-inner")
                    for section in sections:
                        heading_tag = section.find("h4", class_="panel-title")
                        if not heading_tag:
                            continue
                        section_name = heading_tag.get_text(strip=True)
                        print(f"\n🔍 Scraping Year wise: {section_name}")
                        

                        collapse_div = section.find("div", class_="panel-collapse collapse")
                        if not collapse_div:
                            continue

                        nav_tabs = collapse_div.find("ul", class_="nav nav-tabs")
                        if not nav_tabs:
                            continue

                        for li in nav_tabs.find_all("li"):
                            year_link = li.find("a")
                            if not year_link:
                                continue

                            year_id = year_link.get("href", "").replace("#", "")
                            year = year_link.get_text(strip=True)
                            print(f"  📅 Year: {year}")

                            tab_content = collapse_div.find("div", id=year_id)
                            if not tab_content:
                                continue

                            table = tab_content.find("table", id="video-table")
                            if not table:
                                continue

                            for tr in table.find("tbody").find_all("tr"):
                                tds = tr.find_all("td")
                                if len(tds) < 2:
                                    continue

                                title_link = tds[0].find("a")
                                if not title_link:
                                    continue

                                video_url = title_link.get("href", "").strip()
                                video_title = title_link.get_text(strip=True)

                                # Extract date
                                date_text = tds[1].get_text(strip=True)
                                video_date = self.parse_date(date_text)

                                if not video_date:
                                    continue  # Skip if date is invalid

                                # Date filtering (compare as date objects)
                                start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
                                end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()

                                if start_dt <= video_date <= end_dt:
                                    filtered_data.append({
                                        "url": base_domain + video_url,
                                        "title": video_title,
                                        "date": video_date.strftime("%Y-%m-%d"),
                                        "source_type": "video"
                                    })

                    break  # Stop retrying on success
                else:
                    print(f"[✗] Failed to fetch page, Status Code: {response.status_code}, Retrying...")

            except Exception as e:
                print(f"[!] Error with proxy {proxy}: {str(e)}. Retrying...")
                continue


        return filtered_data

    def save(self, filtered_data):

        results = {
            "base_url": self.base_url,
            "medias": filtered_data
        }

        # Load existing data
        with open(self.output_file, 'r') as f:
            existing_data = json.load(f)

        existing_data.append(results)

        # Save updated data
        with open(self.output_file, 'w') as f:
            json.dump(existing_data, f, indent=2)

        print(f"\n[✓] Saved {len(results['medias'])} videos to {self.output_file}")     
        

    def get_direct_url(self,filtered_data):
        end = "/download"
        Non_downloadable_url = [data['url'] for data in filtered_data]
        direct_links = []
        for i in Non_downloadable_url:
            direct_links.append(i+end)
        return direct_links
    
# ========================================================================================================      




# # Example usage:
# with open('Input.json', 'r') as f:
#     input_data = json.load(f)
# start_date = input_data['start_date']  # format: "2024-11-20"
# end_date = input_data['end_date']      # format: "2024-11-26"


# OUTPUT_FILE = "Metadata_result.json"



# proxy_list = [
#     "http://tifmppwg:849zwtk9z39z@198.23.239.134:6540",
#     "http://tifmppwg:849zwtk9z39z@207.244.217.165:6712",
#     "http://tifmppwg:849zwtk9z39z@107.172.163.27:6543",
#     "http://tifmppwg:849zwtk9z39z@161.123.152.115:6360",
#     "http://tifmppwg:849zwtk9z39z@23.94.138.75:6349",
#     "http://tifmppwg:849zwtk9z39z@216.10.27.159:6837",
#     "http://tifmppwg:849zwtk9z39z@136.0.207.84:6661",
#     "http://tifmppwg:849zwtk9z39z@64.64.118.149:6732",
#     "http://tifmppwg:849zwtk9z39z@142.147.128.93:6593",
#     "http://tifmppwg:849zwtk9z39z@154.36.110.199:6853"
# ]

# base_url = "https://winchesterva.civicweb.net/portal/"
# scraper = WinchesterVirginiaScraper(base_url,proxy_list,OUTPUT_FILE)
# filtered_url = scraper.get_filtered_url(start_date,end_date)
# # scraper.save(filtered_videos)
# direct_url = scraper.get_direct_url(filtered_url)


