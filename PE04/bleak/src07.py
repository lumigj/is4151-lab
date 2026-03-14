# demo uart transmit and receive



import asyncio
import traceback
from bleak import BleakScanner

import util
from bleuartlib import BleUartDevice



def bleUartReceiveCallback(data):

	print('Received data = {}'.format(data))



async def main():

	bleUartDevice1 = None
	found_address = None
	target_addresses = {
		'E9:01:B2:1A:C5:4E': 'vavet',
		'E4:C8:06:E7:73:CF': 'vuzuv'
	}

	print('********** Initiating device discovery......')

	devices = await BleakScanner.discover(timeout=2.0)

	for device in devices:

		address = util.normalizeBleAddress(device.address)

		if address in target_addresses:

			print('Found BBC micro:bit [{}]: {}'.format(target_addresses[address], address))
			found_address = address
			break

	if found_address is None:
		print('********** UNKNOWN ERROR')
		return

	try:

		bleUartDevice1 = BleUartDevice(found_address)
		await bleUartDevice1.connect()
		print('Connected to micro:bit device')

		await bleUartDevice1.enable_uart_receive(bleUartReceiveCallback)
		print('Receiving data...')

		while True:

			response = await asyncio.to_thread(input, 'Do you want to transmit command to micro:bit (Y/n) = ')

			if response == 'Y':

				command = await asyncio.to_thread(input, 'Enter command to send = ')
				await bleUartDevice1.send(command)
				print('Finished sending command...')

			await asyncio.sleep(0.1)

	except KeyboardInterrupt:

		print('********** END')

	except Exception as ex:

		print('********** UNKNOWN ERROR')
		print('Error detail: {}'.format(ex))
		traceback.print_exc()

	finally:

		if bleUartDevice1 is not None:
			try:
				await bleUartDevice1.disable_uart_receive()
				await bleUartDevice1.disconnect()
				print('Disconnected from micro:bit device')
			except Exception as ex:
				print('Disconnect error: {}'.format(ex))



if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('********** END')
