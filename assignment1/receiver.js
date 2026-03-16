// @flow
function rememberMessage (messageKey: string) {
    seenMessageKeys.push(messageKey)
    if (seenMessageKeys.length > MAX_SEEN_MESSAGES) {
        seenMessageKeys.shift()
    }
}
function messageSeen (messageKey: string) {
    for (let seenKey of seenMessageKeys) {
        if (seenKey == messageKey) {
            return true
        }
    }
    return false
}
radio.onReceivedString(function (receivedString) {
    parts = receivedString.split("|")
    if (parts[0] == "S") {
        return
    }
    if (parts[0] == "L" || parts[0] == "E") {
        if (parts.length < 5) {
            return
        }
        latestMessageKey = "" + parts[1] + "|" + parts[4]
        if (messageSeen(latestMessageKey)) {
            return
        }
        rememberMessage(latestMessageKey)
        latestScore = receivedString
    } else {
        latestScore = receivedString
    }
    serial.writeLine(latestScore)
})
let latestScore = ""
let latestMessageKey = ""
let parts: string[] = []
let seenMessageKeys: string[] = []
let MAX_SEEN_MESSAGES = 0
MAX_SEEN_MESSAGES = 200
radio.setFrequencyBand(11)
serial.redirectToUSB()
serial.setBaudRate(BaudRate.BaudRate9600)
