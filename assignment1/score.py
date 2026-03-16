import sys

import serial
from serial.tools import list_ports


def resolve_com_port():
    if len(sys.argv) > 1:
        return sys.argv[1]

    candidate_ports = []
    for port in list_ports.comports():
        device = port.device or ""
        description = (port.description or "").lower()
        hwid = (port.hwid or "").lower()

        # Prefer USB serial adapters and Arduino-class devices first.
        if (
            "arduino" in description
            or "usb" in description
            or "acm" in device.lower()
            or "usb" in hwid
        ):
            candidate_ports.insert(0, device)
        else:
            candidate_ports.append(device)

    for port in candidate_ports:
        try:
            test_serial = serial.Serial(port=port, baudrate=9600, timeout=0.1)
            test_serial.close()
            return port
        except serial.SerialException:
            continue

    raise serial.SerialException(
        "No usable serial port found. Pass the port explicitly, for example: python score.py COM3"
    )


try:
    com_port = resolve_com_port()
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
