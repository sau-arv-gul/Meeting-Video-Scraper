# Charleston, West Virginia
import time
import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CivicClerkScraper:
    def __init__(self,base_url,output_file):
        self.base_url = base_url 
        self.output_file = output_file
    
    def create_browser(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)


    def get_all_url(self,scroll_num = 80):

        """ 
        Scrapes video event metadata from the Charleston WV CivicClerk portal using Selenium.

        As the content on the portal is loaded dynamically with infinite scrolling,
        the function performs multiple upward scrolls within the scrollable container 
        to trigger the loading of additional event entries. Once all content is loaded,
        it identifies and extracts data from video-related HTML elements.

        Args:
            base_url (str): The base URL of the CivicClerk portal.
            scroll_num (int): number of times to scroll up 
        
        Returns:
            List[Dict[str, str]]: A list of dictionaries where each dictionary contains:
                - 'url': Full link to the video event page.
                - 'title': The title of the event.
                - 'date': The date of the event in 'YYYY-MM-DD' format.
                - 'source_type': A fixed value "video" indicating the media type.
            

        """

        driver = self.create_browser()

        try:
            driver.get(self.base_url)

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "scroll-wrap"))
            )

            print("[✓] Scroll container loaded.")
            scroll_wrap = driver.find_element(By.ID, "scroll-wrap")

            print("[i] Scrolling up to load all video links...")
            
            for _ in range(scroll_num):
                driver.execute_script("arguments[0].scrollTop -= 3000;", scroll_wrap)
                time.sleep(1.9)

            print("[✓] Scrolling complete.")

            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="video"]'))
            )

            video_entries = []
            video_divs = driver.find_elements(By.CSS_SELECTOR, '[data-testid="video"]')

            for div in video_divs:
                try:
                    anchor = div.find_element(By.TAG_NAME, "a")
                    video_href = anchor.get_attribute("href")
                    video_href = video_href if video_href.startswith("http") else self.base_url.rstrip("/") + video_href

                    # Get event ID from href
                    event_id = video_href.split("/event/")[1].split("/")[0]

                    # Use the event ID to locate the corresponding event container
                    event_container = driver.find_element(By.CSS_SELECTOR, f"#eventListRow-{event_id}")
                    date = event_container.get_attribute("data-date")[:10]  # yyyy-mm-dd

                    # Get title from the datetime div inside
                    datetime_div = event_container.find_element(By.ID, f"eventListRow-{event_id}-datetime")
                    title = datetime_div.get_attribute("aria-label")

                    video_entries.append({
                        "url": video_href,
                        "title": title,
                        "date": date,
                        "source_type": "video"
                    })

                    print(f"[🎥]  {date} : {video_href}")

                except Exception as e:
                    print(f"[!] Failed to extract info for a video element: {e}")

            print(f"\n[✅] Total video entries collected: {len(video_entries)}")
            return video_entries

        finally:
            driver.quit()
    
    

    def get_filtered_url(self, start_date, end_date, all_video_list):
        """
        Filters video data only within the specified date range.
        The input date strings should be in 'YYYY-MM-DD' format.
        Range is [start_date, end_date] both inclusive.

        Args:
            start_date (str): Start date in 'YYYY-MM-DD' format (inclusive).
            end_date (str): End date in 'YYYY-MM-DD' format (inclusive).
            all_video_list (List[Dict[str, str]]): Output list from get_all_video_links().

        Returns:
            List[Dict[str, str]]: Filtered list of video entries within the date range.
        """

        # Convert input strings to datetime objects
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

        filtered_videos = []

        print("Filtering the videos.....")
        for video in all_video_list:
            try:
                video_date = datetime.strptime(video["date"], "%Y-%m-%d").date()
                if start <= video_date <= end:
                    filtered_videos.append(video)
                    print(f"[🎥]  {video['date']} : {video['url']}")
            except Exception as e:
                print(f"[!] Skipping invalid entry: {e}")

        print(f"[✅] Total Filtered vidoes: {len(filtered_videos)}\n")

        return filtered_videos
    

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

    
    def get_direct_url(self,filtered_videos_list, wait_time=2):
        """
        Extracts and returns a list of direct MP4 URLs from a list of video pages using a single WebDriver instance.

        Args:
            filtered_videos_list (List[Dict[str, str]]): List of video metadata.
            wait_time (int): Time to wait for video elements to load.

        Returns:
            List[str]: List of direct MP4 video URLs (empty strings for failures).
        """

        driver = self.create_browser()
        direct_urls = []

        try:
            for idx, video in enumerate(filtered_videos_list, 1):
                driver.get(video["url"])
                if idx in [1,2,3,4,5]:
                    time.sleep(5)
                else: time.sleep(wait_time)
                
                try:
                    video_element = driver.find_element(By.TAG_NAME, "video")
                    video_url = video_element.get_attribute("src")

                    if video_url:
                        print(f"[{idx}/{len(filtered_videos_list)}]   [🎥] Found: {video_url}")
                        direct_urls.append(video_url)
                    else:
                        print("   [✘] Video tag found but no src.")
                        

                except Exception as e:
                    print(f"   [✘] Error: {e}")
                 

        finally:
            driver.quit()

        return direct_urls  

    def single_direct_url(self,page_url: str, wait_time=5) -> str:

        """
        If we want the mp4 link of a single video
        Extracts the direct video URL from a dynamically loaded web page using Selenium.
        
        Args:
            page_url (str): The URL of the web page containing the video.
            wait_time (int, optional): Time (in seconds) to wait for JavaScript to load. Default is 5 seconds.
            
        Returns:
            str: The direct mp4 video URL if found, otherwise an empty string.
            
        """
        
        # Initialize the WebDriver
        driver = self.create_browser(self, page_url)
        driver.get(page_url)

        # Wait for the JS content (video tag) to load
        time.sleep(wait_time)

        # Try to locate the <video> tag and extract the 'src'
        try:
            video_element = driver.find_element(By.TAG_NAME, "video")
            video_url = video_element.get_attribute("src")
            return video_url
        except Exception as e:
            print(f"❌ Error extracting video URL: {e}")
            return ""
        finally:
            driver.quit()



