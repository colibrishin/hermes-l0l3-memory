#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERMES_DIR="${HERMES_HOME:-$HOME/.hermes}"
mkdir -p "$HERMES_DIR/plugins" "$HERMES_DIR/skills"
cp -r "$SCRIPT_DIR/plugins/l0-l3-memory" "$HERMES_DIR/plugins/"
cp -r "$SCRIPT_DIR/skills/l0-l3-memory" "$HERMES_DIR/skills/"
echo "Installed l0-l3-memory plugin and skill to $HERMES_DIR"
