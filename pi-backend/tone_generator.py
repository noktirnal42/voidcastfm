"""
PHANTOM CONTROLLER — Alert Tone Generator
Synthesizes standard alert tones as WAV files for RF broadcast.
Uses only stdlib + wave module (no numpy/scipy needed on Pi Zero W).
"""

import math
import struct
import wave
import os

SAMPLE_RATE = 44100
TONE_DIR = os.path.join(os.path.dirname(__file__), "tones")
os.makedirs(TONE_DIR, exist_ok=True)


def _write_wav(filename, samples, sr=SAMPLE_RATE):
    """Write a list of float [-1.0, 1.0] samples to a 16-bit WAV file."""
    path = os.path.join(TONE_DIR, filename)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            wf.writeframes(struct.pack("<h", int(clamped * 32767)))
    return path


def _synth(samples, sr=SAMPLE_RATE):
    """Helper: generate sample index array."""
    return range(len(samples))


def generate_tornado_siren(duration=30.0):
    """
    Generate a US tornado siren tone.
    Real tornado sirens alternate between two tones (typically ~460Hz and ~580Hz)
    in a slow cycle (~6-8 seconds per sweep), with a characteristic rising/falling
    pitch pattern. The 'Federal Signal' style uses a slow up/down wail.
    """
    n_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * n_samples
    
    # Tornado siren: slow wail cycling between 460-580 Hz over ~7s period
    wail_period = 7.0  # seconds for one full up-down cycle
    f_lo = 460.0
    f_hi = 580.0
    
    phase = 0.0
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # Triangle wave modulation for the wail (smooth up and down)
        cycle_pos = (t % wail_period) / wail_period  # 0..1
        # Triangle wave: 0->1->0 over one period
        if cycle_pos < 0.5:
            mod = cycle_pos * 2.0  # 0..1
        else:
            mod = (1.0 - cycle_pos) * 2.0  # 1..0
        
        freq = f_lo + (f_hi - f_lo) * mod
        
        # FM synthesis: accumulate phase
        phase += 2.0 * math.pi * freq / SAMPLE_RATE
        samples[i] = 0.85 * math.sin(phase)
    
    path = _write_wav("tornado_siren.wav", samples)
    print(f"Generated tornado siren: {path} ({duration}s)")
    return path


def generate_air_raid_siren(duration=20.0):
    """
    Generate a WWII-style air raid siren.
    These use a sharp rising tone (typically 400Hz→900Hz over ~4s)
    then a sharp falling tone (900Hz→400Hz over ~4s), repeated.
    Very distinctive urgent sweep pattern.
    """
    n_samples = int(SAMPLE_RATE * duration)
    samples = [0.0] * n_samples
    
    sweep_period = 8.0  # 4s up + 4s down
    f_lo = 400.0
    f_hi = 900.0
    
    phase = 0.0
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        cycle_pos = (t % sweep_period) / sweep_period  # 0..1
        
        if cycle_pos < 0.5:
            # Rising sweep
            mod = cycle_pos * 2.0  # 0..1
        else:
            # Falling sweep
            mod = (1.0 - cycle_pos) * 2.0  # 1..0
        
        # Exponential curve for more realistic siren sound
        freq = f_lo + (f_hi - f_lo) * (mod ** 0.7)
        
        phase += 2.0 * math.pi * freq / SAMPLE_RATE
        samples[i] = 0.90 * math.sin(phase)
    
    path = _write_wav("air_raid_siren.wav", samples)
    print(f"Generated air raid siren: {path} ({duration}s)")
    return path


def generate_eas_tone(duration=8.0):
    """
    Generate the official USA FEMA EAS (Emergency Alert System) attention tone.
    The EAS uses a dual-tone attention signal: 853 Hz + 960 Hz simultaneously,
    followed by the three EAS data bursts (header codes).
    We generate the classic dual-tone attention signal that everyone recognizes.
    """
    # Attention signal: 853Hz + 960Hz for ~8 seconds (typically 8-25s)
    n_att = int(SAMPLE_RATE * duration)
    samples = [0.0] * n_att
    
    for i in range(n_att):
        t = i / SAMPLE_RATE
        # Two tones mixed at equal amplitude
        tone1 = math.sin(2.0 * math.pi * 853.0 * t)
        tone2 = math.sin(2.0 * math.pi * 960.0 * t)
        # Mix at 0.5 each, with 0.9 master level
        samples[i] = 0.9 * 0.5 * (tone1 + tone2)
        
        # Add a sharp fade-in (0.05s) and fade-out (0.1s) to avoid clicks
        fade_in = min(1.0, t / 0.05)
        fade_out = min(1.0, (duration - t) / 0.1)
        samples[i] *= fade_in * fade_out
    
    path = _write_wav("eas_attention.wav", samples)
    print(f"Generated EAS attention tone: {path} ({duration}s)")
    return path


def generate_all():
    """Generate all alert tones. Returns dict of name -> filepath."""
    tones = {}
    tones["tornado_siren"] = generate_tornado_siren()
    tones["air_raid_siren"] = generate_air_raid_siren()
    tones["eas_attention"] = generate_eas_tone()
    return tones


if __name__ == "__main__":
    tones = generate_all()
    print(f"\nAll tones generated in: {TONE_DIR}")
    for name, path in tones.items():
        size = os.path.getsize(path)
        print(f"  {name}: {path} ({size} bytes)")
