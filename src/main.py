from types import SimpleNamespace
from flask import abort
import pandas as pd
import sqlite3
import logging

from process import (unnest_fields, split_dataframe, clean_fact_episodes,
                     clean_dim_shows, clean_dim_genres, clean_show_genres)
from extract import fetch_episodes_for_date_range
from utils import (save_json, generate_profiling_report, save_parquet,
                   save_dataframes_to_sqlite)
from queries import (query_avg_runtime_show, query_shows_by_genre,
                     query_unique_show_domains)

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
        raw_episodes_data = fetch_episodes_for_date_range(
            '2024-01-01',
            '2024-01-31'
        )

        # Saving Raw data in json folder
        save_json(raw_episodes_data, 'january_2024.json')

        # Unnesting the necessary fields
        episodes_data_unnested = map(unnest_fields, raw_episodes_data)
        episodes_data_unnested = pd.DataFrame(episodes_data_unnested)

        # Splitting data in different tables to construct the sql lite database structure
        # Also in the following step the DataFrames are created
        (
            fact_episodes_df, dim_shows_df,
            dim_genres_df, show_genres_df
        ) = split_dataframe(episodes_data_unnested)


        # Generate the profiling report to analyse the data status in each table
        generate_profiling_report(fact_episodes_df, "tvmaze_january_2024_fact_episodes_profile.html")
        generate_profiling_report(dim_shows_df, "tvmaze_january_2024_dim_shows_profile.html")
        generate_profiling_report(dim_genres_df, "tvmaze_january_2024_dim_genres_profile.html")
        generate_profiling_report(show_genres_df, "tvmaze_january_2024_show_genres_profile.html")

        # Cleaning the DataFrames
        fact_episodes_df = clean_fact_episodes(fact_episodes_df)
        dim_shows_df = clean_dim_shows(dim_shows_df)
        dim_genres_df = clean_dim_genres(dim_genres_df)
        show_genres_df = clean_show_genres(show_genres_df)

        # Creating parquet files
        save_parquet(fact_episodes_df, 'fact_episodes.parquet')
        save_parquet(dim_shows_df, 'dim_shows.parquet')
        save_parquet(dim_genres_df, 'dim_genres.parquet')
        save_parquet(show_genres_df, 'show_genres.parquet')

        # Creating DB and saving the parquet files into SQLite DB
        dataframes = {
            "fact_episodes": fact_episodes_df,
            "dim_shows": dim_shows_df,
            "dim_genres": dim_genres_df,
            "show_genres": show_genres_df,
        }

        save_dataframes_to_sqlite(dataframes, "../db/tvmaze.db")


        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': '*'
        }

        return 'Success Extraction.', 200, headers

    else:
        return abort(405)


if __name__ == '__main__':

    # Executing the start( ) function that contains the flow
    start(SimpleNamespace(method='POST'))

    # Running SQL Queries to the SQLite Data Base
    db_path = "../db/tvmaze.db"
    conn = sqlite3.connect(db_path)

    # Queries results:
    show_avg_runtime = pd.read_sql_query(query_avg_runtime_show, conn)
    shows_by_genre = pd.read_sql_query(query_shows_by_genre, conn)
    unique_show_domains = pd.read_sql_query(query_unique_show_domains, conn)
