radio.onReceivedString(function (receivedString) {
    let parts = receivedString.split("|")
    if (parts[0] == "START") {
        return
    }
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
