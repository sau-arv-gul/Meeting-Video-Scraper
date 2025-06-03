

import os
import time
import json
import random
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from seleniumwire import webdriver as wire_webdriver



# ===================================================== CUSTOME CLASS  ==============================
class CivicMediaScraper:
    def __init__(self, base_url,  output_file,proxy_list):
        self.OUTPUT_FILE = output_file
        self.CivicMedia_url = base_url
        self.proxy_list = proxy_list 
        self.HEADERS = {"User-Agent": "Mozilla/5.0"}
        self._ensure_output_file()
        

    def _ensure_output_file(self):
        """
        Checks if the output file exists. If not, creates a new file with an empty list.

        This method makes sure the file specified by `self.output_file` is present.
        If the file doesn't exist, it creates the file and writes an empty JSON array `[]` to it.
        This helps avoid errors when trying to save or read data later.
        """
        if not os.path.exists(self.OUTPUT_FILE):
            with open(self.OUTPUT_FILE, 'w') as f:
                json.dump([], f)
        
    def get_random_proxy(self):
        return random.choice(self.proxy_list)
    
    def get_all_url(self):

        """
        Get All web url of the vidoes from different pages ( Pagination )
        """
        # Setup Chrome
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
    
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 7)

        # Target URL
        base_url = "https://www.lansdale.org"
        start_url = self.CivicMedia_url
        driver.get(start_url)

        video_links = []
        page_num = 1

        def extract_links():
            elements = driver.find_elements(By.CSS_SELECTOR, 'a[id^="ctl00_ctl00_MainContent_ModuleContent_ctl00_videoListingControl_lvwVideos"]')
            for el in elements:
                href = el.get_attribute('href')
                title = el.text.strip()
                if href and 'VID=' in href:
                    video_links.append((title, href))

        def click_pagination_and_wait(postback_id):
            driver.execute_script(f"document.getElementById('__EVENTTARGET').value = '{postback_id}';")
            driver.execute_script("document.getElementById('aspnetForm').submit();")
            time.sleep(3)

        while True:
            print(f"Scraping Page {page_num}")
            wait.until(EC.presence_of_element_located((By.ID, "ctl00_ctl00_MainContent_ModuleContent_ctl00_videoListingControl_pagingSection")))

            extract_links()

            # Find next pagination link
            pagination = driver.find_elements(By.CSS_SELECTOR, '#ctl00_ctl00_MainContent_ModuleContent_ctl00_videoListingControl_dpgVideos a')
            next_postback_id = None
            for a in pagination:
                if a.text == str(page_num + 1):
                    href = a.get_attribute('href')
                    if "__doPostBack" in href:
                        next_postback_id = href.split("'")[1]
                        break

            if not next_postback_id:
                print("No more pages.")
                break

            click_pagination_and_wait(next_postback_id)
            page_num += 1

        driver.quit()

        ALL_Links = [start_url]
        i = 0
        for _, link in video_links:
            full_link = base_url + link if link.startswith('/') else link
            ALL_Links.append(full_link)
            i = i+1
            print(f"{i}. {full_link}")
            
        print(f"\n[✓] Total Video Links Found: {len(ALL_Links)}")
        return ALL_Links
    
    
    # =========================== PART 1: Filtered the links within [start_date, end_date ] ============================
    def parse_date(self, date_str):
        # e.g., "January 24, 2024"
        return (datetime.strptime(date_str.strip(), "%B %d, %Y") - timedelta(days=1)).date()

    def get_filtered_url( self, start_date, end_date,all_video_urls):
        """
        It returns the links which are within [start_date, end_date]

        """ 
        raw_links = all_video_urls
        print(f"\nFiltering videos between {start_date} and {end_date}...")

        filtered_videos = []

        # Ensure input dates are datetime.date objects
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        

        max_retries = 6
        for link in raw_links:
            for _ in range(max_retries):
                proxy = self.get_random_proxy()
                try:
                    response = requests.get(link, headers=self.HEADERS, proxies={"http": proxy, "https": proxy}, timeout=6)
                    time.sleep(0.5)

                    if response.status_code == 200:
                        print(f"[✓] Success via PROXY : {proxy}")
                        soup = BeautifulSoup(response.text, 'html.parser')

                        title_tag = soup.find('h1')
                        title = title_tag.text.strip() if title_tag else "Untitled"

                        date_tag = soup.select_one('div.videoMeta dd.first')
                        if not date_tag:
                            print(f"[!] Date not found for: {link}")
                            break

                        actual_date = self.parse_date(date_tag.text)

                        if start_date <= actual_date <= end_date:
                            filtered_videos.append({
                                "url": link,
                                "title": title,
                                "date": actual_date.strftime("%Y-%m-%d"),
                                "source_type": "video"
                            })

                        break  # Exit retry loop on success

                    else:
                        print(f"[x] Failed with proxy {proxy}, status: {response.status_code}")

                except Exception as e:
                    print(f"[!] Error with proxy {proxy} on {link}: {e}")

        print(f"\n[✓] Total Filtered:  {len(filtered_videos)} videos ")
        return filtered_videos 

    
    def save(self, filtered_data):
        results = {
            "base_url": self.CivicMedia_url,
            "medias": filtered_data
        }

        # Load existing data
        with open(self.OUTPUT_FILE, 'r') as f:
            existing_data = json.load(f)

        existing_data.append(results)

        # Save updated data
        with open(self.OUTPUT_FILE, 'w') as f:
            json.dump(existing_data, f, indent=2)

        print(f"\n[✓] Saved {len(results['medias'])} videos to {self.OUTPUT_FILE}")

    

    def single_direct_url(self, url):
        """
        The function uses Selenium Wire to capture network requests
        and extract direct video stream URLs (e.g., .m3u8 or .mp4) from a given video page URL.

        Args:
            url (str): The URL of the video page to scrape.

        Returns:
            str: The direct video URL if found, otherwise None.(.m3u8)
        """
        # Setup Chrome with Selenium Wire to capture network requests
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Create a Selenium Wire browser
        driver = wire_webdriver.Chrome(options=chrome_options)

        try:
            driver.get(url)
            time.sleep(3)  # Allow time for page to load and requests to be captured

            # Inspect all captured requests for .m3u8 or .mp4
            for request in driver.requests:
                if request.response and (".m3u8" in request.url or ".mp4" in request.url):
                    print("🎬 Found direct URL:",request.url )
                    
                    return request.url

            print("❌ No direct video URL (.m3u8 or .mp4) found.")
            return None

        finally:
            driver.quit()
    
    def get_direct_url(self, filtered_urls):
        """
        Input list of video metadata and extracts direct video URLs.
        Extracts direct video stream URLs (e.g., .m3u8 or .mp4)
        from a list of video metadata dictionaries.


        Args:
            filtered_urls (List[Dict[str,.,str]]): List of video metadata.

        Returns:
            List[str]: A list of direct video URLs successfully extracted.
        """
        urls = [data["url"] for data in filtered_urls]
        direct_urls = []



        for link in urls:
            print(f"\nExtracting Direct Link ...")
            try:
                direct_url = self.single_direct_url(link)
                if direct_url:
                    direct_urls.append(direct_url)
                else:
                    print(f"[✗] No direct video URL found for: {link}")
            except Exception as e:
                print(f"[!] Error processing {link}: {e}")
                continue  # Ensure the loop continues on error

        return direct_urls
        

    

# ========================================================================================================
    


