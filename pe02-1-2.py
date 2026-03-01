import serial



try:
	comPort = '/dev/ttyACM0'
	debugRaw = False
	
	ser = serial.Serial(port=comPort, baudrate=9600, timeout=0.1)
	
	print('Listening on {}... Press CTRL+C to exit'.format(comPort))
	
	while True:			
		
		# Read newline terminated data
		if ser.in_waiting > 0: # Only read if data is actually there

			msg = ser.readline()

			if debugRaw:

				print('RAW:{} HEX:{}'.format(repr(msg), msg.hex()))
			
			smsg = msg.decode('utf-8', errors='replace').strip()

			if smsg:

				print('RX:{}'.format(smsg))			
	
except serial.SerialException as err:
	
	print('SerialException: {}'.format(err))

except KeyboardInterrupt:
	
	print('Program terminated!')
