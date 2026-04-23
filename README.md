# VoidCastFM

Professional SDR Transmitter Control Station for macOS and Raspberry Pi

## Features

- Multi-mode RF transmission (FM, AM, SSB, VFO, Chirp, IQ)
- Real-time system monitoring
- Emergency alert soundboard
- Live audio streaming
- File playback
- Modern dark theme UI

## Installation

### Requirements

**macOS:**
- macOS 12.0 or later
- Apple Silicon (M1/M2/M3) or Intel (x64)

**Raspberry Pi:**
- Raspberry Pi Zero W / Pi 3 / Pi 4 / Pi 5
- Raspbian 13 (Bookworm) or later
- Python 3.10+
- rpitx installed

### Quick Start

1. **Download** the latest release from [Releases](https://github.com/noktirnal42/voidcastfm/releases)
2. **Install** on Mac: Open DMG and drag to Applications
3. **Setup Pi**: Install backend on Raspberry Pi (see [Installation Guide](docs/installation.md))
4. **Configure**: Open VoidCastFM and click ⚙️ Settings to configure Pi connection
5. **Transmit**: Select frequency, mode, and start transmitting!

## Documentation

- **[Installation Guide](docs/installation.md)** - Setup instructions
- **[Configuration](docs/configuration.md)** - Settings and options
- **[User Guide](docs/usage.md)** - How to use all features
- **[API Reference](docs/api.md)** - Backend API documentation
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues

## Project Structure

```
VodCastFM/
├── mac-app/           # macOS Electron application
│   ├── src/          # Svelte 5 source code
│   ├── electron/     # Electron main process
│   └── public/       # Assets
├── pi-backend/       # Raspberry Pi backend
│   ├── server.py     # FastAPI server
│   ├── tx_engine.py  # RF transmission engine
│   └── tone_generator.py  # Alert tone synthesis
├── docs/             # Documentation
└── releases/         # Built releases
```

## Development

### Build from Source

```bash
# Clone repository
git clone https://github.com/noktirnal42/voidcastfm.git
cd voidcastfm

# Install Mac app dependencies
cd mac-app
npm install

# Development mode
npm run dev

# Build for production
npm run build

# Build DMG installer
npm run electron:build
```

### Pi Backend Setup

```bash
# On Raspberry Pi
cd pi-backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn websockets python-multipart

# Run server
python -m uvicorn server:app --host 0.0.0.0 --port 8080
```

## Brand Identity

### Colors
- **Primary Cyan**: `#00f5ff` - Main accent, buttons, highlights
- **Electric Purple**: `#8b5cf6` - Secondary accent, gradients
- **Deep Space**: `#08080f` - Background
- **Alert Red**: `#ff3c3c` - Warnings, stop actions

### Typography
- **Primary**: SF Mono (macOS system monospace)
- **Fallback**: JetBrains Mono, Fira Code

### Logo Concept
The VoidCastFM logo features a stylized radio wave emerging from a void, representing the transmission of signals from emptiness into reality.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details

## Disclaimer

This software is for **educational and amateur radio use only**. 

- Ensure compliance with local RF transmission laws and regulations
- Unauthorized transmission may be illegal in your jurisdiction
- Only transmit on frequencies you are licensed to use
- The authors are not responsible for misuse or legal violations

## Support

- **Issues**: [GitHub Issues](https://github.com/noktirnal42/voidcastfm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/noktirnal42/voidcastfm/discussions)
- **Documentation**: [Wiki](https://github.com/noktirnal42/voidcastfm/wiki)

## Acknowledgments

- **rpitx**: [https://github.com/F5OEO/rpitx](https://github.com/F5OEO/rpitx)
- **FastAPI**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Svelte 5**: [https://svelte.dev](https://svelte.dev)
- **Electron**: [https://www.electronjs.org](https://www.electronjs.org)

---

Built with ❤️ for the amateur radio community
