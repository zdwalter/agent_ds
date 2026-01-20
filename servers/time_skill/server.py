import datetime
import time
from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("time_skill", log_level="ERROR")


@mcp.tool()
def get_current_time(timezone: Optional[str] = None) -> str:
    """
    Return the current local time and UTC time.

    Args:
        timezone: Optional timezone name (e.g., 'America/New_York'). If omitted, uses local system time.
    """
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    local_now = datetime.datetime.now()

    result = f"UTC: {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
    result += f"Local: {local_now.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"

    if timezone:
        try:
            # Try to use zoneinfo (Python 3.9+)
            from zoneinfo import ZoneInfo

            tz = ZoneInfo(timezone)
            tz_now = datetime.datetime.now(tz)
            result += (
                f"Timezone '{timezone}': {tz_now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
            )
        except ImportError:
            # Fallback to pytz if installed
            try:
                import pytz  # type: ignore

                tz = pytz.timezone(timezone)  # type: ignore
                tz_now = datetime.datetime.now(tz)
                result += (
                    f"Timezone '{timezone}': {tz_now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
                )
            except ImportError:
                result += f"Warning: cannot handle timezone '{timezone}' because zoneinfo/pytz not available."
            except pytz.exceptions.UnknownTimeZoneError:
                result += f"Error: unknown timezone '{timezone}'."
        except Exception as e:
            result += f"Error with timezone '{timezone}': {str(e)}"

    return result


@mcp.tool()
def format_timestamp(timestamp: str, format: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
    """
    Format a Unix timestamp or ISO‑8601 string into a human‑readable date/time.

    Args:
        timestamp: The timestamp (Unix integer or ISO‑8601 string).
        format: Optional strftime format (default '%Y-%m-%d %H:%M:%S %Z').
    """
    dt = None
    try:
        # Try as Unix timestamp (integer string)
        ts_int = int(timestamp)
        dt = datetime.datetime.fromtimestamp(ts_int, tz=datetime.timezone.utc)
    except ValueError:
        # Try as ISO‑8601 string
        try:
            dt = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            return f"Error: invalid timestamp format. Expected Unix integer or ISO‑8601 string."

    if dt is None:
        return "Error: could not parse timestamp."

    try:
        formatted = dt.strftime(format)
        return formatted
    except Exception as e:
        return f"Error formatting: {str(e)}"


@mcp.tool()
def add_time(
    timestamp: str,
    days: float = 0,
    hours: float = 0,
    minutes: float = 0,
    seconds: float = 0,
) -> str:
    """
    Add a specified duration to a given timestamp.

    Args:
        timestamp: Base timestamp (Unix integer or ISO‑8601 string).
        days: Days to add (can be negative).
        hours: Hours to add (can be negative).
        minutes: Minutes to add (can be negative).
        seconds: Seconds to add (can be negative).
    """
    dt = None
    try:
        ts_int = int(timestamp)
        dt = datetime.datetime.fromtimestamp(ts_int, tz=datetime.timezone.utc)
    except ValueError:
        try:
            dt = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            return f"Error: invalid timestamp format. Expected Unix integer or ISO‑8601 string."

    if dt is None:
        return "Error: could not parse timestamp."

    delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    new_dt = dt + delta
    return new_dt.isoformat()


if __name__ == "__main__":
    mcp.run()
