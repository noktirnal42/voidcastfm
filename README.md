# VoidCastFM - SDR Transmitter Control Station

A professional-grade SDR (Software Defined Radio) transmitter control application for macOS that controls a Raspberry Pi running rpitx for RF transmission.

## Features

- **Multiple Modulation Modes**: FM, AM, SSB, VFO, Chirp, and IQ
- **Soundboard**: Pre-loaded emergency alert tones (Tornado Siren, Air Raid Siren, FEMA EAS)
- **File Playback**: Upload and transmit audio files
- **Live Microphone Streaming**: Stream microphone audio over RF
- **System Audio Playback**: Capture and stream Mac system audio
- **Real-time Monitoring**: CPU temp, load, memory, disk usage
- **WebSocket Status**: Live status updates every 2 seconds

## Architecture

``
┌─────────────────┐      REST/WebSocket     ┌──────────────────┐
│  macOS App      │ ◄─────────────────────► │  Raspberry Pi    │
│  (Electron +    │                         │  (FastAPI +      │
│   Svelte 5)     │                         │   rpitx)         │
└─────────────────┘                         └──────────────────┘
         │                                         │
         │                                         ▼
         │                                ┌──────────────────┐
         │                                │  rpitx binary    │
         │                                │  (RF Transmit)   │
         │                                └──────────────────┘
         ▼
   User Interface
   - Frequency control
   - Mode selection
   - Soundboard
   - File upload
   - Live streaming
```

## Project Structure

```
VodCastFM/
├── mac-app/              # macOS Electron application
│   ├── src/             # Svelte 5 source code
│   │   ├── components/  # UI components
│   │   ├── lib/         # Utilities and API client
│   │   └── App.svelte   # Main app component
│   ├── electron/        # Electron main process
│   ├── public/          # Static assets
│   ├── package.json
│   └── vite.config.js
│
├── pi-backend/          # Raspberry Pi backend
│   ├── server.py        # FastAPI server
│   ├── tx_engine.py     # rpitx transmission engine
│   ├── system_monitor.py # System resource monitoring
│   ├── tone_generator.py # Alert tone synthesis
│   ├── start.sh         # Startup script
│   └── phantom-controller.service # systemd service
│
└── README.md
```

## Installation

### Prerequisites

- **Mac**: macOS 12.0+ (Apple Silicon or Intel)
- **Pi**: Raspberry Pi Zero W / Pi 3/4/5 with Raspbian 13+

### Pi Setup

1. Install rpitx on your Raspberry Pi
2. Copy `pi-backend/` to the Pi
3. Install dependencies:
   ```bash
   cd /home/pi/phantom
   python -m pip install fastapi uvicorn websockets python-multipart
   ```
4. Install systemd service:
   ```bash
   sudo cp phantom-controller.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable phantom-controller
   sudo systemctl start phantom-controller
   ```

### Mac App

1. Download the latest DMG from Releases
2. Drag to Applications folder
3. Open and configure Pi connection in Settings

## Configuration

The app requires connection details for your Raspberry Pi:

- **Host**: IP address or hostname (e.g., `192.168.1.25` or `pi0.local`)
- **Port**: Default `8080`
- **SSH Username**: For remote management (optional)

These are configured in the app's Settings panel.

## Development

### Mac App

```bash
cd mac-app
npm install
npm run dev          # Start Vite dev server
npm run electron:dev # Start Electron with hot reload
npm run build        # Build for production
npm run electron:build # Build DMG installer
```

### Pi Backend

```bash
cd pi-backend
python -m uvicorn server:app --host 0.0.0.0 --port 8080 --reload
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/status` | GET | Full system status |
| `/tx/start` | POST | Start transmission |
| `/tx/stop` | POST | Stop transmission |
| `/tx/play_file` | POST | Upload and play audio file |
| `/soundboard/tones` | GET | List available alert tones |
| `/soundboard/play/{tone_id}` | POST | Play alert tone |
| `/stream/audio/start` | POST | Start audio stream listener |
| `/stream/audio/stop` | POST | Stop audio stream |
| `/system` | GET | System resource info |
| `/ws` | WebSocket | Real-time status updates |

## Security Notes

- **No hardcoded credentials**: All connection details are user-provided
- **Local network only**: Designed for isolated LAN use
- **SSH keys recommended**: Use SSH key authentication for Pi access
- **Firewall your Pi**: Only expose necessary ports (8080)

## License

MIT License - see LICENSE file

## Disclaimer

This software is for educational and amateur radio use only. Ensure compliance with local RF transmission laws and regulations. Unauthorized transmission may be illegal.
