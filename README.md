# tidal-mcp

Community derivative of [sickn33/tidal-mcp](https://github.com/sickn33/tidal-mcp), prepared for public source distribution. The upstream MIT license and required attribution are retained. This repository starts with a fresh Git history.

## Install and run

Requires Python 3.11–3.13.

```sh
python -m venv .venv
# Activate .venv using the command appropriate to your shell.
python -m pip install -e .
python -m pip install pytest
python -m pytest
tidal-auth
tidal-mcp
```

Configure your MCP client to launch the installed `tidal-mcp` executable over stdio. Run `tidal-auth` interactively once to authorize your own account. The session is stored in the platform user-data directory. Optional local settings: `TIDAL_MCP_DATA_DIR`, `TIDAL_MCP_SESSION_FILE`, `TIDAL_MCP_DRAFT_TTL_SECONDS` (60–3600). Writes are disabled by default; enable them with `TIDAL_MCP_ENABLE_WRITES=true`. Mutations require the preview/commit approval flow.

## Privacy

No account configuration, OAuth sessions, personal exports, or local Git history are distributed. Examples and tests use fixtures. Never commit your local credentials or session files. Runtime tools can return information from the account you connect; review outputs before sharing them.

## Changes in this derivative

Authentication and logout success messages omit local filesystem paths and account identifiers. Regression tests verify that successful authentication does not print these values.

Only GitHub source distribution is configured; this derivative is not published to npm or PyPI.

On Windows, local session confidentiality relies on the ACLs of your user-data directory; POSIX mode bits do not enforce owner-only access there. Keep custom storage directories private.
