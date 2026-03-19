# trezor-emulator MCP

MCP server for controlling Trezor emulators running inside `trezor-user-env` Docker container.

## How it works

Connects to the `trezor-user-env` WebSocket API on port 9001 to send commands (start/stop, click, input, setup, etc.) and captures screenshots via VNC on port 5900.

The emulator start commands send `use_vnc: true`, which tells `trezor-user-env` to render the emulator GUI inside the Docker container using a virtual display and VNC server instead of forwarding X11 to the host:

```
Emulator binary → renders GUI via SDL2 → Xvfb (virtual framebuffer)
                                              ↓
                                         x11vnc (reads pixels from Xvfb)
                                              ↓
                                         VNC protocol on port 5900
                                              ↓
                                         websockify (TCP→WebSocket bridge)
                                              ↓
                                         noVNC in browser on port 6080
```

## Requirements

- `trezor-user-env` Docker container running with ports 9001, 5900, and 6080 exposed
- VNC support — requires the [`vnc`](https://github.com/trezor/trezor-user-env/tree/vnc) branch of `trezor-user-env` ([PR #348](https://github.com/trezor/trezor-user-env/pull/348))
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
