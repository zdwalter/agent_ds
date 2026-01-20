from typing import List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("web_scraping", log_level="ERROR")


@mcp.tool()
def scrape_url(url: str, selector: Optional[str] = None) -> str:
    """
    Fetch HTML from a URL and extract text. If a CSS selector is provided,
    extract only the elements matching the selector.

    Args:
        url: The URL to scrape.
        selector: Optional CSS selector to filter elements.

    Returns:
        Extracted text or error message.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        if selector:
            elements = soup.select(selector)
            texts = [elem.get_text(strip=True) for elem in elements]
            result = "\n".join(texts)
            return f"Found {len(elements)} element(s). Extracted text:\n{result}"
        else:
            # Extract all text
            text = soup.get_text(strip=True)
            return f"Page text (first 5000 chars):\n{text[:5000]}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {str(e)}"
    except Exception as e:
        return f"Error parsing HTML: {str(e)}"


@mcp.tool()
def extract_links(url: str, base_url: Optional[str] = None) -> str:
    """
    Extract all hyperlinks from a webpage.

    Args:
        url: The URL to scrape.
        base_url: Optional base URL to resolve relative links.
                  If not provided, the original URL is used.

    Returns:
        List of links as a formatted string.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            # Resolve relative URLs
            if base_url:
                resolved = urljoin(base_url, href)
            else:
                resolved = urljoin(url, href)
            links.append(resolved)

        unique_links = list(set(links))
        return f"Found {len(unique_links)} unique links:\n" + "\n".join(
            unique_links[:50]
        )
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {str(e)}"
    except Exception as e:
        return f"Error extracting links: {str(e)}"


@mcp.tool()
def find_elements(html: str, selector: str) -> str:
    """
    Find elements matching a CSS selector within HTML content.

    Args:
        html: HTML string to parse.
        selector: CSS selector.

    Returns:
        Extracted text from matched elements.
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.select(selector)
        texts = [elem.get_text(strip=True) for elem in elements]
        if not texts:
            return "No elements found."
        return f"Found {len(elements)} element(s). Texts:\n" + "\n".join(texts)
    except Exception as e:
        return f"Error parsing HTML: {str(e)}"
