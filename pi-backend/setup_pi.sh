#!/bin/bash
# PHANTOM CONTROLLER — Pi Setup Script
# Run this once on the Pi Zero W to configure everything

set -e

echo "══════════════════════════════════════════"
echo "  PHANTOM CONTROLLER — Pi Setup"
echo "══════════════════════════════════════════"

PI_HOME="/home/noktirnal"
PHANTOM_DIR="$PI_HOME/phantom"
PI_BACKEND="$PHANTOM_DIR/pi-backend"

# ─── 1. System packages ──────────────────────────────
echo "[1/6] Installing system packages..."
sudo apt update
sudo apt install -y git ffmpeg sox python3-pip python3-venv ncurses-base netcat-openbsd

# ─── 2. rpitx (already installed, verify) ─────────────
echo "[2/6] Verifying rpitx..."
if [ ! -f "$PI_HOME/rpitx/rpitx" ]; then
    echo "  Installing rpitx..."
    cd "$PI_HOME"
    git clone https://github.com/F5OEO/rpitx
    cd rpitx
    yes | sudo ./install.sh
    sudo cp src/librpitx/src/librpitx.so /usr/local/lib/
    sudo ldconfig
else
    echo "  rpitx already installed ✓"
fi

# ─── 3. Python venv + packages ────────────────────────
echo "[3/6] Setting up Python environment..."
if [ ! -d "$PHANTOM_DIR" ]; then
    python3 -m venv "$PHANTOM_DIR"
fi
source "$PHANTOM_DIR/bin/activate"
"$PHANTOM_DIR/bin/pip" install --upgrade pip
"$PHANTOM_DIR/bin/pip" install fastapi uvicorn websockets python-multipart

# ─── 4. Copy backend code ─────────────────────────────
echo "[4/6] Deploying backend..."
mkdir -p "$PI_BACKEND"
mkdir -p "$PHANTOM_DIR/uploads"
cp -r "$(dirname "$0")/"*.py "$PI_BACKEND/"
cp "$(dirname "$0")/start.sh" "$PI_BACKEND/"
chmod +x "$PI_BACKEND/start.sh"

# ─── 5. Install systemd service ───────────────────────
echo "[5/6] Installing systemd service..."
sudo cp "$(dirname "$0")/phantom-controller.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable phantom-controller
sudo systemctl start phantom-controller

# ─── 6. Verify ────────────────────────────────────────
echo "[6/6] Verifying..."
sleep 2
if sudo systemctl is-active --quiet phantom-controller; then
    echo ""
    echo "══════════════════════════════════════════"
    echo "  PHANTOM CONTROLLER — ONLINE"
    echo "══════════════════════════════════════════"
    echo "  Backend:  http://$(hostname -I | awk '{print $1}'):8080"
    echo "  WebSocket: ws://$(hostname -I | awk '{print $1}'):8080/ws"
    echo "  Status:   sudo systemctl status phantom-controller"
    echo "  Logs:     journalctl -u phantom-controller -f"
    echo "══════════════════════════════════════════"
else
    echo "ERROR: Service failed to start. Check: journalctl -u phantom-controller"
fi
