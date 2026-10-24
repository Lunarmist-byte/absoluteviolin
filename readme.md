# Virtual Violin — Arduino Nano and Python

A virtual violin project that uses an Arduino Nano and a potentiometer to control violin notes in real time. Python reads potentiometer values over serial communication and generates violin sounds using FluidSynth and a SoundFont file.

## Features

- Potentiometer-based control
- MIDI note generation using Python
- Violin sound synthesis using FluidSynth
- Arduino Nano serial communication
- Real-time interaction between hardware and software

## Hardware Requirements

- Arduino Nano
- 10 kΩ potentiometer (recommended)
- USB cable for the Arduino
- Jumper wires
- Computer running Windows

## Software Requirements

- Python 3
- Arduino IDE
- FluidSynth
- `pyfluidsynth`
- `pyserial`
- A compatible violin SoundFont file (`violin.sf2`)

## Project Structure

Place the files in the following structure:

```text
potenvio/
├── vio1.py
├── test_serial.py
├── violin.sf2
├── arduino/
│   └── virtual_violin.ino
└── README.md
```

## Circuit Connections

Connect the potentiometer to the Arduino Nano:

| Potentiometer | Arduino Nano |
|---|---|
| Outer pin 1 | 5V |
| Middle pin (wiper) | A0 |
| Outer pin 2 | GND |

The potentiometer provides an analog reading between `0` and `1023`, which the Arduino sends to Python over USB serial communication.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY` with your GitHub details.

### 2. Install Python Dependencies

```bash
python -m pip install pyserial pyfluidsynth
```

**Note:** `pyfluidsynth` is a Python wrapper. A compatible native FluidSynth library must also be installed and accessible to Python.

### 3. Add the Violin SoundFont

Place your SoundFont file in the project root:

```text
potenvio/violin.sf2
```
The link for Gdrive for the violin synth:
The Python code should point to the file's location. For example:

```python
SOUNDFONT = r"C:\Users\YOUR_NAME\Documents\Codeworks\potenvio\violin.sf2"
```

For a more portable project, use a path relative to the Python script:

```python
from pathlib import Path

SOUNDFONT = str(Path(__file__).parent / "violin.sf2")
```

**SoundFont licensing:** Before committing `violin.sf2` to a public repository, verify that its licence permits redistribution. If it does not, provide a download link to the original source and its licence instead of uploading the file.

### 4. Upload the Arduino Code

1. Open `virtual_violin.ino` in Arduino IDE.
2. Select the appropriate Arduino Nano board and processor.
3. Select the correct COM port.
4. Upload the sketch.
5. Close Serial Monitor before running Python.

The Arduino sketch should read the potentiometer and transmit the numeric value at `115200` baud.

### 5. Configure the Serial Port

In `vio1.py`, set the port to match your Arduino:

```python
PORT = "COM8"
BAUD_RATE = 115200
```

Your COM port may differ if Windows assigns a different one.

### 6. Run the Project

First, test the serial connection:

```bash
python test_serial.py
```

Then start the virtual violin:

```bash
python vio1.py
```

Turn the potentiometer to control the notes.

## How It Works

1. The potentiometer changes its analog voltage as you turn it.
2. The Arduino Nano reads that voltage using `analogRead(A0)`.
3. The Arduino sends the readings to Python through USB serial communication.
4. Python converts the readings into MIDI note numbers.
5. FluidSynth uses `violin.sf2` to synthesize the violin sound.
6. The computer plays the generated audio.

## Troubleshooting

| Problem | Possible Solution |
|---|---|
| No serial data | Verify the COM port and close Arduino Serial Monitor. |
| `Access is denied` | Another application may be using the serial port. |
| SoundFont cannot load | Check the path to `violin.sf2`. |
| No audio output | Check the FluidSynth audio driver and Windows output device. |
| FluidSynth MIDI-device warnings | The project generates notes directly through FluidSynth; a separate MIDI input device is not normally required. |
| Notes do not respond | Confirm Python receives changing potentiometer readings and check the note-triggering logic. |

## Future Improvements

- Add a physical button for bow control.
- Add pitch bending and vibrato.
- Improve note transitions and sound continuity.
- Add adjustable volume and pitch range.
- Build a graphical user interface.
- Explore pressure-sensitive bow control.

## License

Choose a licence for your original source code, such as the MIT License, if appropriate. Check the SoundFont's separate licence and attribution requirements before redistributing it.

---

Built with Arduino Nano, Python, and FluidSynth.
