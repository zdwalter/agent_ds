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


if __name__ == "__main__":
    mcp.run()
