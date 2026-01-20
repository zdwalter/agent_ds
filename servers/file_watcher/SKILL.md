---
name: file_watcher
description: File system monitoring using watchdog (watch directories for changes).
allowed-tools:
  - watch_directory
  - stop_watching
  - list_watched_directories
  - get_events
---

# File Watcher Skill

This skill enables the agent to monitor directories for file system events (create, modify, delete, move).

## Tools

### watch_directory
Start watching a directory for changes.

- `directory`: Path to the directory to watch.
- `recursive`: Watch subdirectories as well (default True).
- `event_types`: Comma‑separated list of event types to listen for: "created", "modified", "deleted", "moved". Default is all.
- `output_log`: Optional file path to append events as they occur.

### stop_watching
Stop watching a directory.

- `directory`: Path of the directory to stop watching. If not provided, stop all watchers.

### list_watched_directories
List currently watched directories.

- No parameters.

### get_events
Retrieve recent events captured by the watcher.

- `directory`: Optional directory to filter events.
- `limit`: Maximum number of events to return (default 20).
- `clear`: If True, clear the event buffer after returning (default False).

## Dependencies

- watchdog (must be installed via pip)
