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

g_state = False
g_on = False

b_state = False
b_on = False
try:
    while True:
        # 松开才改
        if GPIO.input(butRedPin):
            if r_state:
                r_state = False
                r_on = not r_on
        else:
            if not r_state:
                r_state = True
        GPIO.output(ledRedPin, r_on)

        # 按下就改
        if GPIO.input(butGreenPin):
            if g_state:
                g_state = False
        else:
            if not g_state:
                g_state = True
                g_on = not g_on
        GPIO.output(ledGreenPin, g_on)

        # 亮只需按下，灭却等松开
        if GPIO.input(butBluePin):
            if b_state:
                b_state = False
                if b_on:
                    b_on = False
        else:
            if not b_state:
                b_state = True
                if not b_on:
                    b_on = True
        GPIO.output(ledBluePin, b_on)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated!")

finally:
    GPIO.cleanup()
