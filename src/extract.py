
import requests
import logging


# Configure logging to get status messages on production
logging.basicConfig(level=logging.INFO)


def fetch_series_for_date(target_date: str) -> list:

    """
    Retrieves the series from TVMaze API for a specific date

    Params:
        target_date (str): Date in 'YYYY-MM-DD' format

    Return:
        list: List of series (JSON)
    """

    url = f"http://api.tvmaze.com/schedule/web?date={target_date}"
    logging.info(f" Getting Data for: {target_date}")
    response = requests.get(url)
    response.raise_for_status()

    return response.json()