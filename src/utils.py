# File Created to develop functions that can be used for multiple projects

import json
import logging
from ydata_profiling import ProfileReport
import os
import pandas as pd


def save_json(data: list, filename: str, folder: str = "../json"):

    """
    Record a data list in JSON format.

    Parameters:
        data (list): Data to record as JSON
        filename (str): Name for the final file (for instance: 'january_2024.json')
        folder (str): Route of the folder to save the JSON file
    """

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), folder))
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logging.info(f"   File saved on: {filepath}")


def generate_profiling_report(df, filename: str, folder: str = "../profiling"):
    """
    Generates an HTML profiling report using ydata-profiling.

    Parameters:
        df (pd.DataFrame): DataFrame to analyze
        filename (str): Name of the HTML output file
        folder (str)a: Target folder to save the profiling report
    """
    try: # I Use try because in this step some issues could raise, for instance: creating the profiling

        # Build the path to the output folder
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), folder))
        os.makedirs(output_dir, exist_ok=True)

        # We create the profiling report
        profile = ProfileReport(df, title="Profiling Report", explorative=True)
        output_path = os.path.join(output_dir, filename)

        # Export the report to HTML
        profile.to_file(output_path)

        logging.info(f"Profiling report was saved at: {output_path}")

    except Exception as e:
        logging.error(f"Error generating profiling report: {e}")


def save_parquet(df: pd.DataFrame, filename: str, folder: str = "../data"):
    """
    Save a DataFrame as Parquet with snappy compression.
    Args:
        df (pd.DataFrame): DataFrame to save
        filename (str): Name of the output Parquet file (e.g. 'fact_episodes.parquet')
        folder (str): Destination folder
    """

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), folder))
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    df.to_parquet(filepath, compression='snappy', index=False)

    logging.info(f" Saved Parquet: {filepath}")


