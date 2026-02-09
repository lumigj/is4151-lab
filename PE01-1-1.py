def doRandomNumber():
    global rnum, fdigit, ldigit
    basic.clear_screen()
    rnum = Math.random_range(1, 10000)
    fdigit = rnum
    while fdigit >= 10:
        fdigit /= 10
    ldigit = rnum % 10
    basic.show_string("rnum=" + str(rnum))
    basic.show_string("fd=" + str(Math.floor(fdigit)))
    basic.show_string("ld=" + str(ldigit))

def on_button_pressed_a():
    doRandomNumber()
    clearScreen()
input.on_button_pressed(Button.A, on_button_pressed_a)

def clearScreen():
    basic.clear_screen()
    basic.show_icon(IconNames.YES)
ldigit = 0
rnum = 0
fdigit = 0
rnum = 0
fdigit = 0
ldigit = 0
clearScreen()

def on_forever():
    pass
basic.forever(on_forever)
