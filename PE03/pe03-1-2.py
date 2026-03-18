from gpiozero import MCP3008
from gpiozero import PWMLED
import time



pot = MCP3008(0)
photocell = MCP3008(7) # i am using channel 7 but you should be using channel 0
statusLed = PWMLED(20)
elightLed = PWMLED(21)
statusLed.source = photocell.values

print('Program running... Press CTRL+C to exit')

try:

	while True:
		# print(pot.value)
		print('Analogue Value = {}; Voltage = {}v'.format(photocell.value, photocell.value * 3.3))		 
		
		if photocell.value < 0.2:
			elightLed.on()
		else:
			elightLed.off()
		
		time.sleep(0.1)

except KeyboardInterrupt:	
	print('Program terminated!')
