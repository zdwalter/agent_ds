import json
import re
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("notes", log_level="ERROR")

# Directory for storing notes
NOTES_DIR = Path.cwd() / "artifacts" / "notes"


def _ensure_notes_dir() -> Path:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    return NOTES_DIR


def _title_to_filename(title: str) -> str:
    """Convert a note title to a safe filename."""
    # Lowercase, replace spaces with underscores, remove unsafe characters
    safe = re.sub(r"[^\w\s-]", "", title.strip().lower())
    safe = re.sub(r"[-\s]+", "_", safe)
    if not safe:
        safe = "untitled"
    return f"{safe}.md"


@mcp.tool()
def create_note(title: str, content: str) -> str:
    """
    Create a new note.

    Args:
        title: The title of the note (will be used as the filename).
        content: The text content of the note.

    Returns:
        Success message or error.
    """
    try:
        _ensure_notes_dir()
        filename = _title_to_filename(title)
        filepath = NOTES_DIR / filename

        if filepath.exists():
            return f"Error: A note with title '{title}' already exists."

        filepath.write_text(content, encoding="utf-8")
        return f"Note '{title}' created successfully (saved as {filename})."
    except Exception as e:
        return f"Error creating note: {str(e)}"


@mcp.tool()
def read_note(title: str) -> str:
    """
    Read the content of an existing note.

    Args:
        title: The title of the note to read.

    Returns:
        The note's content as plain text, or an error message.
    """
    try:
        _ensure_notes_dir()
        filename = _title_to_filename(title)
        filepath = NOTES_DIR / filename

        if not filepath.exists():
            return f"Error: Note '{title}' not found."

        return filepath.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading note: {str(e)}"


@mcp.tool()
def update_note(title: str, new_content: str) -> str:
    """
    Update the content of an existing note.

    Args:
        title: The title of the note to update.
        new_content: The new text content that will replace the previous content.

    Returns:
        Success message or error.
    """
    try:
        _ensure_notes_dir()
        filename = _title_to_filename(title)
        filepath = NOTES_DIR / filename

        if not filepath.exists():
            return f"Error: Note '{title}' not found."

        filepath.write_text(new_content, encoding="utf-8")
        return f"Note '{title}' updated successfully."
    except Exception as e:
        return f"Error updating note: {str(e)}"


@mcp.tool()
def delete_note(title: str) -> str:
    """
    Delete a note.

    Args:
        title: The title of the note to delete.

    Returns:
        A success message if the note existed and was deleted, or an error if the note was not found.
    """
    try:
        _ensure_notes_dir()
        filename = _title_to_filename(title)
        filepath = NOTES_DIR / filename

        if not filepath.exists():
            return f"Error: Note '{title}' not found."

        filepath.unlink()
        return f"Note '{title}' deleted successfully."
    except Exception as e:
        return f"Error deleting note: {str(e)}"


@mcp.tool()
def list_notes() -> str:
    """
    List all notes currently stored.

    Returns:
        A bullet‑list of note titles (filenames).
    """
    try:
        _ensure_notes_dir()
        notes = list(NOTES_DIR.glob("*.md"))
        if not notes:
            return "No notes found."

        result = "### Notes\n"
        for note in sorted(notes):
            # Display filename without .md extension
            name = note.stem
            # Replace underscores with spaces for readability
            readable = name.replace("_", " ")
            result += f"- {readable}\n"
        return result
    except Exception as e:
        return f"Error listing notes: {str(e)}"


if __name__ == "__main__":
    mcp.run()
