---
name: web_scraping
description: Web scraping capabilities using BeautifulSoup and requests.
allowed-tools:
  - scrape_url
  - extract_links
  - find_elements
---

# Web Scraping Skill

This skill enables the agent to scrape web pages, extract text, links, and filter elements with CSS selectors.

## Tools

### scrape_url
Fetch HTML from a URL and extract text. If a CSS selector is provided, extract only the elements matching the selector.

Args:
- `url`: The URL to scrape.
- `selector`: Optional CSS selector to filter elements.

Returns:
Extracted text or error message.

### extract_links
Extract all hyperlinks from a webpage.

Args:
- `url`: The URL to scrape.
- `base_url`: Optional base URL to resolve relative links. If not provided, the original URL is used.

Returns:
List of links as a formatted string.

### find_elements
Find elements matching a CSS selector within HTML content.

Args:
- `html`: HTML string to parse.
- `selector`: CSS selector.

Returns:
Extracted text from matched elements.

## Dependencies
- requests (already installed)
- beautifulsoup4 (added to requirements.txt)
