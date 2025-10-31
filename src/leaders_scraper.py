
import os
import json
import csv
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor

MAIN_FOLDER = "/Users/annalalova/workspace/Wikipedia-Scraper/src"
os.makedirs(MAIN_FOLDER, exist_ok=True) #Telling python this folder exist...
filename_json = os.path.join(MAIN_FOLDER, "leaders.json")
filename_csv = os.path.join(MAIN_FOLDER, "leaders.csv")


""""Thread for a single leader, instead of having a leader-in-leaders loop in the countries loop below"""

def threads_leader_paragraph(leader, session): # Passing session; timeout in the requests ensure smooth running of
    wikipedia_url = leader.get("wikipedia_url")
    if wikipedia_url:
        leader["first_paragraph"] = get_first_paragraph(wikipedia_url, leader, session)
    else:
        leader["first_paragraph"] = None
    return leader

with requests.Session() as session: # "with" handles also the closing of the session

    def get_leaders(session):
        #Defining URLs
        root_url = "https://country-leaders.onrender.com"
        countries_url = "countries"
        leaders_url = "leaders"
        cookie_url = "cookie"    
        #Getting cookies 
        req_cookie = session.get(f"{root_url}/{cookie_url}", timeout = 3)
        #Getting countries
        countries = session.get(f"{root_url}/{countries_url}", cookies = req_cookie.cookies, timeout = 3).json()
        #Iterating over countries and saving leaders in a dictionary
        leaders_per_country = {}
        for c in countries:
            leaders = session.get(f"{root_url}/{leaders_url}", cookies = req_cookie.cookies, params = {"country": c}, timeout = 3)
            leaders = leaders.json()
            
            print(f"Processing country: {c}, leaders found: {len(leaders)}") # Checking progress
            
            # Multithreading : executes for 18.3s, while without it - 22.4s
            # Using lambda to apply a thread to each leader in parallel, while sharing the same session
            with ThreadPoolExecutor(max_workers=5) as executor:
                leaders = list(executor.map(lambda l: threads_leader_paragraph(l, session), leaders))

            leaders_per_country[c] = leaders #Append each result to the leaders dictionary
        return leaders_per_country


def get_first_paragraph(wikipedia_url, leader, session):
    try: 
        leader_wiki = session.get(wikipedia_url,headers = {"User-Agent":"Wikipedia-Scraper(learning project; https://github.com/Lalovan/; contact: anna.ivailova@gmail.com)"}, timeout = 3)
    except (requests.RequestException, TypeError, KeyError) as e:
        print("Request failed:", e)
        return ""   

    leader_soup = BeautifulSoup(leader_wiki.text, "html.parser")
  
    paragraphs = [p.get_text() for p in leader_soup.find_all("p")] # This "get" has nothing to do with the HTTP requests, so it remains as it was 
    first_name = (leader.get("first_name") or "").lower()
    #last_name = (leader.get("last_name") or "").lower()
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

    # Returning cleaned text
    return clean_phonetics

#Testing
leaders_per_country = get_leaders(session)


"""
Saving the leaders.json dictionary and checking the data

"""

def save_leaders(leaders_per_country, filename_json = "leaders.json", filename_csv = "leaders.csv"):
    
    with open(filename_json, "w", encoding="utf-8") as f: # Saving as json
        json.dump(leaders_per_country, f, ensure_ascii=False, indent=2)

    with open(filename_csv, "w", newline = "", encoding="utf-8") as csvfile: # Saving as csv
        writer = csv.writer(csvfile)
        writer.writerow(["country", "leader"])

        for country, leaders in leaders_per_country.items():
        #Chekcing whether the value is a list: if a list, it loops through it, if not it treats leaders as a single leader name and writes it once
            if isinstance(leaders, list): 
                for leader in leaders:
                    writer.writerow([country, leader]) #Creates a row per leader
            else:
                writer.writerow([country, str(leaders)])# Runs in the case the value is not a list

save_leaders(leaders_per_country,filename_json,filename_csv)

#Reading it again
#with open("leaders.json", "r", encoding="utf-8") as f:
    #leaders_loaded = json.load(f)

#Checking if the data is the same
#print("Number of countries:", len(leaders_per_country),len(leaders_loaded))
#for country in leaders_per_country:
    #print(country,len(leaders_per_country[country]),len(leaders_loaded.get(country, [])))