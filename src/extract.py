
from datetime import datetime, timedelta
import requests
import logging

# Configure logging to get status messages on production
logging.basicConfig(level=logging.INFO)


def fetch_episodes_for_date_range(start_date_str: str, end_date_str: str) -> list:

    """
    Retrieves the series from TVMaze API for a specific date range and return ir as raw

    Parameters:
        start_date_str (str): Start date string (YYYY-MM-DD)
        end_date_str (str): End date string (YYYY-MM-DD)

    Return:
        list: List of raw series extracted (JSON)
    """

    # Params Validation
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError as e:
        logging.error(f"   Invalid data format: {e}")
        return []

    if start_date > end_date:
        logging.error("   Start_date should be lower than end_date")
        return []

    # Defining output list
    all_raw_data = []
    current_date = start_date

    # Getting data for each day in the range.
    while current_date <= end_date:

        date_str = current_date.isoformat()
        url = f"http://api.tvmaze.com/schedule/web?date={date_str}"
        logging.info(f"   Consulting API for: {date_str}...")

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            all_raw_data.extend(data)

        except requests.RequestException as e:
            logging.error(f"   Error retrieving data for {date_str}: {e}")

        current_date += timedelta(days=1)

    return all_raw_data

