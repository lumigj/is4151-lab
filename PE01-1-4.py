def on_received_number(receivedNumber):
    basic.show_leds("""
        # # # # #
        # # . # #
        # . # . #
        # . . . #
        # # # # #
        """)
    basic.pause(3000)
    showAccordingly(receivedNumber)
radio.on_received_number(on_received_number)

def showAccordingly(i: number):
    if i == 1:
        basic.show_leds("""
            # . . . .
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            """)
    elif i == 2:
        basic.show_leds("""
            # . . . .
            # # . . .
            . . . . .
            . . . . .
            . . . . .
            """)
    elif i == 3:
        basic.show_leds("""
            # . . . .
            # # . . .
            # # # . .
            . . . . .
            . . . . .
            """)
    elif i == 4:
        basic.show_leds("""
            # . . . .
            # # . . .
            # # # . .
            # # # # .
            . . . . .
            """)
    elif i == 5:
        basic.show_leds("""
            # . . . .
            # # . . .
            # # # . .
            # # # # .
            # # # # #
            """)

def on_button_pressed_a():
    global msg
    if msg == 1:
        msg = 2
    elif msg == 2:
        msg = 3
    elif msg == 3:
        msg = 4
    elif msg == 4:
        msg = 5
    else:
        msg = 1
    basic.show_string("" + str(msg))
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_ab():
    global msg
    msg = 0
    basic.show_icon(IconNames.NO)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    if msg == 0:
        basic.show_icon(IconNames.SAD)
        basic.pause(3000)
        basic.show_icon(IconNames.NO)
    else:
        radio.send_number(msg)
        basic.show_icon(IconNames.HAPPY)
        basic.pause(3000)
        showAccordingly(msg)
input.on_button_pressed(Button.B, on_button_pressed_b)

msg = 0
radio.set_frequency_band(11)
msg = 0
basic.show_icon(IconNames.YES)