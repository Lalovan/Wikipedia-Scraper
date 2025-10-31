
import os
import json
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor #For Multithreading

MAIN_FOLDER = "/Users/annalalova/workspace/Wikipedia-Scraper/src"
filename = os.path.join(MAIN_FOLDER, "leaders.json")

class WikipediaScraper:

    def __init__(self, countries_url = "countries",leaders_url = "leaders", cookie_url = "cookie" ):
    #This method initialises a wikipedia scraper object  
        self.root_url = "https://country-leaders.onrender.com"
        self.countries_url = countries_url #endpoint
        self.leaders_url = leaders_url #endpoint
        self.cookie_url = cookie_url #endpoint
        self.leaders_data = leaders_data # dictionary, where we store the data
        self.cookie =  # object used for the API calls
        self.session = requests.session()

    def refresh_cookie(self) -> object: #Returns cookie if cookie has expired
        #Use Session() but need to close it __del__ method or by using context manager inside the class


    def get_countries(self) -> list: #returns a list of the supported countries from the API

    def get_leaders(self, country: str) -> None: #populates the leader_data object with the leaders of a country retrieved from the API
        leaders_data

    def get_first_paragraph(self,wikipedia_url: str): #returns the first paragraph (defined by the HTML tag <p>) with details about the leader

    
    def to_json_file(filepath: str): #stores the data structure into a JSON file

    def close(self): #for closing Session

    def threading(): # for threading def scraping_leaders():



#Test:
#scraper = WikipediaScraper()
#scraper.get_leaders("BE")
#scraper.close()
