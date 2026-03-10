# import the GPIO and time package
import RPi.GPIO as GPIO
import time

# Pin  Definitions
ledRedPin = 11
ledGreenPin = 13
ledBluePin = 15
butRedPin = 12
butGreenPin = 16
butBluePin = 18

# Pin Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledRedPin, GPIO.OUT)
GPIO.setup(ledGreenPin, GPIO.OUT)
GPIO.setup(ledBluePin, GPIO.OUT)
GPIO.setup(butRedPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(butGreenPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(butBluePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Program running... Press CTRL+C to exit")

r_state = False
r_on = False
try:
    while True:
        if GPIO.input(butRedPin):
            if r_state:
                r_state = False
                r_on = not r_on
            GPIO.output(ledRedPin, False)
        else:
            if not r_state:
                r_state = True
            GPIO.output(ledRedPin, True)

        if GPIO.input(butGreenPin):
            GPIO.output(ledGreenPin, False)
        else:
            GPIO.output(ledGreenPin, True)

        if GPIO.input(butBluePin):
            GPIO.output(ledBluePin, False)
        else:
            GPIO.output(ledBluePin, True)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated!")

finally:
    GPIO.cleanup()
