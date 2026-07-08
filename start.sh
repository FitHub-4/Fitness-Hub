#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

VENV_DIR="$ROOT_DIR/.venv"
PYTHON="${PYTHON:-python3}"
PORT="${PORT:-8000}"

echo ""
echo "  Fitness Hub — one-command startup"
echo "  =================================="
echo ""

if ! command -v "$PYTHON" &>/dev/null; then
  echo "Error: python3 not found. Install Python 3.11+ and run again."
  exit 1
fi

if [[ ! -d "$VENV_DIR" ]]; then
  echo "[1/5] Creating virtual environment..."
  "$PYTHON" -m venv "$VENV_DIR"
else
  echo "[1/5] Virtual environment ready"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "[2/5] Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [[ ! -f "$ROOT_DIR/.env" ]]; then
  cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
  echo "      Created .env from .env.example"
fi

echo "[3/5] Running database migrations..."
python manage.py migrate --noinput

echo "[4/5] Seeding exercises, store products, inspiration, achievements..."
python manage.py seed_all

echo "[5/5] Starting server..."
echo ""
echo "  All modules loaded on one server:"
echo "    Home / Exercises .... http://127.0.0.1:${PORT}/"
echo "    Store (products) .... http://127.0.0.1:${PORT}/store/"
echo "    Dashboard ........... http://127.0.0.1:${PORT}/dashboard/"
echo "    Goals ............... http://127.0.0.1:${PORT}/goals/"
echo "    Progress ............ http://127.0.0.1:${PORT}/progress/"
echo "    Diet ................ http://127.0.0.1:${PORT}/diet/"
echo "    Inspiration ......... http://127.0.0.1:${PORT}/inspiration/"
echo "    Chatbot ............. http://127.0.0.1:${PORT}/chatbot/"
echo "    Social .............. http://127.0.0.1:${PORT}/social/"
echo "    Achievements ........ http://127.0.0.1:${PORT}/achievements/"
echo "    Admin ............... http://127.0.0.1:${PORT}/admin/"
echo ""
echo "  Press Ctrl+C to stop."
echo ""

exec python manage.py runserver "127.0.0.1:${PORT}"
