import sys

import serial


try:
    com_port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    ser = serial.Serial(port=com_port, baudrate=9600, timeout=0.1)

    print(f"Listening for scores on {com_port}... Press CTRL+C to exit")

    while True:
        if ser.in_waiting > 0:
            msg = ser.readline()
            score = msg.decode("utf-8", errors="replace").strip()

            if score:
                print(score)

except serial.SerialException as err:
    print(f"SerialException: {err}")

except KeyboardInterrupt:
    print("Program terminated!")
