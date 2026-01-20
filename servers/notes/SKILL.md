---
name: notes
description: Simple note‑taking capabilities.
allowed-tools:
  - create_note
  - read_note
  - update_note
  - delete_note
  - list_notes
---

# Notes Skill

This skill enables the agent to create, read, update, delete, and list plain‑text notes.

## Storage

All notes are saved as Markdown files in the `artifacts/notes` directory.
File names are derived from the note title (lower‑case, spaces replaced with underscores) with a `.md` extension.

## Tools

### create_note
Create a new note.

- `title`: The title of the note (will be used as the filename).
- `content`: The text content of the note.

If a note with the same title already exists, the tool will return an error.

### read_note
Read the content of an existing note.

- `title`: The title of the note to read.

Returns the note's content as plain text. If the note does not exist, returns an error.

### update_note
Update the content of an existing note.

- `title`: The title of the note to update.
- `new_content`: The new text content that will replace the previous content.

If the note does not exist, returns an error.

### delete_note
Delete a note.

- `title`: The title of the note to delete.

Returns a success message if the note existed and was deleted, or an error if the note was not found.

### list_notes
List all notes currently stored.

Returns a bullet‑list of note titles (filenames).
