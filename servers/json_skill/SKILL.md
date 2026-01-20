---
name: json_skill
description: JSON file reading and writing capabilities.
allowed-tools:
  - read_json
  - write_json
  - validate_json
---

# JSON Skill

This skill enables the agent to read and write JSON files, as well as validate JSON strings.

## Tools

### read_json
Read a JSON file and return its parsed content.
- `file_path`: Absolute path to the JSON file.

### write_json
Write data to a JSON file with optional pretty‑printing.
- `file_path`: Absolute path to the JSON file to create.
- `data`: JSON‑serializable data (dictionary, list, etc.).
- `indent`: Number of spaces for indentation (default 2). Use None for compact output.

### validate_json
Validate a JSON string and return its parsed value if valid.
- `json_string`: The JSON string to validate.
