# VoidCastFM v1.0.0 Release

**Build Date:** 2026-04-22  
**Platform:** macOS (Apple Silicon & Intel)  
**Status:** ✅ Production Ready

## Downloads

| Platform | File | Size | SHA256 |
|----------|------|------|--------|
| Apple Silicon (M1/M2/M3) | VoidCastFM-1.0.0-macos-arm64.dmg | 101 MB | `eb55dd118c...` |
| Intel Macs | VoidCastFM-1.0.0-macos-x64.dmg | 107 MB | `f1b4a460ec...` |

## Installation

1. Download the appropriate DMG for your Mac
2. Open the DMG file
3. Drag VoidCastFM to Applications folder
4. Launch from Applications

## First Use

1. Open VoidCastFM
2. Click ⚙️ **Settings** (top right)
3. Enter your Raspberry Pi details:
   - **Host:** IP or hostname (e.g., `192.168.1.25` or `pi0.local`)
   - **Port:** `8080` (default)
   - **SSH User:** `pi` (or your username)
4. Click **Test Connection**
5. Click **Save Settings**

## What's New

- ✅ **Security First:** No hardcoded credentials - all connection details user-configurable
- ✅ **Settings UI:** New modal for configuring Pi connection
- ✅ **Renamed:** PHANTOM CONTROLLER → VoidCastFM
- ✅ **Git Best Practices:** Proper .gitignore, comprehensive README
- ✅ **Signed Builds:** Developer ID signed for macOS

## Requirements

- **macOS:** 12.0+ (Apple Silicon or Intel)
- **Pi Backend:** Raspberry Pi with rpitx and VoidCastFM backend service

## Known Issues

- Svelte A11Y warnings in dev console (non-blocking, will fix in v1.0.1)

## Support

Report issues on GitHub: https://github.com/yourorg/voidcastfm/issues

---
**SHA256 Checksums:**
- ARM64: `eb55dd118c5993bdf86155d314b428ca7789d836772f104efe6c12b9bf8cba4b`
- X64: `f1b4a460ecc2ab1ab56d6bcb47d40a2c663b2b3e6725c3ece1261524d5ca3bce`
