import pandas as pd
import datetime as dt
import gatherer.nyt_gatherer as nyt_gatherer
import gatherer.config as config
import gatherer.melk_format as melk_format

def gatherer(request):
    """
    Main interface. 

    Assembles dataset of relevant items, then saves as a csv file. 

    Returns csv file. 
    """

    start_date, end_date = validate_dates(request.start_date, request.end_date)

    if request.api_key:
        download_limit = request.download_limit
        api_key = request.api_key
    else:
        download_limit = config.NYT_DEFAULT_LIMIT
        api_key = config.NYT_API_KEY
    
    nyt = nyt_gatherer.search_nyt(request.keyword, start_date, end_date, api_key, download_limit)

    filename_out = (
        request.keyword
        + "_" + start_date.isoformat
        + "_" + end_date.isoformat
        + ".csv"
    )
    
    return nyt.to_csv(filename_out)

def validate_dates(start_date:str, end_date:str):
    try:
        start_date = dt.date.fromisoformat(start_date)
        end_date = dt.date.fromisoformat(end_date)
    except ValueError as error:
        raise error
    if start_date >= end_date:
        raise ValueError("Error. Start date must be before end date.")

    return start_date, end_date

    
