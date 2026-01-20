import json
import re
from typing import List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("regex_skill", log_level="ERROR")


@mcp.tool()
def regex_match(pattern: str, text: str) -> str:
    """
    Find all non-overlapping matches of a pattern in a text.

    Args:
        pattern: The regular expression pattern.
        text: The input text to search.
    """
    try:
        matches = re.findall(pattern, text)
        return json.dumps(matches, ensure_ascii=False)
    except re.error as e:
        return f"Error in regular expression: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


@mcp.tool()
def regex_search(pattern: str, text: str) -> str:
    """
    Search for the first occurrence of a pattern in a text, returning match details.

    Args:
        pattern: The regular expression pattern.
        text: The input text to search.
    """
    try:
        match = re.search(pattern, text)
        if match:
            result = {
                "start": match.start(),
                "end": match.end(),
                "group": match.group(),
                "groups": match.groups(),
            }
            return json.dumps(result, ensure_ascii=False)
        else:
            return "No match found."
    except re.error as e:
        return f"Error in regular expression: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


@mcp.tool()
def regex_replace(pattern: str, replacement: str, text: str) -> str:
    """
    Replace all occurrences of a pattern in a text with a replacement string.

    Args:
        pattern: The regular expression pattern.
        replacement: The replacement string.
        text: The input text.
    """
    try:
        replaced = re.sub(pattern, replacement, text)
        return replaced
    except re.error as e:
        return f"Error in regular expression: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


@mcp.tool()
def regex_extract(pattern: str, text: str) -> str:
    """
    Extract captured groups from all matches of a pattern.

    Args:
        pattern: The regular expression pattern.
        text: The input text.
    """
    try:
        groups = re.findall(pattern, text)
        # If pattern contains groups, findall returns tuples
        # Flatten if needed
        flat: List[str] = []
        for g in groups:
            if isinstance(g, tuple):
                flat.extend(g)
            else:
                flat.append(g)
        return json.dumps(flat, ensure_ascii=False)
    except re.error as e:
        return f"Error in regular expression: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


if __name__ == "__main__":
    mcp.run()
