# nyt-archive-search
User friendly web interface for creating datasets from the New York Times archive. 

![Test status](https://github.com/zebbecker/nyt-archive-search/workflows/Django%20CI/badge.svg)
![Python version: 3.9](https://img.shields.io/badge/python-3.9-blue)
![Code style: black](https://img.shields.io/badge/code%20style-black-black)
![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen)

### Project Description

Article Search is a web application that provides an simple, no-code method to search for and download datasets of New York Times articles on a specific topic. 

The ultimate goal of the project is to make an important research method accessible to students and researchers without backgrounds in computer science. The application is pedagogical in nature- dead simple, approachable interfaces take precedence over fine grained control. Users should be able to move on to data analysis within minutes, rather than wasting hours or days setting up custom scripts to download and process data directly from the API that the New York Times provides. 

-----

### Details 

This website is deployed to a Heroku dyno. The Django app runs inside a Gunicorn WSGI and uses '''pandas''' to manage data collection. [nyt_gatherer.py](https://github.com/zebbecker/nyt-archive-search/blob/main/nyt_archive_search/gatherer/nyt_gatherer.py) houses the primary data collection functionality. 

### Developers

To run the project locally: 

  Requires: 
      - python 3.9 
      - pip
    
1. Clone into the repo: 
```git clone https://github.com/zebbecker/nyt-archive-search.git```
2. (Recommended) activate a virtual environment
3. Change into inner project directory: ```cd nyt-archive-search/nyt_archive_search/```
4. Install requirements: 
```pip install -r requirements.txt```
5. Set default API key: open config.py and replace the empty NYT_API_KEY value with your own API key. 
6. Run development server: ```./manage.py runserver```
7. Run automated tests: ```./manage.py test```

Access the app through your browser on port [127.0.0.1:8000](http://127.0.0.1:8000/). 

