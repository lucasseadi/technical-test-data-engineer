"""Module for storing data retrieved from API"""

import logging
import os
from typing import Any, Dict, List, Optional
from tinydb import TinyDB

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def update_storage(key: str, data: Optional[List[Dict[str, Any]]]) -> None:
    """Function for updating database object"""
    try:
        data_dir = "../../data/"
        os.makedirs(data_dir, exist_ok=True)

        db_path = os.path.join(data_dir, f"{key}_mongodb.json")
        db = TinyDB(db_path)

        if key is None:
            logging.warning("No key provided.")
            return

        if data is None:
            logging.warning("No data provided for key: %s", key)
            return

        if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
            logging.error("Invalid data format for key: %s. Expected a list of dictionaries.", key)
            return

        db.truncate()

        for row in data:
            db.insert(row)

        logging.info("%s_mongodb.json updated.", key)

    except FileNotFoundError as e:
        logging.error("Database file not found: %s.", e)
    except PermissionError as e:
        logging.error("Permission denied when accessing the file: %s.", e)
    finally:
        if 'db' in locals():
            db.close()
