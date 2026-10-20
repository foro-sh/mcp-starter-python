# AGENTS.md

A [FastMCP](https://gofastmcp.com) server that deploys to foro.sh. README.md
covers the layout.

## Commands

- `uv run pytest` runs the tests.
- `uvx foro check` runs the checks foro.sh runs at deploy time, in seconds.
- `uvx foro dev` starts the server the way foro.sh does and lists its tools.

## Working here

- **Re-lock after every dependency change.** Use `uv add` / `uv remove`, or run
  `uv lock` after editing `pyproject.toml`, and commit `uv.lock` with it.
  Deploys install from the lockfile as-is (`uv sync --frozen`): a dependency
  that isn't in it is silently skipped, and the server dies on import.
- One tool per file in `tools/`, each with a test in `tests/`.
- `server.py` is the entrypoint and serves with `foro.run(mcp)`. Keep both.
  `mcp.run()` defaults to stdio, which never opens a port.
- Read secrets with `foro.secret("NAME")`. Locally they come from `.env`;
  deployed, from the Secrets tab in the foro.sh dashboard. Never commit one.
- `.foro/` is scratch space, such as API specs fetched to query with `python3 -c`. It is
  gitignored.

## Skills

`.claude/skills/` holds `design-mcp-tools`, `wrap-an-http-api` and
`deploy-to-foro`. Before writing a client for any external API, follow
`wrap-an-http-api`: an endpoint recalled from memory deploys green and 404s.
