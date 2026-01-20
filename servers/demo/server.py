from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo", log_level="ERROR")


@mcp.tool()
def greet(name: str) -> str:
    """
    Return a personalized greeting.

    Args:
        name: The name of the person to greet.
    """
    return f"Hello, {name}! Welcome to the demo skill."


@mcp.tool()
def add_numbers(a: float, b: float) -> str:
    """
    Add two numbers and return the sum.

    Args:
        a: First number.
        b: Second number.
    """
    result = a + b
    return f"The sum of {a} and {b} is {result}."


@mcp.tool()
def reverse_string(s: str) -> str:
    """
    Reverse a string.

    Args:
        s: The input string.
    """
    return s[::-1]


@mcp.tool()
def generate_random_number(low: int = 0, high: int = 100) -> str:
    """
    Generate a random integer between low and high (inclusive).

    Args:
        low: Lower bound (default 0).
        high: Upper bound (default 100).
    """
    import random

    num = random.randint(low, high)
    return f"Random integer between {low} and {high}: {num}"


if __name__ == "__main__":
    mcp.run()
