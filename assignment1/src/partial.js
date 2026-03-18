function sendEndPacket() {
    for (let index = 0; index < RADIO_REPEAT_COUNT; index++) {
        radio.sendString("E|" + DEVICE_NAME + "|" + score)
    }
}
function sendStartPacket() {
    for (let index = 0; index < RADIO_REPEAT_COUNT; index++) {
        radio.sendString("S|" + DEVICE_NAME + "|" + playerName)
    }
}
input.onButtonPressed(Button.A, function () {
    playerName = randomPlayerName()
    score = randint(0, 100)
    sendStartPacket()
    sendEndPacket()
    basic.showString(playerName)
    basic.showNumber(score)
})
function randomPlayerName() {
    name = ""
    for (let index = 0; index < 5; index++) {
        name = "" + name + alphabet.charAt(randint(0, 25))
    }
    return name
}
let name = ""
let score = 0
let playerName = ""
let DEVICE_NAME = ""
let alphabet = ""
let RADIO_REPEAT_COUNT = 0
RADIO_REPEAT_COUNT = 3
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEVICE_NAME = control.deviceName()
radio.setFrequencyBand(11)
basic.showIcon(IconNames.Yes)
