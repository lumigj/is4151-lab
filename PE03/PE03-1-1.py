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

g_on = False
try:
    while True:
        if GPIO.input(butRedPin):
            if r_state:
                r_state = False
                r_on = not r_on
        else:
            if not r_state:
                r_state = True
        GPIO.output(ledRedPin, r_on)

        if GPIO.input(butGreenPin):
            pass
        else:
            g_on = not g_on
        GPIO.output(ledGreenPin, r_on)

        if GPIO.input(butBluePin):
            GPIO.output(ledBluePin, False)
        else:
            GPIO.output(ledBluePin, True)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated!")

finally:
    GPIO.cleanup()
