import subprocess
import sys
from pathlib import Path

from tools.add import add

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_add():
    assert add(2, 3) == 5


def test_entrypoint_registers_every_tool():
    """Guards the wiring rather than the logic. A tool registers as a side
    effect of its module being imported, so an entrypoint that stops calling
    load_tools(), or a tool file that never gets discovered, still starts up
    perfectly well and serves nothing - a failure that stays invisible until
    a client asks for a tool. This turns it into a test failure instead.

    The probe runs in a fresh interpreter on purpose. Registration mutates
    one shared `mcp` object, and this file's own `from tools.add import add`
    already registers `add` in the pytest process - asserting in here would
    pass whatever the entrypoint does. A clean process imports nothing but
    the entrypoint, so what comes back is exactly what a deployed server
    would serve."""
    probe = (
        "import asyncio, importlib;"
        "importlib.import_module('server');"
        "from app import mcp;"
        "print(' '.join(t.name for t in asyncio.run(mcp.list_tools())))"
    )
    result = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=_PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "add" in result.stdout.split(), result.stdout
