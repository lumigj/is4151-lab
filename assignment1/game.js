/**
 * @flow
 */
function startNextRound() {
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
    startNextRound()
})
function showDigitRow(value: number, row: number) {
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
input.onButtonPressed(Button.B, function () {
    if (!(gameStarted) || gameFinished || !(waitingForPress)) {
        return
    }
    if (input.runningTime() >= gameEndTime || input.runningTime() > roundDeadline) {
        return
    }
    pressCount += 1
    startNextRound()
})
function getRowPattern(value: number, row: number) {
    switch (value) {
        case 1:
            switch (row) {
                case 0:
                    return 4
                case 1:
                    return 12
                case 2:
                    return 4
                case 3:
                    return 4
                default:
                    return 14
            }
        case 2:
            switch (row) {
                case 0:
                    return 14
                case 1:
                    return 2
                case 2:
                    return 6
                case 3:
                    return 8
                default:
                    return 14
            }
        case 3:
            switch (row) {
                case 0:
                    return 14
                case 1:
                    return 2
                case 2:
                    return 6
                case 3:
                    return 2
                default:
                    return 14
            }
        case 4:
            switch (row) {
                case 0:
                    return 10
                case 1:
                    return 10
                case 2:
                    return 14
                default:
                    return 2
            }
        case 5:
            switch (row) {
                case 0:
                    return 14
                case 1:
                    return 8
                case 2:
                    return 14
                case 3:
                    return 2
                default:
                    return 14
            }
        default:
            switch (row) {
                case 0:
                    return 14
                case 1:
                    return 8
                case 2:
                    return 14
                case 3:
                    return 10
                default:
                    return 14
            }
    }
}
let beepEndTime = 0
let loopNow = 0
let roundDeadline = 0
let gameEndTime = 0
let gameFinished = false
let pressCount = 0
let gameStarted = false
let nextDisplayTime = 0
let currentDisplayRow = 0
let currentDigit = 0
let displayingDigit = false
let beeping = false
let waitingForPress = false
let GAME_DURATION = 30000 //一共30秒，测试用，到时候改成3分钟
let RESPONSE_WINDOW = 3000 //3秒按下
let DISPLAY_ROW_DELAY = 80
let BEEP_DURATION = 150 //beep响多久
let BEEP_FREQUENCY = 988
basic.forever(function () {
    loopNow = input.runningTime()
    if (!(gameStarted) || gameFinished) {
        return
    }
    if (loopNow >= gameEndTime) {
        if (beeping) {
            music.stopAllSounds()
        }
        gameFinished = true
        waitingForPress = false
        beeping = false
        basic.showNumber(pressCount)
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
        beepEndTime = loopNow + BEEP_DURATION
        music.ringTone(BEEP_FREQUENCY)
        return
    }
    if (beeping && loopNow >= beepEndTime) {
        music.stopAllSounds()
        startNextRound()
    }
})
