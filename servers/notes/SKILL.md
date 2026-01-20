---
name: notes
description: Enhanced note‑taking capabilities with tags, metadata, and search.
allowed-tools:
  - create_note
  - read_note
  - update_note
  - delete_note
  - list_notes
  - add_tag_to_note
  - remove_tag_from_note
  - list_tags
  - search_notes
  - get_note_metadata
---

# Notes Skill

This skill enables the agent to create, read, update, delete, and list notes with metadata support (tags, creation/modification timestamps, author). Notes are stored as Markdown files with YAML frontmatter for metadata.

## Storage

All notes are saved as Markdown files in the `artifacts/notes` directory.
File names are derived from the note title (lower‑case, spaces replaced with underscores) with a `.md` extension.

Each note file may contain a YAML frontmatter block at the top, enclosed by `---` lines, storing metadata such as `title`, `created`, `modified`, `tags`, `author`. If frontmatter is missing, the note is treated as plain text (backward compatible).

## Tools

### create_note
Create a new note.

- `title`: The title of the note (will be used as the filename).
- `content`: The text content of the note.

If a note with the same title already exists, the tool will return an error. The note is created with default metadata (creation time, modification time, empty tags).

### read_note
Read the content of an existing note.

- `title`: The title of the note to read.

Returns the note's content as plain text (without frontmatter). If the note does not exist, returns an error.

### update_note
Update the content of an existing note.

- `title`: The title of the note to update.
- `new_content`: The new text content that will replace the previous content.

If the note does not exist, returns an error. Updates the modification timestamp in metadata.

### delete_note
Delete a note.

- `title`: The title of the note to delete.

Returns a success message if the note existed and was deleted, or an error if the note was not found.

### list_notes
List all notes currently stored.

Returns a bullet‑list of note titles (filenames).

### add_tag_to_note
Add a tag to an existing note.

- `title`: The title of the note.
- `tag`: The tag to add.

If the note does not exist, returns an error. If the tag already exists, does nothing. Updates the modification timestamp.

### remove_tag_from_note
Remove a tag from an existing note.

- `title`: The title of the note.
- `tag`: The tag to remove.

If the note does not exist, returns an error. If the tag does not exist, does nothing. Updates the modification timestamp.

### list_tags
List all unique tags across all notes, along with the notes they appear on.

Returns a bullet‑list of tags and associated note titles.

### search_notes
Search for notes by title, content, or tags.

- `query`: The search string (case‑insensitive).

Returns a list of matching notes with content snippets.

### get_note_metadata
Get metadata of a note (creation time, modification time, tags, author).

- `title`: The title of the note.

Returns formatted metadata. If the note has no metadata, returns a message.
