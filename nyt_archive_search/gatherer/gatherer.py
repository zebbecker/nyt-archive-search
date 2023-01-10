import pandas as pd
import datetime as dt
import gatherer.nyt_gatherer as nyt_gatherer
import gatherer.config as config
import gatherer.melk_format as melk_format


def gatherer(keyword, start_date, end_date, api_key, download_limit):
    """
    Main interface.

    Assembles dataset of relevant items, then saves as a csv file.

    Returns csv file.
    """

    # start_date, end_date = validate_dates(start_date, end_date)

    if not api_key:
        download_limit = config.NYT_DEFAULT_LIMIT
        api_key = config.NYT_API_KEY

    nyt = nyt_gatherer.search_nyt(
        keyword, start_date, end_date, api_key, download_limit
    )

    filename_out = (
        str(keyword)
        + "_"
        + str(start_date.isoformat)
        + "_"
        + str(end_date.isoformat)
        + ".csv"
    )

    return nyt
    return nyt.to_csv(filename_out)


""" def validate_dates(start_date, end_date):

    if not (
        (isinstance(start_date, dt.date) or isinstance(start_date, dt.datetime))
        and (isinstance(end_date, dt.date) or isinstance(end_date, dt.datetime))
    ):
        raise ValueError

    if end_date > start_date:
        raise ValueError("Error: Start date must be before end date.")

    return start_date, end_date """
