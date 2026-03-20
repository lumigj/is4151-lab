import time

import board
from adafruit_bme280 import basic as adafruit_bme280

i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

try:

    while True:

        print('Temperature = {0:0.3f} deg C'.format(bme280.temperature))
        print('Pressure    = {0:0.2f} hpa'.format(bme280.pressure))
        print('Humidity    = {0:0.2f} %'.format(bme280.humidity))

        time.sleep(1)

except KeyboardInterrupt:
    print("Program terminated!")

finally:
    pass
