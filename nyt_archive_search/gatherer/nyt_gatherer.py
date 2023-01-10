import datetime as dt
import pandas as pd
import time
import requests
import requests_html
import json
from gatherer.melk_format import MelkRow, melk_fields

SOURCE_NAME = "new_york_times"
TYPE = "article"
# Currently, Article Search API provides results in pages of 10 articles each.
ARTICLES_PER_PAGE = 10


def search_nyt(
    keyword: str,
    start_date: dt.date,
    end_date: dt.date,
    api_key: str,
    download_limit: int,
):
    """
    Main function. Searches for and downloads NYT articles related to keyword and within date range.

    This function uses the Article Search v2 API provided by the New York Times. Note that the Article Search
    API provides results in pages containing information for 10 articles at a time- if a search returns more than
    10 results, this function handles downloading multiple pages of results, making a seperate request for each page.

    Args:
        keyword: string to be searched for. Currently, only one word strings are explicitly supported.
        start_date: Datetime object representing first day of search period.
        end_date: Datetime object representing last day of search period.
        fields: list of column headers for eventual csv database.

    Returns:
        df: a Pandas Dataframe (df) containing collected information about each relevant NYT article found.
            Structured as defined in the file melk_format.py.
    """

    results_page = 0
    next_page = True
    data = []
    total_articles_collected = 0

    while next_page is True:  # loop through pages of API results
        if total_articles_collected >= download_limit:
            next_page = False
            break

        items_downloaded = download_one_page(
            keyword,
            start_date,
            end_date,
            api_key,
            results_page,
            data,
            total_articles_collected,
        )
        total_articles_collected += items_downloaded

        if (
            items_downloaded < ARTICLES_PER_PAGE
            or total_articles_collected >= download_limit
        ):
            # This must be the last page
            next_page = False

        results_page += 1

        if next_page:
            time.sleep(6)

    df = pd.DataFrame(data, columns=melk_fields)

    return df


def download_one_page(
    keyword: str,
    start_date: dt.date,
    end_date: dt.date,
    api_key: str,
    results_page: int,
    data: list,
    next_id: int,
):
    """Collects one page of 10 articles.

    The Article Search API provides results in pages. Each page contains the information for ten articles.
    This function collects the articles from one of those pages. It constructs the API call

    Args:
        keyword: string to be searched for. Currently, only one word strings are explicitly supported.
        start_date: Datetime object representing first day of search period.
        end_date: Datetime object representing last day of search period.
        fields: list of column headers for eventual csv database.
        data: list of MelkRow objects for each collected article.

    Returns:
        items_downloaded: count of how many items were collected from the page being downloaded.
            Note that this does not neccessarily mean this many articles were downloaded: the API sometimes
            returns non-article items in the search results, and these are ignored.

    Raises:
        TypeError: "Error. API key was not recognized in apiconfig.py. API key must be provided as a string. Ex: new_york_times_api_key = 'my_api_key'"
            The default value for new_york_times_api_key in apiconfig.py is None. If it is not a string, this error is raised.
            Note that this does not check if the string is a valid API key with approval for the Article Search API, just that the
            default value has been changed to a string.
    """
    items_downloaded = 0

    # build API call
    api_prefix = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"
    api_query = "q=" + format_keyword(keyword)
    api_filter = (
        "&begin_date="
        + start_date.strftime("%Y")
        + start_date.strftime("%m")
        + start_date.strftime("%d")
        + "&end_date="
        + end_date.strftime("%Y")
        + end_date.strftime("%m")
        + end_date.strftime("%d")
    )
    api_page = "&page=" + str(results_page)
    api_key = "&api-key=" + api_key

    api_call = api_prefix + api_query + api_filter + api_page + api_key

    # retrieve JSON
    page_meta = requests.get(api_call)

    if page_meta.status_code != requests.codes.ok:
        raise RuntimeError(
            "Request to NYT API returned status "
            + str(page_meta.status_code)
            + ". Make sure API key is valid."
        )

    page_meta_list = json.loads(page_meta.text)

    for doc in page_meta_list["response"]["docs"]:
        items_downloaded += 1
        if doc["document_type"] == "article":
            parse_article(doc, data, next_id)
            next_id += 1

    return items_downloaded


def parse_article(article, data, next_id):
    """Converts information for one article into melk format, adds it as a dictionary to data.

    args:
        article: the JSON object for this article from API response.
        data: list of MelkRow objects for each collected article. Appends this_article to data.
        next_id: counter for the ID number that this article should be assigned in database.
    """

    this_article = MelkRow(
        id=next_id,
        source=SOURCE_NAME,
        full_text=scrape_body_text(article["web_url"]),
        type=TYPE,
        title=article["headline"]["main"],
        section=article["section_name"],
        source_url=article["web_url"],
        date=dt.datetime.fromisoformat(article["pub_date"].split("+")[0]).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    )

    data.append(vars(this_article))


def scrape_body_text(url):
    """Scrapes body text from a New York Times article.

    args:
        url: url of article in New York Times archive.

    returns:
        content: Body text of the article, without paragraph breaks.
    """

    session = requests_html.HTMLSession()
    resp = session.get(url)

    # NYT archive webpages use <p class="css-at9mc1 evys1bk0"> elements for article body paragraphs
    sel = resp.html.find(".css-at9mc1")

    content = ""

    for p in sel:
        content = content + p.text + " "

    return content


def format_keyword(keyword: str):
    """
    Strips leading and trailing whitespace, replaces interior spaces with + signs for API request
    """
    return keyword.strip().replace(" ", "+")
