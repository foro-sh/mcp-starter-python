# mcp-server

A [FastMCP](https://gofastmcp.com) server, ready to deploy on
[foro.sh](https://foro.sh). It ships with one example tool, `add`, so everything
below works before you've written a tool of your own.

## Layout

- `server.py` is the entrypoint foro.sh starts. It loads the tools and serves
  them over streamable HTTP on `$PORT` with `foro.run(mcp)`.
- `app.py` holds the `FastMCP` instance every tool registers against.
- `tools/` has one file per tool. Add a file, decorate its function with
  `@mcp.tool`, and `load_tools()` picks it up: there's no import list to keep
  in sync.
- `tests/` is pytest. `test_tools.py` tests `add`, and checks that the
  entrypoint really registers every tool, since a missing tool doesn't stop the
  server from starting.

## Run it locally

You need [uv](https://docs.astral.sh/uv/).

```bash
uvx foro dev
```

`foro dev` starts the server the way foro.sh will, confirms it would pass the
platform's health check, and lists its tools. The server is then at
`http://localhost:8000/mcp`, so any MCP client can connect to it:

```bash
claude mcp add --transport http mcp-server http://localhost:8000/mcp
```

If a tool needs an API key or another secret, copy `.env.example` to `.env`
and fill it in. `foro dev` loads it, and the code reads it with
`foro.secret("NAME")`. `.env` is never committed or deployed.

## Test

```bash
uv run pytest
```

## Dependencies

Add packages with `uv add <package>`, which updates `pyproject.toml` and
`uv.lock` together, and commit both. foro.sh installs exactly what `uv.lock`
pins, so a package listed only in `pyproject.toml` is never installed and the
server fails on import. `uvx foro check` catches a stale lockfile before you
push.

## Deploy to foro.sh

1. Push this repo to GitHub.
2. In the [foro.sh](https://foro.sh) dashboard, create a project from it and
   add any secrets your tools read under **Secrets**.
3. Deploy. The server comes up at `https://<slug>.foro.sh/mcp`, with a slug
   foro.sh generates.

To ship a change later, push and press **Redeploy**. Run `uvx foro check`
first: it catches most failed deploys in seconds instead of a minute.

## Agent skills

`.claude/skills/` holds three skills for coding agents working in this repo.
Claude Code picks them up automatically.

- **design-mcp-tools**: shaping tool names, descriptions and parameters so a
  model picks the right tool and they're cheap to include in every request.
- **wrap-an-http-api**: building tools on an existing API from its real spec,
  not from half-remembered endpoints.
- **deploy-to-foro**: shipping to foro.sh, and reading the logs when a deploy
  fails.

They're copied from
[foro-sh/foro](https://github.com/foro-sh/foro/tree/main/plugins/claude-code/skills).
Once they're in your repo they're yours, so edit or delete them as the project
grows. `AGENTS.md` has the short version of how to work here.
