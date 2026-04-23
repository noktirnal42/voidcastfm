# Installation Guide

This guide covers installation of both the macOS application and Raspberry Pi backend.

## Prerequisites

### macOS Requirements
- macOS 12.0 (Monterey) or later
- 500 MB free disk space
- Administrator privileges for installation

### Raspberry Pi Requirements
- Raspberry Pi Zero W, Pi 3, Pi 4, or Pi 5
- Raspbian 13 (Bookworm) or later
- Python 3.10 or higher
- rpitx installed
- 200 MB free disk space
- Network connectivity (same network as Mac)

---

## Part 1: Install macOS Application

### Step 1: Download
Download the latest release from [GitHub Releases](https://github.com/noktirnal42/voidcastfm/releases):
- **Apple Silicon (M1/M2/M3)**: `VoidCastFM-1.0.0-macos-arm64.dmg`
- **Intel Macs**: `VoidCastFM-1.0.0-macos-x64.dmg`

### Step 2: Install
1. Open the downloaded `.dmg` file
2. Drag **VoidCastFM** to your Applications folder
3. Launch from Applications folder

### Step 3: First Launch
On first launch, macOS may show a security warning:
1. Click "Cancel" if shown
2. Go to **System Preferences → Security & Privacy**
3. Click "Open Anyway" next to VoidCastFM
4. Confirm by clicking "Open"

---

## Part 2: Install Raspberry Pi Backend

### Step 1: Install rpitx

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install dependencies
sudo apt install -y libuwifi0 libfftw3-bin libfftw3-dev libfftw3-doc \
    python3-dev python3-pip python3-setuptools git build-essential

# Clone and build rpitx
cd ~
git clone https://github.com/F5OEO/rpitx
cd rpitx
sudo ./install.sh
```

### Step 2: Install Python Backend

```bash
# Create directory
mkdir -p ~/voidcastfm
cd ~/voidcastfm

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn websockets python-multipart

# Download backend files
cd ~/voidcastfm
# Copy files from: pi-backend/ directory in this repository
```

### Step 3: Create System Service

```bash
# Create systemd service
sudo nano /etc/systemd/system/voidcastfm.service
```

Paste the following:
```ini
[Unit]
Description=VoidCastFM Backend
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/voidcastfm
ExecStart=/home/pi/voidcastfm/venv/bin/python -m uvicorn server:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable voidcastfm
sudo systemctl start voidcastfm
sudo systemctl status voidcastfm
```

---

## Part 3: Configure Connection

### Step 1: Find Pi IP Address
```bash
# On Raspberry Pi
hostname -I
```

### Step 2: Configure Mac App
1. Open VoidCastFM on Mac
2. Click **⚙️ Settings** (top right)
3. Enter:
   - **Pi Hostname/IP**: Your Pi's IP address (e.g., `192.168.1.25`)
   - **Port**: `8080` (default)
   - **SSH Username**: `pi` (or your username)
4. Click **Test Connection**
5. Click **Save Settings**

### Step 3: Verify Connection
The main dashboard should now show:
- **LINK**: CONNECTED
- **TX**: STANDBY
- System stats from Pi (CPU temp, load, etc.)

---

## Verification

Test your installation:

1. **Basic Test**: Click "START" on the dashboard - rpitx should activate
2. **Soundboard Test**: Try playing the tornado siren alert
3. **File Test**: Upload a short audio file and play it

---

## Next Steps

- **[Quick Start Guide](quickstart.md)** - Learn basic operation
- **[Configuration](configuration.md)** - Advanced settings
- **[Troubleshooting](troubleshooting.md)** - If you encounter issues

---

**Having issues?** Check the [Troubleshooting Guide](troubleshooting.md) or open an issue on [GitHub](https://github.com/noktirnal42/voidcastfm/issues).
