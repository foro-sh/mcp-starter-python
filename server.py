import foro
from app import mcp
from tools import load_tools

load_tools()  # registers every tool in tools/ against `mcp`

if __name__ == "__main__":
    foro.run(mcp)
