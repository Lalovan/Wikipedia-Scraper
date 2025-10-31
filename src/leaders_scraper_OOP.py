import os
import json
import csv
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor #For Multithreading

MAIN_FOLDER = "/Users/annalalova/workspace/Wikipedia-Scraper/src"
os.makedirs(MAIN_FOLDER, exist_ok=True) #Telling python this folder exist...
filename_json = os.path.join(MAIN_FOLDER, "leaders.json")
filename_csv = os.path.join(MAIN_FOLDER, "leaders.csv")

class WikipediaScraper:
    
    """
    This class initialises a wikipedia scraper object  

    Methods: 
    refresh_cookie
    get_countries 
    get_leader
    get_all_leaders
    threads_leader_paragraph
    get_first_paragraph 
    to_json_csv_file
    
    Attributes:
    root_url = "https://country-leaders.onrender.com"
    countries_url = countries_url
    leaders_url = leaders_url 
    cookie_url = cookie_url 
    leaders_per_country = {} 
    session = requests.Session()
    cookie = refresh_cookie() 

    """
    """
    This method initialises a Wikipediascraper object
    """
    def __init__(self, countries_url = "countries",leaders_url = "leaders", cookie_url = "cookie"):
        self.root_url = "https://country-leaders.onrender.com"
        self.countries_url = countries_url #endpoint
        self.leaders_url = leaders_url #endpoint
        self.cookie_url = cookie_url #endpoint
        self.session = requests.Session() # Creating a session first
        self.cookie = self.refresh_cookie() # Using self.session.get() to fetch cookie and storing it
        self.leaders_per_country = {} # initializing a dictionary, where we store the data

    """
    Methods sets up the cookies in the session
    """
    def refresh_cookie(self) -> object: #Returns cookie if cookie has expired; do not need it if session
        req_cookie = self.session.get(f"{self.root_url}/{self.cookie_url}", timeout = 3) #checking for status_code 401, 403
        self.cookie = req_cookie.cookies 
        return req_cookie.cookies

    """
    Core API Fetch Method 1: 
    Retrieving the supported countries
    """
    def get_countries(self) -> list: #returns a list of the supported countries from the API
        countries = self.session.get(f"{self.root_url}/{self.countries_url}", timeout = 3) # Calling the API
        return countries.json() # List of country/countries abbrev .json 
    
    """
    Core API Fetch Method 2: 
    Iterates over countries and calls get_leaders() for each country
    """
    def get_all_leaders(self): #Iterating over countries and saving leaders in a dictionary
        countries = self.get_countries()
        for country in countries: #Iterating over each country
            self.get_leaders(country)
    
    """
    Core API Fetch Method 3:
    Fetches leaders for a single country and starts threads over each
    """

    def get_leaders(self, country: str) -> None: #populates the leader_data object with the leaders of a country retrieved from the API
        leaders = self.session.get(f"{self.root_url}/{self.leaders_url}", cookies = self.cookie, params = {"country": country}, timeout = 3)
        leaders = leaders.json()
        print(f"Processing country: {country}, leaders found: {len(leaders)}")
   
        with ThreadPoolExecutor(max_workers=5) as executor: 
            leaders = list(executor.map(lambda l: self.threads_leader_paragraph(l), leaders)) #Here each call to the threads_leader_paragraph method runs in separate threads.
        self.leaders_per_country[country] = leaders
    
    """
    Processing Method 1: 
    Multithreading
    
    Runs per leader in a thread and delegates the HTTP work (per leader) to the get_first_paragraph method below.
    """

    def threads_leader_paragraph(self, leader):
        wikipedia_url = leader.get("wikipedia_url")
        if wikipedia_url:
            leader["first_paragraph"] = self.get_first_paragraph(wikipedia_url, leader) #Don't need session here, because it uses the one in def get_first_paragraph
        else:
            leader["first_paragraph"] = None
        return leader

    """
    Processing Mehtod 2: 
    Fetches the Wikipedia page and extracts the first paragraph.   
    """
    def get_first_paragraph(self,wikipedia_url: str, leader):
        try: 
            leader_wiki = self.session.get(wikipedia_url,headers = {"User-Agent":"Wikipedia-Scraper(learning project; https://github.com/Lalovan/; contact: anna.ivailova@gmail.com)"}, timeout = 3)
        except (requests.RequestException, TypeError, KeyError) as e:
            print("Request failed:", e)
            return ""   
        
        leader_soup = BeautifulSoup(leader_wiki.text, "html.parser")
        paragraphs = [p.get_text() for p in leader_soup.find_all("p")] # This "get" has nothing to do with the HTTP requests, so it remains as it was 
        first_name = (leader.get("first_name") or "").lower()
        birth_year = (leader.get("birth_date") or "")[:4] 
        
        first_paragraph = ""
        for para in paragraphs:
            para_text = para.strip()
            para_lower = para_text.lower()
            if len(para_text) >= 100 and (first_name in para_lower or birth_year in para_lower):
            # This paragraph passes all checks → pick it
                first_paragraph = para_text
                break
        # Cleaning up the first paragraph; regex
        clean_spaces = re.sub(r"\s+", " ", first_paragraph) # Cleaning up extra spaces
        clean_footnotes = re.sub(r"\[\d+\]", "", clean_spaces) # Cleaning up footnotes numbering [1], [2]
        clean_references = re.sub(r"\[\d+\]", "", clean_footnotes) # Cleaning up references in brackets [a], [b]
        clean_phonetics = re.sub(r"\([^)]*[ˈʃʒɡɲʁðŋ][^)]*\)", "", clean_references) # Cleaning up phenoteic pronunciations
        return clean_phonetics

    """
    Output Method: 
    Saves self.leaders_per_country to .json and .csv
    """
    def to_json_csv_file(self,leaders_per_country, filename_json = "leaders.json", filename_csv = "leaders.csv" ): #stores the data structure into a JSON file
        
        with open(filename_json, "w", encoding="utf-8") as f: # Saving as json
            json.dump(self.leaders_per_country, f, ensure_ascii=False, indent=2)
        with open(filename_csv, "w", newline = "", encoding="utf-8") as csvfile: # Saving as csv
            writer = csv.writer(csvfile)
            writer.writerow(["country", "leader"])
            for country, leaders in self.leaders_per_country.items():
        #Chekcing whether the value is a list: if a list, it loops through it, if not it treats leaders as a single leader name and writes it once
                if isinstance(leaders, list): 
                    for leader in leaders:
                        writer.writerow([country, leader]) #Creates a row per leader
                else:
                    writer.writerow([country, str(leaders)])# Runs in the case the value is not a list

    """
    Cleanup Method:
    Close the underlying session.
    """
    def close(self):
        self.session.close()

#Testing:
scraper = WikipediaScraper("be")
scraper.get_leaders("be")
scraper.to_json_csv_file(filename_json, filename_csv)
scraper.close()
