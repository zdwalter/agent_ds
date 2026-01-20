import hashlib
import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hash_skill", log_level="ERROR")


@mcp.tool()
def hash_string(algorithm: str = "sha256", text: str = "") -> str:
    """
    Compute a hash digest for a given string.

    Args:
        algorithm: Hash algorithm ('md5', 'sha1', 'sha256', default 'sha256').
        text: The input string to hash.
    """
    algo = algorithm.lower()
    if algo not in ("md5", "sha1", "sha256"):
        return f"Error: unsupported algorithm '{algorithm}'. Choose from 'md5', 'sha1', 'sha256'."

    try:
        h = hashlib.new(algo)
        h.update(text.encode("utf-8"))
        return h.hexdigest()
    except Exception as e:
        return f"Error computing hash: {str(e)}"


@mcp.tool()
def hash_file(algorithm: str = "sha256", file_path: str = "") -> str:
    """
    Compute a hash digest for a file.

    Args:
        algorithm: Hash algorithm ('md5', 'sha1', 'sha256', default 'sha256').
        file_path: Absolute path to the file.
    """
    if not os.path.exists(file_path):
        return f"Error: file '{file_path}' does not exist."

    algo = algorithm.lower()
    if algo not in ("md5", "sha1", "sha256"):
        return f"Error: unsupported algorithm '{algorithm}'. Choose from 'md5', 'sha1', 'sha256'."

    try:
        h = hashlib.new(algo)
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return f"Error computing file hash: {str(e)}"


if __name__ == "__main__":
    mcp.run()
