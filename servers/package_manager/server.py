import subprocess
import sys
from typing import List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("package_manager", log_level="ERROR")


def _run_pip_command(args: List[str]) -> str:
    """Run pip command and return stdout+stderr."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip"] + args,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout
        if result.stderr:
            output += "\n" + result.stderr
        if result.returncode != 0:
            output = f"pip command failed (exit {result.returncode}):\n{output}"
        return output.strip()
    except subprocess.TimeoutExpired:
        return "Error: pip command timed out."
    except Exception as e:
        return f"Error executing pip: {str(e)}"


@mcp.tool()
def pip_install(packages: List[str], upgrade: bool = False, user: bool = False) -> str:
    """
    Install one or more packages using pip.

    Args:
        packages: List of package names (with optional version specifiers).
        upgrade: If True, upgrade existing packages (default False).
        user: Install to the user site‑directory (default False).
    """
    if not packages:
        return "Error: No packages specified."
    args = ["install"]
    if upgrade:
        args.append("--upgrade")
    if user:
        args.append("--user")
    args.extend(packages)
    return _run_pip_command(args)


@mcp.tool()
def pip_uninstall(packages: List[str], yes: bool = True) -> str:
    """
    Uninstall packages.

    Args:
        packages: List of package names to remove.
        yes: Assume "yes" to confirmation prompts (default True).
    """
    if not packages:
        return "Error: No packages specified."
    args = ["uninstall"]
    if yes:
        args.append("-y")
    args.extend(packages)
    return _run_pip_command(args)


@mcp.tool()
def pip_list(outdated: bool = False) -> str:
    """
    List installed packages.

    Args:
        outdated: If True, list only outdated packages (default False).
    """
    args = ["list"]
    if outdated:
        args.append("--outdated")
    return _run_pip_command(args)


@mcp.tool()
def pip_search(query: str, limit: int = 20) -> str:
    """
    Search for packages on PyPI.

    Args:
        query: Search term.
        limit: Maximum number of results (default 20).
    """
    # Note: pip search may be disabled or require an external API.
    # Use `pip search` command if available, else fallback.
    args = ["search", query]
    output = _run_pip_command(args)
    # Limit lines
    lines = output.splitlines()
    if len(lines) > limit + 2:  # header + separator
        lines = lines[: limit + 2]
        lines.append(f"... (truncated to {limit} results)")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
