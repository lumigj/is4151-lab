import time

from gpiozero import MCP3008

pot = MCP3008(channel=0)

print('Program running... Press CTRL+C to exit')


try:

    while True:
        print(pot.value)


        time.sleep(0.1)

except KeyboardInterrupt:
    print('Program terminated!')
