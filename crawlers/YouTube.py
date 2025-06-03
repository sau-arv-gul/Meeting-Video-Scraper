
import os
import re
import time
import json
from datetime import datetime
import scrapetube


class YouTubeScraper:
    def __init__(self, channel_url,  output_file):
        self.OUTPUT_FILE = output_file
        self.channel_url = channel_url
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

    def _extract_date_from_title(self, title):
        patterns = [
            (r'(\d{1,2}/\d{1,2}/\d{4})', "%m/%d/%Y"),
            (r'([A-Za-z]+ \d{1,2}, \d{4})', "%B %d, %Y")
        ]

        for pattern, date_format in patterns:
            match = re.search(pattern, title)
            if match:
                try:
                    return datetime.strptime(match.group(1), date_format).date()
                except ValueError:
                    continue

        return None
    
    def get_all_url(self):
        """
        This function extract all the videos of any YouTube channel.
        """
        videos = scrapetube.get_channel(channel_url=self.channel_url,sort_by="newest",content_type="videos")
        print(f"\n[✅] Total YouTube vidoes : {(videos.__sizeof__())}")
        
        i = 0
        all_videos = []
        for video in videos:
            video_id = video["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            all_videos.append(video_url)
            print("[🎥 ]:",video_url )
            i = i+1
         
        print(f"\n[✅] Total YouTube vidoes :",i)
        return all_videos
    
        

    def get_filtered_url(self, start_date, end_date):


        print("================================================")
        print("Scraping YouTube.......")

        videos = scrapetube.get_channel(channel_url=self.channel_url,sort_by="newest",content_type="videos")

        # Convert input strings to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        filtered_video = []
        print("Filtering the videos for [start_date, end_date].........")  
        for video in videos:
            title = video["title"]["runs"][0]["text"]
            video_id = video["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            video_date = self._extract_date_from_title(title)

        
           
            if video_date and start_date <= video_date <= end_date:
                filtered_video.append({
                    "url": video_url,
                    "title": title,
                    "date": video_date.strftime("%Y-%m-%d"),
                    "source_type": "video"
                })

        return filtered_video



    def save(self, filtered_data):
        results = {
            "base_url": self.channel_url,
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

    
    def get_direct_url(self,filtered_videos):
        """
        All extracted links are dwonloadable.
        No need to write seperate code for it 

        """
        return [data['url'] for data in filtered_videos]


# ========================================================================================================

