"""Daily feed main module"""

import asyncio
import logging
import os
import signal
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Dict, List, Optional
import schedule
from src.moovitamix_dailyfeed.fetch_data import fetch_data
from src.moovitamix_dailyfeed.storage import update_storage

def graceful_shutdown() -> None:
    """Function to flush logs when application is interrupted"""
    logging.info("Application interrupted. Flushing logs and shutting down.")
    for handler in logging.getLogger().handlers:
        handler.flush()
        handler.close()
    logging.shutdown()
    sys.exit(0)

def log_config() -> None:
    """Function to config logs"""
    try:
        log_dir = "../../logs/"
        os.makedirs(log_dir, exist_ok=True)

        log_filename = datetime.now().strftime(f"{log_dir}moovitamix_%Y-%m-%d.log")

        log_handler = TimedRotatingFileHandler(
            filename=log_filename,
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8",
            delay=False
        )
        log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        #if not logger.hasHandlers():
        if not any(isinstance(h, TimedRotatingFileHandler) for h in logger.handlers):
            logger.addHandler(log_handler)
            logging.info("Logging configuration successfully set up.")
            log_handler.flush()

        signal.signal(signal.SIGINT, graceful_shutdown)
        signal.signal(signal.SIGTERM, graceful_shutdown)

    except PermissionError as e:
        print(f"Permission error: Unable to write to log directory {log_dir}: {e}")
    except OSError as e:
        print(f"OS error: Failed to create log directory {log_dir}: {e}")

def main() -> None:
    """Data feed main function"""
    log_config()
    logging.info("Starting data ingestion...")

    try:
        tracks: Optional[List[Dict[str, Any]]] = asyncio.run(fetch_data("tracks"))
        users: Optional[List[Dict[str, Any]]] = asyncio.run(fetch_data("users"))
        listen_history: Optional[List[Dict[str, Any]]] = asyncio.run(
            fetch_data("listen_history"))
    except (asyncio.TimeoutError) as e:
        logging.error("Timeout occurred while fetching data: %s", e)
        return
    except (ValueError, TypeError) as e:
        logging.error("Invalid data received: %s", e)
        return
    except ConnectionError as e:
        logging.error("Network connection issue while fetching data: %s", e)
        return
    except RuntimeError as e:
        logging.error("Runtime error during asyncio operation: %s", e)
        return
    if tracks is not None:
        update_storage("tracks", tracks)
    else:
        logging.warning("Tracks data is empty or could not be retrieved.")

    if users is not None:
        update_storage("users", users)
    else:
        logging.warning("Users data is empty or could not be retrieved.")

    if listen_history is not None:
        update_storage("listen_history", listen_history)
    else:
        logging.warning("Listen history data is empty or could not be retrieved.")

    logging.info("Data ingestion ended successfully.")


if __name__ == "__main__":
    #schedule.every().day.at("4:00").do(main)   # daily
    schedule.every(5).seconds.do(main)

    logging.info("Scheduler started...")
    while True:
        schedule.run_pending()
