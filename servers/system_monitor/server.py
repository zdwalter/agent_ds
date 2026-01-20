import os
import signal
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

mcp = FastMCP("system_monitor", log_level="ERROR")


def _check_psutil() -> str:
    if not PSUTIL_AVAILABLE:
        return "Error: psutil package is not installed. Please add 'psutil' to requirements.txt and install it."
    return ""


@mcp.tool()
def get_cpu_usage(interval: float = 1.0, percpu: bool = False) -> str:
    """
    Get current CPU usage percentage.

    Args:
        interval: Optional sampling interval in seconds (default 1.0).
        percpu: If True, returns per‑CPU usage (list). Default False.
    """
    err = _check_psutil()
    if err:
        return err
    try:
        usage = psutil.cpu_percent(interval=interval, percpu=percpu)
        if percpu:
            return f"Per‑CPU usage (%): {usage}"
        else:
            return f"Overall CPU usage: {usage}%"
    except Exception as e:
        return f"Error obtaining CPU usage: {str(e)}"


@mcp.tool()
def get_memory_usage() -> str:
    """Get memory usage statistics (total, available, used, percentage)."""
    err = _check_psutil()
    if err:
        return err
    try:
        mem = psutil.virtual_memory()
        return (
            f"Memory usage:\n"
            f"  Total: {mem.total / (1024**3):.2f} GB\n"
            f"  Available: {mem.available / (1024**3):.2f} GB\n"
            f"  Used: {mem.used / (1024**3):.2f} GB\n"
            f"  Percentage: {mem.percent}%"
        )
    except Exception as e:
        return f"Error obtaining memory usage: {str(e)}"


@mcp.tool()
def get_disk_usage(path: str = "/") -> str:
    """
    Get disk usage statistics for a given path.

    Args:
        path: The directory path to check (default "/").
    """
    err = _check_psutil()
    if err:
        return err
    try:
        usage = psutil.disk_usage(path)
        return (
            f"Disk usage for '{path}':\n"
            f"  Total: {usage.total / (1024**3):.2f} GB\n"
            f"  Used: {usage.used / (1024**3):.2f} GB\n"
            f"  Free: {usage.free / (1024**3):.2f} GB\n"
            f"  Percentage: {usage.percent}%"
        )
    except Exception as e:
        return f"Error obtaining disk usage: {str(e)}"


@mcp.tool()
def list_processes(name_filter: Optional[str] = None, limit: int = 50) -> str:
    """
    List running processes with optional filtering.

    Args:
        name_filter: Optional substring to filter process names.
        limit: Maximum number of processes to return (default 50).
    """
    err = _check_psutil()
    if err:
        return err
    try:
        processes = []
        for proc in psutil.process_iter(
            ["pid", "name", "cpu_percent", "memory_percent"]
        ):
            try:
                info = proc.info
                if name_filter and name_filter.lower() not in info["name"].lower():
                    continue
                processes.append(info)
                if len(processes) >= limit:
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if not processes:
            return "No processes found."
        # Format as table
        lines = ["PID\tName\tCPU%\tMem%"]
        for p in processes:
            lines.append(
                f"{p['pid']}\t{p['name']}\t{p['cpu_percent']:.1f}\t{p['memory_percent']:.1f}"
            )
        return "Processes:\n" + "\n".join(lines)
    except Exception as e:
        return f"Error listing processes: {str(e)}"


@mcp.tool()
def kill_process(pid: int, signal: int = 9) -> str:
    """
    Terminate a process by PID.

    Args:
        pid: Process ID (integer).
        signal: Signal number (default 9 = SIGKILL). Use 15 for SIGTERM.
    """
    err = _check_psutil()
    if err:
        return err
    try:
        proc = psutil.Process(pid)
        proc.send_signal(signal)
        return f"Signal {signal} sent to process {pid} ({proc.name()})."
    except psutil.NoSuchProcess:
        return f"Error: Process with PID {pid} does not exist."
    except psutil.AccessDenied:
        return f"Error: Permission denied to kill process {pid}."
    except Exception as e:
        return f"Error killing process: {str(e)}"


if __name__ == "__main__":
    mcp.run()
