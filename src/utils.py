# File Created to develop functions that can be used for multiple projects

import json
import logging
import os


def save_json(data: list, filename: str, folder: str = "../json"):

    """
    Record a data list in JSON format.

    Params:
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