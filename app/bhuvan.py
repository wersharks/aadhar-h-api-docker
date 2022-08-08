import requests
from bs4 import BeautifulSoup
import re

ENDPOINT_NEARBY_CENTER_LAT_LONG = "https://bhuvan.nrsc.gov.in/aadhaar/usrtask/app_specific/get/getpinsearchDetails.php?sno={y}_{x}_{r}&str=&str2=&arr="
REGEX_EXTRACT_DATA_UNIQ_LAT_LONG = "\",(\d+)\),zoom_to_centre.*addmarker\((.*),(.*)\)"

class BhuvanScraper:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def scrape(self):
        api = ENDPOINT_NEARBY_CENTER_LAT_LONG.format(x=self.x, y=self.y, r=self.r)
        r = requests.get(api)
        soup = BeautifulSoup(r.content, 'html.parser')

        entries = soup.findAll('td', {"onclick" : True})
        data = {}
        data["code"] = 1
        data["data"] = []
        for entry in entries:
            edata = {}
            markerdata = entry["onclick"]
            name = entry.find('div', class_="vCenterName").text
            loc = entry.find('div', class_="vCenterAdd").text

            rgx = re.search(REGEX_EXTRACT_DATA_UNIQ_LAT_LONG, markerdata, re.IGNORECASE)
            if(rgx):
                uniq = rgx.group(1)
                lat = rgx.group(2)
                lon = rgx.group(3)

                edata["uid"] = uniq
                edata["lat"] = lat
                edata["lon"] = lon

            edata["centerName"] = name
            edata["location"] = loc

            data["data"].append(edata)

        data["len"] = len(entries)
        return data

if(__name__=="__main__"):
    # Thapar at 76.3734846_30.3498628_10
    b = BhuvanScraper(30.3498628, 76.3734846, 10)
    print(b.scrape())