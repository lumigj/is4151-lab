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
butFourthPin = 22

# Pin Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledRedPin, GPIO.OUT)
GPIO.setup(ledGreenPin, GPIO.OUT)
GPIO.setup(ledBluePin, GPIO.OUT)
GPIO.setup(butRedPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(butGreenPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(butBluePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(butFourthPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Program running... Press CTRL+C to exit")

r_state = False
r_on = False

g_state = False
g_on = False

b_state = False
b_on = False
b_wait_off = False

f_state = False
f_step = 0
t = time.monotonic()
c = 0
try:
    while True:
        if f_step == 0:
            # 松开才改
            if GPIO.input(butRedPin):
                if r_state:
                    r_state = False
                    r_on = not r_on
                    GPIO.output(ledRedPin, r_on)
            else:
                if not r_state:
                    r_state = True

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
                    if b_wait_off:
                        b_wait_off = False
                        b_on = False
                        GPIO.output(ledBluePin, b_on)
            else:
                if not b_state:
                    b_state = True
                    if b_on:
                        b_wait_off = True
                    else:
                        b_on = True
                        GPIO.output(ledBluePin, b_on)

        else:
            if GPIO.input(butFourthPin):
                if f_state:
                    f_state = False
                    #进入那个pattern模式 用读秒+状态机的方式
                    if f_step == 0:
                        f_step = 1
                        t = time.monotonic()
                        GPIO.output(ledRedPin, False)
                        GPIO.output(ledGreenPin, False)
                        GPIO.output(ledBluePin, False)
                    else:
                        f_step = 0
            else:
                if not f_state:
                    f_state = True
            if f_step == 1 and time.monotonic() > t + 1:
                f_step = 2
                t = time.monotonic()
                GPIO.output(ledRedPin, True)
            elif f_step == 2 and time.monotonic() > t + 1:
                f_step = 3
                t = time.monotonic()
                GPIO.output(ledRedPin, False)
                GPIO.output(ledGreenPin, True)
            elif f_step == 3 and time.monotonic() > t + 1:
                f_step = 4
                t = time.monotonic()
                GPIO.output(ledGreenPin, False)
                GPIO.output(ledBluePin, True)
            elif f_step == 4 and time.monotonic() > t + 1:
                f_step = 5
                t = time.monotonic()
                GPIO.output(ledBluePin, False)
            elif f_step == 5 and time.monotonic() > t + 1:
                f_step = 6
                t = time.monotonic()
                GPIO.output(ledRedPin, True)
                GPIO.output(ledGreenPin, True)
                GPIO.output(ledBluePin, True)
            elif f_step == 6 and time.monotonic() > t + 0.3:
                f_step = 7
                t = time.monotonic()
                c += 1
                GPIO.output(ledRedPin, False)
                GPIO.output(ledGreenPin, False)
                GPIO.output(ledBluePin, False)
            elif f_step == 7 and time.monotonic() > t + 0.3:
                if c < 3:
                    f_step = 6
                    t = time.monotonic()
                    GPIO.output(ledRedPin, True)
                    GPIO.output(ledGreenPin, True)
                    GPIO.output(ledBluePin, True)
                else :
                    f_step = 1
                    t = time.monotonic()
                    c = 0
                    GPIO.output(ledRedPin, False)
                    GPIO.output(ledGreenPin, False)
                    GPIO.output(ledBluePin, False)



        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated!")

finally:
    GPIO.cleanup()
