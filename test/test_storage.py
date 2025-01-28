import pytest
import logging
import os
from unittest.mock import patch, MagicMock
from src.moovitamix_dailyfeed.storage import update_storage
from typing import Any, Dict, List

@pytest.mark.usefixtures("caplog")
def test_update_storage_no_key(caplog):
    test_data: List[Dict[str, Any]] = [
        {'user_id': 56756, 'items': [57852, 53251, 26822, 79688, 39815], 'created_at': '2024-01-02T19:22:45',
         'updated_at': '2024-08-20T04:53:01'}
    ]
    update_storage(None, test_data)
    assert "No key provided." in caplog.text

@pytest.mark.usefixtures("caplog")
def test_update_storage_no_data(caplog):
    update_storage("test_key", None)
    assert "No data provided for key" in caplog.text

@pytest.mark.usefixtures("caplog")
def test_update_storage_file_not_found(caplog):
    test_key = "test_key"
    test_data: List[Dict[str, Any]] = [
        {'user_id': 56756, 'items': [57852, 53251, 26822, 79688, 39815], 'created_at': '2024-01-02T19:22:45',
         'updated_at': '2024-08-20T04:53:01'}
    ]
    with patch("src.moovitamix_dailyfeed.storage.TinyDB",
               side_effect=FileNotFoundError("Mocked file not found")):
        update_storage(test_key, test_data)
        assert "Database file not found" in caplog.text

@pytest.mark.usefixtures("caplog")
def test_update_storage_permission_error(caplog):
    test_key = "test_key"
    test_data: List[Dict[str, Any]] = [
        {'user_id': 56756, 'items': [57852, 53251, 26822, 79688, 39815], 'created_at': '2024-01-02T19:22:45',
         'updated_at': '2024-08-20T04:53:01'}
    ]
    with patch("src.moovitamix_dailyfeed.storage.TinyDB",
               side_effect=PermissionError("Mocked permission error")):
        update_storage(test_key, test_data)
        assert "Permission denied when accessing the file" in caplog.text

@pytest.mark.usefixtures("caplog")
def test_update_storage_success(caplog):
    test_key = "test_key"
    test_data: List[Dict[str, Any]] = [
        {'user_id': 56756, 'items': [57852, 53251, 26822, 79688, 39815], 'created_at': '2024-01-02T19:22:45',
         'updated_at': '2024-08-20T04:53:01'}
    ]

    with patch("src.moovitamix_dailyfeed.storage.os.makedirs") as mock_makedirs, \
        patch("src.moovitamix_dailyfeed.storage.TinyDB") as mock_tinydb:
        mock_db_instance = MagicMock()
        mock_tinydb.return_value = mock_db_instance

        caplog.set_level(logging.INFO)

        update_storage(test_key, test_data)

        mock_makedirs.assert_called_once_with("../../data/", exist_ok=True)
        mock_tinydb.assert_called_once_with(os.path.join("../../data/", f"{test_key}_mongodb.json"))
        mock_db_instance.truncate.assert_called_once()
        assert mock_db_instance.insert.call_count == len(test_data)
        print(f"Captured log: {caplog.text}")  # Print captured logs for debugging
        assert f"{test_key}_mongodb.json updated." in caplog.text
