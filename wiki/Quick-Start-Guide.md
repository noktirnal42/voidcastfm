# Quick Start Guide

Get transmitting in 5 minutes! This guide will help you set up VoidCastFM and make your first transmission.

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **macOS 12.0+** (Monterey or later)
- [ ] **Raspberry Pi** (Zero W, Pi 3/4/5) with Raspbian 13+
- [ ] **rpitx** installed on Pi
- [ ] **Network connection** - Both devices on same network
- [ ] **Python 3.10+** on Pi

---

## Step 1: Install VoidCastFM (2 minutes)

### On macOS:
1. Download latest release from [GitHub Releases](https://github.com/noktirnal42/voidcastfm/releases)
2. Open the `.dmg` file
3. Drag **VoidCastFM** to Applications folder
4. Launch from Applications

> **Note:** On first launch, macOS may show a security warning. Go to System Preferences → Security & Privacy and click "Open Anyway"

---

## Step 2: Configure Connection (1 minute)

1. Open **VoidCastFM** on your Mac
2. Click the **⚙️ Settings** button (top right corner)
3. Enter your Raspberry Pi details:
   - **Pi Hostname/IP**: e.g., `192.168.1.25` or `pi0.local`
   - **Port**: `8080` (default)
   - **SSH Username**: `pi` (or your username)
4. Click **"Test Connection"** - should show green checkmark
5. Click **"Save Settings"**

### Find Your Pi's IP Address:
```bash
# On Raspberry Pi terminal
hostname -I
```

---

## Step 3: Your First Transmission (2 minutes)

### Basic FM Test:
1. In the **TRANSMIT** panel (left column)
2. Set frequency to **434.000 MHz** (ISM band - no license required for testing)
3. Select mode: **FM**
4. Power: **1**
5. Click **▶ START**

You should see:
- Status changes to **TX LIVE** (top right)
- Waveform display shows activity
- Waterfall display shows spectrum
- System panel shows Pi CPU activity

6. Click **■ STOP** to end transmission

---

## Step 4: Try the Soundboard (Optional)

Test the emergency alert system:

1. Scroll to **SOUNDBOARD** panel
2. Frequency: **434.000 MHz**
3. Click **🌪️ Tornado Siren**
4. Listen on an FM radio tuned to the right frequency!

---

## Common First Transmissions

### ISM Band Test (No License Required)
```
Frequency: 434.000 MHz
Mode: FM
Power: 1
Duration: Test only (few seconds)
```

### FM Broadcast (License Required)
```
Frequency: 97.300 MHz (or any unused FM frequency)
Mode: FM
RDS PS: VoidCast
RDS RT: Test transmission
Power: 1
```

### Amateur Radio 2m Band (License Required)
```
Frequency: 144.200 MHz
Mode: FM
Power: 1
```

---

## Troubleshooting

### "NO LINK" or "DISCONNECTED"
- Click ⚙️ Settings
- Verify Pi IP address is correct
- Check both devices on same network
- Click "Test Connection"

### Transmission not starting
- Check Pi is running backend service: `sudo systemctl status voidcastfm`
- Verify rpitx is installed: `which rpitx`
- Check firewall allows port 8080

### Can't hear anything
- Use an FM radio to receive transmissions
- Tune radio to same frequency as transmission
- Check antenna is connected to Pi

---

## Next Steps

Now that you're transmitting, explore:

- **[Transmission Modes](Transmission-Modes)** - Learn FM, AM, SSB, VFO, IQ
- **[Audio Streaming](Audio-Streaming)** - Stream live microphone audio
- **[File Playback](File-Playback)** - Play audio files over RF
- **[Soundboard Guide](Soundboard)** - Emergency alert tones

---

## ⚠️ Legal Notice

**Always comply with local laws and regulations:**

- Only transmit on frequencies you are licensed to use
- ISM bands (433.92 MHz, 915 MHz) are generally open for testing
- FM broadcast band (88-108 MHz) requires appropriate licensing
- Amateur radio bands require amateur radio license
- Unauthorized transmission may be illegal in your jurisdiction

**When in doubt, consult your national radio communications authority.**

---

## Getting Help

- **[Full Documentation](https://noktirnal42.github.io/voidcastfm/)**
- **[Wiki Home](Home)**
- **[GitHub Issues](https://github.com/noktirnal42/voidcastfm/issues)**
- **[Discussions](https://github.com/noktirnal42/voidcastfm/discussions)**

---

**Happy transmitting! 📡**
