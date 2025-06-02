# Fredericksburg City Council Meeting

import os
import re
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FredericksburgCityScraper:
    def __init__(self,base_url, output_file ):
        self.base_url = base_url
        self.output_file = output_file
        self.start_url = "https://www-regionalwebtv-com.filesusr.com/html/2c630b_4169353b52a2aaf92a9c9e1c8f33282b.html" # scraping starts from here
        self._ensure_output_file()
        

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
        
    def create_browser(self):
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)
    
    def get_all_url(self):
        """
        This methods returns all the video links present on the website 

            
        This method uses a Selenium-controlled browser to scroll through the entire webpage,
        ensuring that all dynamically loaded content is visible. It then extracts and returns
        all video URLs by locating anchor elements corresponding to video cards.

        Returns:
            List[str]: A list of video URLs (strings) found on the page.
        
        Notes:
        - The function continuously scrolls to the bottom of the page until no new content is loaded.
        - Video links are extracted from anchor tags with the CSS selector `a.w-video-card`.

        """

        main_url = self.start_url
        driver = self.create_browser()
        driver.get(main_url)

        try:
            SCROLL_PAUSE_TIME = 2
            last_height = driver.execute_script("return document.body.scrollHeight")

            # Scroll to bottom until no new content is loaded
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            wait = WebDriverWait(driver, 15)
            video_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.w-video-card")))

            video_links = [a.get_attribute("href") for a in video_cards]
            print(f"✅ Found {len(video_links)} videos.")
            for link in video_links:
                print(link)

            return video_links

        except Exception as e:
            print("❌ Error:", e)
            return []
        finally:
            driver.quit()


    def parse_date_from_title(self,title):
        """

        Tries to extract and parse a date from a video title.
        Handles formats like:
        - mm/dd/yyyy
        - m-d-yyyy
        - m-d-yy
        - yyyy
        - mm dd yyyy (space-separated)

        """
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',    # mm/dd/yyyy
            r'\b\d{1,2}-\d{1,2}-\d{4}\b',    # m-d-yyyy
            r'\b\d{1,2}-\d{1,2}-\d{2}\b',    # m-d-yy
            r'\b\d{1,2} \d{1,2} \d{4}\b',    # mm dd yyyy
            r'\b\d{4}\b'                     # yyyy
        ]

        for pattern in date_patterns:
            match = re.search(pattern, title)
            if match:
                date_str = match.group()
                for fmt in ("%m/%d/%Y", "%m-%d-%Y", "%m-%d-%y", "%m %d %Y", "%Y"):
                    try:
                        return datetime.strptime(date_str, fmt).date()
                    except ValueError:
                        continue
        print(f"[WARN] Failed to parse date from title: '{title}'")
        return None



    def get_filtered_url(self, start_date_str, end_date_str):

        """
        Extract video data from a dynamically loaded webpage within a specified date range.

        This method scrolls through a webpage to load all video entries, extracts video information,
        parses the date from each title, and filters videos that fall within the inclusive range from
        `start_date_str` to `end_date_str`.

        Args:
            start_date_str (str): Start date in "YYYY-MM-DD" format.
            end_date_str (str): End date in "YYYY-MM-DD" format.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, each containing the following keys:
                - 'title': The title of the video (str).
                - 'url': The URL linking to the video (str).
                - 'date': The date of the video in ISO format (YYYY-MM-DD) (str).

        Notes:
            - Dates are extracted from the last token in the video title (expected in MM/DD/YYYY format).
            - Videos without valid date parsing are ignored.
            - The function prints the number and details of videos found within the range.

        Exceptions:
            Catches and prints any exceptions during execution, returning an empty list in such cases.

        """
        main_url = self.start_url
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        driver = self.create_browser()
        driver.get(main_url)

        try:
            SCROLL_PAUSE_TIME = 2
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            wait = WebDriverWait(driver, 15)
            video_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.w-video-card")))

            filtered_videos = []

            for a in video_cards:
                link = a.get_attribute("href")
                try:
                    title_elem = a.find_element(By.CSS_SELECTOR, "div > div > div:nth-child(2) > h3")
                    title = title_elem.text.strip()
                except:
                    continue  # Skip if title not found

                # Extract date from title (assumed at end)
                if " " in title:
                    last_token = title.strip().split()[-1]  # Expecting mm/dd/yyyy
                    video_date = self.parse_date_from_title(last_token)
                else:
                    video_date = None

                if video_date and start_date <= video_date <= end_date:
                    filtered_videos.append({
                        "title": title,
                        "url": link,
                        "date": video_date.isoformat(),
                        "source_type": "video"
                    })

            print(f"\n✅ Found {len(filtered_videos)} video(s) in range [{start_date} to {end_date}]:")
            for v in filtered_videos:
                print(f"🎬 {v['title']}\n 🔗 {v['url']}\n")

            return filtered_videos  

        except Exception as e:
            print("❌ Error:", e)
            return []
        finally:
            driver.quit()


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


    # ======= Extract m3u8 Video Metadata =======
    def single_video_m3u8(self, single_url):
 
        """

        Extract metadata and direct video URL (m3u8) from a single video page.

        This method opens the provided `single_url` in a Selenium-controlled browser, waits for a
        JSON-LD script tag to load, extracts its content, and parses it to retrieve the video’s title,
        upload date, and direct streamable URL (typically an `.m3u8` link).

        Args:
            single_url (str): The URL of the individual video page to extract data from.

        Returns:
            dict : A dictionary with the following keys if successful:
                - 'title' (str): The title of the video.
                - 'date' (str): The upload date in 'YYYY-MM-DD' format.
                - 'video_url' (str): The direct URL to the video content (an m3u8 stream).
            Returns `None` if extraction fails due to any error.

        Notes:
            - This function relies on the presence of a script tag with ID `w-channel-bxn9claes7-json-ld`
              containing video metadata in JSON-LD format.
            - The browser is properly closed using `driver.quit()` in all cases.

        """

        driver = self.create_browser()
        driver.get(single_url)

        try:
            wait = WebDriverWait(driver, 10)

            # Wait for the element to appear by ID
            wait.until(
                EC.presence_of_element_located((By.ID, "w-channel-bxn9claes7-json-ld"))
            )

            # Re-find the element to avoid stale reference
            script_elem = driver.find_element(By.ID, "w-channel-bxn9claes7-json-ld")

            raw_json = script_elem.get_attribute("innerHTML")
            video_data = json.loads(raw_json)

            title = video_data.get("name", "Untitled").strip()
            date = video_data.get("uploadDate", "").split("T")[0]
            video_url = video_data.get("contentUrl", None)

            print(f"📌 Title     : {title}")
            print(f"📅 Date      : {date}")
            print(f"🎬 Direct URL : {video_url}\n")

            return {
                "title": title,
                "date": date,
                "video_url": video_url
            }

        except Exception as e:
            print("❌ Error:", e)
            return None
        finally:
            driver.quit()


    def get_direct_url(self, filtered_data):
        """
        Extract direct video URLs (.m3u8) and metadata for a list of video pages.

        This function uses a single Selenium browser instance to iterate over a list of filtered
        video URLs. For each URL, it navigates to the video page, waits for a specific JSON-LD
        metadata script to load, parses it, and extracts:
            - Title of the video
            - Upload date
            - Direct .m3u8 stream URL

        The extracted data is stored in a dictionary and appended to the results list.

        Args:
            filtered_data (list): A list of dictionaries, each containing a 'url' key pointing
                                to a video page.

        Returns:
            list: List[str]: List of direct MP4 video URLs (empty strings for failures).

        Notes:
            - Uses one shared Selenium browser instance for better performance and resource management.
        """

        direct_urls = []
        urls = [data['url'] for data in filtered_data]
        driver = self.create_browser()

        try:
            for url in urls:
                print(f"Finding .m3u8 link....")
                time.sleep(0.3)  # wait 
                try:
                    driver.get(url)
                    wait = WebDriverWait(driver, 10)
                    wait.until(EC.presence_of_element_located(
                        (By.ID, "w-channel-bxn9claes7-json-ld")
                    ))

                    script_elem = driver.find_element(By.ID, "w-channel-bxn9claes7-json-ld")
                    raw_json = script_elem.get_attribute("innerHTML")
                    video_data = json.loads(raw_json)

                    title = video_data.get("name", "Untitled").strip()
                    date = video_data.get("uploadDate", "").split("T")[0]
                    video_url = video_data.get("contentUrl", None)

                    print(f"📌 Title     : {title}")
                    print(f"📅 Date      : {date}")
                    print(f"🎬 Direct URL : {video_url}\n")

                    direct_urls.append(video_url)
                except Exception as e:
                    print(f"❌ Error processing {url}: {e}")
                    continue

        finally:
            driver.quit()

        return direct_urls

# ========================================================================================================


# t1 = time.time()
# with open('Input.json', 'r') as f:
#     input_data = json.load(f)
# start_date = input_data['start_date']  # format: "2024-11-20"
# end_date = input_data['end_date']      # format: "2024-11-26"


# base_url = "https://www.regionalwebtv.com/fredcc"
# output_file = "Metadata_result.json"
# scraper = FredericksburgCityScraper(base_url,output_file)
# filter_url = scraper.get_filtered_url(start_date,end_date)
# scraper.save(filter_url)
# direct = scraper.get_direct_url(filter_url)
# print(len(direct))
