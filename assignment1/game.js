// @flow
grove.onGesture(GroveGesture.Down, function () {
    if (!(gameStarted) || gameFinished || !(waitingForPress)) {
        return
    }
    if (input.runningTime() >= gameEndTime || input.runningTime() > roundDeadline) {
        return
    }
    if (currentDigit != 4) {
        return
    }
    pressCount += 1
    sendScore()
    startNextRound()
})
function sendScore () {
    radio.sendString("" + DEVICE_NAME + "|" + PLAYER_NAME + "|" + pressCount)
}
grove.onGesture(GroveGesture.Right, function () {
    if (!(gameStarted) || gameFinished || !(waitingForPress)) {
        return
    }
    if (input.runningTime() >= gameEndTime || input.runningTime() > roundDeadline) {
        return
    }
    if (currentDigit != 2) {
        return
    }
    pressCount += 1
    sendScore()
    startNextRound()
})
function sendFinalScore () {
    radio.sendString("END|" + DEVICE_NAME + "|" + PLAYER_NAME + "|" + pressCount)
}
// @flow
function startNextRound () {
    waitingForPress = false
    beeping = false
    displayingDigit = true
    currentDigit = randint(1, 6)
    currentDisplayRow = 0
    nextDisplayTime = input.runningTime()
    basic.clearScreen()
}
input.onButtonPressed(Button.A, function () {
    if (gameStarted) {
        return
    }
    gameStarted = true
    pressCount = 0
    gameFinished = false
    gameEndTime = input.runningTime() + GAME_DURATION
    sendScore()
    startNextRound()
})
grove.onGesture(GroveGesture.Clockwise, function () {
    if (!(gameStarted) || gameFinished || !(waitingForPress)) {
        return
    }
    if (input.runningTime() >= gameEndTime || input.runningTime() > roundDeadline) {
        return
    }
    if (currentDigit != 5) {
        return
    }
    pressCount += 1
    sendScore()
    startNextRound()
})
grove.onGesture(GroveGesture.Up, function () {
    if (!(gameStarted) || gameFinished || !(waitingForPress)) {
        return
    }
    if (input.runningTime() >= gameEndTime || input.runningTime() > roundDeadline) {
        return
    }
    if (currentDigit != 3) {
        return
    }
    pressCount += 1
    sendScore()
    startNextRound()
})
grove.onGesture(GroveGesture.Left, function () {
    if (!(gameStarted) || gameFinished || !(waitingForPress)) {
        return
    }
    if (input.runningTime() >= gameEndTime || input.runningTime() > roundDeadline) {
        return
    }
    if (currentDigit != 1) {
        return
    }
    pressCount += 1
    sendScore()
    startNextRound()
})
function showDigitRow (value: number, row: number) {
    if (getRowPattern(value, row) & 16) {
        led.plot(0, row)
    } else {
        led.unplot(0, row)
    }
    if (getRowPattern(value, row) & 8) {
        led.plot(1, row)
    } else {
        led.unplot(1, row)
    }
    if (getRowPattern(value, row) & 4) {
        led.plot(2, row)
    } else {
        led.unplot(2, row)
    }
    if (getRowPattern(value, row) & 2) {
        led.plot(3, row)
    } else {
        led.unplot(3, row)
    }
    if (getRowPattern(value, row) & 1) {
        led.plot(4, row)
    } else {
        led.unplot(4, row)
    }
}
grove.onGesture(GroveGesture.Anticlockwise, function () {
    if (!(gameStarted) || gameFinished || !(waitingForPress)) {
        return
    }
    if (input.runningTime() >= gameEndTime || input.runningTime() > roundDeadline) {
        return
    }
    if (currentDigit != 6) {
        return
    }
    pressCount += 1
    sendScore()
    startNextRound()
})
function showFullDigit (value: number) {
    basic.clearScreen()
    showDigitRow(value, 0)
    showDigitRow(value, 1)
    showDigitRow(value, 2)
    showDigitRow(value, 3)
    showDigitRow(value, 4)
}
function getRowPattern (value: number, row: number) {
    switch (value) {
        case 1:
            switch (row) {
                case 0:
                    return 4
                case 1:
                    return 8
                case 2:
                    return 31
                case 3:
                    return 8
                default:
                    return 4
            }
        case 2:
            switch (row) {
                case 0:
                    return 4
                case 1:
                    return 2
                case 2:
                    return 31
                case 3:
                    return 2
                default:
                    return 4
            }
        case 3:
            switch (row) {
                case 0:
                    return 4
                case 1:
                    return 14
                case 2:
                    return 21
                case 3:
                    return 4
                default:
                    return 4
            }
        case 4:
            switch (row) {
                case 0:
                    return 4
                case 1:
                    return 4
                case 2:
                    return 21
                case 3:
                    return 14
                default:
                    return 4
            }
        case 5:
            switch (row) {
                case 0:
                    return 14
                case 1:
                    return 17
                case 2:
                    return 13
                case 3:
                    return 2
                default:
                    return 12
            }
        default:
            switch (row) {
                case 0:
                    return 14
                case 1:
                    return 18
                case 2:
                    return 22
                case 3:
                    return 8
                default:
                    return 6
            }
    }
}
let missFlashTime = 0
let missFlashStep = 0
let beepEndTime = 0
let tooClosePenaltyTime = 0
let tooClosePenaltyStep = 0
let waitingNextRoundAfterMiss = false
let flashingMiss = false
let playerTooClose = false
let distanceCm = 0
let nextDistanceCheckTime = 0
let pendingTooCloseReset = false
let tooClosePenaltyActive = false
let loopNow = 0
let nextDisplayTime = 0
let currentDisplayRow = 0
let displayingDigit = false
let beeping = false
let pressCount = 0
let currentDigit = 0
let roundDeadline = 0
let gameEndTime = 0
let waitingForPress = false
let gameFinished = false
let gameStarted = false
let DEVICE_NAME = ""
let PLAYER_NAME = ""
let GAME_DURATION = 0
let display = grove.createDisplay(DigitalPin.P2, DigitalPin.P16)
// 一共30秒，测试用，到时候改成3分钟
GAME_DURATION = 30000
// 3秒按下
let RESPONSE_WINDOW = 3000
let DISPLAY_ROW_DELAY = 80
// beep响多久
let BEEP_DURATION = 150
let BEEP_FREQUENCY = 988
let BEEP_VOLUME = 10
let MISS_FLASH_DELAY = 80
let DISTANCE_CHECK_DELAY = 100
let MIN_PLAYER_DISTANCE = 20
let TOO_CLOSE_BEEP_ON_DELAY = 70
let TOO_CLOSE_BEEP_OFF_DELAY = 60
let TOO_CLOSE_FLASH_DELAY = 60
PLAYER_NAME = "P1"
DEVICE_NAME = control.deviceName()
grove.initGesture()
radio.setFrequencyBand(11)
music.setVolume(BEEP_VOLUME)
basic.forever(function () {
    loopNow = input.runningTime()
    if (!(gameStarted) || gameFinished) {
        return
    }
    if (loopNow >= gameEndTime) {
        if (beeping || tooClosePenaltyActive) {
            music.stopAllSounds()
        }
        if (pendingTooCloseReset) {
            pressCount = 0
        }
        gameFinished = true
        waitingForPress = false
        beeping = false
        tooClosePenaltyActive = false
        pendingTooCloseReset = false
        sendFinalScore()
        basic.showNumber(pressCount)
        return
    }
    if (loopNow >= nextDistanceCheckTime) {
        nextDistanceCheckTime = loopNow + DISTANCE_CHECK_DELAY
        distanceCm = grove.measureInCentimeters(DigitalPin.P1)
        display.show(distanceCm)
        if (distanceCm > 0 && distanceCm < MIN_PLAYER_DISTANCE) {
            if (!(playerTooClose) && !(tooClosePenaltyActive)) {
                playerTooClose = true
                pendingTooCloseReset = true
                if (beeping || tooClosePenaltyActive) {
                    music.stopAllSounds()
                }
                beeping = false
                flashingMiss = false
                waitingNextRoundAfterMiss = false
                displayingDigit = false
                waitingForPress = false
                tooClosePenaltyActive = true
                tooClosePenaltyStep = 0
                tooClosePenaltyTime = loopNow + TOO_CLOSE_BEEP_ON_DELAY
                music.ringTone(BEEP_FREQUENCY)
            }
        } else {
            playerTooClose = false
        }
    }
    if (tooClosePenaltyActive && loopNow >= tooClosePenaltyTime) {
        if (tooClosePenaltyStep == 0) {
            music.stopAllSounds()
            tooClosePenaltyTime = loopNow + TOO_CLOSE_BEEP_OFF_DELAY
        } else if (tooClosePenaltyStep == 1) {
            music.ringTone(BEEP_FREQUENCY)
            tooClosePenaltyTime = loopNow + TOO_CLOSE_BEEP_ON_DELAY
        } else if (tooClosePenaltyStep == 2) {
            music.stopAllSounds()
            basic.clearScreen()
            tooClosePenaltyTime = loopNow + TOO_CLOSE_FLASH_DELAY
        } else if (tooClosePenaltyStep == 3 || tooClosePenaltyStep == 5 || tooClosePenaltyStep == 7 || tooClosePenaltyStep == 9 || tooClosePenaltyStep == 11) {
            showFullDigit(currentDigit)
            tooClosePenaltyTime = loopNow + TOO_CLOSE_FLASH_DELAY
        } else if (tooClosePenaltyStep == 4 || tooClosePenaltyStep == 6 || tooClosePenaltyStep == 8 || tooClosePenaltyStep == 10 || tooClosePenaltyStep == 12) {
            basic.clearScreen()
            tooClosePenaltyTime = loopNow + TOO_CLOSE_FLASH_DELAY
        } else {
            pressCount = 0
            sendScore()
            pendingTooCloseReset = false
            tooClosePenaltyActive = false
            startNextRound()
            return
        }
        tooClosePenaltyStep += 1
        return
    }
    if (displayingDigit && loopNow >= nextDisplayTime) {
        showDigitRow(currentDigit, currentDisplayRow)
        currentDisplayRow += 1
        if (currentDisplayRow >= 5) {
            displayingDigit = false
            waitingForPress = true
            roundDeadline = loopNow + RESPONSE_WINDOW
        } else {
            nextDisplayTime = loopNow + DISPLAY_ROW_DELAY
        }
        return
    }
    if (waitingForPress && loopNow > roundDeadline) {
        waitingForPress = false
        beeping = true
        flashingMiss = true
        waitingNextRoundAfterMiss = true
        beepEndTime = loopNow + BEEP_DURATION
        missFlashStep = 0
        missFlashTime = loopNow + MISS_FLASH_DELAY
        music.ringTone(BEEP_FREQUENCY)
        return
    }
    if (flashingMiss && loopNow >= missFlashTime) {
        if (missFlashStep == 0 || missFlashStep == 2) {
            basic.clearScreen()
        } else {
            showFullDigit(currentDigit)
        }
        missFlashStep += 1
        if (missFlashStep >= 4) {
            flashingMiss = false
        } else {
            missFlashTime = loopNow + MISS_FLASH_DELAY
        }
        return
    }
    if (beeping && loopNow >= beepEndTime) {
        music.stopAllSounds()
        beeping = false
    }
    if (waitingNextRoundAfterMiss && !(beeping) && !(flashingMiss)) {
        waitingNextRoundAfterMiss = false
        startNextRound()
    }
})
