import os
import sys

import yaml
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("yaml_skill", log_level="ERROR")


@mcp.tool()
def read_yaml(file_path: str) -> str:
    """
    Read a YAML file and return its parsed contents as a Python dictionary.

    Args:
        file_path: Absolute path to the YAML file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        # Convert to string representation for return
        import json

        return json.dumps(data, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except yaml.YAMLError as e:
        return f"Error parsing YAML: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


@mcp.tool()
def write_yaml(data: str, file_path: str) -> str:
    """
    Write a Python dictionary to a YAML file.

    Args:
        data: The dictionary to serialize, provided as a JSON string.
        file_path: Absolute path where the YAML file will be written.
    """
    try:
        import json

        dict_data = json.loads(data)
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(dict_data, f, default_flow_style=False, allow_unicode=True)
        return f"Successfully wrote YAML to {file_path}"
    except json.JSONDecodeError:
        return f"Error: Invalid JSON data provided."
    except Exception as e:
        return f"Error writing YAML: {e}"


@mcp.tool()
def validate_yaml(yaml_string: str) -> str:
    """
    Validate a YAML string for correctness.

    Args:
        yaml_string: The YAML string to validate.
    """
    try:
        yaml.safe_load(yaml_string)
        return "YAML is valid."
    except yaml.YAMLError as e:
        return f"Invalid YAML: {e}"


if __name__ == "__main__":
    mcp.run()
