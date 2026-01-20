"""Unit tests for web_scraping server."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

# Add servers to path
sys.path.insert(0, str(Path(__file__).parent.parent / "servers"))

from web_scraping.server import extract_links, find_elements, scrape_url


def test_scrape_url_without_selector():
    """Test scraping URL without selector."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body><p>Hello world</p></body></html>"
    with patch("web_scraping.server.requests.get", return_value=mock_response):
        result = scrape_url("https://example.com")
        assert "Page text" in result
        assert "Hello world" in result


def test_scrape_url_with_selector():
    """Test scraping URL with CSS selector."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '<html><body><div class="content">Text</div></body></html>'
    with patch("web_scraping.server.requests.get", return_value=mock_response):
        result = scrape_url("https://example.com", selector=".content")
        assert "Found 1 element(s)" in result
        assert "Text" in result


def test_extract_links():
    """Test extracting links from HTML."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = (
        '<html><a href="/about">About</a><a href="https://other.com">Other</a></html>'
    )
    with patch("web_scraping.server.requests.get", return_value=mock_response):
        result = extract_links("https://example.com")
        assert "Found 2 unique links" in result
        assert "/about" in result
        assert "https://other.com" in result


def test_find_elements():
    """Test finding elements in HTML string."""
    html = '<div class="item">One</div><div class="item">Two</div>'
    result = find_elements(html, ".item")
    assert "Found 2 element(s)" in result
    assert "One" in result
    assert "Two" in result


def test_scrape_url_error():
    """Test error handling when request fails."""
    with patch(
        "web_scraping.server.requests.get",
        side_effect=requests.exceptions.RequestException("Network error"),
    ):
        result = scrape_url("https://example.com")
        assert "Error fetching URL" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
