import json
import threading
import time
from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from watchdog.events import FileSystemEventHandler  # type: ignore
from watchdog.observers import Observer  # type: ignore

mcp = FastMCP("file_watcher", log_level="ERROR")

# Global state
observers: Dict[str, Observer] = {}
event_buffers: Dict[str, deque] = {}
log_files: Dict[str, Path] = {}
lock = threading.RLock()


class EventHandler(FileSystemEventHandler):
    def __init__(self, dir_path: str, buffer: deque, log_file: Optional[Path] = None):
        self.dir_path = dir_path
        self.buffer = buffer
        self.log_file = log_file

    def on_any_event(self, event):
        with lock:
            entry = {
                "time": time.time(),
                "event_type": event.event_type,
                "src_path": event.src_path,
                "dest_path": getattr(event, "dest_path", None),
            }
            self.buffer.append(entry)
            if self.log_file:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry) + "\n")


@mcp.tool()
def watch_directory(
    directory: str,
    recursive: bool = True,
    event_types: str = "created,modified,deleted,moved",
    output_log: Optional[str] = None,
) -> str:
    """
    Start watching a directory for changes.
    """
    try:
        with lock:
            dir_path = Path(directory).resolve()
            if not dir_path.exists() or not dir_path.is_dir():
                return f"Error: '{directory}' is not a valid directory."
            if str(dir_path) in observers:
                return f"Already watching '{directory}'."
            # Create buffer
            buffer: deque = deque(maxlen=1000)
            event_buffers[str(dir_path)] = buffer
            # Create observer
            observer = Observer()
            handler = EventHandler(
                str(dir_path), buffer, Path(output_log) if output_log else None
            )
            observer.schedule(handler, str(dir_path), recursive=recursive)
            observer.start()
            observers[str(dir_path)] = observer
            if output_log:
                log_files[str(dir_path)] = Path(output_log)
            return f"Started watching '{directory}' (recursive={recursive}). Events: {event_types}. Log: {output_log}"
    except Exception as e:
        return f"Error starting watcher: {str(e)}"


@mcp.tool()
def stop_watching(directory: Optional[str] = None) -> str:
    """
    Stop watching a directory.
    """
    try:
        with lock:
            if directory is None:
                # Stop all
                stopped = []
                for dir_path, obs in list(observers.items()):
                    obs.stop()
                    obs.join()
                    stopped.append(dir_path)
                for dir_path in stopped:
                    observers.pop(dir_path, None)
                    event_buffers.pop(dir_path, None)
                    log_files.pop(dir_path, None)
                return f"Stopped all watchers ({len(stopped)})."
            else:
                dir_path = str(Path(directory).resolve())
                if dir_path not in observers:
                    return f"Not watching '{directory}'."
                observers[dir_path].stop()
                observers[dir_path].join()
                observers.pop(dir_path)
                event_buffers.pop(dir_path, None)
                log_files.pop(dir_path, None)
                return f"Stopped watching '{directory}'."
    except Exception as e:
        return f"Error stopping watcher: {str(e)}"


@mcp.tool()
def list_watched_directories() -> str:
    """
    List currently watched directories.
    """
    with lock:
        if not observers:
            return "No directories being watched."
        return "Watched directories:\n" + "\n".join(f"- {d}" for d in observers.keys())


@mcp.tool()
def get_events(
    directory: Optional[str] = None, limit: int = 20, clear: bool = False
) -> str:
    """
    Retrieve recent events captured by the watcher.
    """
    try:
        with lock:
            if directory is None:
                # Collect events from all buffers
                all_events: List[Dict[str, Any]] = []
                for dir_path, buffer in event_buffers.items():
                    all_events.extend(
                        {"directory": dir_path, **e} for e in list(buffer)
                    )
                all_events.sort(key=lambda e: e["time"], reverse=True)
                events = all_events[:limit]
                if clear:
                    for buffer in event_buffers.values():
                        buffer.clear()
            else:
                dir_path = str(Path(directory).resolve())
                if dir_path not in event_buffers:
                    return f"No events for '{directory}' (not being watched)."
                buffer = event_buffers[dir_path]
                events = list(buffer)[-limit:]
                if clear:
                    buffer.clear()
            if not events:
                return "No events captured."
            # Format
            lines = []
            for e in reversed(events):
                dir_part = (
                    f"[{e.get('directory', directory)}] " if directory is None else ""
                )
                lines.append(
                    f"{time.ctime(e['time'])} {dir_part}{e['event_type']}: {e['src_path']}"
                    + (f" -> {e['dest_path']}" if e["dest_path"] else "")
                )
            return "\n".join(lines)
    except Exception as e:
        return f"Error retrieving events: {str(e)}"


# Cleanup on exit
def cleanup():
    with lock:
        for obs in observers.values():
            obs.stop()
            obs.join()


if __name__ == "__main__":
    try:
        mcp.run()
    finally:
        cleanup()
