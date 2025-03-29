from flask import abort
from types import SimpleNamespace
import pandas as pd
import logging



from extract import fetch_series_for_date_range
from utils import save_json, generate_profiling_report

# Configure logging to get status messages on production
logging.basicConfig(level=logging.INFO)


def start(request: SimpleNamespace):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '60'
        }
        return '', 204, headers

    elif request.method == 'POST':
        logging.info("  Starting extraction process from API...")


        # Extraction Process
        raw_series_data = fetch_series_for_date_range(
            '2024-01-01',
            '2024-01-31'
        )

        # Saving Raw data in json folder
        save_json(raw_series_data, 'january_2024.json')

        #TODO: Unnest Necessary data
        #TODO: Convert to DataFrame
        #TODO: Split DataFrame in Fact and dimention tables without processing the columns
        #TODO: Do profiling to each data frame, then process

        # Converting JSON file to DataFrame

        raw_series_data_df = pd.DataFrame(raw_series_data)

        # Generate the profiling report to analyse in general the data status

        generate_profiling_report(
            raw_series_data_df,
            "tvmaze_january_2024_profile.html"
        )

        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': '*'
        }

        return 'Success Extraction.', 200, headers

    else:
        return abort(405)


if __name__ == '__main__':
    start(SimpleNamespace(method='POST'))