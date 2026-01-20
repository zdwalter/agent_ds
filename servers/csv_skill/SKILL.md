---
name: csv_skill
description: CSV file reading and writing capabilities.
allowed-tools:
  - read_csv
  - write_csv
  - list_csv_columns
---

# CSV Skill

This skill enables the agent to read and write CSV files, as well as inspect their structure.

## Tools

### read_csv
Read a CSV file and return its contents as a list of dictionaries (each row as a dict with column names as keys).
- `file_path`: Absolute path to the CSV file.
- `delimiter`: Optional delimiter character (default ',').
- `has_header`: Boolean indicating whether the CSV has a header row (default True).

### write_csv
Write data to a CSV file.
- `file_path`: Absolute path to the CSV file to create.
- `data`: List of dictionaries representing rows.
- `delimiter`: Optional delimiter character (default ',').
- `write_header`: Boolean indicating whether to write a header row (default True).

### list_csv_columns
List column names of a CSV file.
- `file_path`: Absolute path to the CSV file.
- `delimiter`: Optional delimiter character (default ',').
