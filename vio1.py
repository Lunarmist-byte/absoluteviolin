
import time
import serial
import fluidsynth

# ---------- SETTINGS ----------
PORT = "COM8"
BAUD_RATE = 115200

SOUNDFONT = r"C:\Users\amals\Documents\Codeworks\potenvio\violin.sf2"

ADC_MAX = 1023
LOW_NOTE = 55
HIGH_NOTE = 88

MOVEMENT_THRESHOLD = 2
SILENCE_DELAY = 0.45
SYNTH_GAIN = 0.8

# ---------- START AUDIO ----------
print("Starting FluidSynth...")

synth = fluidsynth.Synth(gain=SYNTH_GAIN)
synth.start(driver="dsound")

sfid = synth.sfload(SOUNDFONT)

if sfid == -1:
    raise RuntimeError("Could not load violin.sf2")

# General MIDI: program 40 = violin (zero-based)
synth.program_select(0, sfid, 0, 40)
synth.cc(0, 7, 127)
synth.cc(0, 11, 127)

current_note = None
last_position = None
last_movement_time = 0.0


def stop_note():
    global current_note

    if current_note is not None:
        synth.noteoff(0, current_note)
        current_note = None


def play_note(note):
    global current_note

    if current_note == note:
        return

    stop_note()
    synth.noteon(0, note, 120)
    current_note = note


try:
    # Startup audio test: should hear one violin note
    print("Testing violin audio for 1 second...")
    synth.noteon(0, 69, 120)  # A4
    time.sleep(1)
    synth.noteoff(0, 69)
    print("Audio test finished.")

    print(f"Connecting to Arduino on {PORT}...")

    with serial.Serial(PORT, BAUD_RATE, timeout=1) as arduino:
        time.sleep(2)
        arduino.reset_input_buffer()

        print("Connected!")
        print("Turn the potentiometer to play.")
        print("Ctrl+C to stop.\n")
        print("ADC Reading | MIDI Note | Status")
        print("---------------------------------")

        while True:
            line = arduino.readline().decode(
                "utf-8", errors="ignore"
            ).strip()

            if not line:
                continue

            try:
                raw_value = int(line)
            except ValueError:
                continue

            raw_value = max(0, min(ADC_MAX, raw_value))

            # Map 0-1023 to MIDI notes
            note = LOW_NOTE + round(
                raw_value / ADC_MAX * (HIGH_NOTE - LOW_NOTE)
            )

            now = time.monotonic()

            if last_position is None:
                last_position = raw_value

            # Any meaningful change acts like bow movement
            changed = abs(raw_value - last_position) >= MOVEMENT_THRESHOLD

            if changed:
                last_movement_time = now
                play_note(note)

            # Keep the note sounding briefly after movement stops
            if (
                current_note is not None
                and now - last_movement_time > SILENCE_DELAY
            ):
                stop_note()

            status = "PLAYING" if current_note is not None else "SILENT"

            print(
                f"{raw_value:5d}       | {note:3d}       | {status}   ",
                end="\r",
                flush=True,
            )

            last_position = raw_value

except KeyboardInterrupt:
    print("\nStopping...")

except Exception as e:
    print(f"\nERROR: {e}")

finally:
    try:
        stop_note()
        synth.delete()
    except Exception:
        pass
