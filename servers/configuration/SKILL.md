---
name: configuration
description: Configuration file reading/writing and environment variable management.
allowed-tools:
  - read_config
  - write_config
  - get_env_var
  - set_env_var
---

# Configuration Skill

This skill enables the agent to read and write configuration files in various formats (env, ini, json, yaml) and manage environment variables.

## Tools

### read_config
Read a configuration file and return its contents as a dictionary.

Args:
- `file_path`: Path to the configuration file.
- `format`: Format of the file ('env', 'ini', 'json', 'yaml', 'auto'). Default 'auto' detects from file extension.

Returns:
Configuration dictionary as a string, or error message.

### write_config
Write a dictionary to a configuration file.

Args:
- `file_path`: Path to the configuration file.
- `data`: Dictionary to write.
- `format`: Format of the file ('env', 'ini', 'json', 'yaml', 'auto').

Returns:
Success or error message.

### get_env_var
Get an environment variable.

Args:
- `key`: Environment variable name.
- `default`: Optional default value if variable is not set.

Returns:
Value of the environment variable, or default if not set.

### set_env_var
Set an environment variable for the current process.

Args:
- `key`: Environment variable name.
- `value`: Value to set.

Returns:
Confirmation message.

## Supported Formats
- **env**: Key‑value pairs (`.env` files, read via `dotenv`).
- **ini**: INI‑style sections (`.ini`, `.cfg`).
- **json**: JSON objects (`.json`).
- **yaml**: YAML documents (`.yaml`, `.yml`).

## Dependencies
- python‑dotenv (already installed)
- PyYAML (already installed)
- configparser (standard library)
- json (standard library)
