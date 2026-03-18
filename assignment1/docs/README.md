## architecture

### how 2 run
- install all dependencies
- use score.py for rpi, receiver.js for mb v1, the rest for mb v2
- attach v1 to rpi
- run score.py, open browser localhost:8000
- setup game device with sensors
- run game.js on game device 1
- change TARGET_GAME_DEIVCE (match game device 1) on remote controller
- run remote.js on remote controller
- run partial.js on game device 2, press btnA to generate a random score
- btnA start inputing name, use A and B to loop through alphabet, A+B confirm one letter
- once 5 letter confirmed, start playing

### error recovery
each packet sent 3 times. naturally the redundant ones will be dropped, so no need to label or remove duplicate

R: remote -> game (3 times, redundant ones will be dropped, and R will not be handled by receiver)

S: game/partial -> receiver (3 times)

E: game/partial -> receiver (3 times)

L: game/partial -> receiver (3 times)

serial (not handling R): receiver -> score

### in case completed (normal case)
next is shown in scrolling effect, so player can know they need to do the next one

### in case miss
beep once, flash twice, show next (scrolling)

### in case closer than 20cm
beep twice, flash 5 times

### trivial note of error recovery for myself
remote发三次R给game，此时receiverr会忽略R，因为那个bool falg已经是开始了所以后面的没用

game发三次S给receiver，这个score的处理就是一个key写了三个值（device palyer对儿）

然后L和E都是三次

L三次防止丢分，这个会全都用，不去重，没必要

E三次，但是不会出现多个final score，因为E和S对应的，多受到E会提示ignored

partial就是很简单三次S三次E

