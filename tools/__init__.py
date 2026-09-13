"""One file per tool. Drop a new file in this directory and decorate its
function with @mcp.tool (importing `mcp` from `app`) - load_tools() finds
it, so there is no import list here to keep in sync. Modules whose name
starts with an underscore are skipped, for shared helpers that aren't
tools themselves.
"""

import importlib
import pkgutil


def load_tools() -> list[str]:
    """Import every tool module for its registration side effect: importing
    it is what runs its @mcp.tool decorators. Returns the module names that
    were loaded, so a caller (or a test) can tell registration actually
    happened instead of trusting a silent import."""
    loaded = []
    for _, name, _ in pkgutil.iter_modules(__path__):
        if name.startswith("_"):
            continue
        importlib.import_module(f"{__name__}.{name}")
        loaded.append(name)
    return loaded
