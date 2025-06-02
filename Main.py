from crawlers.YouTube import YouTubeScraper
from crawlers.CivicClerk import CivicClerkScraper
from crawlers.Winchester import WinchesterVirginiaScraper
from crawlers.Fredericksburg import FredericksburgCityScraper
from crawlers.CivicMedia import CivicMediaScraper
import json
import time

proxy_list = [
    "http://tifmppwg:849zwtk9z39z@198.23.239.134:6540",
    "http://tifmppwg:849zwtk9z39z@207.244.217.165:6712",
    "http://tifmppwg:849zwtk9z39z@107.172.163.27:6543",
    "http://tifmppwg:849zwtk9z39z@161.123.152.115:6360",
    "http://tifmppwg:849zwtk9z39z@23.94.138.75:6349",
    "http://tifmppwg:849zwtk9z39z@216.10.27.159:6837",
    "http://tifmppwg:849zwtk9z39z@136.0.207.84:6661",
    "http://tifmppwg:849zwtk9z39z@64.64.118.149:6732",
    "http://tifmppwg:849zwtk9z39z@142.147.128.93:6593",
    "http://tifmppwg:849zwtk9z39z@154.36.110.199:6853"
]

with open('Input.json', 'r') as f:
    input_data = json.load(f)
start_date = input_data['start_date']  # format: "2024-11-20"
end_date = input_data['end_date']      # format: "2024-11-26"

BASE_URLS = input_data["base_urls"]
OUTPUT_FILE = "Output.json"

direct_url_list = [] # to store the direct links of filtered url which can be downloaded by yt_dlp

civic_clerk_scroll_num = 20 # 

for base_url in BASE_URLS:

    if "CivicMedia" in base_url:
        scraper = CivicMediaScraper(base_url, OUTPUT_FILE, proxy_list)  # https://www.lansdale.org/CivicMedia?CID=2024-Council-Meetings-26

        all_url= scraper.get_all_url()
        filter = scraper.get_filtered_url(start_date,end_date,all_url)
        scraper.save(filter) # save the data 
        direct = scraper.get_direct_url(filter) # get the direct url of filtered list 
        if direct:
            direct_url_list.extend(direct) 

    if "civicclerk" in base_url:
        scraper = CivicClerkScraper(base_url, OUTPUT_FILE)    # https://charlestonwv.portal.civicclerk.com/

        all_url = scraper.get_all_url(scroll_num=civic_clerk_scroll_num)
        filter = scraper.get_filtered_url(start_date,end_date,all_url)
        scraper.save(filter)

        direct = scraper.get_direct_url(filter)
        if direct: 
            direct_url_list.extend(direct) 

    elif "youtube" in base_url:
        scraper = YouTubeScraper(base_url, OUTPUT_FILE)   # https://www.youtube.com/@SLCLiveMeetings/streams

        filter = scraper.get_filtered_url(start_date,end_date)
        scraper.save(filter)

        direct = scraper.get_direct_url(filter)
        if direct:
            direct_url_list.extend(direct) 

    elif "fredcc" in base_url:
        scraper = FredericksburgCityScraper(base_url, OUTPUT_FILE)  # https://www.regionalwebtv.com/fredcc

        filter = scraper.get_filtered_url(start_date,end_date)
        scraper.save(filter)

        direct = scraper.get_direct_url(filter)
        if direct:
            direct_url_list.extend(direct)

    elif "winchesterva" in base_url:
        scraper = WinchesterVirginiaScraper(base_url, OUTPUT_FILE,proxy_list) # https://winchesterva.civicweb.net/portal/

        filter = scraper.get_filtered_url(start_date,end_date)
        scraper.save(filter)

        direct = scraper.get_direct_url(filter)
        if direct:
            direct_url_list.extend(direct)



# save the direct links in a json file
with open("direct_urls.json", "w") as f:
    json.dump(direct_url_list, f, indent=4)


