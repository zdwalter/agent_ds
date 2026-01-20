---
name: time_skill
description: Time-related utilities (current time, timer, date calculations).
allowed-tools:
  - get_current_time
  - format_timestamp
  - add_time
---

# Time Skill

This skill provides basic time and date operations.

## Tools

### get_current_time
Return the current local time and UTC time.
- `timezone`: Optional timezone name (e.g., 'America/New_York'). If omitted, uses local system time.

### format_timestamp
Format a Unix timestamp or ISO‑8601 string into a human‑readable date/time.
- `timestamp`: The timestamp (Unix integer or ISO‑8601 string).
- `format`: Optional strftime format (default '%Y-%m-%d %H:%M:%S %Z').

### add_time
Add a specified duration to a given timestamp.
- `timestamp`: Base timestamp (Unix integer or ISO‑8601 string).
- `days`: Days to add (can be negative).
- `hours`: Hours to add (can be negative).
- `minutes`: Minutes to add (can be negative).
- `seconds`: Seconds to add (can be negative).
