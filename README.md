# trezor-emulator MCP
# WIP WIP WIP

MCP server for controlling the Trezor T3W1 emulator running inside `trezor-user-env` Docker container.

## Why this exists

VNC clicks, xdotool, and Playwright mouse events all fail on the T3W1 emulator because its firmware uses SDL touchscreen events (`SDL_FINGERDOWN`/`SDL_FINGERUP`) — not X11 mouse events. This server uses the WebSocket API exposed by `trezor-user-env` on port 9001, which bypasses X11/SDL entirely.

## Requirements

- `trezor-user-env` Docker container running with port 9001 exposed
- VNC endpoint for the emulator available on `localhost:5900` (required by `emulator_screenshot`)
- `python3` with `venv` and internet access for `pip install`

## Setup

Use `./run.sh` to start the server. It will:

1. Create/use `.venv` (or `$TREZOR_EMULATOR_VENV` if set).
2. Install missing Python packages with `pip`.
3. Run `server.py` from that virtual environment.

## Use directly from GitHub

1. Clone this repository.
2. Set your MCP config to execute `run.sh` from the cloned folder.

Example VS Code user MCP config entry:

```json
{
	"servers": {
		"trezor-emulator": {
			"type": "stdio",
			"command": "/usr/bin/env",
			"args": [
				"bash",
				"/absolute/path/to/trezor-emulator-mcp/run.sh"
			]
		}
	}
}
```

For first start, internet access is needed so `pip` can install dependencies into `.venv`.

The server is registered in `~/.claude/settings.json` as `trezor-emulator` and starts automatically when Claude Code loads. Restart Claude Code or open `/hooks` after first install.

## Tools

| Tool | Arguments | Description |
|---|---|---|
| `emulator_screenshot` | — | Capture emulator display as PNG image |
| `emulator_click` | `x: int, y: int` | Touch at display coordinates |
| `emulator_press_yes` | — | Press physical YES button |
| `emulator_press_no` | — | Press physical NO button |
| `emulator_input` | `value: str` | Type text (PIN, passphrase) |
| `emulator_stop` | — | Stop the emulator |
| `emulator_ping` | — | Check WebSocket connectivity |


## Files

```
trezor-emulator-mcp/
├── requirements.txt  # Python dependencies
├── server.py   # FastMCP server
└── run.sh      # Launcher (.venv bootstrap)
```
