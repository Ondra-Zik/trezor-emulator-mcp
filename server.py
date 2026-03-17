#!/usr/bin/env python3
"""MCP server for controlling the Trezor T3W1 emulator via WebSocket API."""

import asyncio
import json
import os
import websockets
from mcp.server.fastmcp import FastMCP, Image

# Emulator window position within the X display (:69 runs at 2048×2048)
EMULATOR_X = 824
EMULATOR_Y = 724
EMULATOR_W = 412
EMULATOR_H = 552

WS_URL = "ws://localhost:9001"

mcp = FastMCP("trezor-emulator")


async def _send_command(payload: dict) -> dict:
    """Send a command to the emulator WebSocket and return the response."""
    async with websockets.connect(WS_URL) as ws:
        await ws.recv()  # consume welcome/firmware-list message
        await ws.send(json.dumps(payload))
        raw = await ws.recv()
        return json.loads(raw)


@mcp.tool()
async def emulator_click(x: int, y: int) -> str:
    """
    Touch (click) a coordinate on the Trezor emulator display.

    The display is 412×552 pixels: (0,0) is top-left, (411,551) is bottom-right.

    Common button positions on the THP pairing screen:
      - Confirm / green checkmark: x=255, y=491
      - Dismiss / X button:        x=88,  y=491
    """
    result = await _send_command({"type": "emulator-click", "x": x, "y": y})
    if result.get("success"):
        return f"Clicked at ({x}, {y}): {result.get('response', 'ok')}"
    return f"Click failed: {result}"


@mcp.tool()
async def emulator_press_yes() -> str:
    """Press the physical YES (confirm) button on the Trezor emulator."""
    result = await _send_command({"type": "emulator-press-yes"})
    if result.get("success"):
        return "Pressed YES"
    return f"Press YES failed: {result}"


@mcp.tool()
async def emulator_press_no() -> str:
    """Press the physical NO (cancel) button on the Trezor emulator."""
    result = await _send_command({"type": "emulator-press-no"})
    if result.get("success"):
        return "Pressed NO"
    return f"Press NO failed: {result}"


@mcp.tool()
async def emulator_input(value: str) -> str:
    """Type text into the Trezor emulator (e.g. PIN or passphrase)."""
    result = await _send_command({"type": "emulator-input", "value": value})
    if result.get("success"):
        return f"Typed input: {value!r}"
    return f"Input failed: {result}"


@mcp.tool()
async def emulator_stop() -> str:
    """Stop the Trezor emulator."""
    result = await _send_command({"type": "emulator-stop"})
    return f"Stop result: {result}"


@mcp.tool()
async def emulator_screenshot() -> Image:
    """
    Take a screenshot of the Trezor emulator display and return it as a PNG image.

    Captures directly from the VNC server on port 5900.
    """
    import io
    from vncdotool import api as vncapi

    try:
        client = vncapi.connect("localhost::5900")
        png_buffer = io.BytesIO()
        png_buffer.name = "screenshot.png"
        client.captureScreen(png_buffer)
        client.disconnect()
        png_data = png_buffer.getvalue()
        return Image(data=png_data, format="png")
    except Exception as e:
        raise RuntimeError(f"VNC screenshot failed: {str(e)}")

@mcp.tool()
async def emulator_ping() -> str:
    """Ping the emulator WebSocket server. Returns 'pong' if reachable."""
    result = await _send_command({"type": "ping"})
    return f"Ping result: {result}"


if __name__ == "__main__":
    mcp.run()
