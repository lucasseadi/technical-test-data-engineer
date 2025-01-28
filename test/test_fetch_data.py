import httpx
import pytest
from unittest.mock import patch
from src.moovitamix_dailyfeed.fetch_data import fetch_data, fetch_paginated_data

"""fetch_data tests"""

@pytest.mark.asyncio
@pytest.mark.usefixtures("caplog")
@pytest.mark.parametrize("method, expected_output", [
    ("non_existent_method", "HTTP error occurred while fetching"),
    (None, "No method provided"),
])
async def test_fetch_data_no_method(method, expected_output, caplog):
    data = await fetch_data(method)
    print(f"Captured log: {caplog.text}")  # Print captured logs for debugging
    assert expected_output in caplog.text

@pytest.mark.asyncio
async def test_fetch_data_http_status_error():
    with patch("src.moovitamix_dailyfeed.fetch_data.httpx.AsyncClient.get",
               side_effect=httpx.HTTPStatusError("Mocked error", request=None, response=httpx.Response(500))):
        data = await fetch_data("tracks")
        assert data is None

@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["tracks", "users", "listen_history"])
async def test_fetch_data_success(method):
    data = await fetch_data(method)
    assert data is None or isinstance(data, list), f"Expected None or list, got {type(data)}"
    if data is not None:
        assert all(isinstance(item, dict) for item in data), "All elements in the list should be dictionaries"

"""fetch_paginated_data tests"""

@pytest.mark.asyncio
@pytest.mark.usefixtures("caplog")
@pytest.mark.parametrize("method, expected_output", [
    ("non_existent_method", "HTTP error occurred while fetching"),
    (None, "No method provided"),
])
async def test_fetch_paginated_data_no_method(method, expected_output, caplog):
    data = await fetch_paginated_data(method)
    print(f"Captured log: {caplog.text}")  # Print captured logs for debugging
    assert expected_output in caplog.text

@pytest.mark.asyncio
async def test_fetch_paginated_data_http_status_error():
    with patch("src.moovitamix_dailyfeed.fetch_data.httpx.AsyncClient.get",
               side_effect=httpx.HTTPStatusError("Mocked error", request=None, response=httpx.Response(500))):
        data = await fetch_paginated_data("tracks")
        assert data is None


@pytest.mark.asyncio
@pytest.mark.parametrize("exception, expected_log", [
    (httpx.ConnectTimeout("Mocked connection timeout"), "Read timeout occurred"),
    (httpx.ReadTimeout("Mocked read timeout"), "Read timeout occurred"),
    (httpx.RequestError("Mocked request error"), "Request error"),
])
async def test_fetch_paginated_data_errors(caplog, exception, expected_log):
    with patch("src.moovitamix_dailyfeed.fetch_data.httpx.AsyncClient.get", side_effect=exception):
        data = await fetch_paginated_data("tracks")
        assert data is None
        assert expected_log in caplog.text

@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["tracks", "users", "listen_history"])
async def test_fetch_paginated_data_success(method):
    data = await fetch_paginated_data(method)
    assert data is None or isinstance(data, list), f"Expected None or list, got {type(data)}"

    if data is not None:
        assert all(isinstance(item, dict) for item in data), "All elements in the list should be dictionaries"
