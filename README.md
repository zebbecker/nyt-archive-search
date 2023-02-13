# nyt-archive-search
User friendly web interface for creating datasets from the New York Times archive. 

![Test status](https://github.com/zebbecker/nyt-archive-search/workflows/Django%20CI/badge.svg)
![Python version: 3.9](https://img.shields.io/badge/python-3.9-blue)
![Code style: black](https://img.shields.io/badge/code%20style-black-black)
![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen)

### Archive Search 


### Project Description

Archive Search is a web application that provides an simple, no-code method to search for and download datasets of New York Times articles on a specific topic. With Archive Search, students and researchers can quickly get started on computational text analysis projects. A custom dataset that includes the text of every article in the NYT digital archive that mentions the research topic provides a rich starting point for discovery. 

The ultimate goal of the project is to make an important research method accessible to students and researchers without backgrounds in computer science. The application is pedagogical in nature- dead simple, approachable interfaces take precedence over fine grained control. Users should be able to move on to data analysis within minutes, rather than wasting hours or days setting up custom scripts to download and process data directly from the API that the New York Times provides. 

-----

### Details 

The application is deployed to a small Digital Ocean droplet. The Django app runs inside a Gunicorn WSGI. It uses the ```requests_html``` module to interact with the New York Times Article Search API (v2) and ```pandas``` to manage data collection. [nyt_gatherer.py](https://github.com/zebbecker/nyt-archive-search/blob/main/nyt_archive_search/gatherer/nyt_gatherer.py) houses the primary data collection functionality. 

Because the NYT API has a strict rate limit, users wishing to conduct large searches must provide their own API key. The [Full Search mode](http://159.203.178.166/gatherer/search/) returns a CSV file with metadata and text for each relevant article within the specified date range. 

The [Demo mode](http://159.203.178.166/gatherer/demo/) returns a similar file, but does not require the user to input their own API key. 

### Developers

To run the project locally: 

  Requires: 
   - python 3.9 
   - pip
   - Chrome or chromium
    
1. Clone into the repo: 
```git clone https://github.com/zebbecker/nyt-archive-search.git```
2. (Recommended) activate a [virtual environment](https://docs.python-guide.org/dev/virtualenvs/).
3. Change into inner project directory: ```cd nyt-archive-search/nyt_archive_search/```
4. Install requirements: 
```pip install -r requirements.txt```
5. Set default API key: open the ```config.py``` file and replace the empty NYT_API_KEY value with your own API key. 
6. Run development server: ```./manage.py runserver```
7. Run automated tests: ```./manage.py test```

Access the app through your browser on port [127.0.0.1:8000](http://127.0.0.1:8000/). 

