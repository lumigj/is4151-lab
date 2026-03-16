function randomPlayerName () {
    let name = ""
    for (let index = 0; index < 5; index++) {
        name = "" + name + alphabet.charAt(randint(0, 25))
    }
    return name
}
input.onButtonPressed(Button.A, function () {
    playerName = randomPlayerName()
    score = randint(0, 100)
    radio.sendString("END|" + DEVICE_NAME + "|" + playerName + "|" + score)
    basic.showString(playerName)
    basic.showNumber(score)
})
let score = 0
let playerName = ""
let DEVICE_NAME = ""
let alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEVICE_NAME = control.deviceName()
radio.setFrequencyBand(11)
basic.showIcon(IconNames.Yes)
