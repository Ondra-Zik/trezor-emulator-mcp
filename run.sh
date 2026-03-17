#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
SERVER="$SCRIPT_DIR/server.py"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is not installed." >&2
  exit 1
fi

VENV_DIR="${TREZOR_EMULATOR_VENV:-$SCRIPT_DIR/.venv}"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating Python virtual environment at $VENV_DIR" >&2
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

if ! python3 -m pip --version >/dev/null 2>&1; then
  echo "pip not found in virtual environment, attempting bootstrap via ensurepip" >&2
  python3 -m ensurepip --upgrade >/dev/null 2>&1 || true
fi

if ! python3 -m pip --version >/dev/null 2>&1; then
  echo "Error: pip is unavailable in $VENV_DIR. Install pip for python3 and rerun." >&2
  exit 1
fi

if ! python3 -c "import mcp, websockets, PIL, vncdotool" >/dev/null 2>&1; then
  echo "Installing Python dependencies into $VENV_DIR" >&2
  python3 -m pip install --upgrade pip
  python3 -m pip install -r "$REQUIREMENTS"
fi

echo "Starting with Python virtual environment at $VENV_DIR" >&2
exec python3 "$SERVER"
