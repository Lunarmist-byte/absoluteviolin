
import serial
import time

PORT = "COM8"
BAUD = 115200

print(f"Opening {PORT} at {BAUD} baud...")

try:
    with serial.Serial(PORT, BAUD, timeout=3) as arduino:
        print("Port opened.")
        time.sleep(2)

        print("Bytes waiting:", arduino.in_waiting)
        print("Listening for 10 seconds...")

        start = time.time()

        while time.time() - start < 10:
            data = arduino.readline()
            print("RAW:", repr(data))

except Exception as e:
    print("ERROR:", repr(e))

print("Test finished.")
