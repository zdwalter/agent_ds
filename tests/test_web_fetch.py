"""Unit tests for web_fetch server."""

import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add servers to path
sys.path.insert(0, str(Path(__file__).parent.parent / "servers"))

from web_fetch.server import read_url_jina, search_web_jina


@pytest.mark.xfail(reason="Mocking Jina API not yet implemented")
def test_read_url_jina():
    """Test reading URL via Jina (mocked)."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Article content"
    with patch("web_fetch.server.requests.get", return_value=mock_response):
        result = read_url_jina("https://example.com")
        assert "Article content" in result


@pytest.mark.xfail(reason="Mocking Jina API not yet implemented")
def test_search_web_jina():
    """Test web search via Jina (mocked)."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {"title": "Result 1", "snippet": "Snippet 1", "url": "http://example.com/1"}
        ]
    }
    with patch("web_fetch.server.requests.post", return_value=mock_response):
        result = search_web_jina("test query", limit=5)
        assert "Result 1" in result
        assert "Snippet 1" in result
