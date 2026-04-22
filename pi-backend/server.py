"""
PHANTOM CONTROLLER — Pi Backend Server
FastAPI + WebSocket server for RF transmission control
Runs on Raspberry Pi Zero W at pi0.local:8080
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
import asyncio
import json
import os
import time
import subprocess
import signal
import threading
from pathlib import Path
from typing import Optional

from tx_engine import TXEngine
from system_monitor import SystemMonitor
from tone_generator import generate_all, TONE_DIR

# ─── Config ───────────────────────────────────────────
RPITX_PATH = "/home/noktirnal/rpitx"
RPITX_BIN = f"{RPITX_PATH}/rpitx"
SENDIQ_BIN = f"{RPITX_PATH}/sendiq"
PIFM_BIN = f"{RPITX_PATH}/pifmrds"
UPLOAD_DIR = Path("/home/noktirnal/phantom/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ─── Lifespan (replaces deprecated on_event) ──────────
@asynccontextmanager
async def lifespan(app):
    asyncio.create_task(status_pusher())
    yield

# ─── App ──────────────────────────────────────────────
app = FastAPI(title="Phantom Controller Pi Backend", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Engine + Monitor ─────────────────────────────────
tx = TXEngine(rpitx_path=RPITX_BIN, sendiq_path=SENDIQ_BIN, pifmrds_path=PIFM_BIN)
monitor = SystemMonitor()

# ─── Connected WebSocket clients ──────────────────────
ws_clients: list[WebSocket] = []

# ─── Models ───────────────────────────────────────────
class TXParams(BaseModel):
    freq: int          # Hz
    mode: str          # fm | am | ssb | iq | vfo | chirp
    power: Optional[int] = 1
    ppm: Optional[int] = 0
    rds_ps: Optional[str] = None
    rds_rt: Optional[str] = None

class IQParams(BaseModel):
    freq: int
    sample_rate: int = 48000
    port: int = 8011

# ─── REST API ─────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "name": "Phantom Controller",
        "version": "1.0.0",
        "status": "online",
        "rpitx_available": os.path.exists(RPITX_BIN),
    }

@app.get("/status")
async def get_status():
    """Full system status."""
    return {
        "tx": tx.get_status(),
        "system": monitor.get_snapshot(),
        "rpitx_available": os.path.exists(RPITX_BIN),
        "uptime": time.time() - monitor.start_time,
    }

@app.post("/tx/start")
async def start_tx(params: TXParams):
    """Start RF transmission."""
    if tx.is_running:
        tx.stop()
        await asyncio.sleep(0.3)

    result = tx.start(
        freq=params.freq,
        mode=params.mode,
        power=params.power,
        ppm=params.ppm,
        rds_ps=params.rds_ps,
        rds_rt=params.rds_rt,
    )
    await broadcast_status()
    return result

@app.post("/tx/stop")
async def stop_tx():
    """Stop all RF transmission."""
    result = tx.stop()
    await broadcast_status()
    return result

@app.post("/tx/play_file")
async def play_file(file: UploadFile = File(...), freq: int = 100000000, mode: str = "fm"):
    """Upload and play an audio file via RF."""
    # Save uploaded file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Stop any running transmission
    if tx.is_running:
        tx.stop()
        await asyncio.sleep(0.3)

    result = tx.play_file(str(file_path), freq=freq, mode=mode)
    await broadcast_status()
    return {"status": "playing", "file": file.filename, "freq": freq, "mode": mode}

@app.post("/tx/iq/start")
async def start_iq(params: IQParams):
    """Start IQ stream listener on the Pi."""
    if tx.is_running:
        tx.stop()
        await asyncio.sleep(0.3)

    result = tx.start_iq_listener(freq=params.freq, port=params.port, sample_rate=params.sample_rate)
    await broadcast_status()
    return result

@app.post("/tx/iq/stop")
async def stop_iq():
    """Stop IQ stream."""
    result = tx.stop()
    await broadcast_status()
    return result

@app.get("/system")
async def get_system():
    """System resource monitor."""
    return monitor.get_snapshot()

@app.get("/system/thermal")
async def get_thermal():
    """Pi thermal data."""
    return monitor.get_thermal()

@app.post("/system/reboot")
async def reboot_pi():
    """Reboot the Pi (requires sudo)."""
    subprocess.Popen(["sudo", "reboot"], start_new_session=True)
    return {"status": "rebooting"}

# ─── Audio Stream Endpoint ────────────────────────────

@app.post("/stream/audio/start")
async def start_audio_stream(freq: int = 100000000, mode: str = "fm", port: int = 5000):
    """Start audio stream receiver on Pi — Mac sends UDP audio to this port."""
    if tx.is_running:
        tx.stop()
        await asyncio.sleep(0.3)

    result = tx.start_audio_listener(freq=freq, mode=mode, port=port)
    await broadcast_status()
    return result

@app.post("/stream/audio/stop")
async def stop_audio_stream():
    """Stop audio stream receiver."""
    result = tx.stop()
    await broadcast_status()
    return result

# ─── Soundboard Endpoints ─────────────────────────────

@app.get("/soundboard/tones")
async def list_tones():
    """List available pre-generated alert tones."""
    tone_dir = Path(TONE_DIR)
    tones = {}
    
    # Generate tones if they don't exist
    if not tone_dir.exists() or not list(tone_dir.glob("*.wav")):
        generate_all()
    
    # Build tone info dict
    tone_info = {
        "tornado_siren": {
            "name": "Tornado Siren",
            "description": "US Federal Signal-style tornado warning siren",
            "icon": "🌪️",
            "color": "#ff3c3c",
        },
        "air_raid_siren": {
            "name": "Air Raid Siren",
            "description": "WWII-style air raid warning siren",
            "icon": "✈️",
            "color": "#ff8c00",
        },
        "eas_attention": {
            "name": "EAS Attention",
            "description": "Official FEMA EAS dual-tone attention signal",
            "icon": "📢",
            "color": "#00f5ff",
        },
    }
    
    for name, info in tone_info.items():
        wav_path = tone_dir / f"{name}.wav"
        if wav_path.exists():
            tones[name] = {
                **info,
                "id": name,
                "duration": 30 if "siren" in name else 8,
                "path": str(wav_path),
                "exists": True,
            }
    
    return {"tones": tones, "tone_dir": str(tone_dir)}


@app.post("/soundboard/play/{tone_id}")
async def play_tone(tone_id: str, freq: int = 100000000, mode: str = "fm"):
    """Play a pre-generated alert tone via RF."""
    tone_dir = Path(TONE_DIR)
    wav_path = tone_dir / f"{tone_id}.wav"
    
    # Auto-generate if missing
    if not wav_path.exists():
        if tone_id in ["tornado_siren", "air_raid_siren", "eas_attention"]:
            from tone_generator import generate_tornado_siren, generate_air_raid_siren, generate_eas_tone
            generators = {
                "tornado_siren": generate_tornado_siren,
                "air_raid_siren": generate_air_raid_siren,
                "eas_attention": generate_eas_tone,
            }
            generators[tone_id]()
        else:
            raise HTTPException(status_code=404, detail=f"Tone '{tone_id}' not found")
    
    if not wav_path.exists():
        raise HTTPException(status_code=500, detail=f"Failed to generate tone '{tone_id}'")
    
    # Stop any running transmission
    if tx.is_running:
        tx.stop()
        await asyncio.sleep(0.3)
    
    # Play the tone file
    result = tx.play_file(str(wav_path), freq=freq, mode=mode)
    await broadcast_status()
    
    return {
        "status": "playing",
        "tone": tone_id,
        "freq": freq,
        "mode": mode,
        **result,
    }


@app.post("/soundboard/stop")
async def stop_soundboard():
    """Stop any playing soundboard tone."""
    result = tx.stop()
    await broadcast_status()
    return result


# ─── WebSocket ────────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    ws_clients.append(ws)
    try:
        # Send initial status
        await ws.send_json({
            "type": "status",
            "tx": tx.get_status(),
            "system": monitor.get_snapshot(),
        })
        # Keep alive — listen for commands
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            cmd = msg.get("cmd")

            if cmd == "start":
                result = tx.start(
                    freq=msg.get("freq", 100000000),
                    mode=msg.get("mode", "fm"),
                    power=msg.get("power", 1),
                    ppm=msg.get("ppm", 0),
                )
                await ws.send_json({"type": "cmd_result", "cmd": "start", **result})

            elif cmd == "stop":
                result = tx.stop()
                await ws.send_json({"type": "cmd_result", "cmd": "stop", **result})

            elif cmd == "status":
                await ws.send_json({
                    "type": "status",
                    "tx": tx.get_status(),
                    "system": monitor.get_snapshot(),
                })

    except WebSocketDisconnect:
        ws_clients.remove(ws)

async def broadcast_status():
    """Push status to all connected WebSocket clients."""
    status = {
        "type": "status_update",
        "tx": tx.get_status(),
        "system": monitor.get_snapshot(),
    }
    dead = []
    for ws in ws_clients:
        try:
            await ws.send_json(status)
        except:
            dead.append(ws)
    for ws in dead:
        ws_clients.remove(ws)

# ─── Background Status Push ───────────────────────────

async def status_pusher():
    """Push system stats to all WS clients every 2 seconds."""
    while True:
        await asyncio.sleep(2)
        if ws_clients:
            await broadcast_status()

# ─── Run ──────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
