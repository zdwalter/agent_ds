---
name: data_cleaning
description: Basic data cleaning operations for CSV files using pandas.
allowed-tools:
  - drop_missing_values
  - fill_missing
  - remove_duplicates
  - normalize_column
---

# Data Cleaning Skill

This skill provides tools for cleaning tabular data (CSV files). It uses pandas for data manipulation.

## Dependencies

- pandas (already installed via project requirements)

## Tools

### drop_missing_values
Drop rows with missing values from a CSV file.

- `file_path`: Path to the input CSV file.
- `output_path`: Path to save the cleaned CSV (optional, default: same as input with '_cleaned' suffix).
- `axis`: Drop rows (0) or columns (1). Default is 0 (rows).
- `how`: 'any' or 'all'. Default 'any'.

Returns success message with path to saved file.

### fill_missing
Fill missing values in a CSV file.

- `file_path`: Path to the input CSV file.
- `output_path`: Path to save the filled CSV (optional).
- `method`: 'mean', 'median', 'mode', or a constant value. Default 'mean'.
- `columns`: List of column names to fill (optional, fill all columns if not specified).

Returns success message.

### remove_duplicates
Remove duplicate rows from a CSV file.

- `file_path`: Path to the input CSV file.
- `output_path`: Path to save the deduplicated CSV (optional).
- `subset`: List of column names to consider for duplicates (optional, all columns).
- `keep`: 'first', 'last', or False (drop all duplicates). Default 'first'.

Returns success message.

### normalize_column
Normalize a numeric column using min‑max scaling or standardization.

- `file_path`: Path to the input CSV file.
- `column`: Name of the column to normalize.
- `output_path`: Path to save the normalized CSV (optional).
- `method`: 'minmax' (scale to [0,1]) or 'standard' (z‑score). Default 'minmax'.

Returns success message.
