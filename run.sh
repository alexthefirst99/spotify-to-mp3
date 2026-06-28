#!/bin/bash
set -e
cd "$(dirname "$0")"

GREEN='\033[0;32m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

echo ""
echo -e "${BOLD}Spotify → iPod${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. Python 3 ──────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Python 3 not found.${RESET}"
    echo "  Install it from: https://python.org/downloads"
    exit 1
fi
echo -e "${GREEN}✓${RESET} Python $(python3 --version | cut -d' ' -f2)"

# ── 2. pip packages ──────────────────────────────────────
if ! python3 -c "import spotdl, flask" &>/dev/null 2>&1; then
    echo "  Installing packages (first run only)..."
    pip3 install spotdl flask -q --disable-pip-version-check
fi
echo -e "${GREEN}✓${RESET} Packages ready"

# ── 3. Deno (YouTube Music support) ──────────────────────
python3 -m spotdl --download-deno &>/dev/null 2>&1 || true
echo -e "${GREEN}✓${RESET} YouTube Music support ready"

# ── 4. Launch ────────────────────────────────────────────
echo ""
echo -e "  Opening at ${BOLD}http://127.0.0.1:5001${RESET}"
echo ""
python3 app.py
