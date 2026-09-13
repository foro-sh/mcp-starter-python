from app import mcp


@mcp.tool
def add(a: int, b: int) -> int:
    return a + b
