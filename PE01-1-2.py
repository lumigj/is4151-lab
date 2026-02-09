def on_button_pressed_a():
    global gender, age_group
    if mode == 0:
        gender = "M"
        show_gender()
    elif mode == 1:
        age_group += 0 - 1
        if age_group < 1:
            age_group = 4
        show_age_group()
input.on_button_pressed(Button.A, on_button_pressed_a)

def get_greeting(g: str, grp: number):
    if grp == 0:
        return "Hello boy!" if g == "M" else "Hello girl!"
    if grp == 1:
        return "Hello young man!" if g == "M" else "Hello young lady!"
    if grp == 2:
        return "Hello Sir!" if g == "M" else "Hello Madam!"
    return "Hello old man!" if g == "M" else "Hello old lady!"
def show_gender():
    basic.show_string("G")
    basic.show_string(gender)
def show_age_group():
    basic.show_string("A")
    basic.show_string("" + str(age_group))

def on_button_pressed_ab():
    global mode
    if mode == 0:
        mode = 1
        show_age_group()
    elif mode == 1:
        mode = 2
        basic.show_string("" + str((get_greeting(gender, age_group))))
        mode = 0
        show_gender()
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    global gender, age_group
    if mode == 0:
        gender = "F"
        show_gender()
    elif mode == 1:
        age_group += 1
        if age_group > 4:
            age_group = 1
        show_age_group()
input.on_button_pressed(Button.B, on_button_pressed_b)

age_group = 0
gender = ""
mode = 0
mode = 0
gender = "M"
age_group = 0
show_gender()

def on_forever():
    pass
basic.forever(on_forever)
