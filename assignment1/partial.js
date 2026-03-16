// @flow
function sendFinalScore () {
    messageSequence += 1
    for (let index = 0; index < RADIO_REPEAT_COUNT; index++) {
        radioPacket = "E|" + DEVICE_NAME + "|" + playerName + "|" + encodeBase36(score) + "|" + encodeBase36(messageSequence)
        radio.sendString(radioPacket)
    }
}
input.onButtonPressed(Button.A, function () {
    playerName = randomPlayerName()
    score = randint(0, 10)
    sendFinalScore()
    basic.showString(playerName)
    basic.showNumber(score)
})
function randomPlayerName () {
    name = ""
    for (let index = 0; index < 5; index++) {
        name = "" + name + alphabet.charAt(randint(0, 25))
    }
    return name
}
function encodeBase36 (value: number) {
    if (value == 0) {
        return "0"
    }
    while (value > 0) {
        remainder = value % 36
        encoded = "" + base36Digit(remainder) + encoded
        value = Math.idiv(value, 36)
    }
    return encoded
}
function base36Digit (value: number) {
    return BASE36_DIGITS.charAt(value)
}
let value = 0
let encoded = ""
let remainder = 0
let name = ""
let score = 0
let playerName = ""
let radioPacket = ""
let messageSequence = 0
let DEVICE_NAME = ""
let alphabet = ""
let BASE36_DIGITS = ""
let RADIO_REPEAT_COUNT = 0
RADIO_REPEAT_COUNT = 3
BASE36_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEVICE_NAME = control.deviceName()
radio.setFrequencyBand(11)
basic.showIcon(IconNames.Yes)
