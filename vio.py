
import time
import threading

import numpy as np
import serial
import sounddevice as sd

PORT = "COM8"  # Change this if your Nano uses another port
BAUD = 9600
RATE = 44100

latest_reading = 0
lock = threading.Lock()
phase = 0.0


def read_pot():
    global latest_reading

    with serial.Serial(PORT, BAUD, timeout=1) as board:
        time.sleep(2)
        board.reset_input_buffer()

        while True:
            line = board.readline().decode(errors="ignore").strip()
            try:
                value = int(line)
                with lock:
                    latest_reading = max(0, min(1023, value))
            except ValueError:
                pass


def audio_callback(outdata, frames, time_info, status):
    global phase

    with lock:
        value = latest_reading

    # Map ADC values to G3–G5 (196–784 Hz)
    x = value / 1023.0
    frequency = 196.0 * (4.0 ** x)

    # Generate a violin-like tone using harmonics
    increments = 2 * np.pi * frequency / RATE
    angles = phase + increments * np.arange(frames)

    sound = (
        np.sin(angles)
        + 0.45 * np.sin(2 * angles)
        + 0.20 * np.sin(3 * angles)
        + 0.10 * np.sin(4 * angles)
    )

    outdata[:, 0] = (0.10 * sound).astype(np.float32)
    phase = (phase + increments * frames) % (2 * np.pi)


threading.Thread(target=read_pot, daemon=True).start()

with sd.OutputStream(
    samplerate=RATE,
    channels=1,
    dtype="float32",
    blocksize=512,
    callback=audio_callback,
):
    print("Turn the potentiometer to change pitch. Press Ctrl+C to stop.")
    while True:
        time.sleep(1)
