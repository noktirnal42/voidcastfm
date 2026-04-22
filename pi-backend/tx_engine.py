"""
PHANTOM CONTROLLER — TX Engine
Manages rpitx subprocess lifecycle for all transmission modes.
"""

import subprocess
import os
import time
import signal
import threading
from typing import Optional


class TXEngine:
    def __init__(self, rpitx_path: str, sendiq_path: str, pifmrds_path: str):
        self.rpitx_path = rpitx_path
        self.sendiq_path = sendiq_path
        self.pifmrds_path = pifmrds_path

        self.proc: Optional[subprocess.Popen] = None
        self.audio_proc: Optional[subprocess.Popen] = None
        self.nc_proc: Optional[subprocess.Popen] = None

        self.current_freq: int = 0
        self.current_mode: str = "idle"
        self.is_running: bool = False
        self.start_time: float = 0
        self._lock = threading.Lock()

    def start(self, freq: int, mode: str, power: int = 1, ppm: int = 0,
              rds_ps: str = None, rds_rt: str = None) -> dict:
        """Start transmission in the given mode."""
        self.stop()

        with self._lock:
            try:
                mode_lower = mode.lower()

                if mode_lower == "fm" and (rds_ps or rds_rt):
                    # FM with RDS using pifmrds (frequency in MHz for pifmrds)
                    freq_mhz = freq / 1e6
                    cmd = ["sudo", self.pifmrds_path, "-freq", str(freq_mhz), "-pi", "0x0001"]
                    if rds_ps:
                        cmd.extend(["-ps", rds_ps[:8]])
                    if rds_rt:
                        cmd.extend(["-rt", rds_rt[:64]])
                    if ppm:
                        cmd.extend(["-ppm", str(ppm)])
                    self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                                  stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.DEVNULL)

                elif mode_lower in ("fm", "am", "ssb", "vfo", "chirp"):
                    # Standard rpitx modes — frequency in kHz
                    # Don't pass -p when ppm is 0 (rpitx rejects "-p 0" and "-p 0.0")
                    mode_map = {
                        "fm": "fm",
                        "am": "am",
                        "ssb": "ssb",
                        "vfo": "VFO",
                        "chirp": "chirp",
                    }
                    rpitx_mode = mode_map.get(mode_lower, mode)
                    freq_khz = freq / 1000.0
                    cmd = ["sudo", self.rpitx_path, "-m", rpitx_mode,
                           "-f", str(freq_khz)]
                    if ppm != 0:
                        cmd.extend(["-p", str(float(ppm))])
                    self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                                  stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.DEVNULL)

                elif mode_lower == "iq":
                    return self.start_iq_listener(freq=freq)

                else:
                    return {"status": "error", "message": f"Unknown mode: {mode}"}

                self.current_freq = freq
                self.current_mode = mode_lower
                self.is_running = True
                self.start_time = time.time()

                return {
                    "status": "started",
                    "freq": freq,
                    "mode": mode_lower,
                    "power": power,
                }

            except Exception as e:
                return {"status": "error", "message": str(e)}

    def stop(self) -> dict:
        """Stop all running transmission processes."""
        with self._lock:
            # Kill main TX process
            if self.proc and self.proc.poll() is None:
                try:
                    self.proc.send_signal(signal.SIGINT)
                    try:
                        self.proc.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        self.proc.kill()
                except ProcessLookupError:
                    pass

            # Kill audio process
            if self.audio_proc and self.audio_proc.poll() is None:
                try:
                    self.audio_proc.kill()
                except ProcessLookupError:
                    pass

            # Kill netcat process
            if self.nc_proc and self.nc_proc.poll() is None:
                try:
                    self.nc_proc.kill()
                except ProcessLookupError:
                    pass

            self.proc = None
            self.audio_proc = None
            self.nc_proc = None
            self.is_running = False

            prev_mode = self.current_mode
            self.current_mode = "idle"
            self.current_freq = 0

            return {"status": "stopped", "prev_mode": prev_mode}

    def play_file(self, file_path: str, freq: int, mode: str = "fm") -> dict:
        """Play an audio file via rpitx."""
        self.stop()

        with self._lock:
            try:
                freq_khz = freq / 1000.0
                if mode == "fm":
                    cmd = (f'ffmpeg -i "{file_path}" -f s16le -ar 44100 -ac 1 - '
                           f'| sudo {self.rpitx_path} -i - -m fm -f {freq_khz}')
                    self.proc = subprocess.Popen(cmd, shell=True,
                                                  stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.DEVNULL)
                elif mode == "ssb":
                    cmd = (f'ffmpeg -i "{file_path}" -f s16le -ar 44100 -ac 1 - '
                           f'| sudo {self.rpitx_path} -i - -m ssb -f {freq_khz}')
                    self.proc = subprocess.Popen(cmd, shell=True,
                                                  stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.DEVNULL)
                elif mode == "am":
                    cmd = (f'ffmpeg -i "{file_path}" -f s16le -ar 44100 -ac 1 - '
                           f'| sudo {self.rpitx_path} -i - -m am -f {freq_khz}')
                    self.proc = subprocess.Popen(cmd, shell=True,
                                                  stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.DEVNULL)
                else:
                    return {"status": "error", "message": f"File playback not supported for mode: {mode}"}

                self.current_freq = freq
                self.current_mode = f"play_{mode}"
                self.is_running = True
                self.start_time = time.time()

                return {
                    "status": "playing",
                    "file": file_path,
                    "freq": freq,
                    "mode": mode,
                }

            except Exception as e:
                return {"status": "error", "message": str(e)}

    def start_audio_listener(self, freq: int, mode: str = "fm", port: int = 5000) -> dict:
        """Start a UDP listener that feeds audio to rpitx.
        Mac streams audio via: ffmpeg ... udp://pi0.local:<port>
        """
        self.stop()

        with self._lock:
            try:
                freq_khz = freq / 1000.0
                cmd = (f'nc -l -u {port} '
                       f'| sudo {self.rpitx_path} -i - -m {mode} -f {freq_khz}')
                self.proc = subprocess.Popen(cmd, shell=True,
                                              stdout=subprocess.DEVNULL,
                                              stderr=subprocess.DEVNULL)
                self.current_freq = freq
                self.current_mode = f"stream_{mode}"
                self.is_running = True
                self.start_time = time.time()

                return {
                    "status": "audio_listening",
                    "freq": freq,
                    "mode": mode,
                    "port": port,
                    "instruction": f"On Mac: ffmpeg -f avfoundation -i \":0\" -f s16le -ar 44100 -ac 1 udp://192.168.1.25:{port}",
                }

            except Exception as e:
                return {"status": "error", "message": str(e)}

    def start_iq_listener(self, freq: int, port: int = 8011, sample_rate: int = 48000) -> dict:
        """Start IQ stream listener — Mac sends IQ data to this port.
        sendiq uses Hz (not kHz) for frequency.
        """
        self.stop()

        with self._lock:
            try:
                cmd = (f'nc -l {port} '
                       f'| sudo {self.sendiq_path} -i - -s {sample_rate} -f {freq} -t iqfloat')
                self.proc = subprocess.Popen(cmd, shell=True,
                                              stdout=subprocess.DEVNULL,
                                              stderr=subprocess.DEVNULL)
                self.current_freq = freq
                self.current_mode = "iq"
                self.is_running = True
                self.start_time = time.time()

                return {
                    "status": "iq_listening",
                    "freq": freq,
                    "port": port,
                    "sample_rate": sample_rate,
                    "instruction": f"Send IQ data to 192.168.1.25:{port}",
                }

            except Exception as e:
                return {"status": "error", "message": str(e)}

    def get_status(self) -> dict:
        """Get current TX status."""
        elapsed = time.time() - self.start_time if self.is_running else 0
        proc_alive = self.proc is not None and self.proc.poll() is None if self.proc else False
        return {
            "is_running": self.is_running,
            "mode": self.current_mode,
            "freq": self.current_freq,
            "elapsed": round(elapsed, 1),
            "proc_alive": proc_alive,
        }
