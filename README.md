# Wikipedia-Scraper

**🏢 Description ℹ️**

The ```Wikipedia-Scraper``` is a Python code designed to efficiently retrieve and process data on world leaders from the Country Leaders API. It automatically fetches the list of countries, retrieves leaders for each country, and scrapes the first paragraph of their Wikipedia pages. 

This project provides two Python scripts to retrieve and process data on world leaders from the Country Leaders API.
1. **Procedural Script:** A straightforward, function-based script that fetches countries, retrieves leaders for each, and scrapes the first paragraph from their Wikipedia pages. It demonstrates basic API requests, multithreading for leader pages, and JSON/CSV storage.

2. **OOP Script:** A class-based version using the ```WikipediaScraper``` class. It encapsulates all functionality — session management, cookie handling, data fetching, threading, and saving — into a clean, reusable object-oriented framework. This approach improves readability, maintainability, and scalability, allowing easier modifications or extensions in the future.
Using multithreading, it speeds up the process by fetching multiple leader pages in parallel, while maintaining a shared session for efficient HTTP requests. 

The scraper organizes all data into a dictionary for easy access and later storage. This project demonstrates the power of object-oriented programming for API interaction and web scraping. By encapsulating endpoints, session management, cookie handling, and data parsing in a single class, it offers a clean and reusable framework for structured data retrieval from multiple sources.

**🧱 Repository Structure**

```
Wikipedia-Scraper
.
├── src
├── README.md
├── requirements.txt
├── wikipedia_scraper.ipynb
├── .gitignore
└── src/
├── leaders_scraper_OOP.py
├── leaders_scraper.py

```


**💿 Installation**

Both scripts require Python 3.9+ and the following dependencies:
- ```requests``` for HTTP requests and session management
- ```beautifulsoup4``` for parsing HTML content
- ```lxml``` (or default parser) for efficient HTML parsing


Install dependencies with pip:

```
pip install requests beautifulsoup4 lxml
```

Clone or download the repository, and you can run either script or import the OOP class into your own project.

**📲 Usage**

**Procedural Script:**
```python 

```

**OOP:**
```
```

Both scripts automatically handle cookies and use multithreading to speed up Wikipedia page retrieval. The OOP version additionally organizes functionality into a reusable class with internal state (```self.leaders_per_country```) and shared session management.

**📊 Output:**

Both scripts produce structured output:

**.json:**

```json
{
  "fr": [
    {
      "first_name": "Emmanuel",
      "last_name": "Macron",
      "wikipedia_url": "https://en.wikipedia.org/wiki/Emmanuel_Macron",
      "first_paragraph": "Emmanuel Macron is a French politician..."
    }
```

**csv:**

Mirrors the JSON structure with ```columns``` country and ```leader``` for easy analysis in spreadsheets or data tools like pandas.

The OOP version’s internal workflow is also more modular: 

countries → leaders → threads → first paragraphs → saved files, making it easier to extend or modify, e.g., adding additional parsing or filters per leader.