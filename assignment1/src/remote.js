// @flow
function currentLetter() {
    return alphabet.charAt(currentLetterIndex)
}
input.onButtonPressed(Button.A, function () {
    if (!(inputStarted)) {
        inputStarted = true
        currentLetterIndex = 0
        currentPosition = 0
        playerName = ""
        showCurrentLetter()
        return
    }
    currentLetterIndex += -1
    if (currentLetterIndex < 0) {
        currentLetterIndex = 25
    }
    showCurrentLetter()
})
function showRemoteSplash() {
    basic.showString("REM")
    basic.showString(TARGET_DEVICE_NAME)
    basic.showIcon(IconNames.Yes)
}
function showCurrentLetter() {
    basic.showString("" + (currentLetter()))
}
input.onButtonPressed(Button.AB, function () {
    if (!(inputStarted)) {
        return
    }
    flashCurrentLetter()
    playerName = "" + playerName + currentLetter()
    currentPosition += 1
    if (currentPosition >= 5) {
        inputStarted = false
        for (let index = 0; index < RADIO_REPEAT_COUNT; index++) {
            radio.sendString("R|" + TARGET_DEVICE_NAME + "|" + playerName)
        }
        basic.showString(playerName)
        basic.showIcon(IconNames.Yes)
        showRemoteSplash()
        return
    }
    currentLetterIndex = 0
    showCurrentLetter()
})
input.onButtonPressed(Button.B, function () {
    if (!(inputStarted)) {
        return
    }
    currentLetterIndex += 1
    if (currentLetterIndex > 25) {
        currentLetterIndex = 0
    }
    showCurrentLetter()
})
function flashCurrentLetter() {
    basic.clearScreen()
    basic.pause(70)
    showCurrentLetter()
}
let playerName = ""
let currentPosition = 0
let inputStarted = false
let currentLetterIndex = 0
let alphabet = ""
let RADIO_REPEAT_COUNT = 0
let TARGET_DEVICE_NAME = ""
RADIO_REPEAT_COUNT = 3
TARGET_DEVICE_NAME = "vatoz"
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
radio.setFrequencyBand(11)
showRemoteSplash()
