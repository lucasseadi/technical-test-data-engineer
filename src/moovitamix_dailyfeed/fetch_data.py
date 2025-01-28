"""Module for fetching data from Moovitamix API"""

import logging
from typing import Any, Dict, List, Optional
import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

BASE_URL: str = "http://127.0.0.1:8000"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10),
       retry=retry_if_exception_type(httpx.RequestError), reraise=True)

async def fetch_paginated_data(method: str) -> Optional[List[Dict[str, Any]]]:
    """Function fetching paginated data"""
    if method is None:
        logging.warning("No method provided.")
        return

    all_data = []
    page = 1
    page_size = 500

    async with httpx.AsyncClient() as client:
        try:
            while True:
                response: httpx.Response = await client.get(f"{BASE_URL}/{method}",
                                                            params={"page": page,
                                                                    "size": page_size},
                                                            timeout=10.0)
                response.raise_for_status()

                try:
                    data: List[Dict[str, Any]] = response.json()
                except ValueError:
                    logging.error("Invalid JSON response received from %s.", method)
                    return None

                if 'items' not in data:
                    logging.error("Unexpected response structure from %s: %s.", method, data)
                    return None

                if not data['items']:
                    break

                all_data.extend(data['items'])
                page += 1

            logging.debug("Data fetched from %s: %s", method, all_data)
            return all_data
        except httpx.HTTPStatusError as e:
            logging.error("HTTP error occurred while fetching %s: %s- %s",
                          method, e.response.status_code, e.response.text)
        except httpx.ConnectTimeout:
            logging.error("Read timeout occurred while fetching %s.", method)
        except httpx.ReadTimeout:
            logging.error("Read timeout occurred while fetching %s.", method)
        except httpx.RequestError as e:
            logging.error("Request error: %s", e)
        return None

async def fetch_data(method: str) -> Optional[List[Dict[str, Any]]]:
    """Function fetching data"""
    if method is None:
        logging.warning("No method provided.")
        return

    data: Optional[List[Dict[str, Any]]] = await fetch_paginated_data(method)

    if data is not None and isinstance(data, list):
        logging.info("Fetched %s items (%s).", len(data), method)
    else:
        logging.info("Failed to fetch data from %s. Received empty or invalid response.",
                     method)
        return None

    return data
