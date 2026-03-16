let distance = 0
let display = grove.createDisplay(DigitalPin.P2, DigitalPin.P16)

basic.showIcon(IconNames.Yes)

basic.forever(function () {
    distance = grove.measureInCentimeters(DigitalPin.P1)
    display.show(distance)
    if (distance <= 5) {
        basic.showIcon(IconNames.Sad)
        music.playTone(988, music.beat(BeatFraction.Whole))
    } else {
        basic.showIcon(IconNames.Happy)
    }
    basic.pause(100)
})
