
import time
import fluidsynth

SOUNDFONT = r"C:\Users\amals\Documents\Codeworks\potenvio\violin.sf2"

synth = fluidsynth.Synth(gain=0.8)

try:
    synth.start(driver="dsound")

    sfid = synth.sfload(SOUNDFONT)
    if sfid == -1:
        raise RuntimeError("Could not load violin.sf2")

    # General MIDI program 40 = Violin (zero-based)
    synth.program_select(0, sfid, 0, 40)

    # Increase volume and expression
    synth.cc(0, 7, 127)    # Channel volume
    synth.cc(0, 11, 127)   # Expression
    synth.cc(0, 1, 0)      # Modulation
    synth.cc(0, 10, 64)    # Pan center

    print("Playing loud A4 violin note...")
    synth.noteon(0, 69, 127)
    time.sleep(3)
    synth.noteoff(0, 69)
    time.sleep(1)

finally:
    synth.delete()
