# trezor-emulator MCP

MCP server for controlling Trezor emulators running inside `trezor-user-env` Docker container.

## How it works

Connects to the `trezor-user-env` WebSocket API on port 9001 to send commands (start/stop, click, input, setup, etc.) and captures screenshots via VNC on port 5900.

## Requirements

- `trezor-user-env` Docker container running with port 9001 exposed
- VNC on `localhost:5900` (for `emulator_screenshot`) — requires the [`feature/x11-to-vnc-migration`](https://github.com/trezor/trezor-user-env/tree/feature/x11-to-vnc-migration) branch of `trezor-user-env`
- `python3` with `venv`

## Setup

Run `./run.sh` — it creates `.venv` (or uses `$TREZOR_EMULATOR_VENV`), installs dependencies, and starts the server.

### MCP config example (VS Code)

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

## Tools

| Tool | Arguments | Description |
|---|---|---|
| `emulator_start` | `model`, `version?`, `wipe?` | Start emulator with given model/firmware |
| `emulator_start_from_url` | `url`, `model`, `wipe?` | Start emulator from a firmware URL |
| `emulator_start_from_branch` | `branch`, `model`, `btc_only?`, `wipe?` | Start emulator from a git branch build |
| `emulator_stop` | — | Stop the emulator |
| `emulator_setup` | `mnemonic`, `pin`, `passphrase_protection`, `label`, `needs_backup?` | Set up device with seed and settings |
| `emulator_wipe` | — | Wipe all device data |
| `emulator_apply_settings` | `label?`, `passphrase_always_on_device?`, `auto_lock_delay_ms?` | Apply device settings |
| `emulator_get_features` | — | Get device features/capabilities |
| `emulator_get_debug_state` | — | Get debug state (layout, PIN, mnemonic) |
| `emulator_screenshot` | — | Capture display as PNG via VNC |
| `emulator_click` | `x`, `y` | Touch at display coordinates (412×552) |
| `emulator_swipe` | `direction` | Swipe up/down/left/right |
| `emulator_press_yes` | — | Press physical YES button |
| `emulator_press_no` | — | Press physical NO button |
| `emulator_input` | `value` | Type text (PIN, passphrase) |
| `emulator_ping` | — | Check WebSocket connectivity |
| `bridge_start` | `version?` | Start the Trezor bridge |
| `bridge_stop` | — | Stop the Trezor bridge |
| `background_check` | — | Check status of all running services |
