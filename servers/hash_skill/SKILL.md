---
name: hash_skill
description: Compute hash digests for strings and files (MD5, SHA‑1, SHA‑256).
allowed-tools:
  - hash_string
  - hash_file
---

# Hash Skill

This skill computes cryptographic hash digests for text strings and file contents.

## Tools

### hash_string
Compute a hash digest for a given string.
- `algorithm`: Hash algorithm ('md5', 'sha1', 'sha256', default 'sha256').
- `text`: The input string to hash.

### hash_file
Compute a hash digest for a file.
- `algorithm`: Hash algorithm ('md5', 'sha1', 'sha256', default 'sha256').
- `file_path`: Absolute path to the file.
