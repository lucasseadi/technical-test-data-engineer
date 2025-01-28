import logging
from unittest.mock import MagicMock
from src.moovitamix_dailyfeed.main import graceful_shutdown


def test_graceful_shutdown(mocker):
    """Test graceful shutdown to ensure logs are flushed, closed, and sys.exit is called."""

    # mock sys.exit to prevent the test from actually exiting
    mock_exit = mocker.patch("sys.exit")

    # mock the logger and handlers directly
    mock_handler = MagicMock()
    mock_logger = mocker.patch("logging.getLogger", return_value=logging.getLogger())
    mock_logger.return_value.handlers = [mock_handler]

    graceful_shutdown()

    mock_handler.flush.assert_called_once()
    mock_handler.close.assert_called_once()
    mock_exit.assert_called_once()
