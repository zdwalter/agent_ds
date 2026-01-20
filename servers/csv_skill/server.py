import csv
import os
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("csv_skill", log_level="ERROR")


@mcp.tool()
def read_csv(file_path: str, delimiter: str = ",", has_header: bool = True) -> str:
    """
    Read a CSV file and return its contents as a list of dictionaries.

    Args:
        file_path: Absolute path to the CSV file.
        delimiter: Optional delimiter character (default ',').
        has_header: Boolean indicating whether the CSV has a header row (default True).
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."

    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            rows = list(reader)

        if has_header and rows:
            headers = rows[0]
            data = rows[1:]
            result = []
            for row in data:
                # Ensure row length matches headers length
                padded_row = (
                    row + [None] * (len(headers) - len(row))
                    if len(row) < len(headers)
                    else row[: len(headers)]
                )
                result.append(dict(zip(headers, list(padded_row))))  # type: ignore
            return f"Successfully read CSV with {len(result)} rows. First few rows:\n{result[:5]}"
        else:
            # No header, return as list of lists
            return f"Successfully read CSV with {len(rows)} rows (no header). First few rows:\n{rows[:5]}"
    except Exception as e:
        return f"Error reading CSV: {str(e)}"


@mcp.tool()
def write_csv(
    file_path: str,
    data: List[Dict[str, Any]],
    delimiter: str = ",",
    write_header: bool = True,
) -> str:
    """
    Write data to a CSV file.

    Args:
        file_path: Absolute path to the CSV file to create.
        data: List of dictionaries representing rows.
        delimiter: Optional delimiter character (default ',').
        write_header: Boolean indicating whether to write a header row (default True).
    """
    if not data:
        return "Error: No data provided."

    try:
        # Determine column names from first dictionary keys
        fieldnames = list(data[0].keys())

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
            if write_header:
                writer.writeheader()
            writer.writerows(data)

        return f"Successfully wrote {len(data)} rows to '{file_path}'."
    except Exception as e:
        return f"Error writing CSV: {str(e)}"


@mcp.tool()
def list_csv_columns(file_path: str, delimiter: str = ",") -> str:
    """
    List column names of a CSV file.

    Args:
        file_path: Absolute path to the CSV file.
        delimiter: Optional delimiter character (default ',').
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."

    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            first_row = next(reader, None)
            if first_row is None:
                return "CSV file is empty."
            return f"Columns: {', '.join(first_row)}"
    except Exception as e:
        return f"Error reading CSV columns: {str(e)}"


if __name__ == "__main__":
    mcp.run()
