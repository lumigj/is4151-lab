radio.onReceivedString(function (receivedString) {
    if (receivedString.charAt(0) == "R") {
        return
    }
    serial.writeLine(receivedString)
})
radio.setFrequencyBand(11)
serial.redirectToUSB()
serial.setBaudRate(BaudRate.BaudRate9600)
