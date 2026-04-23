# Quick Start Guide

Get transmitting in 5 minutes!

## Prerequisites
- VoidCastFM installed on Mac
- Backend running on Raspberry Pi
- Both devices on same network

## Step 1: Launch and Connect

1. Open **VoidCastFM** from Applications
2. Check the **LINK** indicator (bottom right):
   - 🟢 **CONNECTED** - Ready to transmit
   - 🔴 **DISCONNECTED** - Click ⚙️ Settings to configure

## Step 2: Configure Frequency

1. In the **TRANSMIT** panel (left column)
2. Enter frequency in the input box or use slider
3. Select modulation mode: **FM**, **AM**, **SSB**, etc.
4. Optional: Add RDS text for FM broadcasts

## Step 3: Start Transmitting

1. Click **▶ START** button
2. Status changes to **TX LIVE** (top right)
3. Waveform and waterfall displays show activity
4. Click **■ STOP** to end transmission

## Step 4: Try the Soundboard

1. Scroll to **SOUNDBOARD** panel
2. Select frequency (default: 434 MHz)
3. Click an alert tone:
   - 🌪️ **Tornado Siren**
   - ✈️ **Air Raid Siren**
   - 📢 **EAS Attention**

## Step 5: Play Audio Files

1. Go to **FILE PLAYER** panel
2. Drag & drop audio file or click "browse"
3. Select frequency and mode
4. Click **▶ PLAY FILE**

## Common First Transmissions

### FM Broadcast Test
```
Frequency: 97.3 MHz (or any FM broadcast frequency)
Mode: FM
RDS PS: VoidCast
RDS RT: Test transmission
Power: 1
```

### Amateur Radio (Requires License!)
```
Frequency: 144.200 MHz (2m band)
Mode: FM
Power: 1
```

### ISM Band Testing (No License Required)
```
Frequency: 434.000 MHz
Mode: FM
Power: 1
```

## Tips

- ⚠️ **Always** ensure you're licensed for the frequency
- Start with low power (power=1) for testing
- Use the waterfall display to monitor your transmission
- Check system temperature during extended use

## Next Steps

- **[Transmission Modes](modes.md)** - Learn about different modulation types
- **[Audio Streaming](streaming.md)** - Stream live audio
- **[Advanced Configuration](configuration.md)** - Fine-tune settings

---

**⚠️ Legal Notice:** Only transmit on frequencies you are licensed to use. Unauthorized transmission may be illegal in your jurisdiction.
