#!python

from urllib3 import PoolManager
from bs4 import BeautifulSoup
import re



class WeatherGetter:
    """A simple WeatherGetter class to fetch the weather for a given URL
    
    TODO: Refactor this into a generic WeatherGetter class.
    """

    moncton = 'https://weather.gc.ca/rss/city/nb-36_e.xml'

    def __init__(self):
        self.http = PoolManager()
        self.location = self.moncton # TODO generic
        self.weather = ''
        self.warnings = ''
        self.condition = ''
        self.forecasts = []

    def get_page(self):
        self.response = self.http.request('GET', self.location)
        if self.response.status == 200:
            self.weather = BeautifulSoup(self.response.data, "lxml-xml")
            return True

        return False
    
    def get_warning(self):
        """Return the text of the current weather warnings, otherwise empty string"""

        return self.warnings
    
    def get_condition(self):
        """Return the text of the current weather condition, otherwise empty string"""

        return self.condition
   
    def parse_weather(self):
        """private method, used to parse weather page and extract current conditions and alerts"""

        if not self.weather:
            return False
        entries = self.weather.find_all("entry")

        self.warnings = ''
        self.condition = ''
        self.forecasts = []

        for entry in entries:
            category = entry.find("category").get("term")
            if category == 'Warnings and Watches':
                self.warnings = entry.find("summary").get_text()
                continue
            if category == 'Current Conditions':
                self.condition = entry.find("summary").get_text()
                continue
            if category == 'Weather Forecasts':
                self.forecasts.append(entry)
                continue

            print(f"Unknown entry: {category}")
        
        return True
            

def main(args):
    wg = WeatherGetter()
    if wg.get_page():
        if wg.parse_weather():
            print(f"Warnings: {wg.get_warning()}")
            print(f"Current Conditions: {wg.get_condition()}")
        else:
            print("No Weather Data")

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
