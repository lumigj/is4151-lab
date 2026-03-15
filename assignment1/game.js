function startNextRound () {
    waitingForPress = true
    beeping = false
    roundDeadline = input.runningTime() + RESPONSE_WINDOW
    showDigit(randint(1, 6))
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
function showDigit (value: number) {
    switch (value) {
        case 1:
            basic.showLeds(`
                . . # . .
                . # # . .
                . . # . .
                . . # . .
                . # # # .
            `)
            break
        case 2:
            basic.showLeds(`
                . # # # .
                . . . # .
                . . # # .
                . # . . .
                . # # # .
            `)
            break
        case 3:
            basic.showLeds(`
                . # # # .
                . . . # .
                . . # # .
                . . . # .
                . # # # .
            `)
            break
        case 4:
            basic.showLeds(`
                . # . # .
                . # . # .
                . # # # .
                . . . # .
                . . . # .
            `)
            break
        case 5:
            basic.showLeds(`
                . # # # .
                . # . . .
                . # # # .
                . . . # .
                . # # # .
            `)
            break
        default:
            basic.showLeds(`
                . # # # .
                . # . . .
                . # # # .
                . # . # .
                . # # # .
            `)
            break
    }
}
let beepEndTime = 0
let loopNow = 0
let gameEndTime = 0
let gameFinished = false
let pressCount = 0
let gameStarted = false
let roundDeadline = 0
let beeping = false
let waitingForPress = false
let RESPONSE_WINDOW = 0
let GAME_DURATION = 0
GAME_DURATION = 30000
RESPONSE_WINDOW = 3000
let BEEP_DURATION = 150
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
