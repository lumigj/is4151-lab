import time

import board
import RPi.GPIO as GPIO
from adafruit_bme280 import basic as adafruit_bme280

# Same BOARD pins as PE03-1-1.py
TEMP_LED_RED_PIN = 11
TEMP_LED_GREEN_PIN = 13
TEMP_LED_BLUE_PIN = 15

TEMP_THRESHOLD = 0.5
CHECK_INTERVAL_SECONDS = 1


def set_temperature_led(red_on, green_on, blue_on):
    GPIO.output(TEMP_LED_RED_PIN, red_on)
    GPIO.output(TEMP_LED_GREEN_PIN, green_on)
    GPIO.output(TEMP_LED_BLUE_PIN, blue_on)


def update_temperature_gauge(current_temp, baseline_temp):
    delta = current_temp - baseline_temp

    if abs(delta) <= TEMP_THRESHOLD:
        set_temperature_led(False, True, False)
        status = "equal to"
    elif delta < 0:
        set_temperature_led(False, False, True)
        status = "lower than"
    else:
        set_temperature_led(True, False, False)
        status = "higher than"

    print(
        "Temperature = {0:0.2f} deg C | Baseline = {1:0.2f} deg C | Status: {2} baseline".format(
            current_temp, baseline_temp, status
        )
    )


i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TEMP_LED_RED_PIN, GPIO.OUT)
GPIO.setup(TEMP_LED_GREEN_PIN, GPIO.OUT)
GPIO.setup(TEMP_LED_BLUE_PIN, GPIO.OUT)

baseline_temperature = bme280.temperature
set_temperature_led(False, True, False)
print("Initial baseline temperature = {0:0.2f} deg C".format(baseline_temperature))

try:
    while True:
        current_temperature = bme280.temperature
        update_temperature_gauge(current_temperature, baseline_temperature)
        time.sleep(CHECK_INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("Program terminated!")

finally:
    GPIO.cleanup()
