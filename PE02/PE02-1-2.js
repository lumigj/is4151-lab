// @flow

function showAccordingly (i: number) {
    if (i == 1) {
        basic.showLeds(`
            # . . . .
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            `)
    } else if (i == 2) {
        basic.showLeds(`
            # . . . .
            # # . . .
            . . . . .
            . . . . .
            . . . . .
            `)
    } else if (i == 3) {
        basic.showLeds(`
            # . . . .
            # # . . .
            # # # . .
            . . . . .
            . . . . .
            `)
    } else if (i == 4) {
        basic.showLeds(`
            # . . . .
            # # . . .
            # # # . .
            # # # # .
            . . . . .
            `)
    } else if (i == 5) {
        basic.showLeds(`
            # . . . .
            # # . . .
            # # # . .
            # # # # .
            # # # # #
            `)
    }
}
input.onButtonPressed(Button.A, function () {
    if (msg == 1) {
        msg = 2
    } else if (msg == 2) {
        msg = 3
    } else if (msg == 3) {
        msg = 4
    } else if (msg == 4) {
        msg = 5
    } else {
        msg = 1
    }
    basic.showString("" + (msg))
})

input.onButtonPressed(Button.AB, function () {
    msg = 0
    basic.showIcon(IconNames.No)
})

radio.onReceivedString(function (receivedString) {
    let part1
    let part2
    let part3
    let flag
    let parts: string[] = receivedString.split("|", 3)
    part1 = parts[0]
    part2 = parts[1]
    part3 = parts[2]
    flag = false
    for (let i of seenlist) {
        if (i == "" + part1 + "|" + part2) {
            // exist already
            flag = true
        }
    }
    if (flag===false) {
        // no exist
        seenlist.push("" + part1 + "|" + part2)
        // re
        if (isRelay) {
            serial.writeString(receivedString) //fogrelay
        } else {
            radio.sendString(receivedString)
        }
        showAccordingly(parseInt(part3))
    }
})
input.onButtonPressed(Button.B, function () {
    console.log(control.deviceName())//注意这个emulator不行 因为两个emulator的name一样的
    ownCounter++
    seenlist.push("" + control.deviceName() + "|" + ownCounter)
    radio.sendString("" + control.deviceName() + "|" + ownCounter + "|" + msg)
    //改这里之前呢seenlist不对，是收到自己传回来的消息一次以后才加入seenlist,现在修好了是发了就加进去了。
    basic.showIcon(IconNames.Happy)
    basic.pause(3000)
    showAccordingly(msg)
 
})
let ownCounter = 0
let msg = 0
let seenlist: string[]
let isRelay = false
radio.setFrequencyBand(11)
msg = 0
ownCounter = 0
seenlist = []

//fogrelay
isRelay = true
serial.redirectToUSB()
serial.setBaudRate(9600)
