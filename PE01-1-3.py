# A控制启停 B控制reset

def on_button_pressed_a():
    global isCounting
    if not (isCounting):
        basic.show_icon(IconNames.DIAMOND)
        isCounting = True
    else:
        basic.show_number(time)
        isCounting = False
input.on_button_pressed(Button.A, on_button_pressed_a)

# counting的时候不能reset

def on_button_pressed_b():
    global time
    if not (isCounting):
        time = 0
        basic.show_icon(IconNames.NO)
    else:
        pass
input.on_button_pressed(Button.B, on_button_pressed_b)

isCounting = False
time = 0
time = 0
isCounting = False

def on_forever():
    global time
    if isCounting:
        basic.pause(1000)
        time += 1
basic.forever(on_forever)
