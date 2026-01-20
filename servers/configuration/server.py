import configparser
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("configuration", log_level="ERROR")


def _detect_format(file_path: str) -> str:
    """Detect config format from file extension."""
    ext = Path(file_path).suffix.lower()
    if ext == ".env":
        return "env"
    elif ext == ".ini" or ext == ".cfg":
        return "ini"
    elif ext == ".json":
        return "json"
    elif ext in (".yaml", ".yml"):
        return "yaml"
    else:
        # Default to ini for unknown
        return "ini"


@mcp.tool()
def read_config(file_path: str, format: str = "auto") -> str:
    """
    Read a configuration file and return its contents as a dictionary.

    Args:
        file_path: Path to the configuration file.
        format: Format of the file ('env', 'ini', 'json', 'yaml', 'auto').
                Default 'auto' detects from file extension.

    Returns:
        Configuration dictionary as a string, or error message.
    """
    try:
        if format == "auto":
            format = _detect_format(file_path)

        if format == "env":
            from dotenv import dotenv_values

            config = dotenv_values(file_path)
            return f"Read {len(config)} environment variables from {file_path}:\n{json.dumps(config, indent=2)}"

        elif format == "ini":
            parser = configparser.ConfigParser()
            parser.read(file_path)
            config = {
                section: dict(parser.items(section)) for section in parser.sections()
            }
            return f"Read INI file {file_path}:\n{json.dumps(config, indent=2)}"

        elif format == "json":
            with open(file_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            return f"Read JSON file {file_path}:\n{json.dumps(config, indent=2)}"

        elif format == "yaml":
            import yaml

            with open(file_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return f"Read YAML file {file_path}:\n{json.dumps(config, indent=2)}"

        else:
            return f"Unsupported format: {format}"
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error reading config file: {str(e)}"


@mcp.tool()
def write_config(file_path: str, data: Dict[str, Any], format: str = "auto") -> str:
    """
    Write a dictionary to a configuration file.

    Args:
        file_path: Path to the configuration file.
        data: Dictionary to write.
        format: Format of the file ('env', 'ini', 'json', 'yaml', 'auto').

    Returns:
        Success or error message.
    """
    try:
        if format == "auto":
            format = _detect_format(file_path)

        if format == "env":
            lines = [f"{key}={value}" for key, value in data.items()]
            content = "\n".join(lines)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote {len(data)} variables to {file_path}"

        elif format == "ini":
            parser = configparser.ConfigParser()
            # Assume data is a dict of sections
            for section, options in data.items():
                parser[section] = options
            with open(file_path, "w", encoding="utf-8") as f:
                parser.write(f)
            return f"Successfully wrote INI file {file_path}"

        elif format == "json":
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return f"Successfully wrote JSON file {file_path}"

        elif format == "yaml":
            import yaml

            with open(file_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False)
            return f"Successfully wrote YAML file {file_path}"

        else:
            return f"Unsupported format: {format}"
    except Exception as e:
        return f"Error writing config file: {str(e)}"


@mcp.tool()
def get_env_var(key: str, default: Optional[str] = None) -> str:
    """
    Get an environment variable.

    Args:
        key: Environment variable name.
        default: Optional default value if variable is not set.

    Returns:
        Value of the environment variable, or default if not set.
    """
    value = os.getenv(key, default)
    if value is None:
        return f"Environment variable '{key}' is not set and no default provided."
    return f"{key}={value}"


@mcp.tool()
def set_env_var(key: str, value: str) -> str:
    """
    Set an environment variable for the current process.

    Args:
        key: Environment variable name.
        value: Value to set.

    Returns:
        Confirmation message.
    """
    os.environ[key] = value
    return f"Set environment variable '{key}' to '{value}' (current process only)."
