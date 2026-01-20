---
name: regex_skill
description: Regular expression matching, searching, replacing, and extracting.
allowed-tools:
  - regex_match
  - regex_search
  - regex_replace
  - regex_extract
---

# Regex Skill

This skill enables the agent to work with regular expressions for text processing.

## Tools

### regex_match
Find all non-overlapping matches of a pattern in a text.

- `pattern`: The regular expression pattern.
- `text`: The input text to search.
- Returns a list of matched strings.

### regex_search
Search for the first occurrence of a pattern in a text, returning match details.

- `pattern`: The regular expression pattern.
- `text`: The input text to search.
- Returns a dictionary with match position and groups.

### regex_replace
Replace all occurrences of a pattern in a text with a replacement string.

- `pattern`: The regular expression pattern.
- `replacement`: The replacement string.
- `text`: The input text.
- Returns the modified text.

### regex_extract
Extract captured groups from all matches of a pattern.

- `pattern`: The regular expression pattern.
- `text`: The input text.
- Returns a list of captured groups.
