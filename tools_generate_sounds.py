"""
Generates placeholder .wav sound files using Python's built-in `wave`
and `math` modules (no external audio assets/licensing needed).
Swap these for real recorded/sourced tones before shipping (PDR 7.4).
"""
import math
import struct
import wave

SAMPLE_RATE = 44100


def tone(freq, duration, volume=0.5, fade=0.02):
    n = int(SAMPLE_RATE * duration)
    fade_n = int(SAMPLE_RATE * fade)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        amp = volume
        if i < fade_n:
            amp *= i / fade_n
        elif i > n - fade_n:
            amp *= (n - i) / fade_n
        samples.append(amp * math.sin(2 * math.pi * freq * t))
    return samples


def chord(freqs, duration, volume=0.4, fade=0.02):
    parts = [tone(f, duration, volume / len(freqs), fade) for f in freqs]
    return [sum(vals) for vals in zip(*parts)]


def silence(duration):
    return [0.0] * int(SAMPLE_RATE * duration)


def write_wav(path, samples):
    samples = [max(-1.0, min(1.0, s)) for s in samples]
    frames = b"".join(struct.pack("<h", int(s * 32767)) for s in samples)
    with wave.open(path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(frames)


def gentle_bell():
    # Soft repeating bell-like chord, 3 pulses
    out = []
    for _ in range(3):
        out += chord([880, 1320], 0.35, volume=0.35)
        out += silence(0.25)
    return out


def classic_alarm():
    # Two-tone alternating beep, classic alarm clock feel
    out = []
    for _ in range(4):
        out += tone(1000, 0.18, volume=0.5)
        out += tone(800, 0.18, volume=0.5)
    return out


def upbeat_chime():
    # Ascending major triad arpeggio, repeated twice
    notes = [523, 659, 784, 1046]  # C5 E5 G5 C6
    out = []
    for _ in range(2):
        for f in notes:
            out += tone(f, 0.14, volume=0.4)
        out += silence(0.15)
    return out


def success_chime():
    # Short bright two-note "ding-ding"
    out = tone(1046, 0.12, volume=0.5) + tone(1318, 0.18, volume=0.5)
    return out


if __name__ == "__main__":
    write_wav("assets/gentle_bell.wav", gentle_bell())
    write_wav("assets/classic_alarm.wav", classic_alarm())
    write_wav("assets/upbeat_chime.wav", upbeat_chime())
    write_wav("assets/success_chime.wav", success_chime())
    print("wrote 4 placeholder .wav files to assets/")
