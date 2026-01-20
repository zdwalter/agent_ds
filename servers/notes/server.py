import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

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


def _parse_note(filepath: Path) -> Tuple[Dict[str, Any], str]:
    """Parse a note file into metadata dict and content string."""
    text = filepath.read_text(encoding="utf-8")
    # 解析 frontmatter
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            content = parts[2]
            if HAS_YAML:
                metadata = yaml.safe_load(frontmatter) or {}
            else:
                # 简单解析：键值对
                metadata = {}
                for line in frontmatter.splitlines():
                    if ":" in line:
                        key, val = line.split(":", 1)
                        key = key.strip()
                        val = val.strip()
                        # 尝试转换列表
                        if val.startswith("[") and val.endswith("]"):
                            # 简单列表解析
                            items = val[1:-1].split(",")
                            val = [item.strip().strip("\"'") for item in items]  # type: ignore
                        metadata[key] = val
            return metadata, content.strip()
    # 无 frontmatter
    return {}, text.strip()


def _serialize_note(metadata: Dict[str, Any], content: str) -> str:
    """Serialize metadata and content into a note file string."""
    if not metadata:
        return content
    if HAS_YAML:
        frontmatter = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)
    else:
        # 简单 YAML 生成
        lines = []
        for key, val in metadata.items():
            if isinstance(val, list):
                val_str = "[" + ", ".join(f'"{v}"' for v in val) + "]"
            elif isinstance(val, str):
                val_str = f'"{val}"'
            else:
                val_str = str(val)
            lines.append(f"{key}: {val_str}")
        frontmatter = "\n".join(lines)
    return f"---\n{frontmatter}---\n{content}"


def _get_default_metadata(title: str) -> Dict[str, Any]:
    """Generate default metadata for a new note."""
    now = datetime.now().isoformat()
    return {"title": title, "created": now, "modified": now, "tags": [], "author": ""}


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

        metadata = _get_default_metadata(title)
        note_text = _serialize_note(metadata, content)
        filepath.write_text(note_text, encoding="utf-8")
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
        The note's content as plain text (without frontmatter), or an error message.
    """
    try:
        _ensure_notes_dir()
        filename = _title_to_filename(title)
        filepath = NOTES_DIR / filename

        if not filepath.exists():
            return f"Error: Note '{title}' not found."

        _, content = _parse_note(filepath)
        return content
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

        metadata, _ = _parse_note(filepath)
        if not metadata:
            metadata = _get_default_metadata(title)
        else:
            metadata["modified"] = datetime.now().isoformat()
        note_text = _serialize_note(metadata, new_content)
        filepath.write_text(note_text, encoding="utf-8")
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


@mcp.tool()
def add_tag_to_note(title: str, tag: str) -> str:
    """
    Add a tag to an existing note.

    Args:
        title: The title of the note.
        tag: The tag to add.

    Returns:
        Success message or error.
    """
    try:
        _ensure_notes_dir()
        filename = _title_to_filename(title)
        filepath = NOTES_DIR / filename
        if not filepath.exists():
            return f"Error: Note '{title}' not found."

        metadata, content = _parse_note(filepath)
        if not metadata:
            metadata = _get_default_metadata(title)
        tags = metadata.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        if tag not in tags:
            tags.append(tag)
            metadata["tags"] = tags
            metadata["modified"] = datetime.now().isoformat()
            note_text = _serialize_note(metadata, content)
            filepath.write_text(note_text, encoding="utf-8")
            return f"Tag '{tag}' added to note '{title}'."
        else:
            return f"Tag '{tag}' already exists on note '{title}'."
    except Exception as e:
        return f"Error adding tag: {str(e)}"


@mcp.tool()
def remove_tag_from_note(title: str, tag: str) -> str:
    """
    Remove a tag from an existing note.

    Args:
        title: The title of the note.
        tag: The tag to remove.

    Returns:
        Success message or error.
    """
    try:
        _ensure_notes_dir()
        filename = _title_to_filename(title)
        filepath = NOTES_DIR / filename
        if not filepath.exists():
            return f"Error: Note '{title}' not found."

        metadata, content = _parse_note(filepath)
        if not metadata:
            metadata = _get_default_metadata(title)
        tags = metadata.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        if tag in tags:
            tags.remove(tag)
            metadata["tags"] = tags
            metadata["modified"] = datetime.now().isoformat()
            note_text = _serialize_note(metadata, content)
            filepath.write_text(note_text, encoding="utf-8")
            return f"Tag '{tag}' removed from note '{title}'."
        else:
            return f"Tag '{tag}' not found on note '{title}'."
    except Exception as e:
        return f"Error removing tag: {str(e)}"


@mcp.tool()
def list_tags() -> str:
    """
    List all unique tags across all notes.

    Returns:
        A bullet‑list of tags and the notes they appear on.
    """
    try:
        _ensure_notes_dir()
        notes = list(NOTES_DIR.glob("*.md"))
        tag_map: Dict[str, List[str]] = {}
        for note in notes:
            metadata, _ = _parse_note(note)
            tags = metadata.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]
            for tag in tags:
                tag_map.setdefault(tag, []).append(note.stem.replace("_", " "))
        if not tag_map:
            return "No tags found."
        result = "### Tags\n"
        for tag, note_titles in sorted(tag_map.items()):
            result += f"- **{tag}**: {', '.join(note_titles)}\n"
        return result
    except Exception as e:
        return f"Error listing tags: {str(e)}"


@mcp.tool()
def search_notes(query: str) -> str:
    """
    Search for notes by title, content, or tags.

    Args:
        query: The search string (case-insensitive).

    Returns:
        A list of matching notes with snippets.
    """
    try:
        _ensure_notes_dir()
        notes = list(NOTES_DIR.glob("*.md"))
        matches = []
        for note in notes:
            metadata, content = _parse_note(note)
            title = note.stem.replace("_", " ")
            tags = metadata.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]
            # Search in title, content, tags
            if (
                query.lower() in title.lower()
                or query.lower() in content.lower()
                or any(query.lower() in tag.lower() for tag in tags)
            ):
                matches.append(
                    (title, content[:100] + "..." if len(content) > 100 else content)
                )
        if not matches:
            return f"No notes found matching '{query}'."
        result = f"### Search results for '{query}'\n"
        for title, snippet in matches:
            result += f"- **{title}**: {snippet}\n"
        return result
    except Exception as e:
        return f"Error searching notes: {str(e)}"


@mcp.tool()
def get_note_metadata(title: str) -> str:
    """
    Get metadata of a note (creation time, modification time, tags, author).

    Args:
        title: The title of the note.

    Returns:
        Formatted metadata or error.
    """
    try:
        _ensure_notes_dir()
        filename = _title_to_filename(title)
        filepath = NOTES_DIR / filename
        if not filepath.exists():
            return f"Error: Note '{title}' not found."

        metadata, _ = _parse_note(filepath)
        if not metadata:
            return f"Note '{title}' has no metadata."
        result = f"### Metadata for '{title}'\n"
        for key, value in metadata.items():
            result += f"- **{key}**: {value}\n"
        return result
    except Exception as e:
        return f"Error retrieving metadata: {str(e)}"


if __name__ == "__main__":
    mcp.run()
