---
name: system_monitor
description: System monitoring capabilities using psutil (CPU, memory, disk, processes).
allowed-tools:
  - get_cpu_usage
  - get_memory_usage
  - get_disk_usage
  - list_processes
  - kill_process
---

# System Monitor Skill

This skill enables the agent to monitor system resources and manage processes.

## Tools

### get_cpu_usage
Get current CPU usage percentage.

- `interval`: Optional sampling interval in seconds (default 1.0).
- `percpu`: If True, returns per‑CPU usage (list). Default False.

### get_memory_usage
Get memory usage statistics (total, available, used, percentage).

- No parameters.

### get_disk_usage
Get disk usage statistics for a given path.

- `path`: The directory path to check (default "/").

### list_processes
List running processes with optional filtering.

- `name_filter`: Optional substring to filter process names.
- `limit`: Maximum number of processes to return (default 50).

### kill_process
Terminate a process by PID.

- `pid`: Process ID (integer).
- `signal`: Signal number (default 9 = SIGKILL). Use 15 for SIGTERM.

## Dependencies

- psutil (must be added to requirements.txt)
