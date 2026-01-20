import json
import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("json_skill", log_level="ERROR")


@mcp.tool()
def read_json(file_path: str) -> str:
    """
    Read a JSON file and return its parsed content.

    Args:
        file_path: Absolute path to the JSON file.
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {str(e)}"
    except Exception as e:
        return f"Error reading JSON file: {str(e)}"


@mcp.tool()
def write_json(file_path: str, data: str, indent: int = 2) -> str:
    """
    Write data to a JSON file with optional pretty‑printing.

    Args:
        file_path: Absolute path to the JSON file to create.
        data: JSON‑serializable data (as a JSON string).
        indent: Number of spaces for indentation (default 2). Use None for compact output.
    """
    try:
        # Parse input data (could be a JSON string or already a Python object)
        # For simplicity, we expect a JSON string.
        parsed = json.loads(data)
    except json.JSONDecodeError:
        # If it's not a JSON string, maybe it's already a Python object (passed by MCP as dict/list).
        # Actually, MCP will pass the data as a Python object, not a string.
        # Let's handle both: if data is a string, try to parse; otherwise assume it's already serializable.
        if isinstance(data, str):
            try:
                parsed = json.loads(data)
            except json.JSONDecodeError:
                return f"Error: Invalid JSON string provided."
        else:
            parsed = data

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=indent, ensure_ascii=False)
        return f"Successfully wrote JSON to '{file_path}'."
    except Exception as e:
        return f"Error writing JSON file: {str(e)}"


@mcp.tool()
def validate_json(json_string: str) -> str:
    """
    Validate a JSON string and return its parsed value if valid.

    Args:
        json_string: The JSON string to validate.
    """
    try:
        parsed = json.loads(json_string)
        return f"Valid JSON. Parsed value:\n{json.dumps(parsed, indent=2, ensure_ascii=False)}"
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {str(e)}"


if __name__ == "__main__":
    mcp.run()
