#!/bin/bash
set -e
cd "$(dirname "$0")"

GREEN='\033[0;32m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

echo ""
echo -e "${BOLD}Spotify to MP3${RESET}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. Python 3 ──────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Python 3 not found.${RESET}"
    echo "  Install from: https://python.org/downloads"
    exit 1
fi
echo -e "${GREEN}✓${RESET} Python $(python3 --version | cut -d' ' -f2)"

# ── 2. Virtual environment ────────────────────────────────
if [ ! -d ".venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv .venv
fi
source .venv/bin/activate

# ── 3. pip packages ──────────────────────────────────────
if ! python -c "import spotdl, flask" &>/dev/null 2>&1; then
    echo "  Installing packages (first run only)..."
    pip install spotdl flask yt-dlp -q --disable-pip-version-check
fi
echo "  Updating download tools..."
pip install -U spotdl yt-dlp -q --disable-pip-version-check
echo -e "${GREEN}✓${RESET} Packages ready"

# ── 4. Deno (YouTube Music support) ──────────────────────
python -m spotdl --download-deno &>/dev/null 2>&1 || true
echo -e "${GREEN}✓${RESET} YouTube Music support ready"

# ── 5. Launch ────────────────────────────────────────────
echo ""
echo -e "  Opening at ${BOLD}http://127.0.0.1:5001${RESET}"
echo ""
python app.py
