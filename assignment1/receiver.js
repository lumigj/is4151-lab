radio.onReceivedString(function (receivedString) {
    latestScore = receivedString
    serial.writeLine(latestScore)
    basic.showLeds(`
        # # # # #
        # # # # #
        # # # # #
        # # # # #
        # # # # #
        `)
    basic.pause(80)
    basic.clearScreen()
})
let latestScore = ""
radio.setFrequencyBand(11)
serial.redirectToUSB()
serial.setBaudRate(BaudRate.BaudRate9600)
